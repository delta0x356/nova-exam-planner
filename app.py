"""Streamlit interface for Nova Exam Planner."""

from __future__ import annotations

import datetime as dt
import base64
import time
from collections import defaultdict
from pathlib import Path
from typing import Optional

import pandas as pd
import streamlit as st

import database as db
import auth
import api_client as api
import subject_catalog as catalog
from ui import (
    apply_theme,
    fmt_hours,
    fmt_minutes,
    h,
    render_page_title,
)
from scheduler import (
    DAY_NAMES,
    compute_analytics,
    generate_study_plan,
    rebalance_course_sessions,
)

APP_TITLE = "Nova Exam Planner"
APP_TAGLINE = "Study sessions planned around real exam dates."
DEFAULT_COUNTRY = "PT"
NOVA_LOGO_PATH = Path(__file__).parent / "assets" / "nova-logo-inverted.png"
NOVA_FAVICON_PATH = Path(__file__).parent / "assets" / "nova-favicon.png"

COURSE_COLORS = [
    "#111111", "#6f6a5f", "#5f6f64", "#755f61", "#6c6477",
    "#8a7a55", "#4f6158", "#7a6c67", "#5c5c5c", "#9a9288",
]

DEFAULT_FOCUS_MINUTES = 45
DIFFICULTY_VALUES = {
    "Low": 1,
    "Medium": 3,
    "High": 5,
}
DIFFICULTY_LABELS = tuple(DIFFICULTY_VALUES)
SEMESTERS = ("Fall", "Spring")
FALL_PERIODS = {"Fall", "S1", "T1", "T2"}
SPRING_PERIODS = {"Spring", "S2", "T3", "T4"}
SEMESTER_START_ESTIMATES = {
    "Fall": (9, 1),
    "Spring": (2, 1),
}
SEMESTER_EXAM_ESTIMATES = {
    "Fall": (12, 15),
    "Spring": (6, 15),
}
PERIOD_EXAM_ESTIMATES = {
    "T1": (10, 31),
    "Fall": (12, 15),
    "S1": (12, 15),
    "T2": (12, 15),
    "T3": (3, 31),
    "Spring": (6, 15),
    "S2": (6, 15),
    "T4": (6, 15),
    "A": (6, 15),
}


def difficulty_label(value: int) -> str:
    if value <= 2:
        return "Low"
    if value >= 4:
        return "High"
    return "Medium"


def difficulty_value(value) -> int:
    label = str(value).strip().title()
    if label in DIFFICULTY_VALUES:
        return DIFFICULTY_VALUES[label]
    try:
        return DIFFICULTY_VALUES[difficulty_label(int(value))]
    except (TypeError, ValueError):
        return DIFFICULTY_VALUES["Medium"]


def study_hours_per_ects(difficulty: int) -> float:
    return 1.5 + 0.5 * int(difficulty)


def estimate_hours(ects: float, difficulty: int) -> float:
    return round(float(ects) * study_hours_per_ects(difficulty), 1)


def _estimate_strip_html(ects: float, difficulty: int,
                         shown_hours: Optional[float] = None) -> str:
    suggested = estimate_hours(ects, difficulty)
    shown = float(shown_hours) if shown_hours is not None else suggested
    if abs(shown - suggested) > 0.01:
        detail = f"Adjusted from {fmt_hours(suggested)} suggested"
    else:
        detail = (
            f"= {ects:g} ECTS × (1.5 + 0.5 × {int(difficulty)}) difficulty"
        )
    return (
        '<div class="study-estimate-strip">'
        '<span>Estimated study hours</span>'
        f'<strong>{fmt_hours(shown)}</strong>'
        f'<small>{h(detail)}</small>'
        '</div>'
    )


def render_estimate_strip(ects: float, difficulty: int,
                          shown_hours: Optional[float] = None) -> None:
    st.markdown(
        _estimate_strip_html(ects, difficulty, shown_hours),
        unsafe_allow_html=True,
    )


def study_hours_control(ects: float, difficulty: int, key_prefix: str,
                        current_hours: Optional[float] = None,
                        always_open: bool = False) -> float:
    suggested = estimate_hours(ects, difficulty)

    key_base = f"{key_prefix}_{float(ects):g}_{int(difficulty)}"
    key_base = key_base.replace(".", "_")
    hours_key = f"{key_base}_study_hours"
    value = float(current_hours) if current_hours is not None else suggested
    if always_open:
        shown = float(st.session_state.get(hours_key, value))
        render_estimate_strip(ects, difficulty, shown)
        return float(st.number_input(
            "Study hours",
            min_value=0.5,
            max_value=300.0,
            value=value,
            step=0.5,
            format="%.1f",
            key=hours_key,
        ))

    shown = float(st.session_state.get(hours_key, value))
    estimate_col, button_col = st.columns(
        [5, 1], gap="small", vertical_alignment="center")
    with estimate_col:
        render_estimate_strip(ects, difficulty, shown)
    with button_col:
        with st.popover(
            "Adjust hours",
            key=f"{key_base}_adjust_hours",
            width="stretch",
        ):
            value = st.number_input(
                "Study hours",
                min_value=0.5,
                max_value=300.0,
                value=value,
                step=0.5,
                format="%.1f",
                key=hours_key,
            )
    return float(value)


def default_exam_date(period: str, today: Optional[dt.date] = None) -> dt.date:
    today = today or dt.date.today()
    month, day = PERIOD_EXAM_ESTIMATES.get(period, (6, 15))
    candidate = dt.date(today.year, month, day)
    if candidate < today:
        candidate = dt.date(today.year + 1, month, day)
    return candidate


def period_semester(period: str) -> str:
    if period in FALL_PERIODS or period == "A":
        return "Fall"
    if period in SPRING_PERIODS:
        return "Spring"
    return "Spring"


def default_exam_date_for_semester(semester: str,
                                   today: Optional[dt.date] = None) -> dt.date:
    today = today or dt.date.today()
    month, day = SEMESTER_EXAM_ESTIMATES[semester]
    candidate = dt.date(today.year, month, day)
    if candidate < today:
        candidate = dt.date(today.year + 1, month, day)
    return candidate


def future_date_value(value: dt.date, today: Optional[dt.date] = None) -> dt.date:
    today = today or dt.date.today()
    return max(value, today)


def default_semester(today: Optional[dt.date] = None) -> str:
    today = today or dt.date.today()
    return "Fall" if today.month >= 8 or today.month == 1 else "Spring"


def semester_index(semester: str) -> int:
    return SEMESTERS.index(semester) if semester in SEMESTERS else 0


def semester_start_date(semester: str, exam_date: dt.date) -> dt.date:
    month, day = SEMESTER_START_ESTIMATES[semester]
    year = exam_date.year if semester == "Fall" else exam_date.year
    return dt.date(year, month, day)


def semester_from_exam_date(exam_date: dt.date) -> str:
    return "Fall" if exam_date.month >= 8 else "Spring"


def course_study_start(course: dict, today: Optional[dt.date] = None) -> dt.date:
    today = today or dt.date.today()
    semester = semester_from_exam_date(course["exam_date"])
    return max(today, semester_start_date(semester, course["exam_date"]))


def semester_label(period: str, exam_date: dt.date) -> str:
    if period in FALL_PERIODS:
        return f"Fall {exam_date.year}"
    if period in SPRING_PERIODS:
        return f"Spring {exam_date.year}"
    if period == "A":
        return f"Academic year {exam_date.year - 1}/{exam_date.year}"
    return f"Next sitting {exam_date.year}"


def unique_course_name(base_name: str, existing_names: list[str]) -> str:
    """Return ``base_name`` or ``base_name (n)`` if the name already exists."""
    clean = base_name.strip()
    existing = {name.strip().lower() for name in existing_names}
    if clean.lower() not in existing:
        return clean

    idx = 2
    while f"{clean} ({idx})".lower() in existing:
        idx += 1
    return f"{clean} ({idx})"


def course_color(name: str, all_names: list[str]) -> str:
    sorted_names = sorted(set(all_names))
    idx = sorted_names.index(name) if name in sorted_names else 0
    return COURSE_COLORS[idx % len(COURSE_COLORS)]


def fmt_task_minutes(minutes: float) -> str:
    minutes = max(0, round(minutes))
    if minutes < 60:
        return f"{minutes} min"
    return fmt_minutes(minutes)


