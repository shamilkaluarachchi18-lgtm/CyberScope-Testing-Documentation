#!/usr/bin/env bash
# Re-capture the trusted baseline on a KNOWN-GOOD device state and
# re-register it with the smart contract. Run as root: sudo bash deploy/rebaseline.sh
set -euo pipefail
APP_DIR=/opt/cyberscope; APP_USER=cyberscope
curl -s -X POST http://127.0.0.1:5000/simulate/stop >/dev/null || true
sudo -u $APP_USER env USER=$APP_USER bash -c "cd $APP_DIR && venv/bin/python collector/collect_attributes.py >/dev/null && venv/bin/python collector/dna_generator.py"
sudo -u $APP_USER bash -c "cd $APP_DIR/blockchain && ../node_modules/.bin/truffle exec scripts/register_dna.js --network development"
sudo -u $APP_USER env USER=$APP_USER bash -c "cd $APP_DIR && venv/bin/python blockchain/blockchain_verify.py | grep 'BLOCKCHAIN RESULT'"
