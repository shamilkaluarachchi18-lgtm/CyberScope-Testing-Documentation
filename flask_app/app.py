from flask import Flask, render_template, redirect, url_for, jsonify
import signal
import sys
import json
import hashlib
import platform
import socket
import psutil
import subprocess
import os
from web3 import Web3


app = Flask(__name__)

# Run from the project root so relative paths (baseline/, blockchain/) resolve
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(PROJECT_ROOT)

# ------------------------------------------------------------
# DEMO: simulated configuration change (opens listening port 8765)
# Equivalent to Step 8 of the demo guide: python3 -m http.server 8765
# ------------------------------------------------------------
SIMULATION_PORT = 8765
simulation_process = None


def simulation_running():
    global simulation_process
    if simulation_process is None:
        return False
    if simulation_process.poll() is not None:
        simulation_process = None
        return False
    return True


def collect_attributes():

    attributes = {}

    attributes["hostname"] = socket.gethostname()
    attributes["os"] = platform.system()
    attributes["os_version"] = platform.version()
    attributes["kernel"] = platform.release()
    attributes["architecture"] = platform.machine()
    attributes["processor"] = platform.processor()
    attributes["cpu_count"] = psutil.cpu_count()
    attributes["username"] = os.getenv("USER")

    interfaces = psutil.net_if_addrs()

    attributes["network_interfaces"] = sorted(
        list(interfaces.keys())
    )

    ip_addresses = []

    for interface, addresses in interfaces.items():
        for address in addresses:

            if address.family == socket.AF_INET:

                if address.address != "127.0.0.1":

                    ip_addresses.append(
                        address.address
                    )

    attributes["ip_addresses"] = sorted(
        ip_addresses
    )

    mac_addresses = []

    for interface, addresses in interfaces.items():
        for address in addresses:

            if str(address.family).endswith(
                "AF_PACKET"
            ):

                if address.address != \
                        "00:00:00:00:00:00":

                    mac_addresses.append(
                        address.address
                    )

    attributes["mac_addresses"] = sorted(
        mac_addresses
    )

    ignored_ports = {
        8545,
        5000
    }

    listening_ports = []

    for connection in psutil.net_connections(
            kind="inet"):

        if connection.status == \
                psutil.CONN_LISTEN:

            if connection.laddr:

                port = connection.laddr.port

                if port not in ignored_ports:

                    listening_ports.append(
                        port
                    )

    attributes["listening_ports"] = sorted(
        list(set(listening_ports))
    )

    try:

        services = subprocess.check_output(
            "service --status-all 2>/dev/null | grep '+'",
            shell=True
        ).decode().strip().split("\n")

        attributes["running_services"] = sorted(
            services
        )

    except Exception:

        attributes["running_services"] = []

    try:

        ssh_status = subprocess.check_output(
            "service ssh status 2>/dev/null | head -1",
            shell=True
        ).decode().strip()

        attributes["ssh_status"] = ssh_status

    except Exception:

        attributes["ssh_status"] = \
            "not available"

    try:

        gateway = subprocess.check_output(
            "ip route | grep default | awk '{print $3}'",
            shell=True
        ).decode().strip()

        attributes["default_gateway"] = gateway

    except Exception:

        attributes["default_gateway"] = \
            "unknown"

    try:

        dns = subprocess.check_output(
            "grep nameserver /etc/resolv.conf",
            shell=True
        ).decode().strip()

        attributes["dns"] = dns

    except Exception:

        attributes["dns"] = \
            "unknown"

    try:

        firewall = subprocess.check_output(
            "sudo ufw status 2>/dev/null | head -1",
            shell=True
        ).decode().strip()

        attributes["firewall_status"] = firewall

    except Exception:

        attributes["firewall_status"] = \
            "unknown"

    try:

        with open(
            "/etc/hosts",
            "rb"
        ) as file:

            hosts_hash = hashlib.sha256(
                file.read()
            ).hexdigest()

        attributes["hosts_file_hash"] = \
            hosts_hash

    except Exception:

        attributes["hosts_file_hash"] = \
            "unknown"

    return attributes


def generate_dna(attributes):

    normalized_data = json.dumps(
        attributes,
        sort_keys=True,
        separators=(",", ":")
    )

    return hashlib.sha256(
        normalized_data.encode()
    ).hexdigest()