def _render_subject_loader(user: dict, existing_courses: list[dict]):
    st.subheader("Add course")
    with st.container(border=True):
        add_mode = st.segmented_control(
            "Course source",
            ["Nova course", "Custom course"],
            default="Nova course",
            key="course_loader_mode",
            width="stretch",
        )
        group_labels = {
            "mandatory": "Mandatory",
            "finance_elective": "Finance electives",
            "other_elective": "Other electives",
        }
        group_order = catalog.GROUP_ORDER
        label_to_group = {group_labels[group]: group for group in group_order}
        default_sem = default_semester()
        existing_names = [
            course["name"].strip()
            for course in existing_courses
        ]

        if add_mode == "Nova course":
            c1, c2, c3 = st.columns([1, 1, 1])
            with c1:
                program = st.selectbox(
                    "Degree",
                    catalog.PROGRAMS,
                    key="subject_loader_program",
                )
            with c2:
                selected_semester = st.selectbox(
                    "Semester",
                    SEMESTERS,
                    index=semester_index(default_sem),
                    format_func=lambda value: f"{value} semester",
                    key="subject_loader_semester",
                )
            with c3:
                group_label = st.selectbox(
                    "Course type",
                    list(label_to_group),
                    key="subject_loader_group",
                )

            group = label_to_group[group_label]
            subjects = [
                subject for subject in catalog.subjects_for(program, [group])
                if period_semester(subject["period"]) == selected_semester
            ]
            subjects.sort(key=lambda subject: (
                catalog.period_sort_key(subject["period"]),
                subject["name"],
            ))
            if not subjects:
                st.info("No courses found for this semester.")
            else:
                subjects_by_key = {
                    catalog.subject_key(subject): subject
                    for subject in subjects
                }
                subject_keys = list(subjects_by_key)
                subject_key = (
                    f"subject_loader_subject_{group}_{selected_semester}"
                )
                pending_subject = st.session_state.pop(
                    "subject_loader_next_subject", None)
                if pending_subject in subject_keys:
                    st.session_state[subject_key] = pending_subject
                if st.session_state.get(subject_key) not in subject_keys:
                    st.session_state[subject_key] = subject_keys[0]

                selected_key = st.selectbox(
                    "Course",
                    subject_keys,
                    format_func=lambda key: catalog.subject_label(
                        subjects_by_key[key]),
                    key=subject_key,
                )

                subject = subjects_by_key[selected_key]
                course_name = catalog.course_name(subject)
                base_lower = course_name.strip().lower()
                name_lower = subject["name"].strip().lower()
                attempts = sum(
                    1 for name in existing_names
                    if name.lower() == base_lower
                    or name.lower().startswith(f"{base_lower} (")
                    or name.lower() == name_lower
                )

                today = dt.date.today()
                exam_default = default_exam_date_for_semester(
                    selected_semester, today)
                semester = f"{selected_semester} {exam_default.year}"
                st.caption(
                    f"{subject['ects']:g} ECTS - "
                    f"{subject['period']} - {semester}"
                )
                if attempts:
                    st.caption(
                        f"Already added {attempts} time"
                        f"{'s' if attempts != 1 else ''}. "
                        "Add again for a retake."
                    )

                d1, d2 = st.columns(2)
                with d1:
                    diff_label = st.selectbox(
                        "Difficulty",
                        DIFFICULTY_LABELS,
                        index=1,
                        key=f"subject_loader_difficulty_{selected_key}",
                    )
                with d2:
                    exam_date = st.date_input(
                        "Exam date",
                        future_date_value(exam_default, today),
                        min_value=today,
                        format="DD/MM/YYYY",
                        key=(
                            f"subject_loader_exam_"
                            f"{selected_key}_{selected_semester}"
                        ),
                    )

                difficulty = DIFFICULTY_VALUES[diff_label]
                estimated = study_hours_control(
                    subject["ects"],
                    difficulty,
                    f"subject_loader_{selected_key}",
                )

                label = "Add another attempt" if attempts else "Add subject"
                if st.button(label, width="stretch", type="primary"):
                    final_name = unique_course_name(course_name, existing_names)
                    db.upsert_course(
                        user["id"],
                        final_name,
                        exam_date,
                        subject["ects"],
                        difficulty,
                        estimated,
                    )
                    idx = subject_keys.index(selected_key)
                    st.session_state["subject_loader_next_subject"] = (
                        subject_keys[(idx + 1) % len(subject_keys)]
                    )
                    st.toast(f"Added {final_name}.")
                    st.rerun()

        else:
            c1, c2, c3 = st.columns([1.5, 0.7, 0.8])
            with c1:
                name = st.text_input(
                    "Course name",
                    placeholder="e.g. Thesis Seminar",
                    key="custom_course_name",
                )
            with c2:
                ects = st.number_input(
                    "ECTS",
                    0.5,
                    30.0,
                    6.0,
                    step=0.5,
                    format="%.1f",
                    key="custom_course_ects",
                )
            with c3:
                custom_semester = st.selectbox(
                    "Semester",
                    SEMESTERS,
                    index=semester_index(default_sem),
                    format_func=lambda value: f"{value} semester",
                    key="custom_course_semester",
                )

            d1, d2 = st.columns(2)
            with d1:
                diff_label = st.selectbox(
                    "Difficulty",
                    DIFFICULTY_LABELS,
                    index=1,
                    key="custom_course_difficulty",
                )
            with d2:
                today = dt.date.today()
                exam_date = st.date_input(
                    "Exam date",
                    future_date_value(
                        default_exam_date_for_semester(custom_semester),
                        today,
                    ),
                    min_value=today,
                    format="DD/MM/YYYY",
                    key=f"custom_course_exam_{custom_semester}",
                )

            difficulty = DIFFICULTY_VALUES[diff_label]
            estimated = study_hours_control(
                ects,
                difficulty,
                "custom_course",
            )

            if st.button("Add custom course",
                         width="stretch", type="primary"):
                if not name.strip():
                    st.warning("Enter a course name.")
                    return
                final_name = unique_course_name(name, existing_names)
                db.upsert_course(
                    user["id"],
                    final_name,
                    exam_date,
                    ects,
                    difficulty,
                    estimated,
                )
                st.toast(f"Added {final_name}.")
                st.rerun()


def _render_study_settings(user: dict):
    con = db.get_constraints(user["id"])
    default_start = max(con["start_date"], dt.date.today())

    with st.expander("Study settings", expanded=False):
        c1, c2, c3 = st.columns(3)
        with c1:
            weekly_hours = st.number_input(
                "Weekly study hours", 1, 80, int(con["weekly_hours"]))
        with c2:
            max_daily = st.number_input(
                "Max hours / day", 1, 16, int(con["max_hours_per_day"]))
        with c3:
            start_date = st.date_input(
                "Plan start date",
                future_date_value(default_start),
                min_value=dt.date.today(),
                format="DD/MM/YYYY",
            )

        preferred_days = st.multiselect(
            "Preferred study days",
            DAY_NAMES,
            default=con["preferred_days"] or DAY_NAMES,
        )
        if not preferred_days:
            st.warning("Select at least one study day.")
            preferred_days = list(DAY_NAMES)

        c4, c5 = st.columns([2, 1])
        with c4:
            skip_holidays = st.checkbox(
                f"Skip public holidays ({user['country_code']})",
                value=bool(con["skip_holidays"]),
                help="Fetches holidays from date.nager.at and excludes them "
                     "from the schedule.",
            )
        with c5:
            if st.button("Save settings", width="stretch"):
                db.save_constraints(
                    user["id"],
                    weekly_hours=weekly_hours,
                    preferred_days=preferred_days,
                    max_hours_per_day=max_daily,
                    start_date=start_date,
                    skip_holidays=skip_holidays,
                )
                st.toast("Settings saved.")

        if skip_holidays:
            with st.expander("Upcoming public holidays"):
                years = sorted({start_date.year, start_date.year + 1})
                holidays = api.get_holidays_detailed(
                    user["country_code"], years)
                future = [
                    h for h in holidays
                    if h["date"] >= dt.date.today()
                ][:12]
                if not future:
                    st.caption("No upcoming holidays found.")
                else:
                    for h in future:
                        st.markdown(
                            f"- **{h['date']:%d %b %Y}** - "
                            f"{h['local_name']} ({h['name']})")

    return weekly_hours, max_daily, start_date, preferred_days, skip_holidays


def _session_done(row: pd.Series) -> bool:
    planned = int(row["planned_minutes"])
    completed = int(row["completed_minutes"])
    return planned > 0 and completed >= planned


def _render_session_card(user_id: int, row: pd.Series, key_prefix: str):
    planned = int(row["planned_minutes"])
    completed = int(row["completed_minutes"])
    remaining = max(0, planned - completed)
    done = _session_done(row)

    with st.container(key=f"{key_prefix}_{int(row['id'])}"):
        label = f"{row['course_name']} - {fmt_task_minutes(planned)}"
        if completed and not done:
            label += f" - {fmt_task_minutes(remaining)} left"
        if done:
            label = f":gray[~~{label}~~]"
        key = f"task_done_{key_prefix}_{int(row['id'])}"
        checked = st.checkbox(label, value=done, key=key)
        if checked != done:
            db.update_session_completed(
                user_id, int(row["id"]), planned if checked else 0)
            st.toast("Session marked done." if checked else "Session reopened.")
            st.rerun()


def _metric_grid(items: list[tuple[str, str, str]]) -> None:
    cells = []
    for label, value, detail in items:
        detail_html = f"<small>{h(detail)}</small>" if detail else ""
        cells.append(
            '<div class="nova-metric">'
            f'<span>{h(label)}</span>'
            f'<strong>{h(value)}</strong>'
            f'{detail_html}'
            '</div>'
        )
    st.markdown(
        f'<div class="nova-metric-grid">{"".join(cells)}</div>',
        unsafe_allow_html=True,
    )


def _focus_summary_html(items: list[tuple[str, str]]) -> str:
    cells = []
    for label, value in items:
        cells.append(
            '<div class="focus-summary-cell">'
            f'<span>{h(label)}</span>'
            f'<strong>{h(value)}</strong>'
            '</div>'
        )
    return f'<div class="focus-summary">{"".join(cells)}</div>'


def _new_timer_state(timer_key: str, total_seconds: int) -> dict:
    return {
        "key": timer_key,
        "total": int(total_seconds),
        "remaining": int(total_seconds),
        "running": False,
        "running_from": int(total_seconds),
        "started_at": None,
        "complete": False,
    }


def _get_timer_state(timer_key: str, total_seconds: int) -> dict:
    state = st.session_state.get("study_mode_timer")
    if (
        not isinstance(state, dict)
        or state.get("key") != timer_key
        or int(state.get("total", 0)) != int(total_seconds)
    ):
        state = _new_timer_state(timer_key, total_seconds)
        st.session_state["study_mode_timer"] = state
    return state


def _sync_timer_state(state: dict) -> None:
    if not state.get("running"):
        return
    elapsed = int(time.time() - float(state.get("started_at") or time.time()))
    remaining = max(0, int(state.get("running_from", 0)) - elapsed)
    state["remaining"] = remaining
    if remaining <= 0:
        state["running"] = False
        state["complete"] = True
    st.session_state["study_mode_timer"] = state


def _clock_text(seconds: int) -> str:
    minutes, rest = divmod(max(0, int(seconds)), 60)
    return f"{minutes:02d}:{rest:02d}"


