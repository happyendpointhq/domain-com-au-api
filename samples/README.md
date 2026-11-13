# Sample responses

Example `200` responses for seven Domain.com.au API endpoints, copied from the API's public
documentation. Long arrays are cut to their first three items, and agent fields are removed.
Field names and values are otherwise unchanged. File names follow the endpoint path.

| File | Request |
|---|---|
| `locations.json` | `GET /locations?query=sydney` |
| `address-suggestions.json` | `GET /address-suggestions?query=4/11 flood st bondi` |
| `search-listings.json` | `GET /search-listings?listing_type=sale&locations=bondi-beach-nsw-2026` |
| `listing.json` | `GET /listing?listing_id=2020620392` |
| `property.json` | `GET /property?property_id=34-moore-street-bondi-nsw-2026` |
| `suburb-market-insights.json` | `GET /suburb-market-insights?suburb=bondi-beach-nsw-2026&property_type=house&bedrooms=3` |
| `auction-results.json` | `GET /auction-results?city=sydney&suburb=abbotsford-nsw-2046` |

They are useful for writing parsers and tests before you subscribe. Live data changes
daily, so do not hard-code these values.