def blockchain_check(current_dna):

    web3 = Web3(
        Web3.HTTPProvider(
            "http://127.0.0.1:8545"
        )
    )

    if not web3.isConnected():

        return {
            "connected": False,
            "status": "BLOCKCHAIN OFFLINE",
            "trusted_dna": "Unavailable",
            "contract_address": "Unavailable",
            "network_id": "Unavailable"
        }

    try:

        with open(
            "blockchain/build/contracts/DeviceDNA.json",
            "r"
        ) as file:

            contract_data = json.load(file)

        abi = contract_data["abi"]
        networks = contract_data["networks"]

        contract_address = None
        network_id = None

        for saved_network_id in networks:

            candidate_address = \
                networks[saved_network_id]["address"]

            code = web3.eth.getCode(
                candidate_address
            )

            if code and code != b"":

                contract_address = \
                    candidate_address

                network_id = \
                    saved_network_id

                break

        if contract_address is None:

            return {
                "connected": True,
                "status": "CONTRACT NOT DEPLOYED",
                "trusted_dna": "Unavailable",
                "contract_address": "Unavailable",
                "network_id": "Unavailable"
            }

        contract = web3.eth.contract(
            address=contract_address,
            abi=abi
        )

        trusted_dna = \
            contract.functions.getTrustedDNA().call()

        if not trusted_dna:

            return {
                "connected": True,
                "status": "DNA NOT REGISTERED",
                "trusted_dna": "Unavailable",
                "contract_address": contract_address,
                "network_id": network_id
            }

        verified = \
            contract.functions.verifyDNA(
                current_dna
            ).call()

        if verified:

            status = "LEGITIMATE"

        else:

            status = "POTENTIAL COMPROMISE"

        return {
            "connected": True,
            "status": status,
            "trusted_dna": trusted_dna,
            "contract_address": contract_address,
            "network_id": network_id
        }

    except Exception as error:

        print(
            "Blockchain error:",
            error
        )

        return {
            "connected": False,
            "status": "BLOCKCHAIN ERROR",
            "trusted_dna": "Unavailable",
            "contract_address": "Unavailable",
            "network_id": "Unavailable"
        }


@app.route("/simulate/start", methods=["POST"])
def simulate_start():
    global simulation_process
    if not simulation_running():
        simulation_process = subprocess.Popen(
            [sys.executable, "-m", "http.server", str(SIMULATION_PORT), "--bind", "127.0.0.1"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        # give the socket a moment to open before re-verifying
        import time
        time.sleep(0.5)
    return redirect(url_for("dashboard"))


@app.route("/simulate/stop", methods=["POST"])
def simulate_stop():
    global simulation_process
    if simulation_running():
        simulation_process.terminate()
        try:
            simulation_process.wait(timeout=5)
        except Exception:
            simulation_process.kill()
        simulation_process = None
        import time
        time.sleep(0.5)
    return redirect(url_for("dashboard"))


@app.route("/api/status")
def api_status():
    attributes = collect_attributes()
    current_dna = generate_dna(attributes)
    result = blockchain_check(current_dna)
    result["current_dna"] = current_dna
    result["simulation_running"] = simulation_running()
    return jsonify(result)


@app.route("/")
def dashboard():

    attributes = \
        collect_attributes()

    current_dna = \
        generate_dna(attributes)

    blockchain_result = \
        blockchain_check(
            current_dna
        )

    with open(
        "baseline/attributes.json",
        "r"
    ) as file:

        baseline_attributes = \
            json.load(file)

    changed_details = []

    for key in baseline_attributes:

        baseline_value = \
            baseline_attributes.get(key)

        current_value = \
            attributes.get(key)

        if baseline_value != current_value:

            changed_details.append(
                {
                    "name": key,
                    "baseline": baseline_value,
                    "current": current_value
                }
            )

    return render_template(
        "index.html",

        status=
        blockchain_result["status"],

        connected=
        blockchain_result["connected"],

        trusted_dna=
        blockchain_result["trusted_dna"],

        current_dna=
        current_dna,

        contract_address=
        blockchain_result[
            "contract_address"
        ],

        network_id=
        blockchain_result[
            "network_id"
        ],

        attributes=
        attributes,

        changed_details=
        changed_details,

        simulation_running=
        simulation_running(),

        simulation_port=
        SIMULATION_PORT
    )


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
