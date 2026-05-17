"""Small API helpers used by the app."""

import datetime as dt
import re
from html import unescape
from typing import Iterable

import requests
import streamlit as st

HOLIDAYS_URL = "https://date.nager.at/api/v3/PublicHolidays/{year}/{country}"
COUNTRIES_URL = "https://date.nager.at/api/v3/AvailableCountries"
CAFETERIA_MENU_URL = "https://monbistrot.pt/display/10"
CAFETERIA_WEEKLY_MENU_URL_TEMPLATE = (
    "https://monbistrot.pt/display-weekly/10?range={range_name}"
)
CAFETERIA_WEEKLY_MENU_URL = (
    CAFETERIA_WEEKLY_MENU_URL_TEMPLATE.format(range_name="current-week")
)
CAFETERIA_WEEKLY_PAGE_URL_TEMPLATE = (
    "https://monbistrot.pt/menu/nova-sbe-semana-de-{start}-{end}"
)
DAILY_QUOTE_URL = "https://zenquotes.io/api/today"

_REQUEST_TIMEOUT = 5  # seconds
_CAFETERIA_TIMEOUT = 12
_QUOTE_FALLBACKS = (
    ("Small steps count when you keep taking them.", "Nova Exam Planner"),
    ("Start with the next useful thing.", "Nova Exam Planner"),
    ("A clear plan makes the hard part lighter.", "Nova Exam Planner"),
    ("Progress is built one focused block at a time.", "Nova Exam Planner"),
    ("Do the work in front of you, then do the next one.", "Nova Exam Planner"),
)


def _clean_menu_line(value) -> str:
    line = unescape(str(value or "")).strip()
    return re.sub(r"\s+", " ", line)


def _build_menu_sections(dishes: list[dict]) -> list[dict]:
    sections_by_key: dict[str, dict] = {}
    section_order: list[str] = []

    for dish in dishes:
        if not isinstance(dish, dict):
            continue

        language = _clean_menu_line(dish.get("language")).lower()
        if language and language != "en":
            continue

        title = _clean_menu_line(dish.get("category"))
        item = _clean_menu_line(dish.get("designation") or dish.get("type"))
        parenthetical = re.fullmatch(r"[^()]+\(([^()]+)\)\s*", item)
        if parenthetical:
            item = _clean_menu_line(parenthetical.group(1))
        if not title or not item:
            continue

        key = title.lower()
        if key not in sections_by_key:
            sections_by_key[key] = {"title": title, "items": []}
            section_order.append(key)

        items = sections_by_key[key]["items"]
        if item.lower() not in {existing.lower() for existing in items}:
            items.append(item)

    return [sections_by_key[key] for key in section_order
            if sections_by_key[key]["items"]]


def _format_menu_day_label(date_text: str) -> str:
    normalized = _clean_menu_line(date_text)
    try:
        parsed = dt.datetime.strptime(normalized, "%Y-%m-%d")
    except ValueError:
        return normalized
    return f"{parsed:%A}, {parsed:%B} {parsed.day}"


def _format_week_label(start_date_text: str, end_date_text: str) -> str:
    try:
        start = dt.datetime.strptime(_clean_menu_line(start_date_text), "%Y-%m-%d")
        end = dt.datetime.strptime(_clean_menu_line(end_date_text), "%Y-%m-%d")
    except ValueError:
        return f"{start_date_text} - {end_date_text}"

    if start.month == end.month:
        month = start.strftime("%B")
        return f"{month} {start.day} - {month} {end.day}"
    return f"{start:%B} {start.day} - {end:%B} {end.day}"


def _current_week_bounds(
    reference_date: dt.date | None = None,
) -> tuple[dt.date, dt.date]:
    today = reference_date or dt.date.today()
    monday = today - dt.timedelta(days=today.weekday())
    friday = monday + dt.timedelta(days=4)
    return monday, friday


def _weekly_page_url(reference_date: dt.date | None = None) -> str:
    monday, friday = _current_week_bounds(reference_date)
    return CAFETERIA_WEEKLY_PAGE_URL_TEMPLATE.format(
        start=monday.isoformat(),
        end=friday.isoformat(),
    )


def _weekly_page_day_label(day_token: str) -> str:
    mapping = {
        "segunda": "Monday",
        "terca": "Tuesday",
        "ter\u00e7a": "Tuesday",
        "quarta": "Wednesday",
        "quinta": "Thursday",
        "sexta": "Friday",
    }
    return mapping.get(_clean_menu_line(day_token).lower(), day_token.title())


