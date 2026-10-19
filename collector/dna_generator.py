import json
import hashlib


with open(
    "baseline/attributes.json",
    "r"
) as file:

    attributes = json.load(file)


normalized_data = json.dumps(
    attributes,
    sort_keys=True,
    separators=(",", ":")
)


device_dna = hashlib.sha256(
    normalized_data.encode()
).hexdigest()


with open(
    "baseline/baseline_hash.txt",
    "w"
) as file:

    file.write(device_dna)


print("")
print("========================================")
print("        CYBERSCOPE DEVICE DNA")
print("========================================")
print("")
print("SHA-256 Device DNA:")
print(device_dna)
print("")
print("Device DNA saved successfully.")
print("")
