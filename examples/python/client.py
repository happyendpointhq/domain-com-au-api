"""Minimal client for the Domain.com.au API on RapidAPI.

Set RAPIDAPI_KEY in your environment (or in a .env file at the repo root).
"""

import os

import requests

HOST = "domain-com-au1.p.rapidapi.com"


def _load_dotenv():
    """Read RAPIDAPI_KEY from a .env in the current folder or the repo root, if present."""
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
    for path in (".env", os.path.join(root, ".env")):
        if os.path.exists(path):
            for line in open(path, encoding="utf-8"):
                key, sep, value = line.strip().partition("=")
                if sep and value and not key.startswith("#"):
                    os.environ.setdefault(key.strip(), value.strip())


_load_dotenv()


def get(path, **params):
    """GET an endpoint and return the `data` object of the response."""
    key = os.environ.get("RAPIDAPI_KEY")
    if not key:
        raise SystemExit("Set RAPIDAPI_KEY first (see .env.example).")
    response = requests.get(
        f"https://{HOST}{path}",
        params={k: v for k, v in params.items() if v is not None},
        headers={"x-rapidapi-host": HOST, "x-rapidapi-key": key},
        timeout=60,
    )
    response.raise_for_status()
    body = response.json()
    if not body.get("success", True):
        raise RuntimeError(f"{path} failed: {body}")
    return body["data"]


def suburb_token(place):
    """Turn a place name ("Bondi Beach") into the suburb token the searches take
    ("bondi-beach-nsw-2026"). Several suburbs share a name across states, so the first
    suburb match is used and printed; pass the token itself to skip the lookup."""
    if place.count("-") >= 2 and place.split("-")[-1].isdigit():
        return place
    matches = get("/locations", query=place)["results"]
    suburbs = [m for m in matches if m["type"] == "suburb"] or matches
    if not suburbs:
        raise SystemExit(f"No Domain location matches {place!r}.")
    print(f"Using {suburbs[0]['display_name']} ({suburbs[0]['location']})")
    return suburbs[0]["location"]


def money(value):
    return f"${value:,.0f}" if value else "-"
