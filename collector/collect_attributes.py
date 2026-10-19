import platform
import socket
import psutil
import json
import subprocess
import hashlib
import os


attributes = {}


# 1. Hostname
attributes["hostname"] = socket.gethostname()


# 2. Operating system
attributes["os"] = platform.system()


# 3. OS version
attributes["os_version"] = platform.version()


# 4. Kernel version
attributes["kernel"] = platform.release()


# 5. Architecture
attributes["architecture"] = platform.machine()


# 6. Processor
attributes["processor"] = platform.processor()


# 7. CPU count
attributes["cpu_count"] = psutil.cpu_count()


# 8. Username
attributes["username"] = os.getenv("USER")


# Network information
interfaces = psutil.net_if_addrs()


# 9. Network interfaces
attributes["network_interfaces"] = sorted(
    list(interfaces.keys())
)


# 10. IP addresses
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


# 11. MAC addresses
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


# 12. Listening ports
# Ignore CyberScope's own ports:
# 8545 = Ganache
# 5000 = Flask

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


# 13. Running services
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


# 14. SSH service status
try:

    ssh_status = subprocess.check_output(
        "service ssh status 2>/dev/null | head -1",
        shell=True
    ).decode().strip()

    attributes["ssh_status"] = ssh_status

except Exception:

    attributes["ssh_status"] = \
        "not available"


# 15. Default gateway
try:

    gateway = subprocess.check_output(
        "ip route | grep default | awk '{print $3}'",
        shell=True
    ).decode().strip()

    attributes["default_gateway"] = gateway

except Exception:

    attributes["default_gateway"] = \
        "unknown"


# 16. DNS configuration
try:

    dns = subprocess.check_output(
        "grep nameserver /etc/resolv.conf",
        shell=True
    ).decode().strip()

    attributes["dns"] = dns

except Exception:

    attributes["dns"] = \
        "unknown"


# 17. Firewall status
try:

    firewall = subprocess.check_output(
        "sudo ufw status 2>/dev/null | head -1",
        shell=True
    ).decode().strip()

    attributes["firewall_status"] = \
        firewall

except Exception:

    attributes["firewall_status"] = \
        "unknown"


# 18. /etc/hosts file hash
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


# Save trusted baseline
with open(
    "baseline/attributes.json",
    "w"
) as file:

    json.dump(
        attributes,
        file,
        indent=4,
        sort_keys=True
    )


print("")
print("========================================")
print("     CYBERSCOPE BASELINE COLLECTOR")
print("========================================")

print("")
print(
    "Number of monitored attributes:",
    len(attributes)
)

print("")
print(
    json.dumps(
        attributes,
        indent=4,
        sort_keys=True
    )
)

print("")
print(
    "Trusted baseline saved successfully."
)

print("")
