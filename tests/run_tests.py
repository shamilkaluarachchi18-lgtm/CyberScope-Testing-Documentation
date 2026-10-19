import os
import sys
import json
import time
import csv
import hashlib
import platform
import socket
import psutil
import subprocess

from web3 import Web3


PROJECT_DIR = os.path.expanduser("~/CyberScope")

CONTRACT_FILE = os.path.join(
    PROJECT_DIR,
    "blockchain",
    "build",
    "contracts",
    "DeviceDNA.json"
)

RESULT_FILE = os.path.join(
    PROJECT_DIR,
    "results",
    "test_results.csv"
)

SUMMARY_FILE = os.path.join(
    PROJECT_DIR,
    "results",
    "evaluation_summary.txt"
)


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

            if str(address.family).endswith("AF_PACKET"):

                if address.address != "00:00:00:00:00:00":

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

    for connection in psutil.net_connections(kind="inet"):

        if connection.status == psutil.CONN_LISTEN:

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

        attributes["ssh_status"] = "not available"

    try:

        gateway = subprocess.check_output(
            "ip route | grep default | awk '{print $3}'",
            shell=True
        ).decode().strip()

        attributes["default_gateway"] = gateway

    except Exception:

        attributes["default_gateway"] = "unknown"

    try:

        dns = subprocess.check_output(
            "grep nameserver /etc/resolv.conf",
            shell=True
        ).decode().strip()

        attributes["dns"] = dns

    except Exception:

        attributes["dns"] = "unknown"

    try:

        firewall = subprocess.check_output(
            "sudo ufw status 2>/dev/null | head -1",
            shell=True
        ).decode().strip()

        attributes["firewall_status"] = firewall

    except Exception:

        attributes["firewall_status"] = "unknown"

    try:

        with open("/etc/hosts", "rb") as file:

            attributes["hosts_file_hash"] = hashlib.sha256(
                file.read()
            ).hexdigest()

    except Exception:

        attributes["hosts_file_hash"] = "unknown"

    return attributes


def generate_dna(attributes):

    normalized = json.dumps(
        attributes,
        sort_keys=True,
        separators=(",", ":")
    )

    return hashlib.sha256(
        normalized.encode()
    ).hexdigest()


def get_contract():

    web3 = Web3(
        Web3.HTTPProvider(
            "http://127.0.0.1:8545"
        )
    )

    if not web3.isConnected():

        raise Exception(
            "Cannot connect to Ganache"
        )

    with open(
        CONTRACT_FILE,
        "r"
    ) as file:

        contract_data = json.load(file)

    abi = contract_data["abi"]

    contract_address = None

    for network_id in contract_data["networks"]:

        address = contract_data[
            "networks"
        ][network_id]["address"]

        code = web3.eth.getCode(
            address
        )

        if code and code != b"":

            contract_address = address
            break

    if contract_address is None:

        raise Exception(
            "No DeviceDNA contract found"
        )

    return web3.eth.contract(
        address=contract_address,
        abi=abi
    )


def verify(contract):

    start = time.time()

    attributes = collect_attributes()

    current_dna = generate_dna(
        attributes
    )

    verified = contract.functions.verifyDNA(
        current_dna
    ).call()

    end = time.time()

    detection_time = end - start

    if verified:

        status = "LEGITIMATE"

    else:

        status = "POTENTIAL COMPROMISE"

    return status, detection_time


def save_result(
        test_type,
        expected,
        actual,
        detection_time):

    file_exists = os.path.exists(
        RESULT_FILE
    )

    with open(
        RESULT_FILE,
        "a",
        newline=""
    ) as file:

        writer = csv.writer(file)

        if not file_exists:

            writer.writerow(
                [
                    "Test ID",
                    "Test Type",
                    "Expected Result",
                    "Actual Result",
                    "Correct",
                    "Detection Time Seconds"
                ]
            )

        test_id = 1

        if file_exists:

            with open(
                RESULT_FILE,
                "r"
            ) as read_file:

                rows = list(
                    csv.reader(
                        read_file
                    )
                )

                test_id = len(rows)

        if actual == expected:

            correct = "YES"

        else:

            correct = "NO"

        writer.writerow(
            [
                test_id,
                test_type,
                expected,
                actual,
                correct,
                "{:.4f}".format(
                    detection_time
                )
            ]
        )


def update_summary():

    with open(
        RESULT_FILE,
        "r"
    ) as file:

        reader = csv.DictReader(file)

        rows = list(reader)

    total_tests = len(rows)

    correct_tests = 0
    legitimate_tests = 0
    false_positives = 0

    total_time = 0

    for row in rows:

        if row["Correct"] == "YES":

            correct_tests += 1

        if row["Expected Result"] == "LEGITIMATE":

            legitimate_tests += 1

            if row["Actual Result"] == \
                    "POTENTIAL COMPROMISE":

                false_positives += 1

        total_time += float(
            row["Detection Time Seconds"]
        )

    accuracy = (
        correct_tests /
        total_tests
    ) * 100

    if legitimate_tests > 0:

        false_positive_rate = (
            false_positives /
            legitimate_tests
        ) * 100

    else:

        false_positive_rate = 0

    average_time = (
        total_time /
        total_tests
    )

    with open(
        SUMMARY_FILE,
        "w"
    ) as file:

        file.write(
            "CYBERSCOPE EVALUATION SUMMARY\n"
        )

        file.write(
            "============================\n\n"
        )

        file.write(
            "Total Tests: {}\n".format(
                total_tests
            )
        )

        file.write(
            "Correct Tests: {}\n".format(
                correct_tests
            )
        )

        file.write(
            "Detection Accuracy: "
            "{:.2f}%\n".format(
                accuracy
            )
        )

        file.write(
            "False Positive Rate: "
            "{:.2f}%\n".format(
                false_positive_rate
            )
        )

        file.write(
            "Average Detection Time: "
            "{:.4f} seconds\n".format(
                average_time
            )
        )


def main():

    if len(sys.argv) != 2:

        print("")
        print(
            "Usage:"
        )

        print(
            "python tests/run_tests.py legitimate"
        )

        print(
            "OR"
        )

        print(
            "python tests/run_tests.py compromised"
        )

        print("")

        return

    mode = sys.argv[1].lower()

    if mode == "legitimate":

        expected = "LEGITIMATE"
        test_type = "Normal Device"

    elif mode == "compromised":

        expected = "POTENTIAL COMPROMISE"
        test_type = "Tampered Device"

    else:

        print(
            "Use legitimate or compromised"
        )

        return

    contract = get_contract()

    print("")
    print("==============================")
    print("CYBERSCOPE TEST")
    print("==============================")

    print("")
    print(
        "Expected:",
        expected
    )

    actual, detection_time = \
        verify(contract)

    print(
        "Actual:",
        actual
    )

    print(
        "Detection Time:",
        "{:.4f}".format(
            detection_time
        ),
        "seconds"
    )

    save_result(
        test_type,
        expected,
        actual,
        detection_time
    )

    update_summary()

    print("")
    print(
        "Result recorded successfully."
    )

    print("")


if __name__ == "__main__":
    main()