def _build_weekly_sections_from_text(day_text: str) -> list[dict]:
    text = _clean_menu_line(day_text)
    if not text:
        return []

    label_patterns = [
        ("Soup", [r"Soup", r"Sopa"]),
        (
            "Meat or Fish",
            [r"Meat\s+Or\s+Fish\s*\|\s*EN", r"Meat\s+Or\s+Fish",
             r"Carne\s+ou\s+Peixe"],
        ),
        (
            "Green Vibes",
            [r"Green\s+Vibes\s*\|\s*EN", r"Green\s+Vibes", r"Vegetariano"],
        ),
        ("Nomad", [r"Nomad\s*\|\s*EN", r"Nomad"]),
    ]
    boundary = (
        r"(?:Soup|Sopa|Meat\s+Or\s+Fish(?:\s*\|\s*(?:EN|PT))?|"
        r"Carne\s+ou\s+Peixe|Green\s+Vibes(?:\s*\|\s*(?:EN|PT))?|"
        r"Vegetariano|Nomad(?:\s*\|\s*(?:EN|PT))?|"
        r"Segunda|Ter(?:c|\u00e7)a|Quarta|Quinta|Sexta|$)"
    )

    sections = []
    for title, patterns in label_patterns:
        item = ""
        for pattern in patterns:
            match = re.search(
                rf"{pattern}\s+(.*?)(?={boundary})",
                text,
                flags=re.IGNORECASE,
            )
            if match:
                item = _clean_menu_line(match.group(1))
                if item:
                    break
        if item:
            sections.append({"title": title, "items": [item]})
    return sections


def _fetch_weekly_menu_from_page(
    reference_date: dt.date | None = None,
) -> dict:
    source_url = _weekly_page_url(reference_date)
    response = requests.get(source_url, timeout=_CAFETERIA_TIMEOUT)
    response.raise_for_status()

    html = re.sub(
        r"<script\b[^>]*>.*?</script>",
        " ",
        response.text,
        flags=re.IGNORECASE | re.DOTALL,
    )
    html = re.sub(
        r"<style\b[^>]*>.*?</style>",
        " ",
        html,
        flags=re.IGNORECASE | re.DOTALL,
    )
    text = unescape(re.sub(r"<[^>]+>", " ", html))
    text = re.sub(r"\s+", " ", text)

    pattern = re.compile(r"\b(Segunda|Ter(?:c|\u00e7)a|Quarta|Quinta|Sexta)\b",
                         flags=re.IGNORECASE)
    matches = list(pattern.finditer(text))
    if not matches:
        raise ValueError("Could not locate weekday blocks in weekly menu page")

    monday, _ = _current_week_bounds(reference_date)
    day_index = {
        "segunda": 0,
        "terca": 1,
        "ter\u00e7a": 1,
        "quarta": 2,
        "quinta": 3,
        "sexta": 4,
    }
    days = []
    for idx, match in enumerate(matches):
        token_raw = _clean_menu_line(match.group(1))
        block_start = match.end()
        block_end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        sections = _build_weekly_sections_from_text(text[block_start:block_end])
        offset = day_index.get(token_raw.lower())
        if offset is None or not sections:
            continue
        day_date = monday + dt.timedelta(days=offset)
        days.append({
            "date": day_date.isoformat(),
            "date_label": f"{_weekly_page_day_label(token_raw)}, {day_date.isoformat()}",
            "sections": sections,
        })

    if not days:
        raise ValueError("Could not parse any weekly day sections")
    return {"source": source_url, "days": sorted(days, key=lambda d: d["date"])}


def _parse_weekly_json_menus(menus: list[dict]) -> list[dict]:
    days = []
    for menu_day in menus:
        day_date = _clean_menu_line(menu_day.get("date"))
        sections = _build_menu_sections(menu_day.get("dishes") or [])
        if day_date and sections:
            days.append({
                "date": day_date,
                "date_label": _format_menu_day_label(day_date),
                "sections": sections,
            })
    return sorted(days, key=lambda day: day.get("date", ""))


def _last_menu_date(days: list[dict]) -> dt.date | None:
    parsed = []
    for day in days:
        try:
            parsed.append(dt.date.fromisoformat(str(day.get("date"))))
        except ValueError:
            continue
    return max(parsed) if parsed else None


def _choose_weekly_candidate(candidates: list[dict]) -> dict:
    today = dt.date.today()
    current = next(
        (candidate for candidate in candidates
         if candidate.get("range_name") == "current-week"),
        None,
    )
    next_week = next(
        (candidate for candidate in candidates
         if candidate.get("range_name") == "next-week"),
        None,
    )

    if next_week and (not current or (_last_menu_date(current["days"]) or today) < today):
        return next_week
    return current or next_week or candidates[0]


