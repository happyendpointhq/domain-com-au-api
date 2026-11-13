# Domain.com.au API and Scraper

The Domain.com.au API returns Australian property data from domain.com.au as JSON: homes for
sale, for rent and sold, new developments, property valuations and rental estimates, sale and
rental history, suburb median prices, weekly auction results and clearance rates, schools,
agents and agencies, commercial property and businesses for sale. It is a REST API, so you get
the data in your own code without building and maintaining a Domain scraper.

Built and maintained by [Happy Endpoint](https://happyendpoint.com/library/domain-com-au-api?utm_source=github&utm_medium=readme&utm_campaign=domain-com-au-api).

- Subscribe and test every endpoint on RapidAPI: https://rapidapi.com/happyendpoint/api/domain-com-au1
- Product page: https://happyendpoint.com/library/domain-com-au-api?utm_source=github&utm_medium=readme&utm_campaign=domain-com-au-api

---

## At a glance

| | |
|---|---|
| Base URL | `https://domain-com-au1.p.rapidapi.com` |
| Auth | `x-rapidapi-key` and `x-rapidapi-host` headers |
| Endpoints | 44, all `GET` |
| Coverage | Australia: every state and territory, including Sydney, Melbourne, Brisbane, Perth, Adelaide, Canberra, Hobart and Darwin |
| Listing types | For sale, for rent, sold, share accommodation, new homes and off-the-plan projects, commercial property, businesses for sale |
| Page size | `page_size`, default 20, with `total` and `total_pages` on every search |
| Format | JSON, every response wrapped in `{"success": true, "data": {...}}` |

---

## What data you get

**Listings**
- Search homes for sale, for rent, sold, share and new homes by suburb, area, region, postcode or state, with about 40 filters: price, bedrooms, bathrooms, car spaces, land size, property type, features, keywords, inspection times, auction dates, listed or updated since
- Search inside a map rectangle, a polygon or a radius, or paste a domain.com.au search link
- Full listings: description, photos, floor plans, inspections, auction details and nearby schools

**Properties**
- Domain's automated valuation (low, mid and high, with a confidence level) for any address
- Weekly rental estimate and gross rental yield
- The full sale and rental history of a home, land and internal area, zoning, lot boundaries and similar homes

**Suburbs and the market**
- Median sold price, price range, annual growth and a yearly sales series by property type and bedrooms
- Suburb profiles with census figures and live listing counts, and the buyer demand index
- Weekly auction results and clearance rates for Sydney, Melbourne, Brisbane, Adelaide and Canberra, with every reported result

**Agents, schools, commercial and news**
- Agents and agencies by suburb, with sales statistics, listings and reviews
- School profiles with enrolments, ICSEA and catchment zones
- Commercial property for sale and lease, businesses for sale, and Domain's property news

---

## Quick start

### 1. Get an API key

Subscribe on [RapidAPI](https://rapidapi.com/happyendpoint/api/domain-com-au1). Current plans are listed there. Copy `.env.example` to `.env` and paste your key.

### 2. Make a request

Searches take a suburb token such as `bondi-beach-nsw-2026`. `/locations` finds it from a name:

```bash
curl "https://domain-com-au1.p.rapidapi.com/locations?query=bondi%20beach" \
  -H "x-rapidapi-host: domain-com-au1.p.rapidapi.com" \
  -H "x-rapidapi-key: YOUR_RAPIDAPI_KEY"

curl "https://domain-com-au1.p.rapidapi.com/search-listings?listing_type=sale&locations=bondi-beach-nsw-2026&min_bedrooms=2" \
  -H "x-rapidapi-host: domain-com-au1.p.rapidapi.com" \
  -H "x-rapidapi-key: YOUR_RAPIDAPI_KEY"
```

### Python

```bash
pip install -r requirements.txt
cd examples/python
python quickstart.py "Bondi Beach"
```

```python
from client import get

results = get("/search-listings", listing_type="sale", locations="bondi-beach-nsw-2026", min_bedrooms=2)
for home in results["results"]:
    print(home["price"]["display_price"], home["bedrooms"], home["address"]["display_address"])

week = get("/auction-results", city="sydney")
print(week["summary"]["adj_clearance_rate"])  # 0.429 means 42.9%
```

### JavaScript

```bash
RAPIDAPI_KEY=your_key node examples/javascript/quickstart.mjs "Bondi Beach"
```

---

## Example response

`GET /property?property_id=34-moore-street-bondi-nsw-2026`, trimmed. Values are the example
in the API's public documentation. More responses are in [`samples/`](samples/).

```json
{
  "success": true,
  "data": {
    "property_id": "CG-4221-UX",
    "slug": "34-moore-street-bondi-nsw-2026",
    "type": "House",
    "market_status": "ON_MARKET",
    "bedrooms": 4,
    "bathrooms": 3,
    "land_area": 311,
    "valuation": {
      "lower_price": 4070000,
      "mid_price": 4640000,
      "upper_price": 5210000,
      "price_confidence": "High",
      "source": "APM",
      "date": "2026-10-02T01:03:53.000Z"
    },
    "rental_estimate": {
      "weekly_rent_estimate": 2830,
      "percent_yield_rent_estimate": 3.2,
      "estimate_date": "2026-09-30"
    },
    "timeline": [
      {
        "category": "Rental",
        "date": "2013-07-24T00:00:00.000Z",
        "price": 1000,
        "price_description": "PER WEEK"
      }
    ],
    "suburb_sales_by_year": [
      { "year": 2022, "median_sold_price": 4550000, "number_sold": 22, "annual_growth": 0 }
    ]
  }
}
```

---

## Endpoints

Base URL: `https://domain-com-au1.p.rapidapi.com`

### Locations

| Endpoint | Returns |
|---|---|
| `GET /locations` | Suburb, area, region and postcode tokens for the listing searches, from the start of a place name |
| `GET /address-suggestions` | Matching street addresses, each with the property id and slug that `/property` takes |

### Listings

| Endpoint | Returns |
|---|---|
| `GET /search-listings` | Homes for sale, for rent, sold, share or new homes in one or more locations, with every filter |
| `GET /search-listings-by-area` | The same search inside a map rectangle, a polygon or a radius around a point |
| `GET /listings-by-url` | The results of a domain.com.au search link, with the link read back as search parameters |
| `GET /listing` | One listing in full by listing id, including the property id of the home |
| `GET /listing-by-url` | One listing in full from its domain.com.au link |
| `GET /listing-schools` | Government and non-government schools near a listing, with distances |
| `GET /project` | A new development: description, features, media, display suite times and its child listings |

### Properties

| Endpoint | Returns |
|---|---|
| `GET /property` | One home's valuation, rental estimate, sale and rental history, attributes, comparable sales and nearby schools |
| `GET /property-by-url` | The same profile from a domain.com.au property-profile link |
| `GET /similar-properties` | Homes similar to one property: recently sold, for sale and for rent |

### Suburbs and the market

| Endpoint | Returns |
|---|---|
| `GET /suburb-market-insights` | Median sold price, recent price range, annual growth, days on market and yearly figures, by property type and bedrooms |
| `GET /suburb-profile` | Census summary, live for-sale and for-rent counts, neighbouring suburbs and schools |
| `GET /suburb-buyer-demand` | Market temperature and the monthly likely-buyers index for houses or units |
| `GET /auction-results` | A city's weekly clearance rate and every reported auction result by suburb, for the latest or a recent week |
| `GET /school` | A school's enrolments, staffing, ICSEA, nearby schools and catchment zones |

### Agents and agencies

| Endpoint | Returns |
|---|---|
| `GET /agent-suggestions` | Agents and agencies by part of their name, with their ids |
| `GET /agents` | Agents working in one or more suburbs, with local sales and leasing activity and ratings |
| `GET /agencies` | Agencies working in one or more suburbs, with local activity and ratings |
| `GET /agent` | One agent's profile by contact id |
| `GET /agent-listings` | An agent's for-sale, sold, for-rent or leased listings |
| `GET /agent-reviews` | An agent's reviews, page by page, with the overall rating |
| `GET /agent-testimonials` | Client testimonials on an agent's profile |
| `GET /agent-sales-statistics` | An agent's sold totals, average price, days on market and top sale, overall or for one suburb |
| `GET /agency` | One agency's profile by agency id |
| `GET /agency-agents` | Every agent at an agency |
| `GET /agency-listings` | An agency's for-sale, sold, for-rent or leased listings |
| `GET /agency-reviews` | An agency's reviews, page by page, with the overall rating |
| `GET /agency-sales-statistics` | An agency's sold totals, average price, days on market and top sale |
| `GET /agent-by-url` | An agent's profile from its domain.com.au link |
| `GET /agency-by-url` | An agency's profile from its domain.com.au link |

### Commercial property and businesses

| Endpoint | Returns |
|---|---|
| `GET /commercial-locations` | Location tokens for the commercial and business searches |
| `GET /commercial-categories` | Category ids such as offices, retail, industrial, cafes and restaurants |
| `GET /commercial-listings` | Commercial property for sale, for lease, sold or leased, with size, price, occupancy and category filters |
| `GET /business-listings` | Businesses for sale by location, category and price |
| `GET /commercial-listing` | One commercial listing in full: sizes, price, zoning, images, documents and transport |
| `GET /business-listing` | One business-for-sale listing in full |
| `GET /commercial-agencies` | Commercial agencies and business brokers active in a location |
| `GET /commercial-agents` | Commercial agents and business brokers active in a location or state |
| `GET /commercial-agency` | One commercial agency's profile, team and listing statistics |

### News and health

| Endpoint | Returns |
|---|---|
| `GET /articles` | Property news by tag or section, newest first |
| `GET /article` | One news article in full |
| `GET /status` | Service health |

---

## Things to know about the data

These come from running the examples against the live API on 28 October 2026. They are the
mistakes that produce wrong numbers rather than errors.

- **The advertised price is often not a number.** Most Bondi Beach listings showed
  `display_price` as "Auction", "Contact Agent" or "Expressions Of Interest". The figure
  behind it, when the agent supplied one, is in `price.price_from` and `price.price_to` on
  search results and in `price.exact_price` on `/listing`. Use those numbers and keep
  `display_price` as text.
- **New developments are mixed into searches.** Off-the-plan homes come back as listings with
  `property_type: "NewApartments"` (in Bondi Beach, three- and four-bedroom residences at
  $10.6 million to $19.5 million behind "Contact Agent"), and whole projects can come back
  with `result_type: "project"`. Filter on both before you take a median of resale prices.
- **The clearance rate is Domain's own tally, not a count of the rows.** For Sydney in the
  week of 24 October, the summary said 252 sold out of 587 auctioned (42.9%), while the 804
  result rows held 278 sales, because the rows include homes sold before auction. Report the
  `summary` figures and use the rows for suburb detail.
- **Many sale prices are withheld.** Only 142 of the 278 sales that week disclosed a price;
  `price` is missing (not `null`) on the rest. Count sales and average prices from different
  sets of rows, and say how many had a price.
- **Result codes are passed through as Domain publishes them.** Several codes mean the same
  outcome (`AUSD` and `AUSN` are both "sold at auction"). The full mapping is in
  [`auction_results_to_csv.py`](examples/python/auction_results_to_csv.py).
- **Valuations come with a confidence level, and it matters.** A four-bedroom beachfront
  apartment asking $11,000,000 was valued at $2,360,000 to $3,080,000 with `Low` confidence.
  Check `price_confidence` before comparing a price with the valuation.
- **The rent estimate is in `rental_estimate`.** `valuation.rent_per_week` and
  `valuation.rent_yield` were `null` on every home we read; `rental_estimate` had the weekly
  rent and gross yield.
- **A median of 0 means no figure.** In `suburb_sales_by_year` and `/suburb-market-insights`,
  a year with a `0` median had sales but no published median. Treat 0 as missing.
- **Property history mixes sales and rentals.** `timeline` holds both, with `category` set to
  `Sale` or `Rental` and rents priced per week. On the home we checked, the current listing
  appeared with `price: null`.
- **Comparable sales on `/property` carry no price.** They give the address, rooms and photos.
  Sold prices come from `/search-listings` with `listing_type=sold`.
- **Searches take tokens, not names.** "Bondi Beach" has to become `bondi-beach-nsw-2026`
  first, and some suburb names are used more than once across Australia. `client.suburb_token()` looks it
  up and prints which suburb it picked.

---

## Examples in this repo

| File | What it does |
|---|---|
| [`examples/python/quickstart.py`](examples/python/quickstart.py) | Homes for sale in a suburb, then the suburb's median price for 3-bedroom houses by year |
| [`examples/python/auction_results_to_csv.py`](examples/python/auction_results_to_csv.py) | One week of auction results for a city: the clearance rate, every result to CSV and the busiest suburbs |
| [`examples/python/guide_vs_valuation.py`](examples/python/guide_vs_valuation.py) | Homes for sale with their asking price against Domain's valuation range and rental yield, to CSV |
| [`examples/javascript/quickstart.mjs`](examples/javascript/quickstart.mjs) | The quickstart in Node 18+, no dependencies |
| [`samples/`](samples/) | Documented example responses for seven endpoints |

---

## API or your own Domain scraper

A homemade domain.com.au scraper works until the site changes its pages or blocks the
traffic, and then it returns nothing or the wrong fields. This API returns the same listings,
valuations and auction results as documented JSON with a stable contract, so the work you keep
is the analysis, not the parser. If you need a one-off national file or a recurring export
rather than API calls, [contact us](https://happyendpoint.com/contact?utm_source=github&utm_medium=readme&utm_campaign=domain-com-au-api).

---

## Use it from Claude, Cursor or any MCP client

RapidAPI exposes every endpoint as an MCP tool, so an AI assistant can query Australian
property data without code:

```json
{
  "mcpServers": {
    "domain-com-au": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "https://mcp.rapidapi.com",
        "--header",
        "x-api-host: domain-com-au1.p.rapidapi.com",
        "--header",
        "x-api-key: YOUR_RAPIDAPI_KEY"
      ]
    }
  }
}
```

| Client | Config path |
|---|---|
| Claude Desktop (macOS) | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Claude Desktop (Windows) | `%APPDATA%\Claude\claude_desktop_config.json` |
| Cursor | `~/.cursor/mcp.json` |
| Claude Code | `.mcp.json` in your project root |

---

## FAQ

### Is there a Domain.com.au API?

Domain has its own developer portal with official APIs, which need a Domain developer
account. This API is a separate option: built and
maintained by Happy Endpoint, independent of Domain, and available to anyone with a RapidAPI
key. It returns the property data that Domain publishes on domain.com.au.

### Is there a realestate.com.au API?

realestate.com.au does not offer a public API for its listings; its developer APIs are for
agencies and their software providers. Domain covers the same national market, so for
Australian listings, sold prices, valuations and suburb data, this API is a practical
alternative.

### Can I get Australian sold prices and auction results?

Yes. `/search-listings` with `listing_type=sold` returns sold homes with their sale price where
it was disclosed, and `/auction-results` returns the weekly clearance rate and every reported
result for Sydney, Melbourne, Brisbane, Adelaide and Canberra.
[`auction_results_to_csv.py`](examples/python/auction_results_to_csv.py) exports a week to CSV.

### Can I get a property valuation for an address?

Yes. `/address-suggestions` turns an address into a property id, and `/property` returns
Domain's valuation range with its confidence level, the weekly rental estimate and yield, and
the home's sale and rental history.

### How do I use the Domain API in Python?

Install `requests`, set `RAPIDAPI_KEY`, and call the endpoints with the two RapidAPI headers.
[`examples/python/client.py`](examples/python/client.py) is a short client with a helper that
turns a suburb name into the token the searches take, and the other scripts in that folder are
ready to run.

### Is there a free Domain API?

Plans, including what each one allows, are on the
[RapidAPI listing](https://rapidapi.com/happyendpoint/api/domain-com-au1), where every endpoint
can also be tested in the browser.

### Where is the documentation?

Every endpoint, parameter and response is documented on the RapidAPI listing, and the endpoint
tables above summarise them. Example responses are in [`samples/`](samples/).

---

## Related repos

- [awesome-real-estate-apis](https://github.com/happyendpointhq/awesome-real-estate-apis) - real estate APIs and data sources by country, including free and official ones
- [rent-com-api](https://github.com/happyendpointhq/rent-com-api) - US rental listings, with a watchlist and CSV export
- [yad2-api](https://github.com/happyendpointhq/yad2-api) - Israel listings with registered sale prices
- [fotocasa-api](https://github.com/happyendpointhq/fotocasa-api) - Spain homes for sale and rent
- [uae-real-estate-api](https://github.com/happyendpointhq/uae-real-estate-api) - asking versus paid prices in Dubai

---

## Disclaimer

Happy Endpoint is an independent provider. This project is **not affiliated
with, endorsed by, sponsored by, or connected to** any of the websites,
platforms, retailers, or marketplaces referenced here or reachable through the
underlying APIs.

All product names, brands, trademarks, and registered trademarks are the
property of their respective owners. Any reference to them is descriptive only,
to identify the subject matter of the data, and does not imply any association
or endorsement.

Users are responsible for ensuring their use of any data complies with
applicable laws and the terms of service of the relevant source.

---

## About Happy Endpoint

[Happy Endpoint](https://happyendpoint.com) builds and maintains real-time data
APIs for property portals, retailers, and marketplaces. All APIs are available on
RapidAPI with a free tier.

- Catalogue: [happyendpoint.com/library](https://happyendpoint.com/library)
- Datasets: [happyendpoint.com/datasets](https://happyendpoint.com/datasets)
- Documentation: [docs.happyendpoint.com](https://docs.happyendpoint.com)
- Contact: hello@happyendpoint.com

## Licence

MIT. See [LICENSE](LICENSE).
