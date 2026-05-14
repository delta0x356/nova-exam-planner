"""Study-plan scheduling helpers."""

import datetime as dt
from typing import Iterable, Optional

import pandas as pd

DAY_NAMES = [
    "Monday", "Tuesday", "Wednesday", "Thursday",
    "Friday", "Saturday", "Sunday",
]

BLOCK_MINUTES = 45
ROUNDING_MINUTES = 5


def _available_days(start: dt.date, end: dt.date,
                    preferred: set[str],
                    exclude: Optional[set[dt.date]] = None) -> list[dt.date]:
    """Study days before an exam."""
    exclude = exclude or set()
    out, cur = [], start
    while cur < end:
        if DAY_NAMES[cur.weekday()] in preferred and cur not in exclude:
            out.append(cur)
        cur += dt.timedelta(days=1)
    return out


def _week_start(day: dt.date) -> dt.date:
    """Monday of the calendar week containing ``day``."""
    return day - dt.timedelta(days=day.weekday())


def _floor_to_5(minutes: float) -> int:
    """Round down to the nearest 5-minute block."""
    return max(0, int(minutes // 5) * 5)


def _round_to_5(minutes: float) -> int:
    return max(0, int(round(minutes / ROUNDING_MINUTES) * ROUNDING_MINUTES))


def _split_into_blocks(total_minutes: float) -> list[int]:
    """Make near-45 minute sessions without losing the target total."""
    total = _round_to_5(total_minutes)
    if total <= 0:
        return []

    block_count = max(1, round(total / BLOCK_MINUTES))
    base = max(ROUNDING_MINUTES, _floor_to_5(total / block_count))
    blocks = [base for _ in range(block_count)]

    spare = total - sum(blocks)
    i = 0
    while spare >= ROUNDING_MINUTES:
        blocks[i % block_count] += ROUNDING_MINUTES
        spare -= ROUNDING_MINUTES
        i += 1

    return blocks


def _target_index(day_count: int, block_index: int,
                  block_count: int) -> int:
    if day_count <= 1:
        return 0
    if block_count <= 1:
        return day_count // 2
    return round(block_index * (day_count - 1) / (block_count - 1))


def _nearby_indices(day_count: int, target: int):
    yield target
    for offset in range(1, day_count):
        left = target - offset
        right = target + offset
        if left >= 0:
            yield left
        if right < day_count:
            yield right


def _room_on(day: dt.date, day_used: dict, week_used: dict,
             max_daily: int, max_weekly: Optional[float]) -> float:
    daily_room = max_daily - day_used.get(day, 0)
    if max_weekly is None:
        return daily_room
    weekly_room = max_weekly - week_used.get(_week_start(day), 0)
    return min(daily_room, weekly_room)


def generate_study_plan(courses: list[dict], *,
                        preferred_days: Iterable[str],
                        max_hours_per_day: int,
                        start_date: dt.date,
                        weekly_hours: Optional[float] = None,
                        exclude_dates: Optional[Iterable[dt.date]] = None
                        ) -> list[dict]:
    """Build study sessions that respect daily and weekly limits."""
    if not courses:
        return []

    preferred = set(preferred_days)
    max_daily = max_hours_per_day * 60
    max_weekly = weekly_hours * 60 if weekly_hours else None
    exclude = set(exclude_dates) if exclude_dates else set()

    day_used: dict[dt.date, int] = {}
    week_used: dict[dt.date, int] = {}
    course_allocs: dict[int, dict] = {}

    ordered_courses = sorted(courses, key=lambda c: c["exam_date"])
    for c in ordered_courses:
        exam_d = c["exam_date"]
        if isinstance(exam_d, str):
            exam_d = dt.date.fromisoformat(exam_d)
        course_start = c.get("study_start_date", start_date)
        if isinstance(course_start, str):
            course_start = dt.date.fromisoformat(course_start)
        course_start = max(start_date, course_start)
        avail = _available_days(course_start, exam_d, preferred, exclude)

        blocks = _split_into_blocks(c["estimated_hours"] * 60)
        if not avail or not blocks:
            continue

        alloc: dict[dt.date, int] = {}
        for block_index, minutes in enumerate(blocks):
            target = _target_index(len(avail), block_index, len(blocks))
            for day_index in _nearby_indices(len(avail), target):
                day = avail[day_index]
                if _room_on(day, day_used, week_used,
                            max_daily, max_weekly) < minutes:
                    continue

                alloc[day] = alloc.get(day, 0) + minutes
                day_used[day] = day_used.get(day, 0) + minutes
                week = _week_start(day)
                week_used[week] = week_used.get(week, 0) + minutes
                break

        course_allocs[c["id"]] = {
            "name": c["name"],
            "exam_date": exam_d,
            "alloc": alloc,
        }

    sessions: list[dict] = []
    for cid, v in course_allocs.items():
        for day, mins in sorted(v["alloc"].items()):
            if mins > 0:
                sessions.append({
                    "course_id": cid,
                    "course_name": v["name"],
                    "session_date": day,
                    "planned_minutes": int(mins),
                    "completed_minutes": 0,
                })
    return sessions


def rebalance_course_sessions(sessions_df: pd.DataFrame,
                              course_id: int,
                              target_total_minutes: float,
                              today: Optional[dt.date] = None) -> pd.DataFrame:
    """Redistribute one course after a manual edit."""
    if today is None:
        today = dt.date.today()
    if sessions_df.empty:
        return sessions_df

    mask = sessions_df["course_id"] == course_id
    rows = sessions_df.loc[mask].copy()
    if rows.empty:
        return sessions_df

    rows["_date"] = pd.to_datetime(rows["session_date"]).dt.date
    eligible = (rows["completed_minutes"] == 0) & (rows["_date"] >= today)
    eligible_total = rows.loc[eligible, "planned_minutes"].sum()
    current_total  = rows["planned_minutes"].sum()
    locked_total   = current_total - eligible_total

    if eligible.sum() == 0:
        return sessions_df

    needed_future = _round_to_5(max(0, target_total_minutes - locked_total))
    idxs = rows.loc[eligible].sort_values("_date").index.tolist()
    base = _floor_to_5(needed_future / len(idxs)) if idxs else 0
    for idx in idxs:
        sessions_df.at[idx, "planned_minutes"] = int(base)

    remainder = needed_future - base * len(idxs)
    i = 0
    while remainder >= ROUNDING_MINUTES and idxs:
        idx = idxs[i % len(idxs)]
        sessions_df.at[idx, "planned_minutes"] += ROUNDING_MINUTES
        remainder -= ROUNDING_MINUTES
        i += 1

    return sessions_df


def compute_analytics(sessions_df: pd.DataFrame) -> dict:
    """Aggregate the sessions DataFrame into chart-ready pieces."""
    if sessions_df.empty:
        return {
            "total_planned": 0, "total_completed": 0,
            "total_remaining": 0, "total_days": 0, "pct": 0,
            "per_course": pd.DataFrame(
                columns=["course_name", "planned", "completed",
                         "remaining", "pct"]),
            "weekly": pd.DataFrame(),
            "week_order": [],
            "daily": pd.DataFrame(),
        }

    p = sessions_df.copy()
    p["date"] = pd.to_datetime(p["session_date"])

    total_planned   = int(p["planned_minutes"].sum())
    total_completed = int(p["completed_minutes"].sum())
    total_days      = int(p["date"].nunique())
    pct = (total_completed / total_planned * 100) if total_planned else 0

    per_course = (
        p.groupby("course_name")
         .agg(planned=("planned_minutes", "sum"),
              completed=("completed_minutes", "sum"))
         .reset_index()
    )
    per_course["remaining"] = per_course["planned"] - per_course["completed"]
    per_course["pct"] = (
        per_course["completed"] / per_course["planned"] * 100
    ).fillna(0)

    p["week_label"] = p["date"].apply(
        lambda d: (d - pd.Timedelta(days=d.weekday())).strftime("%d %b"))
    week_order = p.sort_values("date")["week_label"].unique().tolist()

    weekly = (
        p.groupby(["week_label", "course_name"])["planned_minutes"]
         .sum().reset_index()
    )

    daily = (
        p.groupby("date")["planned_minutes"].sum()
         .reset_index()
         .rename(columns={"planned_minutes": "total_minutes"})
    )

    return {
        "total_planned":   total_planned,
        "total_completed": total_completed,
        "total_remaining": total_planned - total_completed,
        "total_days":      total_days,
        "pct":             pct,
        "per_course":      per_course,
        "weekly":          weekly,
        "week_order":      week_order,
        "daily":           daily,
    }
