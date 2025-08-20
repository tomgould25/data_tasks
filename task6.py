import json
from collections import defaultdict

# Load ATL data
with open("atl.json", "r", encoding="utf-8") as f:
    atl_data = json.load(f)

# Aggregate spend by channel and region
spend_table = defaultdict(lambda: defaultdict(float))
channels = set()
regions = set()

for entry in atl_data:
    channel = entry["channel"].lower()
    region = entry["region"].upper()
    spend = float(entry["spend"])
    spend_table[channel][region] += spend
    channels.add(channel)
    regions.add(region)

channels = sorted(channels)
regions = sorted(regions)

# Print header
header = ["Media Channel"] + regions
print("\t".join(header))

# Print rows
for channel in channels:
    row = [channel]
    for region in regions:
        value = spend_table[channel].get(region, 0.0)
        value_millions = round(value / 1_000_000, 2)
        row.append(f"{value_millions:.2f}")
    print("\t".join(row))