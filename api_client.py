"""Public-holiday API helpers."""

import datetime as dt
from typing import Iterable

import requests
import streamlit as st

HOLIDAYS_URL = "https://date.nager.at/api/v3/PublicHolidays/{year}/{country}"
COUNTRIES_URL = "https://date.nager.at/api/v3/AvailableCountries"

_REQUEST_TIMEOUT = 5  # seconds

@st.cache_data(ttl=86_400, show_spinner=False)
def fetch_public_holidays(country_code: str, year: int) -> list[dict]:
    """Fetch one country's holidays for a year."""
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
    """Return holiday dates only."""
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
    """Return holidays with date and names."""
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
