# HW-08: Dashboard for the monitored application


Needed by: the Day 13 lab (instrument, dashboard, drift, alert).

## Decision

Two dashboard tools are ready. The instructor selects one after the test on
the Raspberry Pi.

| Option | Tool | State |
|---|---|---|
| A | Grafana with Prometheus (`grafana/`) | Prepared. The syllabus names it as the default tool. |
| B | Python dashboard (`python_dashboard/`) | Prepared. **The lab uses this option until the instructor selects.** |

Both options read the same MQTT messages:

| Item | Decision |
|---|---|
| Topic | `edgeai/<group>/pi/metrics` |
| Payload | `{"seq":12,"ts":1790000000.5,"latency_ms":41.3,"fps":22.8,"confidence":0.84,"cpu_temp_c":58.2,"cpu_percent":71.0,"ram_used_mb":1830.4}` |
| Sender | `metrics_publisher.py`: the class `MetricsPublisher` in the application |
| Alert rule | The mean confidence is below 0.6 |

```
application --MQTT--> broker --+--> dashboard.py --> CSV files + web page      (option B)
                               |
                               +--> mqtt_exporter.py --> Prometheus --> Grafana (option A)
```

## Reason

- Part B of the lab says: "Publish the metrics with MQTT, store them, and
  build a live dashboard." One message format for both options lets a group
  change the tool with no change of the application.
- Option B is one Python file and one web page. It needs only `paho-mqtt`.
  The page loads no file from the internet, so it works in Part D of Day 12
  and in a lab with no internet link. A student can read all of its code in
  the lab time.
- Option A shows the tools that production systems use: a time-series
  database, a query language, and alert rules in a file. It needs three
  services and a bridge, because Prometheus cannot read MQTT. The setup time
  is the risk.
- The plan keeps option B as the lab tool until a test on the Raspberry Pi
  shows that option A fits in the 45 minutes of Part B.
- The confidence rule needs no labels. Day 13 teaches drift detection from
  the confidence values.

## Comparison

| Topic | A: Grafana with Prometheus | B: Python dashboard |
|---|---|---|
| Services on the Raspberry Pi | Prometheus, node exporter, Grafana, `mqtt_exporter.py` | `dashboard.py` |
| Install | `apt` packages and the Grafana repository (internet necessary) | none, `paho-mqtt` is in `~/yolo` |
| Storage | Prometheus database | One CSV file for each day |
| Alert | Rule file of Prometheus | One rule in `dashboard.py` |
| History | Days | 10 minutes on the page, all data in the CSV files |
| Student work in the lab | Add a panel and a rule in a query language | Change Python code |
| Tested on the work computer | Yes: Prometheus 3.15.0 and Grafana 13.2.3 load the files, and the alert fires | Yes: 52 messages, the alert fires |

## Sources

| Item | Source |
|---|---|
| Metrics to collect | Day 13 of the syllabus, and "Machine Learning Systems", chapter "ML Operations" |
| CSV log | `SLMs_for_IoT_CONTROL/data_logger.py` of "EdgeML with Raspberry Pi" (GPL-3.0) |
| Temperature command | Lab "Small Language Models" of "Machine Learning Systems" |
| Prometheus settings and rules | Prometheus documentation (`prometheus.io/docs`) |
| Grafana install and provisioning | Grafana documentation (`grafana.com/docs/grafana/latest`) |
| Python client for Prometheus | `prometheus_client` documentation |

All code of this folder is new.

## Files

| File | Content |
|---|---|
| `metrics_publisher.py` | Sends the metrics. Real system metrics. Simulated model metrics with `--simulate`. |
| `python_dashboard/dashboard.py` | Option B: MQTT to CSV files, web page, alert |
| `python_dashboard/index.html` | The web page of option B: six charts, no library |
| `grafana/install_monitoring.sh` | Option A: installs Prometheus, the node exporter, and Grafana |
| `grafana/mqtt_exporter.py` | Option A: bridge from MQTT to Prometheus |
| `grafana/prometheus.yml` | Option A: three scrape targets, 2 s interval |
| `grafana/alert_rules.yml` | Option A: `LowConfidence`, `DeviceSilent`, `HighTemperature` |
| `grafana/provisioning/` | Option A: data source and dashboard provider of Grafana |
| `grafana/dashboards/edgeai_overview.json` | Option A: dashboard with 12 panels |

