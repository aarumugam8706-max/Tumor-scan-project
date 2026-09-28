import argparse
import csv
import json
import re
from collections import defaultdict
from pathlib import Path

import numpy as np

from ml.signal import resample_signal

LABELS = {
    "pd": "pd",
    "parkinson": "pd",
    "parkinson's disease": "pd",
    "parkinsons disease": "pd",
    "healthy": "hc",
    "healthy control": "hc",
    "hc": "hc",
    "dd": "dd",
    "differential": "dd",
    "differential diagnosis": "dd",
    "differential diagnoses": "dd",
    "essential tremor": "dd",
    "multiple sclerosis": "dd",
    "atypical parkinsonism": "dd",
    "secondary parkinsonism": "dd",
    "secondary causes of parkinsonism": "dd",
}


def normalize_label(value):
    label = re.sub(r"\s+", " ", str(value).strip().lower())
    if label in LABELS:
        return LABELS[label]
    if "parkinson" in label:
        return "pd"
    if label in {"control", "control group"}:
        return "hc"
    raise ValueError(f"Unmapped diagnosis label: {value}")


def windows(values, rate, window_seconds=9.5, stride_seconds=5):
    data = np.asarray(values, dtype=np.float32)
    if data.ndim != 2 or data.shape[1] != 3:
        raise ValueError("Expected a rows-by-three-axis acceleration matrix.")
    size = int(rate * window_seconds)
    stride = int(rate * stride_seconds)
    for start in range(0, len(data) - size + 1, stride):
        segment = data[start:start + size]
        times = np.arange(size, dtype=np.float64) * 1000.0 / rate
        resampled = resample_signal(times, segment, sample_rate=50, length=475)
        yield resampled


def write_window(
    output,
    manifest,
    source,
    subject,
    label,
    task,
    index,
    signal,
    recording="",
):
    if recording:
        name = f"{source.lower()}_{subject}_{task}_{recording}_{index:04d}.npy"
    else:
        name = f"{source.lower()}_{subject}_{task}_{index:04d}.npy"
    np.save(output / name, signal.astype(np.float32), allow_pickle=False)
    manifest.writerow({
        "path": name,
        "subject_id": f"{source}:{subject}",
        "label": label,
        "source": source,
        "task": task,
        "sample_rate_hz": "50",
        "signal_format": "raw_axes_v1",
    })


def prepare_pads(root, output, manifest):
    people = {}
    for path in (root / "patients").glob("patient_*.json"):
        person = json.loads(path.read_text(encoding="utf-8"))
        people[str(person.get("id", "")).zfill(3)] = normalize_label(person["condition"])
    files = sorted((root / "movement" / "timeseries").glob("*.txt"))
    emitted = 0
    for path in files:
        match = re.match(r"(\d+)_([^_]+(?:_[^_]+)*)_(LeftWrist|RightWrist)\.txt$", path.name)
        if not match:
            continue
        subject, task, wrist = match.groups()
        subject = subject.zfill(3)
        task = f"{task}_{wrist}"
        if subject not in people:
            continue
        values = np.loadtxt(path, delimiter=",").astype(np.float32)
        if values.ndim == 1:
            continue
        values = values[:, :3]
        values = values[int(0.5 * 100) :]
        for index, signal in enumerate(windows(values, 100), start=1):
            write_window(
                output,
                manifest,
                "PADS",
                subject,
                people[subject],
                task,
                index,
                signal,
            )
            emitted += 1
    if not emitted:
        raise RuntimeError(
            "No PADS windows found. Expected patients/*.json and "
            "movement/timeseries/*.txt."
        )
    return emitted


def prepare_mpower(csv_path, output, manifest):
    grouped = defaultdict(list)
    with csv_path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        required = {
            "participant_id",
            "record_id",
            "condition",
            "task",
            "timestamp_ms",
            "acceleration_x",
            "acceleration_y",
            "acceleration_z",
            "sample_rate_hz",
        }
        if not required.issubset(reader.fieldnames or []):
            columns = ",".join(sorted(required))
            raise ValueError(f"mPower export must have these columns: {columns}.")
        for row in reader:
            key = (
                row["participant_id"],
                row["record_id"],
                normalize_label(row["condition"]),
                row["task"],
                float(row["sample_rate_hz"]),
            )
            axes = [
                float(row["acceleration_x"]),
                float(row["acceleration_y"]),
                float(row["acceleration_z"]),
            ]
            grouped[key].append((float(row["timestamp_ms"]), axes))
    emitted = 0
    for (subject, record_id, label, task, rate), records in grouped.items():
        records.sort(key=lambda item: item[0])
        times = np.asarray([item[0] for item in records], dtype=np.float64)
        axes = np.asarray([item[1] for item in records], dtype=np.float32)
        if len(times) < 2:
            continue
        interval = 1000.0 / rate
        chunks = []
        start = 0
        for index in range(1, len(times)):
            if times[index] - times[index - 1] > interval * 2.5:
                chunks.append((start, index))
                start = index
        chunks.append((start, len(times)))
        window_index = 0
        for left, right in chunks:
            segment_times = times[left:right]
            segment_axes = axes[left:right]
            if len(segment_times) < 2:
                continue
            offsets = np.arange(segment_times[0], segment_times[-1] - 9500, 5000)
            for offset in offsets:
                mask = (segment_times >= offset) & (
                    segment_times < offset + 9500
                )
                if mask.sum() < int(rate * 8):
                    continue
                signal = resample_signal(
                    segment_times[mask],
                    segment_axes[mask],
                    sample_rate=50,
                    length=475,
                )
                write_window(
                    output,
                    manifest,
                    "mPower",
                    subject,
                    label,
                    task,
                    window_index,
                    signal,
                    recording=record_id,
                )
                window_index += 1
                emitted += 1
    if not emitted:
        raise RuntimeError("No mPower windows could be created from the exported CSV.")
    return emitted


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pads", type=Path)
    parser.add_argument("--mpower-export", type=Path)
    parser.add_argument("--output", type=Path, default=Path("data/processed"))
    args = parser.parse_args()
    if not args.pads or not args.mpower_export:
        raise SystemExit(
            "Both --pads and --mpower-export are required to build the "
            "two-source training set."
        )
    args.output.mkdir(parents=True, exist_ok=True)
    manifest_path = args.output / "manifest.csv"
    with manifest_path.open("w", newline="", encoding="utf-8") as handle:
        manifest = csv.DictWriter(
            handle,
            fieldnames=[
                "path",
                "subject_id",
                "label",
                "source",
                "task",
                "sample_rate_hz",
                "signal_format",
            ],
        )
        manifest.writeheader()
        pads_count = prepare_pads(args.pads, args.output, manifest)
        mpower_count = prepare_mpower(args.mpower_export, args.output, manifest)
    print(json.dumps({
        "manifest": str(manifest_path),
        "PADS_windows": pads_count,
        "mPower_windows": mpower_count,
    }))


if __name__ == "__main__":
    main()
