import subprocess
import socket
import json
import sys
from datetime import datetime

BASELINE_FILE = "cyberscope_baseline_v2.json"

IGNORED_INTERNAL_PORTS = {
    5000,   # Flask dashboard
    8545    # Ganache blockchain
}

def run_command(command):
    try:
        result = subprocess.check_output(
            command,
            shell=True,
            universal_newlines=True,
            stderr=subprocess.STDOUT
        )
        return result.strip()
    except subprocess.CalledProcessError:
        return ""

def get_active_interface():
    route = run_command("ip route | grep default")
    if route:
        parts = route.split()
        if "dev" in parts:
            return parts[parts.index("dev") + 1]
    return "unknown"

def get_ephemeral_range():
    try:
        with open("/proc/sys/net/ipv4/ip_local_port_range", "r") as file:
            values = file.read().split()
            return int(values[0]), int(values[1])
    except Exception:
        return 32768, 60999

def get_listening_ports():
    output = run_command("ss -tulnH")

    stable_ports = []
    dynamic_udp_ports = []
    ignored_internal_ports = []

    low_ephemeral, high_ephemeral = get_ephemeral_range()

    for line in output.splitlines():
        parts = line.split()
        if len(parts) < 5:
            continue

        protocol = parts[0].lower()
        local_address = parts[4]

        try:
            port = int(local_address.rsplit(":", 1)[1])
        except Exception:
            continue

        port_entry = "{} {}".format(protocol, local_address)

        if port in IGNORED_INTERNAL_PORTS:
            ignored_internal_ports.append(port_entry)
            continue

        if protocol.startswith("udp") and low_ephemeral <= port <= high_ephemeral:
            dynamic_udp_ports.append(port_entry)
            continue

        stable_ports.append(port_entry)

    return {
        "stable": sorted(stable_ports),
        "dynamic_udp": sorted(dynamic_udp_ports),
        "ignored_internal": sorted(ignored_internal_ports)
    }

def collect_attributes():
    interface = get_active_interface()
    hostname = socket.gethostname()
    ip_address = run_command("hostname -I | awk '{print $1}'")

    if interface != "unknown":
        mac_address = run_command(
            "cat /sys/class/net/{}/address".format(interface)
        )
    else:
        mac_address = "unknown"

    default_gateway = run_command(
        "ip route | grep default | awk '{print $3}' | head -n 1"
    )

    ports = get_listening_ports()

    return {
        "hostname": hostname,
        "interface": interface,
        "ip_address": ip_address,
        "mac_address": mac_address,
        "default_gateway": default_gateway,
        "stable_listening_ports": ports["stable"],
        "dynamic_udp_ports": ports["dynamic_udp"],
        "ignored_internal_ports": ports["ignored_internal"]
    }

def create_baseline():
    attributes = collect_attributes()

    baseline = {
        "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "attributes": attributes
    }

    with open(BASELINE_FILE, "w") as file:
        json.dump(baseline, file, indent=4)

    print("======================================")
    print(" CyberScope V2 Trusted Baseline Created")
    print("======================================")
    print("Hostname:", attributes["hostname"])
    print("Interface:", attributes["interface"])
    print("IP Address:", attributes["ip_address"])
    print("MAC Address:", attributes["mac_address"])
    print("Default Gateway:", attributes["default_gateway"])

    print("\nStable Listening Ports:")
    for port in attributes["stable_listening_ports"]:
        print(port)

    print("\nDynamic UDP Ports:")
    for port in attributes["dynamic_udp_ports"]:
        print(port)

    print("\nCyberScope Internal Ports Ignored:")
    for port in attributes["ignored_internal_ports"]:
        print(port)

    print("\nBaseline saved to", BASELINE_FILE)

def compare_runtime():
    try:
        with open(BASELINE_FILE, "r") as file:
            baseline = json.load(file)
    except IOError:
        print("Baseline file not found.")
        print("Run: python3 cyberscope_compare_v2.py baseline")
        return

    trusted = baseline["attributes"]
    current = collect_attributes()
    important_change = False

    print("======================================")
    print(" CyberScope V2 Runtime Comparison")
    print("======================================")

    attributes = [
        "hostname",
        "interface",
        "ip_address",
        "mac_address",
        "default_gateway"
    ]

    for attribute in attributes:
        baseline_value = trusted.get(attribute)
        current_value = current.get(attribute)

        if baseline_value == current_value:
            status = "MATCH"
        else:
            status = "CHANGED"
            important_change = True

        print("\n{}: {}".format(attribute.upper(), status))
        print("Baseline:", baseline_value)
        print("Current :", current_value)

    baseline_ports = set(trusted.get("stable_listening_ports", []))
    current_ports = set(current.get("stable_listening_ports", []))

    new_ports = current_ports - baseline_ports
    removed_ports = baseline_ports - current_ports

    print("\nSTABLE LISTENING PORTS:")

    if not new_ports and not removed_ports:
        print("MATCH")
    else:
        important_change = True
        print("CHANGED")

        if new_ports:
            print("New stable ports:")
            for port in sorted(new_ports):
                print(" +", port)

        if removed_ports:
            print("Removed stable ports:")
            for port in sorted(removed_ports):
                print(" -", port)

    print("\nDYNAMIC UDP PORTS:")
    print("Baseline:", trusted.get("dynamic_udp_ports", []))
    print("Current :", current.get("dynamic_udp_ports", []))
    print("These changes are informational and do not automatically indicate compromise.")

    print("\nCYBERSCOPE INTERNAL PORTS:")
    print(current.get("ignored_internal_ports", []))
    print("Ports 5000 and 8545 are ignored.")

    print("\n======================================")

    if important_change:
        print("RESULT: POTENTIAL COMPROMISE")
    else:
        print("RESULT: LEGITIMATE")

    print("======================================")

if len(sys.argv) != 2:
    print("Usage:")
    print("python3 cyberscope_compare_v2.py baseline")
    print("python3 cyberscope_compare_v2.py compare")
elif sys.argv[1] == "baseline":
    create_baseline()
elif sys.argv[1] == "compare":
    compare_runtime()
else:
    print("Unknown option.")
