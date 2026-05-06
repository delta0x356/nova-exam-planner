"""
External API clients.
====================

Two free public APIs, no keys needed:

* `date.nager.at`   → public holidays per country / year
* `zenquotes.io`    → daily motivational quote

All calls are cached via ``st.cache_data`` so we don't hammer the services
and the app stays fast even if the network is flaky.  Every function falls
back to a sensible local default if the request fails.
"""

import datetime as dt
import random
from typing import Iterable

import requests
import streamlit as st

HOLIDAYS_URL   = "https://date.nager.at/api/v3/PublicHolidays/{year}/{country}"
COUNTRIES_URL  = "https://date.nager.at/api/v3/AvailableCountries"
QUOTE_URL      = "https://zenquotes.io/api/today"
RANDOM_QUOTE_URL = "https://zenquotes.io/api/random"

_REQUEST_TIMEOUT = 5  # seconds


# ─────────────────────────────────────────────────────────────────────────────
# Holidays
# ─────────────────────────────────────────────────────────────────────────────

@st.cache_data(ttl=86_400, show_spinner=False)
def fetch_public_holidays(country_code: str, year: int) -> list[dict]:
    """Return raw holiday dicts from the Nager.Date API, or [] on failure."""
    try:
        r = requests.get(
            HOLIDAYS_URL.format(year=year, country=country_code.upper()),
            timeout=_REQUEST_TIMEOUT,
        )
        if r.ok:
            return r.json()
    except Exception:
        pass
    return []


def get_holiday_dates(country_code: str, years: Iterable[int]) -> set[dt.date]:
    """Flatten the API results into a set of `date` objects."""
    out: set[dt.date] = set()
    for y in years:
        for h in fetch_public_holidays(country_code, y):
            try:
                y2, m, d = map(int, h["date"].split("-"))
                out.add(dt.date(y2, m, d))
            except (KeyError, ValueError, TypeError):
                continue
    return out


def get_holidays_detailed(country_code: str, years: Iterable[int]) -> list[dict]:
    """Return a normalized list: [{date: date, name: str, local_name: str}]."""
    out = []
    for y in years:
        for h in fetch_public_holidays(country_code, y):
            try:
                y2, m, d = map(int, h["date"].split("-"))
                out.append({
                    "date": dt.date(y2, m, d),
                    "name": h.get("name", ""),
                    "local_name": h.get("localName", ""),
                })
            except (KeyError, ValueError, TypeError):
                continue
    out.sort(key=lambda x: x["date"])
    return out


# ─────────────────────────────────────────────────────────────────────────────
# Countries
# ─────────────────────────────────────────────────────────────────────────────

_COUNTRY_FALLBACK = [
    ("DE", "Germany"), ("AT", "Austria"), ("CH", "Switzerland"),
    ("PT", "Portugal"), ("ES", "Spain"), ("FR", "France"),
    ("IT", "Italy"), ("NL", "Netherlands"), ("BE", "Belgium"),
    ("PL", "Poland"), ("GB", "United Kingdom"), ("IE", "Ireland"),
    ("US", "United States"), ("CA", "Canada"), ("BR", "Brazil"),
    ("MX", "Mexico"),
]


@st.cache_data(ttl=604_800, show_spinner=False)
def list_supported_countries() -> list[tuple[str, str]]:
    try:
        r = requests.get(COUNTRIES_URL, timeout=_REQUEST_TIMEOUT)
        if r.ok:
            data = r.json()
            return sorted(
                [(c["countryCode"], c["name"]) for c in data],
                key=lambda x: x[1],
            )
    except Exception:
        pass
    return _COUNTRY_FALLBACK


# ─────────────────────────────────────────────────────────────────────────────
# Quotes
# ─────────────────────────────────────────────────────────────────────────────

_FALLBACK_QUOTES = [
    ("The expert in anything was once a beginner.", "Helen Hayes"),
    ("Success is the sum of small efforts, repeated day in and day out.",
     "Robert Collier"),
    ("The beautiful thing about learning is that no one can take it away from you.",
     "B.B. King"),
    ("Don't watch the clock; do what it does. Keep going.", "Sam Levenson"),
    ("An investment in knowledge pays the best interest.", "Benjamin Franklin"),
    ("The only way to do great work is to love what you do.", "Steve Jobs"),
    ("Learning never exhausts the mind.", "Leonardo da Vinci"),
    ("Study hard what interests you the most in the most undisciplined, "
     "irreverent and original manner possible.", "Richard Feynman"),
    ("Discipline equals freedom.", "Jocko Willink"),
    ("You don't have to be great to start, but you have to start to be great.",
     "Zig Ziglar"),
]


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_daily_quote() -> tuple[str, str]:
    """Return ``(quote, author)``.  Falls back to a curated local list."""
    try:
        r = requests.get(QUOTE_URL, timeout=_REQUEST_TIMEOUT)
        if r.ok:
            data = r.json()
            if isinstance(data, list) and data:
                q = (data[0].get("q") or "").strip()
                a = (data[0].get("a") or "Unknown").strip()
                if q:
                    return q, a
    except Exception:
        pass
    return random.choice(_FALLBACK_QUOTES)
