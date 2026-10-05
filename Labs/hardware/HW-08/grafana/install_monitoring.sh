#!/usr/bin/env bash
# install_monitoring.sh - install Prometheus and Grafana on the Raspberry Pi
#
# Run on: the Raspberry Pi 5, after setup_pi.sh of HW-04.
# Use:    bash install_monitoring.sh
#
# The script installs:
#   - Prometheus and the node exporter, from the packages of the system
#   - Grafana, from the package repository of Grafana Labs
#   - the settings, the alert rules, and the dashboard of this folder
#
# Sources: grafana.com/docs/grafana/latest/setup-grafana/installation/debian
# and prometheus.io/docs.
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"

echo "=== Prometheus and node exporter ==="
sudo apt-get update
sudo apt-get install -y prometheus prometheus-node-exporter

echo "=== Grafana ==="
sudo apt-get install -y apt-transport-https wget gpg
sudo mkdir -p /etc/apt/keyrings
wget -q -O - https://apt.grafana.com/gpg.key | gpg --dearmor \
    | sudo tee /etc/apt/keyrings/grafana.gpg > /dev/null
echo "deb [signed-by=/etc/apt/keyrings/grafana.gpg] https://apt.grafana.com stable main" \
    | sudo tee /etc/apt/sources.list.d/grafana.list > /dev/null
sudo apt-get update
sudo apt-get install -y grafana

echo "=== Settings of Prometheus ==="
if [ -f /etc/prometheus/prometheus.yml ] && [ ! -f /etc/prometheus/prometheus.yml.orig ]; then
    sudo cp /etc/prometheus/prometheus.yml /etc/prometheus/prometheus.yml.orig
fi
sudo cp "$HERE/prometheus.yml" /etc/prometheus/prometheus.yml
sudo cp "$HERE/alert_rules.yml" /etc/prometheus/alert_rules.yml
promtool check config /etc/prometheus/prometheus.yml

echo "=== Settings of Grafana ==="
sudo cp "$HERE/provisioning/datasources/prometheus.yml" \
    /etc/grafana/provisioning/datasources/edgeai.yml
sudo cp "$HERE/provisioning/dashboards/edgeai.yml" \
    /etc/grafana/provisioning/dashboards/edgeai.yml
sudo mkdir -p /var/lib/grafana/dashboards
sudo cp "$HERE/dashboards/edgeai_overview.json" /var/lib/grafana/dashboards/
sudo chown -R grafana:grafana /var/lib/grafana/dashboards

echo "=== Start the services ==="
sudo systemctl enable --now prometheus prometheus-node-exporter
sudo systemctl restart prometheus
sudo systemctl enable --now grafana-server
sudo systemctl restart grafana-server

echo
echo "Prometheus: http://$(hostname).local:9090"
echo "Grafana:    http://$(hostname).local:3000  (first login: admin / admin)"
echo "Next: start mqtt_exporter.py. See the README of this folder."