## Steps for both options

The broker of `HW-07` must run. Use the environment `~/yolo` of `HW-04`.

### 1. Send metrics

For a first test with no detector:

```bash
source ~/yolo/bin/activate
python3 metrics_publisher.py --group g07 --simulate
```

The system metrics are real. The model metrics are random numbers.

In the Day 8 application, send the real numbers:

```python
from metrics_publisher import MetricsPublisher

publisher = MetricsPublisher("localhost", "g07")
# in the loop, after each inference:
publisher.publish(latency_ms=latency_ms, fps=fps, confidence=best_score)
```

### 2. Simulate a drift event

```bash
python3 metrics_publisher.py --group g07 --simulate --drift-after 60
```

After 60 seconds, the simulated confidence goes from about 0.85 to about
0.45. The alert of each option must fire.

## Option B: Python dashboard

```bash
cd python_dashboard
python3 dashboard.py --group g07
```

Open `http://pi-07.local:8080` on the laptop.

- The page shows six charts of the last 5 minutes and updates each second.
- The bar at the top shows the number of messages, the lost messages, the
  age of the last message, and the alert state. The bar is red during an
  alert and yellow when no message arrived for 5 seconds.
- The folder `metrics_log/` holds one CSV file for each day.
- The terminal prints one line when the alert starts and when it stops.

Options:

| Option | Default | Content |
|---|---|---|
| `--alert-threshold` | 0.6 | The alert is active when the mean confidence is below this value |
| `--alert-window` | 20 | Number of messages for the mean |
| `--http-port` | 8080 | Port of the web page |
| `--log-dir` | `metrics_log` | Folder of the CSV files |

## Option A: Grafana with Prometheus

### A1. Install (one time, on the master card)

```bash
bash grafana/install_monitoring.sh
```

### A2. Start the bridge

```bash
source ~/yolo/bin/activate
python3 grafana/mqtt_exporter.py --group g07
```

Check: `curl http://localhost:9200/metrics | grep edgeai_`.

### A3. Open the tools

| Tool | Address | What you see |
|---|---|---|
| Prometheus targets | `http://pi-07.local:9090/targets` | The jobs `edgeai`, `prometheus`, and `node` are `UP` |
| Prometheus alerts | `http://pi-07.local:9090/alerts` | The three rules and their state |
| Grafana | `http://pi-07.local:3000` | Login `admin` / `admin`. Folder `Edge AI`, dashboard `Edge AI overview`. |

### A4. Work for the students

- Add a panel with the 95th percentile of the latency:
  `quantile_over_time(0.95, edgeai_latency_ms[1m])`.
- Change the threshold of the rule `LowConfidence` in
  `/etc/prometheus/alert_rules.yml`, then
  `sudo systemctl restart prometheus`.

Metric names:

| Metric | Content |
|---|---|
| `edgeai_latency_ms`, `edgeai_fps`, `edgeai_confidence` | Model metrics |
| `edgeai_cpu_temp_celsius`, `edgeai_cpu_percent`, `edgeai_ram_used_mb` | System metrics |
| `edgeai_messages_total`, `edgeai_messages_lost_total` | Message counters |
| `edgeai_last_message_timestamp_seconds` | Time of the newest message |

Each metric has the labels `group` and `device`.

## Result of the test on the work computer

No Raspberry Pi was used. The test used a broker on the work computer and
`metrics_publisher.py --simulate --drift-after`.