def _timer_card_html(state: dict) -> str:
    total = max(1, int(state["total"]))
    remaining = max(0, int(state["remaining"]))
    pct = ((total - remaining) / total) * 100
    if state.get("complete"):
        label, caption = "Complete", "Block finished"
    elif state.get("running"):
        label, caption = "Focus", "Focus running"
    elif remaining < total:
        label, caption = "Paused", "Paused"
    else:
        label, caption = "Ready", "Focus block ready"
    return f"""
        <div style="
            background:#ffffff;
            border:1px solid rgba(17,17,17,0.12);
            border-radius:14px;
            color:#111111;
            margin:0.9rem auto 0.45rem;
            max-width:360px;
            padding:18px;
            text-align:center;">
            <div style="
                color:#111111;
                font-size:0.78rem;
                font-weight:800;
                letter-spacing:0.08em;
                margin-bottom:6px;
                text-transform:uppercase;">{h(label)}</div>
            <div style="
                color:#111111;
                font-size:3.25rem;
                font-weight:850;
                line-height:1;
                margin:12px 0;">{_clock_text(remaining)}</div>
            <div style="
                background:#e6e6e6;
                border-radius:999px;
                height:5px;
                margin-top:14px;
                overflow:hidden;
                width:100%;">
                <div style="
                    background:#111111;
                    border-radius:999px;
                    height:100%;
                    width:{pct:.1f}%;"></div>
            </div>
            <div style="
                color:#555555;
                font-size:0.78rem;
                margin-top:10px;">{h(caption)}</div>
        </div>
    """


@st.fragment(run_every="1s")
def render_focus_timer(timer_key: str, total_seconds: int) -> None:
    state = _get_timer_state(timer_key, total_seconds)
    _sync_timer_state(state)
    st.markdown(_timer_card_html(state), unsafe_allow_html=True)

    _, controls, _ = st.columns([1, 1.1, 1])
    with controls:
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button(
                "Start",
                key=f"{timer_key}:start",
                disabled=state["running"] or state["complete"],
                type="primary",
                width="stretch",
            ):
                state["running"] = True
                state["complete"] = False
                state["running_from"] = int(state["remaining"])
                state["started_at"] = time.time()
                st.session_state["study_mode_timer"] = state
        with c2:
            if st.button(
                "Pause",
                key=f"{timer_key}:pause",
                disabled=not state["running"] or state["complete"],
                width="stretch",
            ):
                _sync_timer_state(state)
                state["running"] = False
                st.session_state["study_mode_timer"] = state
        with c3:
            if st.button("Reset", key=f"{timer_key}:reset", width="stretch"):
                st.session_state["study_mode_timer"] = _new_timer_state(
                    timer_key, total_seconds)


def _daily_quote_html(quote: dict) -> str:
    source_html = ""
    if quote.get("ok") and quote.get("source"):
        source_html = (
            f' <a href="{h(quote["source"])}" target="_blank" '
            'rel="noopener noreferrer">ZenQuotes</a>'
        )
    return (
        '<div class="daily-quote">'
        '<span>Daily quote</span>'
        f'<p>{h(quote.get("quote") or "")}</p>'
        f'<small>{h(quote.get("author") or "Unknown")}{source_html}</small>'
        '</div>'
    )


def _course_line(c: dict, days_until: int) -> str:
    status = f"{days_until}d left" if days_until >= 0 else "Past"
    if days_until == 0:
        status = "Today"
    elif days_until == 1:
        status = "Tomorrow"
    return (
        '<div class="course-line">'
        '<div>'
        f'<strong>{h(c["name"])}</strong>'
        f'<small>Exam {c["exam_date"]:%d %b %Y}</small>'
        '</div>'
        '<div class="course-meta">'
        f'<span>{c["ects"]:g} ECTS</span>'
        f'<span>{h(difficulty_label(int(c["difficulty"])))}</span>'
        f'<span>{fmt_hours(c["estimated_hours"])}</span>'
        f'<span>{h(status)}</span>'
        '</div>'
        '</div>'
    )


def _week_overview_html(sessions_df: pd.DataFrame, sel_week: dt.date,
                        courses: list[dict]) -> str:
    today = dt.date.today()
    rows = []
    for offset in range(7):
        day = sel_week + dt.timedelta(days=offset)
        day_data = sessions_df[sessions_df["session_date"] == day]
        total = int(day_data["planned_minutes"].sum()) if not day_data.empty \
            else 0
        done = int(day_data.apply(_session_done, axis=1).sum()) \
            if not day_data.empty else 0
        course_names = list(dict.fromkeys(
            str(name) for name in day_data["course_name"].tolist()
        ))
        if not course_names:
            summary = "No study"
        elif len(course_names) <= 2:
            summary = ", ".join(course_names)
        else:
            summary = f"{', '.join(course_names[:2])} +{len(course_names) - 2}"

        exams = [c["name"] for c in courses if c["exam_date"] == day]
        if exams:
            summary = f"Exam: {exams[0]}"

        row_class = "week-row today" if day == today else "week-row"
        rows.append(
            f'<div class="{row_class}">'
            '<div>'
            f'<strong>{DAY_NAMES[day.weekday()][:3]}</strong>'
            f'<small>{day:%d %b}</small>'
            '</div>'
            '<div>'
            f'<span>{h(summary)}</span>'
            f'<small>{done}/{len(day_data)} done</small>'
            '</div>'
            f'<em>{fmt_task_minutes(total)}</em>'
            '</div>'
        )
    return f'<div class="week-list">{"".join(rows)}</div>'


def _course_progress_html(courses: list[dict],
                          sessions_df: pd.DataFrame) -> str:
    rows = []
    for c in courses:
        cp = sessions_df[sessions_df["course_id"] == c["id"]]
        total_p = int(cp["planned_minutes"].sum()) if not cp.empty else 0
        total_c = int(cp["completed_minutes"].sum()) if not cp.empty else 0
        pct = min(total_c / total_p, 1.0) if total_p else 0
        rows.append(
            '<div class="progress-row">'
            '<div class="progress-row-head">'
            f'<strong>{h(c["name"])}</strong>'
            f'<span>{fmt_minutes(total_c)} / {fmt_minutes(total_p)}</span>'
            '</div>'
            '<div class="progress-track">'
            f'<div class="progress-fill" style="width:{pct * 100:.0f}%"></div>'
            '</div>'
            '</div>'
        )
    return f'<div class="progress-list">{"".join(rows)}</div>'


def _course_balance(sessions_df: pd.DataFrame,
                    totals: dict[int, float]) -> pd.DataFrame:
    if sessions_df.empty:
        return pd.DataFrame(columns=[
            "course_id", "course_name", "planned", "target", "diff",
        ])
    per_course = (
        sessions_df.groupby(["course_id", "course_name"])["planned_minutes"]
        .sum().reset_index()
        .rename(columns={"planned_minutes": "planned"})
    )
    per_course["target"] = per_course["course_id"].map(
        lambda cid: int(totals.get(int(cid), 0))
    )
    per_course["diff"] = per_course["planned"].astype(int) - per_course["target"]
    return per_course.sort_values(
        "diff", key=lambda series: series.abs(), ascending=False)


def _balance_html(balance: pd.DataFrame) -> str:
    rows = []
    for _, r in balance.iterrows():
        diff = int(r["diff"])
        ok = abs(diff) < 10
        diff_text = "balanced" if ok else (
            f"+{fmt_minutes(diff)}" if diff > 0
            else f"-{fmt_minutes(abs(diff))}"
        )
        klass = "balance-row" if ok else "balance-row review"
        rows.append(
            f'<div class="{klass}">'
            '<div>'
            f'<strong>{h(r["course_name"])}</strong>'
            f'<span>{fmt_minutes(int(r["planned"]))} planned / '
            f'{fmt_minutes(int(r["target"]))} target</span>'
            '</div>'
            f'<em>{h(diff_text)}</em>'
            '</div>'
        )
    return f'<div class="balance-list">{"".join(rows)}</div>'


def greeting() -> str:
    h = dt.datetime.now().hour
    if h < 5:
        return "Still awake"
    if h < 12:
        return "Good morning"
    if h < 18:
        return "Good afternoon"
    return "Good evening"


