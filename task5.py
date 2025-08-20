import csv
from collections import defaultdict
from datetime import datetime

# File paths
input_file = "sales - sales.csv"
output_file = "weekly_revenue_summary.csv"

# Dictionary: {(year, week, region): revenue_sum}
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
            iso_year, iso_week, _ = date.isocalendar()
            revenue_data[(iso_year, iso_week, region)] += revenue

# Prepare the output data
weeks = sorted({(year, week) for (year, week, _) in revenue_data.keys()})
regions = sorted({region for (_, _, region) in revenue_data.keys()})

# Write the output CSV
with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    writer.writerow(["Week"] + regions)

    for (year, week) in weeks:
        week_label = f"{year}-W{week:02d}"
        row = [week_label]
        for region in regions:
            revenue = revenue_data.get((year, week, region), 0.0)
            row.append(round(revenue / 1_000_000, 2))  # in millions
        writer.writerow(row)

print("Revenue summary saved as 'weekly_revenue_summary.csv'")
# Now the output file contains weekly revenue summaries per region.