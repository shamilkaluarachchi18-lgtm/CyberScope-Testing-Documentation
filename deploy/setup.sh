#!/usr/bin/env bash
# CyberScope one-shot server setup for Ubuntu 22.04 (GCP Compute Engine).
# Run as root:  sudo bash deploy/setup.sh
# Installs Python/Node deps, deploys the DeviceDNA contract to a persistent
# Ganache chain, generates + registers the trusted baseline, and starts
# Ganache + Flask as systemd services behind nginx on port 80.
set -euo pipefail

APP_USER=cyberscope
APP_DIR=/opt/cyberscope
SRC_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "== 1. System packages"
export DEBIAN_FRONTEND=noninteractive
apt-get update -q
apt-get install -y -q python3 python3-venv python3-pip git curl rsync nginx ufw ca-certificates gnupg
# Node 20 (needed by ganache 7 / truffle 5)
if ! command -v node >/dev/null || [ "$(node -v | cut -d. -f1 | tr -d v)" -lt 18 ]; then
  curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
  apt-get install -y -q nodejs
fi
# Keep the device fingerprint stable: no surprise kernel/OS upgrades
systemctl disable --now unattended-upgrades 2>/dev/null || true
apt-get remove -y -q unattended-upgrades 2>/dev/null || true

echo "== 2. App user + files"
id -u $APP_USER >/dev/null 2>&1 || useradd -m -s /bin/bash $APP_USER
# collector runs 'sudo ufw status' - allow it without a password
echo "$APP_USER ALL=(root) NOPASSWD: /usr/sbin/ufw status" > /etc/sudoers.d/cyberscope
chmod 440 /etc/sudoers.d/cyberscope
mkdir -p $APP_DIR
if [ "$SRC_DIR" != "$APP_DIR" ]; then
  rsync -a --delete --exclude venv --exclude node_modules --exclude ganache-db --exclude .git "$SRC_DIR/" "$APP_DIR/"
fi
chown -R $APP_USER:$APP_USER $APP_DIR

echo "== 3. Python venv + Node modules"
sudo -u $APP_USER bash -c "cd $APP_DIR && python3 -m venv venv && venv/bin/pip install -q --upgrade pip && venv/bin/pip install -q -r requirements.txt"
sudo -u $APP_USER bash -c "cd $APP_DIR && npm install --no-audit --no-fund --silent"

echo "== 4. systemd services"
cat > /etc/systemd/system/cyberscope-ganache.service <<UNIT
[Unit]
Description=CyberScope Ganache (local Ethereum test chain)
After=network.target

[Service]
User=$APP_USER
WorkingDirectory=$APP_DIR
ExecStart=$APP_DIR/node_modules/.bin/ganache --host 127.0.0.1 --port 8545 --wallet.deterministic --chain.networkId 1337 --chain.chainId 1337 --database.dbPath $APP_DIR/ganache-db --miner.blockTime 0
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
UNIT

cat > /etc/systemd/system/cyberscope-flask.service <<UNIT
[Unit]
Description=CyberScope Flask dashboard
After=network.target cyberscope-ganache.service
Requires=cyberscope-ganache.service

[Service]
User=$APP_USER
Environment=USER=$APP_USER
WorkingDirectory=$APP_DIR
ExecStart=$APP_DIR/venv/bin/python flask_app/app.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
UNIT

systemctl daemon-reload
systemctl enable --now cyberscope-ganache
sleep 5

echo "== 5. Deploy contract + register baseline"
sudo -u $APP_USER bash -c "cd $APP_DIR/blockchain && ../node_modules/.bin/truffle migrate --reset --network development"
# Baseline must be captured in the SAME environment the dashboard runs in
# (user, env, services) so the hashes agree. USER is set explicitly.
sudo -u $APP_USER env USER=$APP_USER bash -c "cd $APP_DIR && venv/bin/python collector/collect_attributes.py && venv/bin/python collector/dna_generator.py"
sudo -u $APP_USER bash -c "cd $APP_DIR/blockchain && ../node_modules/.bin/truffle exec scripts/register_dna.js --network development"

systemctl enable --now cyberscope-flask

echo "== 6. nginx reverse proxy on :80"
cat > /etc/nginx/sites-available/cyberscope <<'NG'
server {
    listen 80 default_server;
    server_name _;
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_read_timeout 60s;
    }
}
NG
ln -sf /etc/nginx/sites-available/cyberscope /etc/nginx/sites-enabled/cyberscope
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl restart nginx

echo "== 7. Verify"
sleep 3
sudo -u $APP_USER env USER=$APP_USER bash -c "cd $APP_DIR && venv/bin/python collector/verify_device.py | tail -n 12"
curl -s -o /dev/null -w "Dashboard HTTP %{http_code}\n" http://127.0.0.1/
echo "DONE. Dashboard: http://$(curl -s -H 'Metadata-Flavor: Google' http://169.254.169.254/computeMetadata/v1/instance/network-interfaces/0/access-configs/0/external-ip 2>/dev/null || hostname -I | awk '{print $1}')/"