def logo_data_uri() -> str:
    data = base64.b64encode(NOVA_LOGO_PATH.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{data}"


def go_to_page(page_name: str) -> None:
    st.session_state["pending_page_choice"] = page_name


def apply_pending_page_choice(page_names: list[str]) -> None:
    pending = st.session_state.pop("pending_page_choice", None)
    if pending in page_names:
        st.session_state["page_choice"] = pending


def sessions_as_df(user_id: int) -> pd.DataFrame:
    sessions = db.list_sessions(user_id)
    if not sessions:
        return pd.DataFrame(columns=[
            "id", "course_id", "course_name", "session_date",
            "planned_minutes", "completed_minutes",
        ])
    df = pd.DataFrame(sessions)
    df["session_date"] = pd.to_datetime(df["session_date"]).dt.date
    return df


def courses_total_minutes(user_id: int) -> dict[int, float]:
    """Map course_id to required total study minutes."""
    return {c["id"]: c["estimated_hours"] * 60
            for c in db.list_courses(user_id)}


def render_capacity_warning(courses: list[dict], sessions_df: pd.DataFrame):
    """Warn when the generated plan cannot fit all requested study hours."""
    if not courses or sessions_df.empty:
        return

    target_min = int(sum(c["estimated_hours"] * 60 for c in courses))
    planned_min = int(sessions_df["planned_minutes"].sum())
    gap = target_min - planned_min
    if gap < 5:
        return

    st.warning(
        f"Your current limits only scheduled **{fmt_minutes(planned_min)}** "
        f"out of **{fmt_minutes(target_min)}** needed. "
        f"That leaves **{fmt_minutes(gap)} unscheduled**. "
        "Increase weekly study hours, max hours per day, available study "
        "days, or move the exam date further away."
    )


def missed_sessions_df(sessions_df: pd.DataFrame,
                       today: Optional[dt.date] = None) -> pd.DataFrame:
    """Return past sessions with unfinished planned minutes."""
    if today is None:
        today = dt.date.today()
    if sessions_df.empty:
        return sessions_df
    missed = sessions_df[
        (sessions_df["session_date"] < today)
        & (sessions_df["planned_minutes"] > sessions_df["completed_minutes"])
    ].copy()
    missed["missed_minutes"] = (
        missed["planned_minutes"] - missed["completed_minutes"]
    ).clip(lower=0).astype(int)
    return missed[missed["missed_minutes"] > 0]


def _week_start(day: dt.date) -> dt.date:
    return day - dt.timedelta(days=day.weekday())


def _floor_to_5(minutes: float) -> int:
    return max(0, int(minutes // 5) * 5)


def _reschedule_days(start: dt.date, end: dt.date,
                     preferred_days: list[str],
                     exclude_dates: set[dt.date]) -> list[dt.date]:
    out, cur = [], start
    preferred = set(preferred_days or DAY_NAMES)
    while cur < end:
        if DAY_NAMES[cur.weekday()] in preferred and cur not in exclude_dates:
            out.append(cur)
        cur += dt.timedelta(days=1)
    return out


def redistribute_missed_sessions(user: dict,
                                 missed: pd.DataFrame) -> tuple[int, int]:
    """Move missed minutes into future sessions while respecting constraints."""
    if missed.empty:
        return 0, 0

    today = dt.date.today()
    con = db.get_constraints(user["id"])
    courses = {c["id"]: c for c in db.list_courses(user["id"])}
    if not courses:
        return 0, int(missed["missed_minutes"].sum())

    max_daily = int(con["max_hours_per_day"]) * 60
    max_weekly = int(con["weekly_hours"]) * 60
    preferred_days = con["preferred_days"] or DAY_NAMES

    exclude: set[dt.date] = set()
    if con["skip_holidays"]:
        future_exams = [c["exam_date"] for c in courses.values()
                        if c["exam_date"] > today]
        if future_exams:
            end = max(future_exams)
            years = range(today.year, end.year + 1)
            exclude = api.get_holiday_dates(user["country_code"], years)

    sessions = db.list_sessions(user["id"])
    future_sessions = [s for s in sessions if s["session_date"] >= today]

    day_used = defaultdict(int)
    week_used = defaultdict(int)
    existing: dict[tuple[int, dt.date], dict] = {}
    for s in future_sessions:
        day = s["session_date"]
        planned = int(s["planned_minutes"])
        day_used[day] += planned
        week_used[_week_start(day)] += planned
        existing[(int(s["course_id"]), day)] = s

    missed_by_course = defaultdict(int)
    for _, row in missed.iterrows():
        missed_by_course[int(row["course_id"])] += int(row["missed_minutes"])

        # Keep completed time, drop only the missed part.
        completed = int(row["completed_minutes"])
        if completed > 0:
            db.update_session_planned(user["id"], int(row["id"]), completed)
        else:
            db.delete_session(user["id"], int(row["id"]))

    scheduled = 0
    unscheduled = 0
    ordered = sorted(
        missed_by_course.items(),
        key=lambda item: courses.get(item[0], {}).get("exam_date", today),
    )

    for course_id, minutes in ordered:
        course = courses.get(course_id)
        if not course or course["exam_date"] <= today:
            unscheduled += minutes
            continue

        remaining = minutes
        days = _reschedule_days(
            today, course["exam_date"], preferred_days, exclude)
        for day in days:
            if remaining < 5:
                break
            daily_room = max_daily - day_used[day]
            weekly_room = max_weekly - week_used[_week_start(day)]
            add = _floor_to_5(min(remaining, daily_room, weekly_room))
            if add <= 0:
                continue

            session = existing.get((course_id, day))
            if session:
                new_total = int(session["planned_minutes"]) + add
                db.update_session_planned(
                    user["id"], int(session["id"]), new_total)
                session["planned_minutes"] = new_total
            else:
                new_id = db.insert_session(user["id"], course_id, day, add)
                existing[(course_id, day)] = {
                    "id": new_id,
                    "course_id": course_id,
                    "session_date": day,
                    "planned_minutes": add,
                    "completed_minutes": 0,
                    "course_name": course["name"],
                }

            day_used[day] += add
            week_used[_week_start(day)] += add
            scheduled += add
            remaining -= add

        unscheduled += max(0, int(remaining))

    return scheduled, unscheduled


def render_adaptive_rescheduler(user: dict):
    """Offer to move unfinished past sessions without blocking the page."""
    sessions_df = sessions_as_df(user["id"])
    missed = missed_sessions_df(sessions_df)
    if missed.empty:
        st.session_state.pop("missed_rescheduler_dismissed", None)
        return

    signature = "|".join(
        f"{int(r.id)}:{int(r.planned_minutes)}:{int(r.completed_minutes)}"
        for r in missed.itertuples()
    )
    if st.session_state.get("missed_rescheduler_dismissed") == signature:
        return

    missed_total = int(missed["missed_minutes"].sum())
    by_course = (
        missed.groupby("course_name")["missed_minutes"]
        .sum().sort_values(ascending=False)
    )

    with st.expander(f"Missed study time ({fmt_minutes(missed_total)})",
                     expanded=False):
        st.caption(
            f"{fmt_minutes(missed_total)} of past study time is unfinished."
        )
        for course_name, minutes in by_course.items():
            st.caption(f"{course_name}: {fmt_minutes(int(minutes))}")

        c1, c2 = st.columns(2)
        if c1.button("Redistribute missed time", type="primary",
                     width="stretch"):
            scheduled, unscheduled = redistribute_missed_sessions(user, missed)
            if scheduled:
                st.toast(f"Redistributed {fmt_minutes(scheduled)}.")
            if unscheduled:
                st.toast(
                    f"{fmt_minutes(unscheduled)} could not fit under your "
                    "current limits."
                )
            st.session_state["missed_rescheduler_dismissed"] = signature
            st.rerun()
        if c2.button("Remind me later", width="stretch"):
            st.session_state["missed_rescheduler_dismissed"] = signature
            st.rerun()


def page_auth():
    """Unauthenticated entry screen."""
    _, center, _ = st.columns([1, 2, 1])
    with center:
        render_page_title(
            APP_TITLE,
            APP_TAGLINE,
            "login",
            logo_src=logo_data_uri(),
        )

        tab_login, tab_register = st.tabs(["Log in", "Create account"])

        with tab_login:
            with st.form("login_form", clear_on_submit=False):
                u = st.text_input("Username", key="login_u",
                                  placeholder="your_username")
                p = st.text_input("Password", type="password", key="login_p")
                submit = st.form_submit_button(
                    "Log in", type="primary", width="stretch")
            if submit:
                user = auth.authenticate(u.strip(), p)
                if user:
                    auth.login_session(user)
                    st.success(f"Welcome back, {user['display_name']}!")
                    st.rerun()
                else:
                    st.error("Invalid username or password.")

        with tab_register:
            with st.form("register_form", clear_on_submit=False):
                c1, c2 = st.columns(2)
                with c1:
                    ru = st.text_input("Username *", key="reg_u",
                                       placeholder="pick_a_handle")
                with c2:
                    rd = st.text_input("Display name",
                                       placeholder="How should we call you?")
                re_mail = st.text_input(
                    "Email (optional)",
                    placeholder="you@example.com")

                countries = api.list_supported_countries()
                country_idx = next(
                    (i for i, (code, _) in enumerate(countries)
                     if code == DEFAULT_COUNTRY),
                    0)
                country_code = st.selectbox(
                    "Country (for public holidays)",
                    options=[c[0] for c in countries],
                    format_func=lambda c: next(
                        (f"{cc} - {name}" for cc, name in countries if cc == c),
                        c),
                    index=country_idx,
                )

                rp = st.text_input(
                    "Password *",
                    type="password",
                    help="At least 8 characters, with letters and digits",
                )
                rp2 = st.text_input("Confirm password *", type="password")
                reg_submit = st.form_submit_button(
                    "Create account", type="primary",
                    width="stretch")

            if reg_submit:
                if rp != rp2:
                    st.error("Passwords don't match.")
                else:
                    uid, err = auth.register_user(
                        ru.strip(), re_mail.strip(), rp,
                        display_name=rd.strip() or None,
                        country_code=country_code,
                    )
                    if err:
                        st.error(err)
                    else:
                        user = db.get_user_by_id(uid)
                        auth.login_session(user)
                        st.success("Account created. Welcome.")
                        st.rerun()


def page_dashboard(user: dict):
    courses = db.list_courses(user["id"])
    sessions_df = sessions_as_df(user["id"])

    if not courses:
        render_page_title(
            "Nova Exam Planner",
            "Add your courses once, then follow the daily checklist.",
            "dashboard",
        )
        st.info(
            "Start by opening Courses in the sidebar, adding your first "
            "course, and generating a plan."
        )
        _render_quickstart()
        return

    total_planned = (
        int(sessions_df["planned_minutes"].sum()) if not sessions_df.empty else 0
    )
    total_completed = (
        int(sessions_df["completed_minutes"].sum()) if not sessions_df.empty else 0
    )
    pct = (total_completed / total_planned * 100) if total_planned else 0
    next_exam = min(
        (c for c in courses if c["exam_date"] >= dt.date.today()),
        key=lambda c: c["exam_date"], default=None)

    today = dt.date.today()
    today_tasks = sessions_df[sessions_df["session_date"] == today] \
        if not sessions_df.empty else pd.DataFrame()
    today_total = int(today_tasks["planned_minutes"].sum()) \
        if not today_tasks.empty else 0
    today_done = int(today_tasks.apply(_session_done, axis=1).sum()) \
        if not today_tasks.empty else 0

    render_page_title(
        "Today",
        (
            f"{fmt_task_minutes(today_total)} planned - "
            f"{today_done}/{len(today_tasks)} sessions done"
        ),
        "dashboard",
    )

    quote = api.get_daily_motivational_quote(today.isoformat())
    st.markdown(_daily_quote_html(quote), unsafe_allow_html=True)

    if today_tasks.empty:
        st.caption("No sessions today.")
    else:
        for _, row in today_tasks.iterrows():
            _render_session_card(
                user["id"], row,
                key_prefix=f"dashboard_{today.isoformat()}",
            )

    next_exam_value = "-"
    next_exam_detail = ""
    if next_exam:
        days = (next_exam["exam_date"] - dt.date.today()).days
        next_exam_value = f"{days}d"
        next_exam_detail = next_exam["name"]

    with st.expander("Overview", expanded=False):
        _metric_grid([
            ("Courses", str(len(courses)), ""),
            ("Planned", fmt_minutes(total_planned), ""),
            ("Completed", f"{pct:.0f}%", fmt_minutes(total_completed)),
            ("Next exam", next_exam_value, next_exam_detail),
        ])

    render_capacity_warning(courses, sessions_df)

    upcoming = [c for c in courses
                if 0 <= (c["exam_date"] - today).days <= 21]
    upcoming.sort(key=lambda c: c["exam_date"])
    if upcoming:
        st.markdown(
            '<div class="simple-section-title">'
            '<h3>Upcoming exams</h3><span>next 3 weeks</span>'
            '</div>',
            unsafe_allow_html=True,
        )
        for c in upcoming:
            d = (c["exam_date"] - today).days
            chip_class = "chip-urgent" if d <= 3 \
                else "chip-warn" if d <= 10 else "chip-ok"
            label = "today!" if d == 0 \
                else "tomorrow" if d == 1 \
                else f"in {d} days"
            st.markdown(
                f"""
                <div style="display:flex;align-items:center;margin-bottom:6px;">
                    <span class="nova-chip {chip_class}">{h(label)}</span>
                    <strong>{h(c['name'])}</strong>
                    <span style="margin-left:auto;color:var(--muted);">
                        {c['exam_date']:%a, %d %b}
                    </span>
                </div>
                """,
                unsafe_allow_html=True,
            )


def _render_quickstart():
    """Three-step intro for brand-new users."""
    st.markdown("### First setup")
    cards = [
        (
            "1. Add courses",
            "Pick a Nova course or custom course, then choose difficulty.",
        ),
        (
            "2. Set constraints",
            "Choose weekly hours, study days, daily caps, and holidays.",
        ),
        (
            "3. Generate plan",
            "Build the balanced schedule after courses and limits are ready.",
        ),
    ]
    with st.container(key="quickstart_actions"):
        cols = st.columns(3)
        for idx, (title, body) in enumerate(cards):
            with cols[idx]:
                st.button(
                    f"**{title}**\n\n{body}",
                    key=f"quickstart_action_{idx}",
                    width="stretch",
                    on_click=go_to_page,
                    args=("Courses",),
                )


def _cafeteria_lunch_summary(menu: dict) -> str:
    sections = menu.get("sections") or []
    priority = ("Meat or Fish", "Green Vibes", "Nomad", "Soup")
    for preferred in priority:
        section = next(
            (s for s in sections
             if preferred.lower() in str(s.get("title", "")).lower()),
            None,
        )
        if section and section.get("items"):
            return f"{section['title']}: {section['items'][0]}"

    if sections and sections[0].get("items"):
        return f"{sections[0]['title']}: {sections[0]['items'][0]}"
    return "check today's cafeteria options before scheduling long blocks."


def _weekly_cafeteria_html(days: list[dict]) -> str:
    cards = []
    for day in days:
        rows = []
        for section in day.get("sections", []):
            items = section.get("items") or []
            if not items:
                continue
            rows.append(
                '<div class="nova-menu-row">'
                f'<span>{h(section.get("title") or "Menu")}</span>'
                f'<p>{h(" / ".join(items))}</p>'
                '</div>'
            )
        if rows:
            cards.append(
                '<section class="nova-menu-day">'
                f'<h4>{h(day.get("date_label") or "Menu")}</h4>'
                f'{"".join(rows)}'
                '</section>'
            )
    return f'<div class="nova-weekly-menu">{"".join(cards)}</div>'


def page_cafeteria(user: dict):
    render_page_title(
        "Cafeteria",
        "Nova SBE lunch menus from MON BISTRO.",
        "lunch",
    )

    daily = api.get_daily_cafeteria_menu()
    weekly = api.get_weekly_cafeteria_menu()
    if not daily.get("ok") and not weekly.get("ok"):
        st.info("Cafeteria menu is unavailable right now.")
        st.caption("Source: monbistrot.pt")
        return

    if daily.get("ok"):
        st.markdown(
            f'<div class="nova-lunch-line">'
            f'<strong>Today:</strong> {h(_cafeteria_lunch_summary(daily))}'
            f'</div>',
            unsafe_allow_html=True,
        )
        st.caption(
            f"{daily.get('unit_name', 'NOVA SBE')} - "
            f"{daily.get('date_label', '')}"
        )
    else:
        st.info("Today's cafeteria menu is unavailable right now.")

    st.divider()
    st.subheader("Weekly Menu")
    if not weekly.get("ok"):
        st.info("Weekly cafeteria menu is unavailable right now.")
        return

    st.caption(f"{weekly.get('unit_name', 'NOVA SBE')} - "
               f"{weekly.get('week_label', '')}")
    st.markdown(_weekly_cafeteria_html(weekly.get("days", [])),
                unsafe_allow_html=True)


def _render_generate_plan(user: dict, courses: list[dict],
                          weekly_hours: int, max_daily: int,
                          start_date: dt.date, preferred_days: list[str],
                          skip_holidays: bool) -> None:
    notice = st.session_state.pop("plan_generated_notice", None)
    if notice:
        st.success(notice)
    warning = st.session_state.pop("plan_generated_warning", None)
    if warning:
        st.warning(warning)

    if st.button("Generate study plan", type="primary",
                 width="stretch"):
        with st.spinner("Building your schedule..."):
            today = dt.date.today()
            plan_start = max(start_date, today)
            db.save_constraints(
                user["id"],
                weekly_hours=weekly_hours,
                preferred_days=preferred_days,
                max_hours_per_day=max_daily,
                start_date=plan_start,
                skip_holidays=skip_holidays,
            )

            scheduled_courses = []
            for course in courses:
                scheduled = dict(course)
                scheduled["study_start_date"] = max(
                    plan_start,
                    course_study_start(course, today),
                )
                scheduled_courses.append(scheduled)

            exclude = set()
            if skip_holidays:
                end = max((c["exam_date"] for c in scheduled_courses),
                          default=plan_start)
                years = list(range(plan_start.year, end.year + 1))
                exclude = api.get_holiday_dates(
                    user["country_code"], years)

            sessions = generate_study_plan(
                scheduled_courses,
                preferred_days=preferred_days,
                max_hours_per_day=max_daily,
                start_date=plan_start,
                weekly_hours=weekly_hours,
                exclude_dates=exclude,
            )

        if not sessions:
            st.error(
                "Could not generate a plan. Check that exam dates are in "
                "the future and at least one study day is selected.")
            return

        db.replace_sessions(user["id"], sessions)
        total_min = sum(s["planned_minutes"] for s in sessions)
        target_min = int(sum(c["estimated_hours"] * 60 for c in courses))
        st.session_state["plan_generated_notice"] = (
            f"Plan generated: {len(sessions)} sessions, "
            f"{fmt_minutes(total_min)} total."
        )
        if total_min + 5 < target_min:
            st.session_state["plan_generated_warning"] = (
                f"{fmt_minutes(target_min - total_min)} could not fit under "
                "your current limits."
            )
        st.rerun()


def page_courses(user: dict):
    render_page_title(
        "Courses",
        "Add courses, generate the plan, edit details if needed.",
        "setup",
    )

    existing_courses = db.list_courses(user["id"])
    _render_subject_loader(user, existing_courses)

    st.divider()

    courses = db.list_courses(user["id"])
    if courses:
        weekly_hours, max_daily, start_date, preferred_days, skip_holidays = (
            _render_study_settings(user)
        )
        _render_generate_plan(
            user, courses, weekly_hours, max_daily, start_date,
            preferred_days, skip_holidays,
        )
        st.divider()

    st.subheader("Courses")
    if not courses:
        st.info("No courses yet. Add one above to get started.")
        return

    for c in courses:
        days_until = (c["exam_date"] - dt.date.today()).days
        due = "past" if days_until < 0 else f"{days_until}d left"
        summary = f"{c['name']} - {c['exam_date']:%d %b} - {due}"

        with st.expander(summary, expanded=False):
            st.markdown(_course_line(c, days_until), unsafe_allow_html=True)
            with st.form(f"edit_course_form_{c['id']}"):
                e1, e2 = st.columns(2)
                with e1:
                    edit_name = st.text_input(
                        "Course name", c["name"],
                        key=f"edit_name_{c['id']}",
                    )
                    edit_ects = st.number_input(
                        "ECTS", 0.5, 30.0, float(c["ects"]),
                        step=0.5, format="%.1f",
                        key=f"edit_ects_{c['id']}",
                    )
                with e2:
                    edit_exam = st.date_input(
                        "Exam date",
                        future_date_value(c["exam_date"]),
                        min_value=dt.date.today(),
                        format="DD/MM/YYYY",
                        key=f"edit_exam_{c['id']}",
                    )
                    current_difficulty = difficulty_label(
                        int(c["difficulty"])
                    )
                    edit_difficulty_label = st.selectbox(
                        "Difficulty",
                        DIFFICULTY_LABELS,
                        index=DIFFICULTY_LABELS.index(
                            current_difficulty),
                        key=f"edit_difficulty_{c['id']}",
                    )
                    edit_difficulty = DIFFICULTY_VALUES[
                        edit_difficulty_label]

                edit_estimated = study_hours_control(
                    edit_ects,
                    edit_difficulty,
                    f"edit_course_{c['id']}",
                    current_hours=c["estimated_hours"],
                    always_open=True,
                )

                other_names = [
                    item["name"] for item in courses
                    if item["id"] != c["id"]
                ]
                duplicate_name = (
                    bool(edit_name.strip())
                    and edit_name.strip().lower()
                    in {name.lower() for name in other_names}
                )
                separated_name = unique_course_name(
                    edit_name, other_names) if edit_name.strip() else ""
                save_as_copy = False
                if duplicate_name:
                    st.warning(
                        f"A course named **{edit_name.strip()}** already "
                        f"exists. Save as **{separated_name}** to keep both."
                    )
                    save_as_copy = st.checkbox(
                        f"Save anyway as {separated_name}",
                        key=f"edit_duplicate_{c['id']}",
                    )

                s1, s2 = st.columns([1, 1])
                save = s1.form_submit_button("Save changes", type="primary")
                delete = s2.form_submit_button("Delete course")

                if delete:
                    db.delete_course(user["id"], c["id"])
                    st.toast(f"Deleted {c['name']}.")
                    st.rerun()

                if save:
                    if not edit_name.strip():
                        st.warning("Course name is required.")
                        return
                    if duplicate_name and not save_as_copy:
                        st.error(
                            "That course name already exists. Tick the "
                            "checkbox to save a separated copy."
                        )
                        return

                    final_name = separated_name \
                        if duplicate_name and save_as_copy \
                        else edit_name.strip()
                    db.upsert_course(
                        user["id"],
                        final_name,
                        edit_exam,
                        edit_ects,
                        edit_difficulty,
                        edit_estimated,
                        course_id=c["id"],
                    )
                    st.toast(f"Updated {final_name}.")
                    st.rerun()


def page_study_plan(user: dict):
    render_page_title(
        "Study Plan",
        "Select a day and tick sessions done.",
        "plan",
    )

    sessions_df = sessions_as_df(user["id"])
    if sessions_df.empty:
        st.info("Generate a plan on the Courses page first.")
        return

    courses = db.list_courses(user["id"])
    today = dt.date.today()

    render_capacity_warning(courses, sessions_df)

    dates = sorted(sessions_df["session_date"].unique())
    future_dates = [day for day in dates if day >= today]
    default_day = today if today in dates else (
        future_dates[0] if future_dates else dates[-1])

    def day_label(day: dt.date) -> str:
        total = int(
            sessions_df.loc[
                sessions_df["session_date"] == day, "planned_minutes"
            ].sum()
        )
        if day == today:
            prefix = "Today"
        elif day == today + dt.timedelta(days=1):
            prefix = "Tomorrow"
        else:
            prefix = f"{day:%a}"
        return f"{prefix}, {day:%d %b} - {fmt_task_minutes(total)}"

    day_labels = [day_label(day) for day in dates]
    selected_label = st.selectbox(
        "Study day",
        day_labels,
        index=dates.index(default_day),
    )
    selected_day = dates[day_labels.index(selected_label)]

    day_tasks = sessions_df[
        sessions_df["session_date"] == selected_day
    ].sort_values(["completed_minutes", "course_name"])

    heading = "Today" if selected_day == today else f"{selected_day:%A, %d %b}"
    planned = int(day_tasks["planned_minutes"].sum()) if not day_tasks.empty \
        else 0
    done = int(day_tasks.apply(_session_done, axis=1).sum()) \
        if not day_tasks.empty else 0
    st.markdown(
        '<div class="simple-section-title">'
        f'<h3>{h(heading)}</h3>'
        f'<span>{fmt_task_minutes(planned)} - {done}/{len(day_tasks)} done</span>'
        '</div>',
        unsafe_allow_html=True,
    )
    if day_tasks.empty:
        st.info("No study sessions on this day.")
    else:
        for _, row in day_tasks.iterrows():
            _render_session_card(
                user["id"], row,
                key_prefix=f"study_day_{selected_day.isoformat()}",
            )

    exams = [c for c in courses if c["exam_date"] == selected_day]
    for course in exams:
        st.warning(f"Exam today: {course['name']}")

    render_adaptive_rescheduler(user)

    with st.expander("Week overview", expanded=False):
        min_d = sessions_df["session_date"].min()
        max_d = sessions_df["session_date"].max()

        weeks = []
        ws = min_d - dt.timedelta(days=min_d.weekday())
        while ws <= max_d:
            weeks.append(ws)
            ws += dt.timedelta(days=7)

        week_labels = [
            f"{w:%d %b} - {(w + dt.timedelta(days=6)):%d %b %Y}"
            for w in weeks
        ]
        cur_mon = today - dt.timedelta(days=today.weekday())
        default_idx = max((i for i, w in enumerate(weeks) if w <= cur_mon),
                          default=0)

        week_label = st.selectbox(
            "Week",
            week_labels,
            index=min(default_idx, len(week_labels) - 1))
        sel_week = weeks[week_labels.index(week_label)]

        st.markdown(
            _week_overview_html(sessions_df, sel_week, courses),
            unsafe_allow_html=True,
        )

    with st.expander("Course progress", expanded=False):
        st.markdown(
            _course_progress_html(courses, sessions_df),
            unsafe_allow_html=True,
        )


def page_customize(user: dict):
    render_page_title(
        "Customize",
        "Adjust one course and fine-tune its sessions.",
        "edit",
    )

    sessions_df = sessions_as_df(user["id"])
    if sessions_df.empty:
        st.info("Generate a plan on the Courses page first.")
        return

    courses = db.list_courses(user["id"])
    if not courses:
        st.info("Add courses first.")
        return

    totals = courses_total_minutes(user["id"])
    balance = _course_balance(sessions_df, totals)
    review_count = int((balance["diff"].abs() >= 10).sum())

    course_by_name = {c["name"]: c for c in courses}
    course_names = [
        c["name"] for c in sorted(courses, key=lambda c: c["exam_date"])
    ]
    default_course = (
        str(balance.iloc[0]["course_name"])
        if not balance.empty and str(balance.iloc[0]["course_name"]) in course_by_name
        else course_names[0]
    )

    selected_course = st.selectbox(
        "Course to adjust",
        course_names,
        index=course_names.index(default_course),
    )
    selected = course_by_name[selected_course]
    today = dt.date.today()
    course_sessions = sessions_df[
        sessions_df["course_id"] == selected["id"]
    ].copy()
    planned_min = int(course_sessions["planned_minutes"].sum())
    completed_min = int(course_sessions["completed_minutes"].sum())
    target_min = int(round(float(selected["estimated_hours"]) * 60))
    diff_min = planned_min - target_min
    diff_label = "On target"
    if abs(diff_min) >= 5:
        diff_label = (
            f"+{fmt_minutes(diff_min)}"
            if diff_min > 0 else f"-{fmt_minutes(abs(diff_min))}"
        )

    _metric_grid([
        ("Planned", fmt_minutes(planned_min), "Current schedule"),
        ("Target", fmt_minutes(target_min), "Course study hours"),
        ("Done", fmt_minutes(completed_min), "Already logged"),
        ("Balance", diff_label, "Planned minus target"),
    ])

    with st.form(f"customize_course_target_{selected['id']}"):
        target_hours = st.number_input(
            "Target study hours",
            min_value=0.5,
            max_value=300.0,
            value=float(selected["estimated_hours"]),
            step=0.5,
            format="%.1f",
        )
        apply_target = st.form_submit_button(
            "Apply and rebalance future sessions",
            type="primary",
            width="stretch",
        )
        if apply_target:
            db.upsert_course(
                user["id"],
                selected["name"],
                selected["exam_date"],
                float(selected["ects"]),
                int(selected["difficulty"]),
                float(target_hours),
                course_id=int(selected["id"]),
            )
            updated = rebalance_course_sessions(
                sessions_df.copy(),
                int(selected["id"]),
                float(target_hours) * 60,
            )
            changed = updated[updated["course_id"] == selected["id"]]
            for _, row in changed.iterrows():
                planned = max(
                    int(row["planned_minutes"]),
                    int(row["completed_minutes"]),
                )
                if planned <= 0 and int(row["completed_minutes"]) <= 0:
                    db.delete_session(user["id"], int(row["id"]))
                else:
                    db.update_session_planned(
                        user["id"], int(row["id"]), planned)
            st.toast(f"Updated {selected_course}.")
            st.rerun()

    st.divider()
    view = st.segmented_control(
        "Sessions to edit",
        ["Upcoming", "This week", "All"],
        default="Upcoming",
        key=f"customize_view_{selected['id']}",
    )

    filtered_sessions = course_sessions.copy()
    if view == "Upcoming":
        filtered_sessions = filtered_sessions[
            filtered_sessions["session_date"] >= today
        ]
    elif view == "This week":
        start = today - dt.timedelta(days=today.weekday())
        end = start + dt.timedelta(days=7)
        filtered_sessions = filtered_sessions[
            (filtered_sessions["session_date"] >= start)
            & (filtered_sessions["session_date"] < end)
        ]

    edit_df = filtered_sessions[[
        "id", "session_date", "planned_minutes", "completed_minutes",
    ]].rename(columns={
        "session_date": "Date",
        "planned_minutes": "Planned minutes",
        "completed_minutes": "Completed",
    }).copy()
    edit_df["Planned minutes"] = edit_df["Planned minutes"].astype(int)
    edit_df["Completed"] = edit_df["Completed"].astype(int)

    if edit_df.empty:
        st.info("No sessions match this view.")
        edited = edit_df
    else:
        editor_df = edit_df.set_index("id")
        edited = st.data_editor(
            editor_df,
            column_config={
                "Date": st.column_config.DateColumn(
                    "Date", disabled=True, format="DD MMM YYYY"),
                "Planned minutes": st.column_config.NumberColumn(
                    "Planned minutes", min_value=0, max_value=480, step=5),
                "Completed": st.column_config.NumberColumn(
                    "Completed", disabled=True),
            },
            column_order=["Date", "Planned minutes", "Completed"],
            width="stretch",
            hide_index=True,
            num_rows="fixed",
            height=min(420, max(180, len(edit_df) * 38 + 44)),
            key=f"plan_editor_{selected['id']}_{view}",
        )

    if st.button(
        "Save session edits",
        width="stretch",
        type="primary",
        disabled=edit_df.empty,
    ):
        for session_id, row in edited.iterrows():
            completed = int(row.get("Completed", 0))
            planned = max(int(row["Planned minutes"]), completed)
            if planned <= 0 and completed <= 0:
                db.delete_session(user["id"], int(session_id))
            else:
                db.update_session_planned(user["id"], int(session_id), planned)
        st.toast("Session edits saved.")
        st.rerun()

    with st.expander(f"All course balance ({review_count} to review)",
                     expanded=False):
        st.markdown(_balance_html(balance), unsafe_allow_html=True)


def page_analytics(user: dict):
    import plotly.express as px
    import plotly.graph_objects as go

    render_page_title(
        "Analytics",
        "Check workload, course balance, and completion progress.",
        "stats",
    )

    sessions_df = sessions_as_df(user["id"])
    if sessions_df.empty:
        st.info("Generate a plan first to see analytics.")
        return

    a = compute_analytics(sessions_df)
    con = db.get_constraints(user["id"])

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total planned", fmt_minutes(a["total_planned"]))
    k2.metric("Study days", a["total_days"])
    k3.metric("Completed", fmt_minutes(a["total_completed"]))
    k4.metric("Remaining", fmt_minutes(a["total_remaining"]))

    st.divider()

    courses = db.list_courses(user["id"])
    all_names = [c["name"] for c in courses]
    cmap = {n: course_color(n, all_names) for n in all_names}

    st.subheader("Study time per course")
    pc = a["per_course"].sort_values("planned", ascending=True).copy()
    pc["label"] = pc["planned"].apply(fmt_minutes)
    fig1 = px.bar(
        pc, x="planned", y="course_name", orientation="h",
        color="course_name", color_discrete_map=cmap, text="label")
    max_planned = max(float(pc["planned"].max()), 1.0)
    fig1.update_traces(
        cliponaxis=False,
        hovertemplate="%{y}<br>%{text} planned<extra></extra>",
        marker_line_color="#ffffff",
        marker_line_width=1,
        textposition="outside",
    )
    fig1.update_layout(
        showlegend=False,
        height=max(250, len(pc) * 60),
        margin=dict(l=0, r=120, t=10, b=0),
        xaxis_range=[0, max_planned * 1.18],
        xaxis_title="Planned Minutes", yaxis_title="")
    st.plotly_chart(fig1, width="stretch")

    st.divider()

    st.subheader("Weekly workload")
    weekly = a["weekly"].copy()
    weekly["hours"] = weekly["planned_minutes"] / 60
    fig2 = px.bar(
        weekly, x="week_label", y="hours",
        color="course_name", color_discrete_map=cmap,
        labels={"week_label": "Week of", "hours": "Hours",
                "course_name": "Course"},
        category_orders={"week_label": a["week_order"]})
    fig2.update_traces(
        hovertemplate="%{fullData.name}<br>%{x}: %{y:.1f}h<extra></extra>",
        marker_line_color="#ffffff",
        marker_line_width=0.8,
    )
    fig2.update_layout(
        barmode="stack", height=380,
        margin=dict(l=0, r=0, t=10, b=0),
        legend=dict(orientation="h", y=-0.25))
    st.plotly_chart(fig2, width="stretch")

    st.divider()

    st.subheader("Daily load")
    daily = a["daily"].copy()
    daily["date"] = pd.to_datetime(daily["date"]).dt.normalize()
    daily["hours"] = daily["total_minutes"] / 60
    fig3 = px.area(
        daily, x="date", y="hours",
        color_discrete_sequence=["#111111"],
        labels={"date": "Date", "hours": "Hours"})
    fig3.update_traces(
        hovertemplate="%{x|%d %b %Y}<br>%{y:.1f}h<extra></extra>")
    fig3.add_hline(
        y=int(con["max_hours_per_day"]),
        line_dash="dash", line_color="#555555",
        annotation_text="Daily max")
    fig3.update_layout(height=300, margin=dict(l=0, r=0, t=10, b=0))
    fig3.update_xaxes(
        hoverformat="%d %b %Y",
        range=[
            daily["date"].min() - pd.Timedelta(days=1),
            daily["date"].max() + pd.Timedelta(days=1),
        ],
        tickformat="%d %b<br>%Y",
    )
    st.plotly_chart(fig3, width="stretch")

    st.divider()

    st.subheader("Completed vs remaining")
    pc2 = a["per_course"].copy()
    pc2_colors = [cmap.get(name, "#111111") for name in pc2["course_name"]]
    fig4 = go.Figure()
    fig4.add_trace(go.Bar(
        name="Completed", x=pc2["course_name"],
        y=pc2["completed"] / 60, marker_color=pc2_colors))
    fig4.add_trace(go.Bar(
        name="Remaining", x=pc2["course_name"],
        y=pc2["remaining"] / 60, marker_color="#e9ecef"))
    fig4.update_traces(
        hovertemplate="%{x}<br>%{y:.1f}h<extra>%{fullData.name}</extra>",
        marker_line_color="#ffffff",
        marker_line_width=0.8,
    )
    fig4.update_layout(
        barmode="stack", height=380,
        margin=dict(l=0, r=0, t=10, b=0),
        yaxis_title="Hours",
        legend=dict(orientation="h", y=-0.15))
    st.plotly_chart(fig4, width="stretch")

    st.divider()

    st.subheader("Completion progress")
    for _, r in a["per_course"].iterrows():
        pct = r["pct"] / 100
        st.markdown(
            f"**{r['course_name']}** - {fmt_minutes(r['completed'])} / "
            f"{fmt_minutes(r['planned'])}  ({r['pct']:.0f}%)")
        st.progress(min(pct, 1.0))

    st.metric("Overall completion",
              f"{a['pct']:.1f}%",
              f"{fmt_minutes(a['total_completed'])} / "
              f"{fmt_minutes(a['total_planned'])}")


def page_study_mode(user: dict):
    render_page_title(
        "Study Mode",
        "Run a focus block and log the time into today's plan.",
        "focus",
    )
    notice = st.session_state.pop("study_mode_notice", None)
    if notice:
        st.success(notice)

    courses = db.list_courses(user["id"])
    if not courses:
        st.info("Add a course first, then come back here to study it.")
        return

    sessions_df = sessions_as_df(user["id"])
    today = dt.date.today()
    today_sessions = sessions_df[
        (sessions_df["session_date"] == today)
        & (sessions_df["planned_minutes"] > sessions_df["completed_minutes"])
    ].copy() if not sessions_df.empty else pd.DataFrame()

    targets = []
    for _, row in today_sessions.iterrows():
        remaining = int(row["planned_minutes"] - row["completed_minutes"])
        targets.append({
            "kind": "session",
            "label": (
                f"{row['course_name']} - {fmt_minutes(remaining)} "
                "remaining today"
            ),
            "session_id": int(row["id"]),
            "course_id": int(row["course_id"]),
            "course_name": row["course_name"],
            "planned_minutes": int(row["planned_minutes"]),
            "completed_minutes": int(row["completed_minutes"]),
            "remaining_minutes": remaining,
        })

    targets += [{
        "kind": "course",
        "label": f"Extra study - {c['name']}",
        "course_id": int(c["id"]),
        "course_name": c["name"],
        "remaining_minutes": 60,
    } for c in courses]

    labels = [t["label"] for t in targets]
    stored_label = st.session_state.get("study_mode_session")
    label_index = labels.index(stored_label) if stored_label in labels else 0
    selected_label = st.selectbox(
        "Session", labels, index=label_index, key="study_mode_session")
    target = targets[labels.index(selected_label)]

    st.divider()

    mode = st.radio(
        "Focus length",
        ["45 min study", "25 min focus", "Custom"],
        horizontal=True)

    if mode.startswith("45"):
        focus_min, break_min, label = DEFAULT_FOCUS_MINUTES, 10, "Study block"
    elif mode.startswith("25"):
        focus_min, break_min, label = 25, 5, "Pomodoro"
    else:
        label = "Custom"
        c1, c2 = st.columns(2)
        with c1:
            focus_min = st.number_input(
                "Focus minutes", 5, 180, DEFAULT_FOCUS_MINUTES, step=5)
        with c2:
            break_min = st.number_input(
                "Break minutes", 0, 60, 10, step=5)

    remaining = int(target.get("remaining_minutes", focus_min))
    block_minutes = int(focus_min)
    if target["kind"] == "session":
        block_minutes = min(block_minutes, remaining)

    st.markdown(
        _focus_summary_html([
            ("Course", target["course_name"]),
            (
                "Remaining",
                fmt_minutes(remaining)
                if target["kind"] == "session" else "Extra study",
            ),
            ("Block", fmt_minutes(block_minutes)),
            ("Break", f"{int(break_min)} min"),
        ]),
        unsafe_allow_html=True,
    )

    if target["kind"] == "session":
        st.progress(
            min(target["completed_minutes"] / target["planned_minutes"], 1.0))
        st.caption(
            f"{fmt_minutes(target['completed_minutes'])} completed out of "
            f"{fmt_minutes(target['planned_minutes'])} planned today.")
    else:
        st.caption(
            "Extra study is logged as a completed session for today, so it "
            "appears in your analytics and progress totals.")

    st.markdown(
        f"**{label}** - {block_minutes} min focus / "
        f"{int(break_min)} min break")

    timer_key = (
        f"{user['id']}:{target['course_id']}:"
        f"{int(focus_min)}:{int(break_min)}"
    )
    render_focus_timer(timer_key, block_minutes * 60)

    c1, c2 = st.columns(2)
    with c1:
        if st.button(
            f"Log block ({fmt_minutes(block_minutes)})",
            type="primary",
            width="stretch",
        ):
            logged = log_study_minutes(user["id"], target, block_minutes)
            if logged:
                st.success(
                    f"Logged {fmt_minutes(logged)} for "
                    f"{target['course_name']}."
                )
            else:
                st.info(
                    "Nothing was logged because this session is already done."
                )
    with c2:
        if target["kind"] == "session":
            if st.button("Mark selected session complete",
                         width="stretch"):
                remaining_now = (
                    target["planned_minutes"] - target["completed_minutes"])
                if remaining_now > 0:
                    logged = log_study_minutes(user["id"], target, remaining_now)
                    st.session_state["study_mode_notice"] = (
                        f"Completed {target['course_name']} "
                        f"({fmt_minutes(logged)} logged)."
                    )
                    st.rerun()
        else:
            st.empty()

def log_study_minutes(user_id: int, target: dict, minutes: int) -> int:
    """Add completed focus time to a scheduled session or extra course study."""
    minutes = max(0, int(minutes))
    if minutes <= 0:
        return 0

    if target["kind"] == "session":
        planned = int(target["planned_minutes"])
        completed = int(target["completed_minutes"])
        new_completed = min(planned, completed + minutes)
        logged = new_completed - completed
        if logged > 0:
            db.update_session_completed(
                user_id, int(target["session_id"]), new_completed)
        return logged

    today = dt.date.today()
    sessions = db.list_sessions(user_id)
    existing = next(
        (s for s in sessions
         if int(s["course_id"]) == int(target["course_id"])
         and s["session_date"] == today),
        None,
    )
    if existing:
        new_planned = int(existing["planned_minutes"]) + minutes
        new_completed = int(existing["completed_minutes"]) + minutes
        db.update_session_planned(user_id, int(existing["id"]), new_planned)
        db.update_session_completed(user_id, int(existing["id"]), new_completed)
    else:
        db.insert_session(
            user_id, int(target["course_id"]), today,
            planned_minutes=minutes, completed_minutes=minutes)
    return minutes


def page_profile(user: dict):
    render_page_title(
        "Profile",
        "Account settings and local data controls.",
        "account",
    )

    st.markdown(
        f"""
        <div class="nova-sidebar-meta">
            <div class="hello">Signed in as</div>
            <div class="name">{h(user['display_name'])}
                <span style="color:var(--muted);font-weight:400;">
                    @{h(user['username'])}
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("Edit profile")
    with st.form("profile_form"):
        c1, c2 = st.columns(2)
        with c1:
            display = st.text_input("Display name", user["display_name"])
        with c2:
            email = st.text_input("Email", user.get("email") or "")

        countries = api.list_supported_countries()
        codes = [c[0] for c in countries]
        current_code = user.get("country_code", DEFAULT_COUNTRY)
        country_idx = codes.index(current_code) if current_code in codes else 0
        country = st.selectbox(
            "Country", codes,
            format_func=lambda c: next(
                (f"{cc} - {name}" for cc, name in countries if cc == c), c),
            index=country_idx,
            help="Used for public holidays when 'Skip holidays' is enabled.")

        if st.form_submit_button("Save profile", type="primary"):
            if not auth.is_valid_email(email):
                st.error("Please enter a valid email address.")
            else:
                db.update_user_profile(
                    user["id"],
                    display_name=display.strip(),
                    email=(email.strip() or None),
                    country_code=country,
                )
                st.toast("Profile updated.")
                st.rerun()

    st.divider()

    st.subheader("Change password")
    with st.form("pw_form", clear_on_submit=True):
        cur_pw = st.text_input("Current password", type="password")
        new_pw = st.text_input(
            "New password",
            type="password",
            help="At least 8 characters, with letters and digits",
        )
        new_pw2 = st.text_input("Confirm new password", type="password")
        if st.form_submit_button("Update password"):
            if new_pw != new_pw2:
                st.error("New passwords don't match.")
            else:
                ok, msg = auth.change_password(user["id"], cur_pw, new_pw)
                (st.success if ok else st.error)(msg)

    st.divider()

    with st.expander("Danger zone"):
        st.caption(
            "Wipe all your courses, sessions, and generated plan.  "
            "Your account and settings are kept.")
        if st.button("Clear my study data", type="secondary"):
            db.clear_user_data(user["id"])
            st.toast("All courses and sessions deleted.")
            st.rerun()


def page_export(user: dict):
    render_page_title(
        "Export & Import",
        "Move courses in or take your schedule out.",
        "files",
    )

    sessions_df = sessions_as_df(user["id"])
    courses = db.list_courses(user["id"])

    if not sessions_df.empty:
        st.subheader("Export study plan")
        c1, c2 = st.columns(2)
        with c1:
            st.download_button(
                "Download as CSV",
                sessions_df.to_csv(index=False),
                file_name=f"nova_plan_{user['username']}.csv",
                mime="text/csv", width="stretch")
        with c2:
            ics_bytes = _build_ics(sessions_df, courses, user)
            st.download_button(
                "Download as ICS (calendar)",
                ics_bytes,
                file_name=f"nova_plan_{user['username']}.ics",
                mime="text/calendar", width="stretch",
                help="Import into Google Calendar, Outlook, Apple Calendar.")

    if courses:
        st.subheader("Export courses")
        cdf = pd.DataFrame([
            {"name": c["name"],
             "exam_date": c["exam_date"].isoformat(),
             "ects": c["ects"],
             "difficulty": difficulty_label(int(c["difficulty"])),
             "estimated_hours": c["estimated_hours"]}
            for c in courses
        ])
        st.download_button(
            "Download courses (CSV)",
            cdf.to_csv(index=False),
            file_name=f"nova_courses_{user['username']}.csv",
            mime="text/csv", width="stretch")

    st.divider()

    st.subheader("Import courses")
    st.caption(
        "Columns: `name, exam_date, ects, difficulty`. Difficulty can be "
        "Low, Medium, or High. Existing courses with the same name will be "
        "updated.")
    uploaded = st.file_uploader("Upload CSV", type=["csv"])
    if uploaded:
        try:
            df = pd.read_csv(uploaded, parse_dates=["exam_date"])
            imported = 0
            for _, r in df.iterrows():
                exam_d = r["exam_date"]
                if hasattr(exam_d, "date"):
                    exam_d = exam_d.date()
                existing = next(
                    (c for c in db.list_courses(user["id"])
                     if c["name"] == str(r["name"])), None)
                ects_value = float(r["ects"])
                difficulty = difficulty_value(r["difficulty"])
                estimated = (
                    float(r["estimated_hours"])
                    if "estimated_hours" in df.columns
                    else estimate_hours(ects_value, difficulty)
                )
                db.upsert_course(
                    user["id"],
                    name=str(r["name"]).strip(),
                    exam_date=exam_d,
                    ects=ects_value,
                    difficulty=difficulty,
                    estimated_hours=estimated,
                    course_id=existing["id"] if existing else None,
                )
                imported += 1
            st.success(f"Imported/updated {imported} courses.")
        except Exception as e:
            st.error(f"Import failed: {e}")


def _build_ics(sessions_df: pd.DataFrame, courses: list[dict],
               user: dict) -> bytes:
    """Produce a minimal valid ICS feed of all sessions + exam events."""
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        f"PRODID:-//Nova Exam Planner//{user['username']}//EN",
        "CALSCALE:GREGORIAN",
    ]
    now = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    for _, r in sessions_df.iterrows():
        d = r["session_date"]
        ds = d.strftime("%Y%m%d")
        dnext = (d + dt.timedelta(days=1)).strftime("%Y%m%d")
        duration_h = int(r["planned_minutes"]) / 60
        uid = f"nova-sess-{r['id']}@nova"
        lines += [
            "BEGIN:VEVENT",
            f"UID:{uid}",
            f"DTSTAMP:{now}",
            f"DTSTART;VALUE=DATE:{ds}",
            f"DTEND;VALUE=DATE:{dnext}",
            f"SUMMARY:Study: {r['course_name']} "
            f"({duration_h:.1f}h)",
            f"DESCRIPTION:Planned {int(r['planned_minutes'])} min "
            f"via Nova Exam Planner.",
            "END:VEVENT",
        ]

    for c in courses:
        ds = c["exam_date"].strftime("%Y%m%d")
        dnext = (c["exam_date"] + dt.timedelta(days=1)).strftime("%Y%m%d")
        lines += [
            "BEGIN:VEVENT",
            f"UID:nova-exam-{c['id']}@nova",
            f"DTSTAMP:{now}",
            f"DTSTART;VALUE=DATE:{ds}",
            f"DTEND;VALUE=DATE:{dnext}",
            f"SUMMARY:Exam: {c['name']}",
            "END:VEVENT",
        ]

    lines.append("END:VCALENDAR")
    return "\r\n".join(lines).encode("utf-8")


PAGES = [
    ("Dashboard", page_dashboard),
    ("Courses", page_courses),
    ("Study Plan", page_study_plan),
    ("Customize", page_customize),
    ("Analytics", page_analytics),
    ("Cafeteria", page_cafeteria),
    ("Study Mode", page_study_mode),
    ("Export", page_export),
    ("Profile", page_profile),
]
PAGE_NAMES = [name for name, _ in PAGES]
PAGE_BY_NAME = dict(PAGES)


def render_sidebar(user: dict) -> str:
    with st.sidebar:
        st.markdown(
            f"""
            <div class="nova-sidebar-logo">
                <img src="{logo_data_uri()}" alt="Nova SBE" />
            </div>
            <div class="nova-sidebar-meta">
                <div class="hello">Signed in as</div>
                <div class="name">{h(user['display_name'])}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.divider()
        if st.session_state.get("page_choice") not in PAGE_NAMES:
            st.session_state["page_choice"] = "Dashboard"
        choice = st.radio(
            "Navigation",
            PAGE_NAMES,
            key="page_choice",
            label_visibility="collapsed",
        )
        st.divider()

        n_courses = len(db.list_courses(user["id"]))
        st.caption(f"{n_courses} course{'s' if n_courses != 1 else ''}")
        if db.has_plan(user["id"]):
            df = sessions_as_df(user["id"])
            total = int(df["planned_minutes"].sum())
            done = int(df["completed_minutes"].sum())
            st.caption(f"{fmt_minutes(total)} planned")
            st.caption(f"{fmt_minutes(done)} done")

        st.divider()
        if st.button("Log out", width="stretch"):
            auth.logout()
            st.rerun()

        st.caption(APP_TITLE)
        return choice


def main():
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon=str(NOVA_FAVICON_PATH),
        layout="wide",
        initial_sidebar_state="expanded",
    )
    db.init_db()
    apply_theme()

    user = auth.current_user()
    if not user:
        page_auth()
        return

    apply_pending_page_choice(PAGE_NAMES)
    choice = render_sidebar(user)
    PAGE_BY_NAME[choice](user)


if __name__ == "__main__":
    main()
