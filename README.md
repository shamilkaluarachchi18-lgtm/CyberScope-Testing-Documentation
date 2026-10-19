# CyberScope — Device-DNA Integrity Monitoring and Blockchain Verification

CyberScope fingerprints 18 attributes of the host it runs on (hostname, OS, kernel,
network interfaces, listening ports, services, firewall, `/etc/hosts` hash, …), hashes them
with SHA-256 into a **Device DNA**, registers the trusted DNA in a `DeviceDNA` smart contract
on a Ganache Ethereum test chain, and continuously verifies the live DNA against the
blockchain record. A Flask dashboard shows the result.

## Live demo

The dashboard is hosted on a Google Cloud Compute Engine VM (Ubuntu 22.04):

- **Dashboard:** see `DEPLOYMENT.md` for the current URL
- **Simulate Configuration Change** button opens a temporary listening port (8765) on the
  server. Listening ports are a monitored attribute, so the status flips to
  **POTENTIAL COMPROMISE**; **Stop Simulated Change** closes it and the status returns to
  **LEGITIMATE** without touching the trusted baseline.
- `GET /api/status` returns the verification result as JSON.

## Project layout

| Path | Purpose |
|---|---|
| `collector/collect_attributes.py` | Collects the 18 attributes → `baseline/attributes.json` |
| `collector/dna_generator.py` | SHA-256 of the baseline → `baseline/baseline_hash.txt` |
| `collector/verify_device.py` | Local comparison of live vs baseline |
| `blockchain/contracts/DeviceDNA.sol` | Smart contract: `registerDNA`, `getTrustedDNA`, `verifyDNA` |
| `blockchain/scripts/register_dna.js` | Registers the baseline hash in the contract (Truffle) |
| `blockchain/blockchain_verify.py` | Live DNA vs blockchain record (web3.py) |
| `flask_app/app.py` | Dashboard + demo controls |
| `tests/run_tests.py`, `results/` | Evaluation (10 tests, 100% detection, 0% FPR) |
| `deploy/setup.sh` | One-shot server install (systemd + nginx) |
| `deploy/rebaseline.sh` | Re-capture + re-register a known-good baseline |

## Run locally (Ubuntu)

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
npm install

# Terminal 1
npx ganache
# Terminal 2
python collector/collect_attributes.py
python collector/dna_generator.py
cd blockchain && npx truffle migrate --reset --network development
npx truffle exec scripts/register_dna.js --network development && cd ..
python blockchain/blockchain_verify.py
# Terminal 3
python flask_app/app.py      # http://127.0.0.1:5000
```

## Deploy to a fresh Ubuntu 22.04 server

```bash
git clone https://github.com/shamilkaluarachchi18-lgtm/CyberScope-Testing-Documentation.git
cd CyberScope-Testing-Documentation
sudo bash deploy/setup.sh
```

Services: `cyberscope-ganache`, `cyberscope-flask` (`systemctl status …`, `journalctl -u … -f`).
Ganache runs with a deterministic wallet and a persistent database, so the contract address
and registered DNA survive reboots.
