"""Compare the asking price of homes for sale with Domain's valuation of each home.

    python guide_vs_valuation.py "Bondi Beach" --limit 5

For each listing: /listing gives the property id, /property gives the valuation range
(low, mid, high) and the rental estimate. That is two calls per home plus two for the
search, so --limit caps it.
A price outside the valuation range is a prompt to look closer, not proof of anything:
the valuation is an automated estimate with its own confidence level.
"""

import argparse
import csv

from client import get, money, suburb_token

parser = argparse.ArgumentParser()
parser.add_argument("suburb", nargs="?", default="Bondi Beach")
parser.add_argument("--limit", type=int, default=5, help="homes to look up (2 calls each)")
parser.add_argument("--out", default="guide_vs_valuation.csv")
args = parser.parse_args()

suburb = suburb_token(args.suburb)
results = get("/search-listings", listing_type="sale", locations=suburb, page_size=20)
# Keep listings with a price figure; new-development projects have no single home to value.
homes = [
    h for h in results["results"]
    if h["result_type"] == "listing" and (h["price"]["price_from"] or h["price"]["exact_price"])
][: args.limit]

rows = []
for home in homes:
    listing = get("/listing", listing_id=home["listing_id"])
    if not listing.get("property_id"):
        print(f"  {home['address']['display_address']}: no property record, skipped")
        continue
    profile = get("/property", property_id=listing["property_id"])
    valuation = profile.get("valuation") or {}
    rent = profile.get("rental_estimate") or {}
    asking = home["price"]["exact_price"] or home["price"]["price_from"]
    mid = valuation.get("mid_price")
    if not mid:
        position = "no valuation"
    elif asking < valuation["lower_price"]:
        position = "below range"
    elif asking > valuation["upper_price"]:
        position = "above range"
    else:
        position = "in range"
    rows.append(
        {
            "address": home["address"]["display_address"],
            "property_type": home["property_type"],
            "bedrooms": home["bedrooms"],
            "advertised": home["price"]["display_price"],
            "asking": asking,
            "valuation_low": valuation.get("lower_price"),
            "valuation_mid": mid,
            "valuation_high": valuation.get("upper_price"),
            "confidence": valuation.get("price_confidence"),
            "asking_vs_mid_pct": round(100 * (asking - mid) / mid, 1) if mid else None,
            "position": position,
            # The weekly rent is in rental_estimate; valuation.rent_per_week is usually null.
            "weekly_rent_estimate": rent.get("weekly_rent_estimate"),
            "gross_yield_pct": rent.get("percent_yield_rent_estimate"),
            "url": home["url"],
        }
    )
    print(
        f"  {home['address']['display_address']}: asking {money(asking)}, "
        f"valued {money(valuation.get('lower_price'))} to {money(valuation.get('upper_price'))} "
        f"({valuation.get('price_confidence') or '-'}), {position}"
    )

with open(args.out, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0]) if rows else ["address"])
    writer.writeheader()
    writer.writerows(rows)
print(f"\nWrote {len(rows)} rows to {args.out}")