**Option B.** `dashboard.py` received 52 messages in 26 seconds with 0 lost.
The alert went on after the drift (mean confidence 0.578, threshold 0.60).
The CSV file has 52 rows. The address `/data.json` gives the data, and an
unknown address gives the code 404. A port in use gives a clear error. The
JavaScript of the page passed a syntax check. **Nobody looked at the page in
a browser.**

**Option A.** `promtool` of Prometheus 3.15.0 accepts `prometheus.yml` and
the three rules. Prometheus read the bridge (target `edgeai` up). The rule
`LowConfidence` reached the state `firing` with the text "The mean confidence
of 30 s is 0.49". Grafana 13.2.3 loaded the data source and the dashboard
into the folder `Edge AI`. All 13 queries of the 12 panels returned the
status 200 through Grafana. **Nobody looked at the dashboard in a browser.**

## Code status

| File | State | Change |
|---|---|---|
| `metrics_publisher.py` | new | tested on the work computer. `vcgencmd` not tested. |
| `python_dashboard/dashboard.py` | new | tested on the work computer |
| `python_dashboard/index.html` | new | syntax check only. Not seen in a browser. |
| `grafana/mqtt_exporter.py` | new | tested on the work computer with Prometheus 3.15.0 |
| `grafana/prometheus.yml`, `grafana/alert_rules.yml` | new | checked with `promtool` 3.15.0 and tested with Prometheus 3.15.0 |
| `grafana/provisioning/`, `grafana/dashboards/` | new | loaded by Grafana 13.2.3 on the work computer |
| `grafana/install_monitoring.sh` | new | not tested. It needs `sudo` and a Raspberry Pi. |

Open points for the test:

- The `apt` package of Prometheus on Raspberry Pi OS is older than version
  3.15.0. The settings file uses only basic keys. The test must confirm it.
- The CPU load and the RAM of the three services of option A on the
  Raspberry Pi are not known. The detector needs the CPU.
- The Grafana package needs internet access during the installation.

## Test steps for the instructor

- Date of the test:
- Versions: Prometheus, Grafana, `paho-mqtt`, `prometheus-client`:

| Step | What to do | What to record | Result |
|---|---|---|---|
| 1 | Run step 1 with `--simulate` on the Raspberry Pi | Does `cpu_temp_c` show the value of `vcgencmd measure_temp`? | |
| 2 | Run option B. Open the page on a laptop. | Do the six charts move? Is the text readable on a projector? | |
| 3 | Run step 2 with option B | Seconds from the drift to the red bar | |
| 4 | `htop` with option B active | CPU percent and RAM of `dashboard.py` | |
| 5 | Run A1 | Time of the installation. Versions that `apt` installs. Errors. | |
| 6 | Run A2 and A3 | State of the three targets. Does the dashboard show data? | |
| 7 | Run step 2 with option A | Seconds from the drift to the state `firing` | |
| 8 | `htop` with option A active | CPU percent and RAM of Prometheus, Grafana, and the bridge | |
| 9 | Run the Day 8 detector with `MetricsPublisher` and each option | Frame rate of the detector with no dashboard, with option A, and with option B | |
| 10 | Do the student work of A4, and the same change in `dashboard.py` | Minutes for each. The plan for Part B is 45 minutes. | |
| 11 | **Select the tool for the lab** | A or B, and the reason | |

Problems found:

| Problem | Fix | File to correct |
|---|---|---|

## After the test

1. Change the line `Hardware status:` to `tested on hardware (YYYY-MM-DD)`.
2. Write the selected option at the top of this file and in Section 13 of
   the execution plan.
3. Write the versions in `Labs/VERSIONS.md`.
4. If the lab uses option A, run `install_monitoring.sh` on the master card
   (`HW-04`, step 4).

## Credits

The CSV log follows `data_logger.py` of "EdgeML with Raspberry Pi" by Marcelo
Rovai (github.com/Mjrovai/EdgeML-with-Raspberry-Pi, GPL-3.0). The other code
of this folder is new.
