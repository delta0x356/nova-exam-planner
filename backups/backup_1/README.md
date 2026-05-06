# Nova Exam Planner v4 🎓

A multi-user study scheduler that builds balanced plans around your exams,
integrates public-holiday data from a live API, and lives in your browser
as a Streamlit app.

---

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

On first start a `data/nova.db` SQLite file is created automatically.

---

## Features

### 👥 Multi-user
- Register with username + password (+ optional email)
- Passwords stored as salted **PBKDF2-HMAC-SHA256** hashes (stdlib-only,
  no `bcrypt` or `argon2` dependency)
- Every row in `courses`, `constraints`, and `study_sessions` is keyed
  by `user_id`, so data is fully isolated per account

### 🌐 External APIs
- **Public holidays** — [date.nager.at](https://date.nager.at): holidays
  for the user's country are pulled on demand and skipped by the
  scheduler when the *Skip public holidays* option is on.
- **Daily quote** — [zenquotes.io](https://zenquotes.io): the dashboard
  greets you with a fresh motivational quote each hour.
- Both calls are cached with `st.cache_data` and fall back to a curated
  local list if the network is unavailable.

### 🧠 Scheduling algorithm (unchanged core, now testable)
Three-step balanced scheduler:
1. Equal distribution of each course's total minutes across its
   available study days.
2. Proportional trim where the daily total would exceed the cap.
3. Overflow redistribution, closest-exam-first.

Extracted into `scheduler.py` so it can be tested / reused without
Streamlit.

### 💡 UI / UX
- Landing page with tabbed login / register.
- Personalised **Dashboard** — greeting, quote, today's tasks, next-exam
  countdown chips, and quickstart for empty accounts.
- Gradient hero banners, custom metric cards, friendlier empty states.
- Sidebar shows an avatar chip (initials), quick stats, and a logout
  button.
- **ICS export** — download the plan as a calendar feed and import into
  Google Calendar, Outlook, or Apple Calendar.

---

## Project structure

```
code/
├── app.py           Streamlit UI (pages, routing, theme)
├── database.py      SQLite schema + CRUD, user-scoped
├── auth.py          PBKDF2 hashing, login / register / session
├── api_client.py    Holidays + quotes APIs (cached, with fallback)
├── scheduler.py     Scheduling + rebalance + analytics (no Streamlit)
├── requirements.txt
└── data/
    └── nova.db      (created on first run — do not check into git)
```

### Data model

```
users (id, username UNIQUE, email, password_hash, display_name, country_code)
  1───* courses            (user_id, name, exam_date, ects, difficulty, estimated_hours)
  1───1 constraints        (user_id, weekly_hours, preferred_days, max_hours_per_day,
                            start_date, skip_holidays)
  1───* study_sessions     (user_id, course_id → courses.id, session_date,
                            planned_minutes, completed_minutes)
```

Foreign keys cascade on delete, so dropping a course removes its
sessions automatically.

---

## Deploy

Push to GitHub → [share.streamlit.io](https://share.streamlit.io) →
select repo → Deploy.

> Note: Streamlit Cloud uses an ephemeral filesystem; the SQLite DB is
> reset on every redeploy.  For durable multi-user hosting, run on a VPS
> or swap the DB path into a persistent volume.

---

## Changelog

### v4 — Multi-user + APIs + refreshed UI
- SQLite with user-scoped tables replaces per-user CSVs
- Account registration with secure password hashing
- Holiday API integration (auto-skip holidays in plan)
- Motivational quote API on dashboard
- Dashboard page, profile page, password change, ICS export
- Custom CSS theme, gradient cards, friendlier empty states
- Scheduler + analytics extracted into `scheduler.py`

### v3 — Balanced scheduler + customize page
- Single-source-of-truth DataFrame: `planned_minutes` +
  `completed_minutes`
- Three-step balanced scheduler (equal → trim → redistribute)
- Editable `st.data_editor` with per-course rebalance button
- Rebuilt analytics with pre-aggregated charts

### v2 — Pomodoro / Ultradian study mode, ECTS 0.5 increments
