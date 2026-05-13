"""Small UI helpers shared by the Streamlit pages."""

from html import escape
import streamlit as st


CUSTOM_CSS = """
<style>
:root {
    --paper: #f7f6f1;
    --panel: #ffffff;
    --ink: #111111;
    --muted: #666666;
    --line: rgba(17, 17, 17, 0.12);
    --line-strong: rgba(17, 17, 17, 0.18);
    --accent: #111111;
    --success: #111111;
    --warn: #666666;
    --danger: #111111;
    --soft: #f1f1ef;
    --soft-2: #e8e8e6;
    --radius-lg: 12px;
    --radius-md: 8px;
    --shadow: 0 8px 22px rgba(17, 17, 17, 0.045);
}

.stApp {
    background: var(--paper);
    color: var(--ink);
}

header[data-testid="stHeader"] {
    background: var(--paper);
}

.stDeployButton {
    display: none !important;
}

.main .block-container {
    max-width: 1040px;
    padding-top: 0.55rem;
    padding-bottom: 1.6rem;
}

.main .block-container [data-testid="stVerticalBlock"] {
    gap: 0.42rem;
}

h1, h2, h3 {
    color: var(--ink);
    letter-spacing: 0;
}

a[aria-label="Link to heading"] {
    display: none !important;
}

p, li, label, span {
    letter-spacing: 0;
}

[data-testid="stWidgetLabel"],
[data-testid="stWidgetLabel"] p,
.stTextInput label,
.stNumberInput label,
.stDateInput label {
    color: var(--ink) !important;
    opacity: 1 !important;
}

[data-testid="stSidebar"] {
    background: var(--paper);
    border-right: 1px solid var(--line);
}

div[data-testid="stMetric"] {
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: var(--radius-md);
    padding: 0.6rem 0.7rem;
    box-shadow: none;
}

[data-testid="stVerticalBlockBorderWrapper"] {
    border-color: var(--line) !important;
    border-radius: var(--radius-lg) !important;
    padding: 0.75rem !important;
}

code {
    background: var(--soft) !important;
    border: 1px solid var(--line);
    border-radius: 10px !important;
    color: var(--ink) !important;
    font-family: inherit !important;
    font-weight: 700;
}

[data-testid="stAlert"],
[data-testid="stAlertContainer"],
div[role="alert"] {
    background: var(--soft-2) !important;
    border: 1px solid var(--line) !important;
    border-radius: var(--radius-md) !important;
    color: var(--ink) !important;
    box-shadow: none !important;
}

[data-testid="stAlert"] *,
[data-testid="stAlertContainer"] *,
div[role="alert"] * {
    color: var(--ink) !important;
}

[data-testid="stAlert"] svg,
[data-testid="stAlertContainer"] svg,
div[role="alert"] svg {
    display: none;
}

.stTextInput input,
.stNumberInput input,
.stDateInput input,
textarea,
input {
    background: #ffffff !important;
    border-color: var(--line) !important;
    border-radius: 10px !important;
    color: var(--ink) !important;
}

.stTextInput input,
.stNumberInput input,
.stDateInput input,
[data-baseweb="select"] > div {
    min-height: 2.45rem !important;
}

input::placeholder,
textarea::placeholder {
    color: #7a7a7a !important;
    opacity: 1 !important;
}

input:focus,
textarea:focus {
    border-color: rgba(17, 17, 17, 0.32) !important;
    box-shadow: 0 0 0 3px rgba(17, 17, 17, 0.08) !important;
    outline: none !important;
}

[data-baseweb="input"],
[data-baseweb="select"],
[data-baseweb="textarea"],
[data-baseweb="base-input"] {
    background: #ffffff !important;
    border-radius: 10px !important;
}

[data-baseweb="tab-highlight"] {
    background-color: var(--ink) !important;
}

.stButton > button,
[data-testid="stFormSubmitButton"] button {
    border: 1px solid var(--line);
    border-radius: var(--radius-md);
    background: var(--panel);
    color: var(--ink);
    font-weight: 700;
    min-height: 2.25rem;
    box-shadow: none;
}

.stButton > button:hover,
[data-testid="stFormSubmitButton"] button:hover {
    border-color: var(--line);
    background: var(--soft);
    color: var(--ink);
}

.stButton > button[kind="primary"],
.stButton > button[kind="primaryFormSubmit"],
button[kind="primary"],
button[kind="primaryFormSubmit"],
[data-testid="stBaseButton-primary"],
[data-testid="stBaseButton-primaryFormSubmit"] {
    background: var(--ink);
    color: #ffffff;
    border-color: var(--ink);
}

.stButton > button[kind="primary"] *,
.stButton > button[kind="primaryFormSubmit"] *,
button[kind="primary"] *,
button[kind="primaryFormSubmit"] *,
[data-testid="stBaseButton-primary"] *,
[data-testid="stBaseButton-primaryFormSubmit"] * {
    color: #ffffff !important;
}

.stProgress > div > div > div > div {
    background: var(--accent);
}

.stTabs [data-baseweb="tab"] {
    border: 1px solid var(--line);
    border-bottom: none;
    border-radius: 14px 14px 0 0;
    background: var(--paper);
    padding: 0.55rem 1rem;
}

.stTabs [role="tab"] p {
    color: var(--ink) !important;
    opacity: 1 !important;
}

.stTabs [aria-selected="true"] {
    background: var(--panel);
    color: var(--ink);
}

.nova-page-title {
    background: transparent;
    border: 0;
    border-bottom: 1px solid var(--line);
    border-radius: 0;
    box-shadow: none;
    padding: 0.15rem 0 0.55rem;
    margin-bottom: 0.55rem;
}

.nova-page-title.with-logo {
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow);
    padding: 0.78rem 0.9rem 0.85rem;
}

.nova-title-row {
    display: flex;
    gap: 1rem;
    align-items: center;
}

.nova-title-logo {
    flex: 0 0 auto;
    width: 68px;
    min-height: 42px;
    border-radius: var(--radius-md);
    background: var(--ink);
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0.55rem;
}

.nova-title-logo img {
    display: block;
    width: 100%;
    height: auto;
}

.nova-kicker {
    font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
    font-size: 0.78rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.25rem;
}

.nova-page-title h1 {
    margin: 0;
    font-size: 1.65rem;
    line-height: 1.05;
    font-weight: 900;
}

.nova-page-title p {
    margin: 0.25rem 0 0;
    color: var(--muted);
}

.nova-sidebar-logo {
    background: var(--ink);
    border: 1px solid var(--ink);
    border-radius: var(--radius-md);
    padding: 0.6rem;
    margin: 0.1rem 0 0.75rem;
    box-shadow: none;
}

.nova-sidebar-logo img {
    display: block;
    width: min(118px, 100%);
    height: auto;
}

.nova-sidebar-meta {
    border-bottom: 1px solid var(--line);
    padding-bottom: 0.75rem;
    margin-bottom: 0.75rem;
}

.nova-sidebar-meta .hello {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--muted);
}

.nova-sidebar-meta .name {
    font-weight: 800;
    color: var(--ink);
}

[data-testid="stSidebar"] [data-testid="stRadio"] label {
    min-height: 2.05rem;
    border-bottom: 1px solid var(--line);
    padding: 0.18rem 0;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label > div:first-child {
    display: none !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label p {
    color: var(--ink) !important;
    font-size: 1rem;
    font-weight: 700;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) p {
    font-weight: 900;
    text-decoration: underline;
    text-decoration-thickness: 2px;
    text-underline-offset: 0.25rem;
}

.nova-chip {
    display: inline-block;
    padding: 0.2rem 0.55rem;
    border: 1px solid currentColor;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 800;
    margin-right: 0.45rem;
}

.chip-urgent { color: var(--ink); background: #eeeeee; }
.chip-warn { color: var(--ink); background: #f4f4f4; }
.chip-ok { color: var(--ink); background: #ffffff; }

.calendar-day {
    border: 1px solid var(--line);
    border-radius: 12px;
    background: var(--panel);
    padding: 0.4rem 0.2rem;
    text-align: center;
    margin-bottom: 0.35rem;
}

.calendar-day.today {
    background: var(--ink);
    color: #ffffff;
}

.mini-session {
    border-left: 3px solid var(--accent);
    background: #f8f8f8;
    border-radius: 9px;
    padding: 0.22rem 0.38rem;
    margin: 0.18rem 0;
    font-size: 0.78rem;
}

.nova-metric-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 0.55rem;
    margin: 0.55rem 0 0.75rem;
}

.nova-metric {
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: var(--radius-md);
    padding: 0.62rem 0.7rem;
}

.nova-metric span {
    color: var(--muted);
    display: block;
    font-size: 0.76rem;
    font-weight: 700;
}

.nova-metric strong {
    display: block;
    font-size: 1.45rem;
    line-height: 1.15;
    margin-top: 0.15rem;
}

.nova-metric small {
    color: var(--muted);
    display: block;
    font-size: 0.72rem;
    margin-top: 0.1rem;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.nova-today-strip,
.nova-day-summary {
    align-items: center;
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: var(--radius-md);
    display: flex;
    gap: 0.75rem;
    justify-content: space-between;
    margin: 0.45rem 0 0.6rem;
    padding: 0.62rem 0.75rem;
}

.simple-section-title {
    align-items: baseline;
    display: flex;
    gap: 0.55rem;
    justify-content: space-between;
    margin: 0.45rem 0 0.25rem;
}

.simple-section-title h3 {
    font-size: 1.15rem;
    margin: 0;
}

.simple-section-title span {
    color: var(--muted);
    font-size: 0.82rem;
}

.nova-today-strip strong,
.nova-day-summary strong {
    display: block;
    font-size: 1rem;
    line-height: 1.2;
}

.nova-today-strip span,
.nova-day-summary span {
    color: var(--muted);
    font-size: 0.82rem;
}

.course-line {
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: var(--radius-md);
    display: grid;
    grid-template-columns: minmax(0, 1.4fr) minmax(0, 1.6fr);
    gap: 0.7rem;
    margin-bottom: 0.28rem;
    padding: 0.62rem 0.7rem;
}

.course-line strong {
    display: block;
    font-size: 0.98rem;
    line-height: 1.22;
}

.course-line small {
    color: var(--muted);
    display: block;
    font-size: 0.76rem;
    margin-top: 0.12rem;
}

.course-meta {
    align-items: center;
    display: flex;
    flex-wrap: wrap;
    gap: 0.3rem;
    justify-content: flex-end;
}

.course-meta span {
    background: var(--soft);
    border: 1px solid var(--line);
    border-radius: 999px;
    color: var(--ink);
    font-size: 0.75rem;
    font-weight: 700;
    padding: 0.15rem 0.45rem;
}

.study-row-title strong {
    display: block;
    font-size: 0.96rem;
    line-height: 1.2;
}

.study-row-title span,
.study-row-time span {
    color: var(--muted);
    display: block;
    font-size: 0.78rem;
    margin-top: 0.08rem;
}

.study-row-time strong {
    display: block;
    font-size: 0.98rem;
}

[class*="st-key-course_item_"] {
    margin-bottom: 0.28rem;
}

[class*="st-key-course_item_"] [data-testid="stHorizontalBlock"],
[class*="st-key-study_day_"] [data-testid="stHorizontalBlock"],
[class*="st-key-dashboard_"] [data-testid="stHorizontalBlock"] {
    align-items: center;
}

[class*="st-key-course_item_"] [data-testid="stButton"] button {
    width: 100%;
}

[class*="st-key-study_day_"],
[class*="st-key-dashboard_"] {
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: var(--radius-md);
    margin-bottom: 0.38rem;
    padding: 0.2rem 0.62rem;
    transition: background 120ms ease, border-color 120ms ease,
        opacity 120ms ease;
}

[data-testid="stExpander"] details {
    background: var(--panel);
    border-color: var(--line) !important;
    border-radius: var(--radius-md) !important;
}

[data-testid="stExpander"] summary {
    min-height: 2.4rem;
}

[data-testid="stExpander"] summary p {
    font-size: 0.94rem;
    font-weight: 750;
}

[class*="st-key-study_day_"] [data-testid="stCheckbox"] label,
[class*="st-key-dashboard_"] [data-testid="stCheckbox"] label {
    min-height: 2.35rem;
    padding: 0 !important;
}

[class*="st-key-study_day_"] [data-testid="stCheckbox"] p,
[class*="st-key-dashboard_"] [data-testid="stCheckbox"] p {
    color: var(--ink) !important;
    font-size: 0.9rem;
    font-weight: 460 !important;
    line-height: 1.2;
}

[class*="st-key-study_day_"] [data-testid="stCheckbox"] del,
[class*="st-key-dashboard_"] [data-testid="stCheckbox"] del {
    color: var(--muted) !important;
    font-weight: 400 !important;
    text-decoration-color: var(--ink);
    text-decoration-thickness: 1.5px;
}

[class*="st-key-study_day_"]:has(input:checked),
[class*="st-key-dashboard_"]:has(input:checked) {
    background: rgba(255, 255, 255, 0.55);
    border-color: rgba(17, 17, 17, 0.08);
}

[class*="st-key-study_day_"]:has(input:checked) [data-testid="stCheckbox"] p,
[class*="st-key-dashboard_"]:has(input:checked) [data-testid="stCheckbox"] p {
    color: var(--muted) !important;
    font-weight: 400 !important;
    text-decoration: line-through;
    text-decoration-thickness: 1.5px;
    text-decoration-color: var(--ink);
    text-underline-offset: 0.12rem;
}

.week-list {
    display: grid;
    gap: 0.35rem;
    margin-top: 0.45rem;
}

.week-row {
    align-items: center;
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: var(--radius-md);
    display: grid;
    gap: 0.5rem;
    grid-template-columns: 4.8rem minmax(0, 1fr) auto;
    padding: 0.48rem 0.6rem;
}

.week-row.today {
    border-color: var(--ink);
}

.week-row strong {
    display: block;
    line-height: 1.15;
}

.week-row small,
.week-row span {
    color: var(--muted);
    display: block;
    font-size: 0.78rem;
    line-height: 1.25;
}

.week-row em {
    color: var(--ink);
    font-style: normal;
    font-weight: 800;
    white-space: nowrap;
}

.progress-list {
    display: grid;
    gap: 0.5rem;
}

.progress-row {
    display: grid;
    gap: 0.25rem;
}

.progress-row-head {
    align-items: baseline;
    display: flex;
    gap: 0.5rem;
    justify-content: space-between;
}

.progress-row-head strong {
    font-size: 0.9rem;
}

.progress-row-head span {
    color: var(--muted);
    font-size: 0.78rem;
    white-space: nowrap;
}

.progress-track {
    background: #ffffff;
    border-radius: 999px;
    height: 0.36rem;
    overflow: hidden;
}

.progress-fill {
    background: var(--ink);
    border-radius: inherit;
    height: 100%;
}

.balance-list {
    display: grid;
    gap: 0.35rem;
}

.balance-row {
    align-items: center;
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: var(--radius-md);
    display: grid;
    gap: 0.6rem;
    grid-template-columns: minmax(0, 1fr) auto;
    padding: 0.48rem 0.6rem;
}

.balance-row strong {
    display: block;
    font-size: 0.9rem;
    line-height: 1.2;
}

.balance-row span {
    color: var(--muted);
    display: block;
    font-size: 0.76rem;
}

.balance-row em {
    border: 1px solid var(--line);
    border-radius: 999px;
    color: var(--ink);
    font-size: 0.76rem;
    font-style: normal;
    font-weight: 800;
    padding: 0.16rem 0.48rem;
    white-space: nowrap;
}

.balance-row.review em {
    background: var(--soft);
}

.focus-summary {
    display: grid;
    gap: 0.5rem;
    grid-template-columns: 1.5fr 0.8fr 0.7fr 0.6fr;
    margin: 0.55rem 0 0.45rem;
}

.focus-summary-cell {
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: var(--radius-md);
    min-width: 0;
    padding: 0.55rem 0.65rem;
}

.focus-summary-cell span {
    color: var(--muted);
    display: block;
    font-size: 0.72rem;
    font-weight: 800;
}

.focus-summary-cell strong {
    display: block;
    font-size: 0.95rem;
    line-height: 1.2;
    margin-top: 0.16rem;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.exam-tag {
    border: 1px solid var(--danger);
    color: var(--danger);
    border-radius: 999px;
    padding: 0.2rem 0.4rem;
    font-size: 0.76rem;
    text-align: center;
    margin-top: 0.4rem;
    font-weight: 800;
}

.nova-lunch-line {
    background: #ffffff;
    border: 1px solid var(--line);
    border-radius: var(--radius-md);
    color: var(--ink);
    font-size: 1.05rem;
    line-height: 1.45;
    padding: 0.9rem 1.05rem;
    margin-bottom: 0.45rem;
}

.nova-weekly-menu {
    display: grid;
    gap: 0.75rem;
    grid-template-columns: repeat(auto-fit, minmax(245px, 1fr));
    margin-top: 0.75rem;
}

.nova-menu-day {
    background: #ffffff;
    border: 1px solid var(--line);
    border-radius: var(--radius-md);
    padding: 0.8rem 0.9rem 0.7rem;
}

.nova-menu-day h4 {
    color: var(--ink);
    font-size: 0.98rem;
    line-height: 1.2;
    margin: 0 0 0.55rem;
}

.nova-menu-row {
    border-top: 1px solid var(--line);
    padding: 0.45rem 0 0.05rem;
}

.nova-menu-row:first-of-type {
    border-top: 0;
    padding-top: 0;
}

.nova-menu-row span {
    color: var(--muted);
    display: block;
    font-size: 0.72rem;
    font-weight: 800;
    margin-bottom: 0.08rem;
    text-transform: uppercase;
}

.nova-menu-row p {
    color: var(--ink);
    font-size: 0.9rem;
    line-height: 1.35;
    margin: 0;
}

[class*="st-key-quickstart_actions"] {
    margin-top: 0.9rem;
}

[class*="st-key-quickstart_actions"] [data-testid="stHorizontalBlock"] {
    gap: 1rem;
}

[class*="st-key-quickstart_actions"] [data-testid="column"] {
    min-width: 0;
}

[class*="st-key-quickstart_actions"] [data-testid="stButton"] button {
    min-height: 118px;
    display: flex !important;
    align-items: flex-start !important;
    justify-content: flex-start !important;
    text-align: left !important;
    white-space: normal !important;
    padding: 0.95rem 1rem;
    border: 1px solid var(--line);
    border-radius: var(--radius-md);
    background: rgba(255, 255, 255, 0.76);
    box-shadow: 0 12px 32px rgba(17, 17, 17, 0.04);
    cursor: pointer;
    transition: transform 140ms ease, box-shadow 140ms ease,
        background 140ms ease;
}

[class*="st-key-quickstart_actions"] [data-testid="stButton"] button:hover {
    background: #ffffff;
    transform: translateY(-2px);
    box-shadow: 0 20px 46px rgba(17, 17, 17, 0.08);
}

[class*="st-key-quickstart_actions"] [data-testid="stButton"] button p {
    color: var(--muted) !important;
    font-size: 0.9rem;
    line-height: 1.35;
    font-weight: 600;
    white-space: normal !important;
    text-align: left !important;
}

[class*="st-key-quickstart_actions"] [data-testid="stButton"] button p:first-child {
    margin-bottom: 0.45rem;
}

[class*="st-key-quickstart_actions"] [data-testid="stButton"] button strong {
    color: var(--ink) !important;
    font-size: 1.35rem;
    line-height: 1.05;
    font-weight: 900;
}

@media (max-width: 900px) {
    .main .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .nova-title-row {
        gap: 0.7rem;
    }

    .nova-page-title h1 {
        font-size: 1.55rem;
    }

    .nova-page-title p {
        font-size: 0.92rem;
    }

    .nova-metric-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }

    .focus-summary {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }

    .course-line {
        grid-template-columns: 1fr;
        gap: 0.45rem;
    }

    .course-meta {
        justify-content: flex-start;
    }

    .week-row {
        grid-template-columns: 3.6rem minmax(0, 1fr);
    }

    .week-row em {
        grid-column: 2;
        justify-self: start;
    }

    [class*="st-key-quickstart_actions"] [data-testid="stHorizontalBlock"] {
        flex-direction: column;
    }
}

@media (max-width: 520px) {
    .main .block-container {
        padding-left: 0.75rem;
        padding-right: 0.75rem;
    }

    .nova-title-logo {
        display: none;
    }

    .nova-metric-grid {
        grid-template-columns: 1fr 1fr;
        gap: 0.4rem;
    }

    .nova-metric strong {
        font-size: 1.2rem;
    }

    .focus-summary {
        gap: 0.4rem;
    }

    .nova-today-strip,
    .nova-day-summary {
        align-items: flex-start;
        flex-direction: column;
        gap: 0.25rem;
    }
}
</style>
"""


def apply_theme():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def fmt_minutes(minutes: float) -> str:
    minutes = max(0, round(minutes))
    return f"{minutes // 60}h {minutes % 60:02d}m"


def fmt_hours(hours: float) -> str:
    return fmt_minutes(hours * 60)


def h(value) -> str:
    """Escape text before placing it inside custom HTML."""
    return escape(str(value), quote=True)


def render_page_title(title: str, subtitle: str = "", kicker: str = "nova",
                      logo_src: str = ""):
    subtitle_html = f"<p>{h(subtitle)}</p>" if subtitle else ""
    logo_html = (
        f'<div class="nova-title-logo"><img src="{h(logo_src)}" alt="Nova SBE" /></div>'
        if logo_src else ""
    )
    klass = "nova-page-title with-logo" if logo_src else "nova-page-title"
    html = (
        f'<div class="{klass}">'
        '<div class="nova-title-row">'
        f'{logo_html}'
        '<div>'
        f'<div class="nova-kicker">{h(kicker)}</div>'
        f'<h1>{h(title)}</h1>'
        f'{subtitle_html}'
        '</div>'
        '</div>'
        '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)