@st.cache_data(ttl=600, show_spinner=False)
def get_daily_cafeteria_menu() -> dict:
    """Fetch the Nova SBE daily cafeteria menu."""
    try:
        response = requests.get(CAFETERIA_MENU_URL, timeout=_CAFETERIA_TIMEOUT)
        response.raise_for_status()
        data = response.json()

        menus = data.get("menus") or []
        if not menus:
            raise ValueError("Cafeteria source returned no menus")

        today = dt.date.today().isoformat()
        selected = next(
            (menu for menu in menus if menu.get("date") == today),
            menus[0],
        )
        sections = _build_menu_sections(selected.get("dishes") or [])
        if not sections:
            raise ValueError("Could not parse English daily menu")

        unit = data.get("unit") or {}
        return {
            "ok": True,
            "source": CAFETERIA_MENU_URL,
            "unit_name": _clean_menu_line(unit.get("name")) or "NOVA SBE",
            "date_label": _format_menu_day_label(selected.get("date") or today),
            "sections": sections,
        }
    except Exception as exc:
        return {
            "ok": False,
            "source": CAFETERIA_MENU_URL,
            "error": str(exc),
            "sections": [],
        }


@st.cache_data(ttl=600, show_spinner=False)
def get_weekly_cafeteria_menu() -> dict:
    """Fetch the Nova SBE weekly cafeteria menu."""
    try:
        candidates = []
        next_week_reference = dt.date.today() + dt.timedelta(days=7)

        for range_name in ("current-week", "next-week"):
            source_url = CAFETERIA_WEEKLY_MENU_URL_TEMPLATE.format(
                range_name=range_name
            )
            data = {}
            try:
                response = requests.get(source_url, timeout=_CAFETERIA_TIMEOUT)
                response.raise_for_status()
                data = response.json() if response.text else {}
                days = _parse_weekly_json_menus(data.get("menus") or [])
                if days:
                    candidates.append({
                        "range_name": range_name,
                        "source": source_url,
                        "unit": data.get("unit") or {},
                        "days": days,
                    })
            except (requests.RequestException, ValueError):
                pass

        if not candidates:
            for range_name, reference in (
                ("current-week", dt.date.today()),
                ("next-week", next_week_reference),
            ):
                try:
                    fallback = _fetch_weekly_menu_from_page(reference)
                    candidates.append({
                        "range_name": range_name,
                        "source": fallback["source"],
                        "unit": {},
                        "days": fallback["days"],
                    })
                except (requests.RequestException, ValueError):
                    pass

        if not candidates:
            raise ValueError("Could not parse weekly menu")

        selected = _choose_weekly_candidate(candidates)
        days = selected["days"]
        unit = selected.get("unit") or {}
        return {
            "ok": True,
            "source": selected["source"],
            "unit_name": _clean_menu_line(unit.get("name")) or "NOVA SBE",
            "week_label": _format_week_label(days[0]["date"], days[-1]["date"]),
            "range_name": selected.get("range_name", "current-week"),
            "days": days,
        }
    except Exception as exc:
        return {
            "ok": False,
            "source": CAFETERIA_WEEKLY_MENU_URL,
            "error": str(exc),
            "days": [],
        }


def _fallback_quote(day_key: str) -> dict:
    idx = sum(ord(char) for char in day_key) % len(_QUOTE_FALLBACKS)
    quote, author = _QUOTE_FALLBACKS[idx]
    return {
        "ok": False,
        "quote": quote,
        "author": author,
        "source": DAILY_QUOTE_URL,
        "source_name": "local fallback",
    }


@st.cache_data(ttl=86_400, show_spinner=False)
def get_daily_motivational_quote(day_key: str) -> dict:
    """Fetch one quote for the dashboard and cache it for the day."""
    try:
        response = requests.get(DAILY_QUOTE_URL, timeout=_REQUEST_TIMEOUT)
        response.raise_for_status()
        data = response.json()
        if not isinstance(data, list) or not data:
            raise ValueError("Quote source returned no quote")

        item = data[0]
        quote = _clean_menu_line(item.get("q"))
        author = _clean_menu_line(item.get("a"))
        if not quote or quote.lower().startswith("too many requests"):
            raise ValueError("Quote source was rate limited")

        return {
            "ok": True,
            "quote": quote,
            "author": author or "Unknown",
            "source": "https://zenquotes.io/",
            "source_name": "ZenQuotes",
        }
    except Exception:
        return _fallback_quote(day_key)


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
