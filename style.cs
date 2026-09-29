:root {
  font-family: 'DM Sans',sans-serif;
  color: #edf3fc;
  background: #0b1120;
  font-synthesis: none;
  text-rendering: optimizeLegibility;
  font-smooth: always;
  font-weight: 400;
  --bg: #0b1120;
  --panel: #121a2b;
  --stroke: #26344a;
  --muted: #8998ae;
  --teal: #72e4cf;
  --blue: #84a9ff;
  --purple: #b399ff;
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  min-width: 320px;
  background: radial-gradient(ellipse at 50% -35%,#182a43 0%,var(--bg) 58%);
}

button,select {
  font: inherit;
}

.app-shell {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 46px;
}

.topbar {
  height: 78px;
  border-bottom: 1px solid rgba(117,139,171,.16);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.brand {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #f4f7fb;
  text-decoration: none;
  font: 700 19px Manrope,sans-serif;
  letter-spacing: -.7px;
}

.brand-light {
  color: #7cdccb;
  font-weight: 500;
}

.brand-mark {
  width: 34px;
  height: 34px;
  border: 1px solid #376b75;
  border-radius: 10px;
  display: grid;
  place-items: center;
  color: var(--teal);
  background: #123039;
}

.topbar-right {
  display: flex;
  align-items: center;
  gap: 22px;
}

.system-state,.version-label {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #a6b3c6;
  font-size: 11px;
}

.version-label,.eyebrow,.capture-badge,.stat span,.result-label,footer {
  font: 500 10px 'DM Mono',monospace;
  letter-spacing: 1.15px;
}

.version-label {
  border: 1px solid #344157;
  border-radius: 99px;
  padding: 7px 10px;
  color: #96a4b9;
}

.dot {
  display: inline-block;
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #64748b;
}

.dot.online {
  background: #74e2c7;
  box-shadow: 0 0 10px #5ed7bd;
}

.hero {
  min-height: 365px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 48px 52px 40px 28px;
  border-bottom: 1px solid rgba(117,139,171,.16);
  overflow: hidden;
}

.hero-copy {
  max-width: 530px;
  z-index: 1;
}

.eyebrow {
  color: #77dcca;
}

.hero h1 {
  font: 700 clamp(38px,5vw,59px)/1.07 Manrope,sans-serif;
  letter-spacing: -2.8px;
  margin: 15px 0;
}

.hero h1 span {
  color: #8fb5ff;
}

.hero-copy>p {
  max-width: 440px;
  color: #a4b0c2;
  font-size: 15px;
  line-height: 1.7;
  margin: 0;
}

.hero-note {
  display: flex;
  gap: 9px;
  align-items: flex-start;
  margin-top: 20px;
  color: #8a9bb0;
  font-size: 11px;
  line-height: 1.5;
}

.hero-note svg {
  flex: none;
  color: #e7b66e;
}

.hero-orbit {
  position: relative;
  width: 280px;
  height: 255px;
  flex: none;
  margin-left: 20px;
  display: grid;
  place-items: center;
}

.orbit {
  position: absolute;
  border: 1px solid #213a50;
  border-radius: 50%;
  transform: rotate(-18deg);
}

.orbit-outer {
  width: 250px;
  height: 142px;
}

.orbit-inner {
  width: 190px;
  height: 210px;
  border-color: #263250;
  transform: rotate(48deg);
}

.orbit-core {
  width: 80px;
  height: 80px;
  border: 1px solid #2a7775;
  border-radius: 50%;
  display: grid;
  place-items: center;
  color: #84eed8;
  background: radial-gradient(circle,#174047,#102432);
  box-shadow: 0 0 50px #39c3b84d;
  z-index: 1;
}

.orbit-tag {
  position: absolute;
  padding: 6px 8px;
  background: #111d2c;
  border: 1px solid #31425b;
  border-radius: 5px;
  color: #a9bbcf;
  font: 9px 'DM Mono',monospace;
  letter-spacing: .8px;
}

.tag-one {
  top: 18px;
  left: 62px;
}

.tag-two {
  right: 10px;
  top: 115px;
}

.tag-three {
  left: 33px;
  bottom: 23px;
}

.workspace {
  padding: 35px 0 45px;
}

.section-heading {
  display: flex;
  justify-content: space-between;
  align-items: end;
  margin-bottom: 16px;
}

.section-heading h2 {
  font: 600 23px Manrope,sans-serif;
  letter-spacing: -.7px;
  margin: 7px 0 0;
}

.capture-badge {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #a3b2c4;
  border: 1px solid #2c394c;
  padding: 8px 10px;
  border-radius: 5px;
}

.capture-badge.recording,.capture-badge.ready {
  color: #80e6d1;
  border-color: #28645c;
}

.capture-card,.panel {
  background: linear-gradient(145deg,#141e30,#111827);
  border: 1px solid var(--stroke);
  border-radius: 10px;
}

.capture-card {
  padding: 20px 22px;
}

.capture-tools {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.sensor-title,.panel-heading {
  display: flex;
  align-items: center;
  gap: 11px;
}

.sensor-title strong,.panel h3 {
  display: block;
  font: 600 13px Manrope,sans-serif;
  margin: 0;
}

.sensor-title small,.panel-heading p {
  display: block;
  font-size: 11px;
  color: var(--muted);
  margin: 4px 0 0;
}

.icon-tile {
  width: 37px;
  height: 37px;
  display: grid;
  place-items: center;
  border: 1px solid #35535e;
  background: #173039;
  color: var(--teal);
  border-radius: 8px;
}

.task-picker {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #9baabe;
  font-size: 11px;
}

.task-picker select {
  padding: 9px 28px 9px 10px;
  color: #d8e2f1;
  background: #10192a;
  border: 1px solid #344159;
  border-radius: 5px;
}

.chart {
  height: 175px;
  margin: 17px 0 8px;
  border: 1px solid #25344a;
  border-radius: 6px;
  background: linear-gradient(180deg,#101828,#0d1523);
  overflow: hidden;
}

.chart svg {
  width: 100%;
  height: 100%;
}

.grid-line {
  stroke: #253146;
  stroke-width: 1;
  stroke-dasharray: 3 6;
}

.capture-stats {
  display: grid;
  grid-template-columns: repeat(3,1fr);
  border-top: 1px solid #25344a;
  border-bottom: 1px solid #25344a;
  padding: 13px 0;
  margin-bottom: 16px;
}

.stat {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 0 16px;
  border-right: 1px solid #25344a;
}

.stat:first-child {
  padding-left: 0;
}

.stat:last-child {
  border: 0;
}

.stat span {
  color: #7d8ca2;
  font-size: 9px;
}

.stat strong {
  font: 600 20px Manrope,sans-serif;
}

.stat small {
  color: #73839a;
  font-size: 10px;
}

.capture-actions {
  display: flex;
  gap: 10px;
}

.button {
  height: 40px;
  padding: 0 14px;
  border: 1px solid transparent;
  border-radius: 5px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  color: #101b25;
  font-weight: 600;
  font-size: 12px;
  cursor: pointer;
}

.button:disabled {
  opacity: .45;
  cursor: not-allowed;
}

.button-primary {
  background: var(--teal);
}

.button-primary:hover:not(:disabled) {
  background: #9af1e2;
}

.button-muted {
  color: #d5dfeb;
  background: #1b2638;
  border-color: #35435a;
}

.error-box {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px;
  margin-top: 13px;
  border: 1px solid #753d4e;
  border-radius: 5px;
  background: #321b29;
  color: #f3a9b1;
  font-size: 12px;
}

.capture-hint {
  margin: 12px 0 0;
  color: #8a9bb0;
  font-size: 11px;
}

.analysis-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
  margin-top: 14px;
}

.panel {
  padding: 18px 19px;
  min-height: 215px;
}

.purple {
  color: #c3adff;
  background: #28213e;
  border-color: #4b3e72;
}

.amber {
  color: #f3c579;
  background: #332b1d;
  border-color: #64502a;
}

.source-list {
  margin-top: 16px;
}

.source-row {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 11px 0;
  border-top: 1px solid #26344a;
}

.source-row>div {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.source-row strong {
  font-size: 11px;
  font-weight: 600;
}

.source-row small {
  font-size: 10px;
  color: #8c9cb0;
}

.source-row>svg {
  color: #728198;
}

.source-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex: none;
}

.source-indicator.sage {
  background: #82b8ff;
}

.source-indicator.pads {
  background: #d6a7ff;
}

.source-footnote {
  font-size: 10px;
  line-height: 1.5;
  color: #77879d;
  margin: 8px 0 0;
}

.empty-state {
  min-height: 125px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  gap: 10px;
  text-align: center;
  color: #8594aa;
  font-size: 11px;
  line-height: 1.5;
}

.empty-state svg {
  color: #7989a2;
}

.result-block {
  margin-top: 15px;
}

.result-label {
  font-size: 9px;
  color: #e7b66e;
}

.result-block>strong {
  display: block;
  font: 600 19px Manrope,sans-serif;
  margin: 8px 0;
}

.result-block p {
  font-size: 11px;
  line-height: 1.5;
  color: #a7b3c5;
  margin: 0 0 13px;
}

.confidence-row {
  display: flex;
  justify-content: space-between;
  font-size: 11px;
  color: #9baabe;
}

.confidence-row strong {
  color: #eaf2fb;
}

.confidence-bar {
  height: 5px;
  background: #28344a;
  border-radius: 10px;
  overflow: hidden;
  margin: 7px 0 11px;
}

.confidence-bar i {
  height: 100%;
  display: block;
  border-radius: 10px;
  background: linear-gradient(90deg,#70d9c5,#8bacff);
}

.result-block>small {
  color: #7d8ca2;
  font-size: 9px;
}

footer {
  min-height: 55px;
  border-top: 1px solid #26344a;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 15px;
  color: #75849a;
  font-size: 9px;
}

footer span:last-child {
  display: flex;
  align-items: center;
  gap: 7px;
}

@media (max-width: 760px) {

  .app-shell {
    padding: 0 20px;
  }

  .topbar {
    height: 66px;
  }

  .topbar-right {
    gap: 10px;
  }

  .version-label {
    display: none;
  }

  .hero {
    padding: 42px 3px 32px;
    min-height: 320px;
  }

  .hero-orbit {
    width: 190px;
    transform: scale(.8);
    transform-origin: right center;
    margin-left: -15px;
  }

  .hero h1 {
    font-size: 43px;
    letter-spacing: -2px;
  }

  .hero-copy>p {
    font-size: 13px;
  }

  .analysis-grid {
    grid-template-columns: 1fr;
  }

  .workspace {
    padding-top: 27px;
  }
}

@media (max-width: 520px) {

  .app-shell {
    padding: 0 14px;
  }

  .system-state {
    font-size: 0;
  }

  .system-state .dot {
    width: 9px;
    height: 9px;
  }

  .hero {
    min-height: 0;
    padding: 39px 4px 28px;
  }

  .hero-orbit {
    position: absolute;
    right: -92px;
    opacity: .42;
  }

  .hero-copy {
    max-width: 100%;
  }

  .hero h1 {
    font-size: 39px;
  }

  .hero-copy>p {
    max-width: 330px;
  }

  .section-heading h2 {
    font-size: 20px;
  }

  .capture-card {
    padding: 15px 13px;
  }

  .capture-tools {
    align-items: flex-start;
    gap: 12px;
    flex-direction: column;
  }

  .task-picker {
    width: 100%;
    justify-content: space-between;
  }

  .task-picker select {
    flex: 1;
    max-width: 180px;
  }

  .chart {
    height: 145px;
  }

  .stat {
    padding: 0 8px;
  }

  .stat strong {
    font-size: 17px;
  }

  .capture-actions {
    flex-direction: column;
  }

  .button {
    width: 100%;
  }

  footer {
    align-items: flex-start;
    flex-direction: column;
    justify-content: center;
    padding: 10px 0;
    line-height: 1.7;
  }
}
