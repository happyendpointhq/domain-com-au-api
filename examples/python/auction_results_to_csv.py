"""Export one week of auction results for an Australian city to CSV.

    python auction_results_to_csv.py sydney
    python auction_results_to_csv.py melbourne --date 2026-10-17

One call returns the city's clearance rate and every reported result, grouped by suburb.
Cities: sydney, melbourne, brisbane, adelaide, canberra.
"""

import argparse
import csv
from collections import Counter, defaultdict

from client import get, money

# Domain's result codes, grouped. Several codes mean the same outcome.
OUTCOMES = {
    "AUSD": "sold at auction", "AUSN": "sold at auction",
    "AUSA": "sold after auction", "AUSS": "sold after auction",
    "AUSP": "sold prior", "AUPN": "sold prior",
    "AUPI": "passed in", "AUHB": "passed in", "AUNB": "passed in",
    "AUVB": "passed in (vendor bid)",
    "AUPP": "postponed", "AUWD": "withdrawn",
    "PTSD": "sold by private treaty or tender", "PTSN": "sold by private treaty or tender",
    "PTAW": "sold by private treaty or tender", "PTLA": "sold by private treaty or tender",
    "PTSW": "sold by private treaty or tender", "TNSD": "sold by private treaty or tender",
    "TNSN": "sold by private treaty or tender",
    "NP": "not published",
}

parser = argparse.ArgumentParser()
parser.add_argument("city", nargs="?", default="sydney")
parser.add_argument("--date", help="a Saturday from available_dates, YYYY-MM-DD (default: latest)")
parser.add_argument("--out", default="auction_results.csv")
args = parser.parse_args()

week = get("/auction-results", city=args.city, date=args.date)
summary = week["summary"]
print(f"{args.city.title()}, week of {week['auction_date'][:10]}")
# The headline figures are Domain's own tally. Do not recompute them from the rows: the
# rows are only the results reported so far, and many sold rows have no price.
if summary["adj_clearance_rate"]:
    print(
        f"Clearance rate {summary['adj_clearance_rate']:.1%} "
        f"(a year ago {summary.get('last_year_clearance_rate') or 0:.1%}), "
        f"{summary['number_auctioned']} auctioned, {summary['number_sold']} sold, "
        f"median {money(summary['median'])}"
    )
else:
    print("Domain has not published a clearance rate for this week.")

rows = []
for group in week["suburbs"]:
    for home in group["results"]:
        street = " ".join(filter(None, [home.get("street_number"), home.get("street_name"), home.get("street_type")]))
        unit = home.get("unit_number")
        rows.append(
            {
                "suburb": home["suburb"],
                "location": home["location"],
                "address": f"{unit}/{street}" if unit else street,
                "property_type": home["property_type"],
                "bedrooms": home["bedrooms"],
                "result_code": home["result"],
                "outcome": OUTCOMES.get(home["result"], home["result"]),
                "price": home.get("price"),  # absent when the price was not disclosed
                "agency": home.get("agency_name"),
                "listing_id": home.get("listing_id"),
            }
        )

with open(args.out, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0]) if rows else ["suburb"])
    writer.writeheader()
    writer.writerows(rows)

outcomes = Counter(row["outcome"] for row in rows)
sold = [row for row in rows if row["outcome"].startswith("sold")]
print(f"\n{len(rows)} results reported: " + ", ".join(f"{n} {o}" for o, n in outcomes.most_common()))
print(f"{sum(1 for r in sold if r['price'])} of {len(sold)} sales disclose a price")

# The busiest suburbs this week.
by_suburb = defaultdict(Counter)
for row in rows:
    by_suburb[row["suburb"]][row["outcome"].split(" ")[0]] += 1
print("\nBusiest suburbs (sold / passed in / withdrawn or postponed):")
for name, c in sorted(by_suburb.items(), key=lambda kv: -sum(kv[1].values()))[:10]:
    print(f"  {name:<22} {c['sold']:>3} / {c['passed']:>3} / {c['withdrawn'] + c['postponed']:>3}")

print(f"\nWrote {len(rows)} rows to {args.out}")
