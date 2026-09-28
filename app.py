import numpy as np


def extract_features(signal, sample_rate_hz=50.0):
    values = np.asarray(signal, dtype=np.float32)
    if values.ndim == 2 and values.shape[1] == 3:
        values = values.T
    if values.ndim != 2 or values.shape[0] != 3:
        raise ValueError("Expected a three-axis signal with shape 3 by samples.")
    if values.shape[1] < 4:
        raise ValueError("At least four samples are required to extract features.")
    if sample_rate_hz <= 0:
        raise ValueError("Sample rate must be greater than zero.")
    if not np.isfinite(values).all():
        raise ValueError("Signal values must be finite.")

    x_channel = values[0] - values[0].mean()
    window = np.hanning(len(x_channel)).astype(np.float32)
    spectrum = np.abs(np.fft.rfft(x_channel * window))
    frequencies = np.fft.rfftfreq(len(x_channel), d=1.0 / sample_rate_hz)

    if len(spectrum) > 1:
        peak_frequency_hz = float(frequencies[1 + np.argmax(spectrum[1:])])
    else:
        peak_frequency_hz = 0.0

    quadratic_mean = float(np.sqrt(np.mean(np.square(values))))
    return np.asarray([peak_frequency_hz, quadratic_mean], dtype=np.float32)


===== ml/fetch_mpower.py =====
import csv
import hashlib
import json
import os
import re
from pathlib import Path

import synapseclient

PROJECT_ID = "syn4993293"


def normalized(value):
    return re.sub(r"[^a-z0-9]", "", str(value).lower())


def get_dataframe(syn, entity_id):
    result = syn.tableQuery(f"SELECT * FROM {entity_id}")
    frame = result.asDataFrame(rowIdAndVersionInIndex=False)
    return result, frame


def table_ids(syn):
    query = f"SELECT id,name FROM table WHERE parentId='{PROJECT_ID}'"
    result = syn.tableQuery(query)
    frame = result.asDataFrame(rowIdAndVersionInIndex=False)
    return [
        (str(row["id"]), str(row["name"]))
        for _, row in frame.iterrows()
    ]


def choose_table(entries, exact_name):
    wanted = normalized(exact_name)
    matches = [
        (entity_id, name)
        for entity_id, name in entries
        if normalized(name) == wanted
    ]
    if len(matches) != 1:
        raise RuntimeError(
            f"Expected one Synapse table named {exact_name}; "
            f"found {len(matches)}."
        )
    return matches[0][0]


def truth_value(value):
    return str(value).strip().lower() in {"true", "1", "yes"}


def extract_items(path):
    with Path(path).open(encoding="utf-8") as handle:
        payload = json.load(handle)

    items = payload.get("items", payload) if isinstance(payload, dict) else payload
    if not isinstance(items, list):
        raise ValueError(f"Unexpected accelerometer JSON format in {path}.")

    points = []
    for item in items:
        if not isinstance(item, dict):
            continue
        try:
            timestamp_seconds = float(item["timestamp"])
            axes = [float(item[axis]) for axis in ("x", "y", "z")]
        except (KeyError, TypeError, ValueError):
            continue
        points.append((timestamp_seconds * 1000.0, *axes))

    return points


def fetch_mpower_export(destination):
    token = os.environ.get("SYNAPSE_AUTH_TOKEN")
    if not token:
        raise RuntimeError(
            "Set SYNAPSE_AUTH_TOKEN to a Synapse personal access token "
            "authorized to download mPower."
        )

    syn = synapseclient.Synapse()
    syn.login(authToken=token)
    entries = table_ids(syn)
    walking_id = choose_table(entries, "Walking Activity")
    demographics_id = choose_table(entries, "Demographics")
    walking_result, walking = get_dataframe(syn, walking_id)
    _, demographics = get_dataframe(syn, demographics_id)

    required_demo = {"healthCode", "professional.diagnosis"}
    if not required_demo.issubset(demographics.columns):
        raise RuntimeError(
            "The mPower Demographics table is missing healthCode or "
            "professional.diagnosis."
        )

    demographics = demographics.drop_duplicates("healthCode").set_index("healthCode")
    available_columns = [
        column
        for column in walking.columns
        if "accel" in normalized(column) and "walking" in normalized(column)
    ]
    if not available_columns:
        raise RuntimeError(
            "The mPower Walking Activity table has no walking "
            "accelerometer file columns."
        )

    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    download_dir = destination.parent / "mpower_files"
    file_map = syn.downloadTableColumns(
        walking_result,
        available_columns,
        downloadLocation=str(download_dir),
    )

    fields = [
        "participant_id",
        "record_id",
        "condition",
        "task",
        "timestamp_ms",
        "acceleration_x",
        "acceleration_y",
        "acceleration_z",
        "sample_rate_hz",
    ]
    count = 0

    with destination.open("w", encoding="utf-8", newline="") as output:
        writer = csv.writer(output)
        writer.writerow(fields)

        for _, row in walking.iterrows():
            participant = row.get("healthCode")
            if participant not in demographics.index:
                continue

            diagnosis = demographics.loc[
                participant,
                "professional.diagnosis",
            ]
            valid_diagnosis = str(diagnosis).strip().lower() in {
                "true",
                "false",
                "1",
                "0",
                "yes",
                "no",
            }
            if not valid_diagnosis:
                continue

            condition = "PD" if truth_value(diagnosis) else "HC"
            participant_id = hashlib.sha256(
                str(participant).encode("utf-8")
            ).hexdigest()
            record_id = hashlib.sha256(
                str(row.get("recordId", "")).encode("utf-8")
            ).hexdigest()

            for column in available_columns:
                handle_id = row.get(column)
                if handle_id is None:
                    continue

                key = str(int(handle_id)) if str(handle_id).endswith(".0") else str(handle_id)
                local_path = file_map.get(key)
                if not local_path and key.isdigit():
                    local_path = file_map.get(int(key))
                if not local_path:
                    continue

                task = (
                    normalized(column)
                    .replace("accel", "")
                    .replace("walking", "")
                    .replace("jsonitems", "")
                    or "walking"
                )
                points = extract_items(local_path)
                if len(points) < 2:
                    continue

                intervals = [
                    points[index][0] - points[index - 1][0]
                    for index in range(1, len(points))
                    if points[index][0] > points[index - 1][0]
                ]
                if not intervals:
                    continue

                median_interval = sorted(intervals)[len(intervals) // 2]
                sample_rate = 1000.0 / median_interval

                for timestamp, x, y, z in points:
                    writer.writerow([
                        participant_id,
                        record_id,
                        condition,
                        task,
                        f"{timestamp:.6f}",
                        f"{x:.9g}",
                        f"{y:.9g}",
                        f"{z:.9g}",
                        f"{sample_rate:.6f}",
                    ])
                    count += 1

    if not count:
        raise RuntimeError(
            "No mPower accelerometer samples were exported. Check Synapse "
            "access and table contents."
        )

    return count
