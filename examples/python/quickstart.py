"""Search homes for sale in an Australian suburb, then read that suburb's median price.

    python quickstart.py "Bondi Beach"
"""

import sys

from client import get, money, suburb_token

suburb = suburb_token(sys.argv[1] if len(sys.argv) > 1 else "Bondi Beach")

# 1. Homes for sale with 2+ bedrooms, newest first.
results = get(
    "/search-listings",
    listing_type="sale",
    locations=suburb,
    min_bedrooms=2,
    sort_by="date-listed",
    sort_order="desc",
    page_size=20,
)
print(f"{results['total']} homes for sale, showing {results['count']}\n")
for home in results["results"]:
    if home["result_type"] != "listing":
        continue  # new-development projects are mixed in; read them with /project
    price = home["price"]
    # display_price is the advertised text ("Auction", "Contact Agent", "Guide $2,500,000").
    # price_from / price_to hold the figures behind it when the agent supplied them.
    print(
        f"{price['display_price'][:28]:<28} {money(price['price_from']):>12}  "
        f"{home['bedrooms']} bd {home['bathrooms']} ba  {home['property_type']:<18} "
        f"{home['address']['display_address']}"
    )

# 2. The suburb's median sold price for 3-bedroom houses, with its yearly series.
market = get("/suburb-market-insights", suburb=suburb, property_type="house", bedrooms=3)
print(f"\n3-bedroom houses in {market['suburb']['name']}: median {money(market['median_sold_price'])}")
for year in market["yearly"]:
    # A 0 median means Domain published no figure for that year.
    print(f"  {year['year']}: {money(year['median_sold_price']):>12}  ({year['number_sold']} sold)")
