import csv
from collections import defaultdict
from datetime import datetime

# File paths
input_file = "sales - sales.csv"
output_file = "revenue_summary.csv"

# Dictionary: {(year, region): revenue_sum}
revenue_data = defaultdict(float)

# Read the CSV
with open(input_file, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    # Organize data by (date, region)
    records = defaultdict(dict)
    for row in reader:
        date = datetime.strptime(row["date"], "%d-%b-%Y")
        region = row["region"]
        metric = row["metric"]

        # Handle missing/invalid values
        value_str = row["value"].strip()
        if value_str in ("", "-", "NA", "N/A"):
            value = 0.0
        else:
            value = float(value_str)

        records[(date, region)][metric] = value

    # Calculate revenues
    for (date, region), metrics in records.items():
        if "units" in metrics and "price" in metrics:
            revenue = metrics["units"] * metrics["price"]
            year = date.year
            revenue_data[(year, region)] += revenue

years = sorted({year for (year, _) in revenue_data.keys()})
regions = sorted({region for (_, region) in revenue_data.keys()})

with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    writer.writerow(["Year"] + regions)

    for year in years:
        row = [year]
        for region in regions:
            revenue = revenue_data.get((year, region), 0.0)
            row.append(round(revenue / 1_000_000, 2))  # in millions
        writer.writerow(row)

print(f"✅ Pivot-style revenue summary saved as {output_file}")