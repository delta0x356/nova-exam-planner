"""Built-in subject lists used by the course loader."""

PROGRAMS = ("Master of Finance",)

GROUP_ORDER = ("mandatory", "finance_elective", "other_elective")
GROUP_LABELS = {
    "mandatory": "Mandatory Master of Finance",
    "finance_elective": "Finance electives",
    "other_elective": "Other electives",
}

PERIOD_ORDER = {
    "Fall": 0,
    "Spring": 1,
    "A": 2,
    "S1": 3,
    "T1": 4,
    "T2": 5,
    "S2": 6,
    "T3": 7,
    "T4": 8,
}

_RAW_SUBJECTS = """
mandatory|2229|Fall|Investments|7
mandatory|2269|T1|Empirical Methods for Finance|3.5
mandatory|2270|T2|Financial Modelling|3.5
mandatory|2253|Fall|Corporate Finance|7
mandatory|2578|Fall|Mastering Your Career|2
mandatory|MODULES|Spring|Modules|2
finance_elective|2260|A|Nova Students Portfolio|7
finance_elective|2232|S1|Applied Corporate Finance|7
finance_elective|2206|S1|Banking|7
finance_elective|2460|S1|Strategy Consulting|7
finance_elective|2477|S1|Introduction to Programming|7
finance_elective|2652|S1|Fundamentals on Environment and Sustainability|7
finance_elective|2218|T1|Derivatives|3.5
finance_elective|2233|T1|Macroeconomics of Financial Markets|3.5
finance_elective|2238|T1|Financial Reporting|3.5
finance_elective|2277|T1|Impact Investments|3.5
finance_elective|2783|T1|Corporate Financial Risk Management|3.5
finance_elective|2768|T1|Personal Finance|3.5
finance_elective|2185|T2|Game Theory|3.5
finance_elective|2222|T2|Financial Statement Analysis|3.5
finance_elective|2215|T2|Auditing|3.5
finance_elective|2217|T2|Corporate Governance|3.5
finance_elective|2236|T2|Private Equity|3.5
finance_elective|2277|T2|Impact Investments|3.5
finance_elective|2491|T2|Data Visualization|3.5
finance_elective|2493|T2|Marketing Analytics|3.5
finance_elective|2621|T2|Algorithmic Governance|3.5
finance_elective|2622|T2|Blockchain Fundamentals|3.5
finance_elective|2649|T2|Energy and Climate Change|3.5
finance_elective|2691|T2|Climate Finance|3.5
finance_elective|2165|S2|Microeconometrics|7
finance_elective|2168|S2|Macroeconometrics|7
finance_elective|2232|S2|Applied Corporate Finance|7
finance_elective|2206|S2|Banking|7
finance_elective|2220|S2|Entrepreneurial Finance & Venture Capital|7
finance_elective|2460|S2|Strategy Consulting|7
finance_elective|2652|S2|Fundamentals on Environment and Sustainability|7
finance_elective|2695|S2|Introduction to Machine Learning|7
finance_elective|2214|T3|Asset Management|3.5
finance_elective|2218|T3|Derivatives|3.5
finance_elective|2226|T3|Hedge Funds|3.5
finance_elective|2248|T3|Fixed Income|3.5
finance_elective|2215|T3|Auditing|3.5
finance_elective|2217|T3|Corporate Governance|3.5
finance_elective|2239|T3|Corporate Valuation|3.5
finance_elective|2278|T3|Sustainable Finance|3.5
finance_elective|2238|T3|Financial Reporting|3.5
finance_elective|2243|T3|Real Estate Finance|3.5
finance_elective|2236|T3|Private Equity|3.5
finance_elective|2273|T3|Fintech Ventures|3.5
finance_elective|2646|T3|Strategic Costing|3.5
finance_elective|2755|T3|Advanced Financial Transactions in M&A|3.5
finance_elective|2622|T3|Blockchain Fundamentals|3.5
finance_elective|2635|T3|Organizing for Good in the digital age|3.5
finance_elective|2668|T3|Sustainability Evaluation of Policies, Plans and Projects|3.5
finance_elective|2691|T3|Climate Finance|3.5
finance_elective|2768|T3|Personal Finance|3.5
finance_elective|2772|T3|Research Methods for Finance|3.5
finance_elective|2185|T4|Game Theory|3.5
finance_elective|2218|T4|Derivatives|3.5
finance_elective|2243|T4|Real Estate Finance|3.5
finance_elective|2225|T4|Risk Management|3.5
finance_elective|2226|T4|Hedge Funds|3.5
finance_elective|2233|T4|Macroeconomics of Financial Markets|3.5
finance_elective|2215|T4|Auditing|3.5
finance_elective|2239|T4|Corporate Valuation|3.5
finance_elective|2236|T4|Private Equity|3.5
finance_elective|2281|T4|Behavioral Finance|3.5
finance_elective|2282|T4|Sovereign Advisory|3.5
finance_elective|2491|T4|Data Visualization|3.5
finance_elective|2623|T4|Network Analytics|3.5
finance_elective|2635|T4|Organizing for Good in the digital age|3.5
finance_elective|2236|T4|Private Equity|3.5
finance_elective|2235|T4|Credit Risk|3.5
finance_elective|2240|T4|Financial Intermediation|3.5
finance_elective|2673|T4|Decentralized Finance|3.5
finance_elective|2279|T4|Islamic Finance|3.5
finance_elective|2736|T4|Numerical Methods for Economics and Finance|3.5
finance_elective|2647|T4|Strategic Planning and Control|3.5
finance_elective|2676|T4|Finance and the transition to net zero|3.5
finance_elective|2755|T4|Advanced Financial Transactions in M&A|3.5
finance_elective|2775|T4|Investment Philosophies|3.5
finance_elective|2959|T4|Private Equity and Financial Restructuring|3.5
finance_elective|2960|T4|Blue Finance|3.5
other_elective|2176|S1|Development Economics|7
other_elective|2327|S1|Brand Management|7
other_elective|2386|S1|Persuasion and Negotiation|7
other_elective|2421|S1|Applied Entrepreneurship|7
other_elective|2483|S1|Applied Social Entrepreneurship|7
other_elective|2484|S1|Corporate Strategy and Transformation|7
other_elective|2648|S1|Diversity & Inclusion|7
other_elective|2784|S1|Curricular Internship - Semestral|7
other_elective|2800|S1|Extracurricular Internship - Semestral|0
other_elective|2388|T1|Leadership and Change Management|3.5
other_elective|2193|T1|Behavioral Economics and Finance|3.5
other_elective|2329|T1|Consumer and Managerial Decision Making|3.5
other_elective|2332|T1|Entrepreneurship|3.5
other_elective|2352|T1|Quality Management|3.5
other_elective|2364|T1|Venture Simulation|3.5
other_elective|2375|T1|Corporate Social Responsibility|3.5
other_elective|2376|T1|Project Management|3.5
other_elective|2389|T1|Customer Relationship Management|3.5
other_elective|2416|T1|Family Business|3.5
other_elective|2446|T1|Small Business Management|3.5
other_elective|2454|T1|Doing Business in China|3.5
other_elective|2468|T1|Technology Strategy|3.5
other_elective|2473|T1|Negotiation|3.5
other_elective|2480|T1|Digital Strategy and Transformation|3.5
other_elective|2481|T1|Product Design and Development|3.5
other_elective|2490|T1|Geoeconomics and International Relations|3.5
other_elective|2496|T1|Strategic Foresight and Scenario Planning|3.5
other_elective|2613|T1|Asian Brands|3.5
other_elective|2639|T1|Entrepreneurial Strategy|3.5
other_elective|2643|T1|Social Media Marketing|3.5
other_elective|2688|T1|Curricular Internship - Trimestral|3.5
other_elective|2799|T1|Extracurricular Internship - Trimestral|0
other_elective|2440|T2|Big Data Analysis|3.5
other_elective|2194|T2|History of Economic Analysis|3.5
other_elective|2329|T2|Consumer and Managerial Decision Making|3.5
other_elective|2346|T2|Modeling Business Decisions|3.5
other_elective|2359|T2|Operations Management|3.5
other_elective|2441|T2|Digital Marketing|3.5
other_elective|2446|T2|Small Business Management|3.5
other_elective|2448|T2|Business Model Innovation|3.5
other_elective|2468|T2|Technology Strategy|3.5
other_elective|2480|T2|Digital Strategy and Transformation|3.5
other_elective|2500|T2|Performance and Progress|3.5
other_elective|2588|T2|Science-Based Entrepreneurship and Innovation|3.5
other_elective|2590|T2|Leading Social Enterprises with Impact in International Development|3.5
other_elective|2651|T2|Digital Transformation in Hospitality|3.5
other_elective|2688|T2|Curricular Internship - Trimestral|3.5
other_elective|2796|T2|Economics of the European Union|3.5
other_elective|2799|T2|Extracurricular Internship - Trimestral|0
other_elective|2327|S2|Brand Management|7
other_elective|2421|S2|Applied Entrepreneurship|7
other_elective|2438|S2|Cross-Cultural Issues for Marketing|7
other_elective|2483|S2|Applied Social Entrepreneurship|7
other_elective|2484|S2|Corporate Strategy and Transformation|7
other_elective|2485|S2|Innovation and Value Creation Wheel|7
other_elective|2580|S2|Value-Based Health Care|7
other_elective|2638|S2|Design Thinking for Social Innovation|7
other_elective|2784|S2|Curricular Internship - Semestral|7
other_elective|2800|S2|Extracurricular Internship - Semestral|0
other_elective|2134|T3|Economics of Education|3.5
other_elective|2135|T3|Economics of Health and Health Care|3.5
other_elective|2138|T3|Environmental Policy|3.5
other_elective|2145|T3|Labor Economics|3.5
other_elective|2173|T3|Macroeconomic Theory|3.5
other_elective|2181|T3|Policy Evaluation|3.5
other_elective|2184|T3|Political Economy|3.5
other_elective|2196|T3|International Migration|3.5
other_elective|2330|T3|Consumer Behavior|3.5
other_elective|2332|T3|Entrepreneurship|3.5
other_elective|2338|T3|International Business|3.5
other_elective|2352|T3|Quality Management|3.5
other_elective|2371|T3|CIRCULAR ECONOMY: Eliminate, Circulate and Regenerate|3.5
other_elective|2389|T3|Customer Relationship Management|3.5
other_elective|2416|T3|Family Business|3.5
other_elective|2448|T3|Business Model Innovation|3.5
other_elective|2465|T3|Open Innovation|3.5
other_elective|2481|T3|Product Design and Development|3.5
other_elective|2490|T3|Geoeconomics and International Relations|3.5
other_elective|2496|T3|Strategic Foresight and Scenario Planning|3.5
other_elective|2613|T3|Asian Brands|3.5
other_elective|2614|T3|Revenue Management|3.5
other_elective|2616|T3|Cracking the Sales Code|3.5
other_elective|2633|T3|System Change|3.5
other_elective|2636|T3|Brands and Marketing in Asia's Emerging Markets|3.5
other_elective|2643|T3|Social Media Marketing|3.5
other_elective|2657|T3|Hospitality Operations Management|3.5
other_elective|2667|T3|Service Excellence|3.5
other_elective|2688|T3|Curricular Internship - Trimestral|3.5
other_elective|2752|T3|Team Dynamics in Organizations|3.5
other_elective|2770|T3|Power and Social Change|3.5
other_elective|2795|T3|Innovations in the Experience Economy|3.5
other_elective|2799|T3|Extracurricular Internship - Trimestral|0
other_elective|2141|T4|Global Energy Markets|3.5
other_elective|2158|T4|Economics of Health Systems|3.5
other_elective|2197|T4|Advanced Behavioral Economics|3.5
other_elective|2330|T4|Consumer Behavior|3.5
other_elective|2332|T4|Entrepreneurship|3.5
other_elective|2338|T4|International Business|3.5
other_elective|2351|T4|Pricing Strategies|3.5
other_elective|2359|T4|Operations Management|3.5
other_elective|2375|T4|Corporate Social Responsibility|3.5
other_elective|2397|T4|Innovation Management|3.5
other_elective|2417|T4|Management of Non-Profit Organizations|3.5
other_elective|2441|T4|Digital Marketing|3.5
other_elective|2448|T4|Business Model Innovation|3.5
other_elective|2458|T4|Talent Development|3.5
other_elective|2465|T4|Open Innovation|3.5
other_elective|2473|T4|Negotiation|3.5
other_elective|2475|T4|Sales and Retailing|3.5
other_elective|2500|T4|Performance and Progress|3.5
other_elective|2588|T4|Science-Based Entrepreneurship and Innovation|3.5
other_elective|2592|T4|Strategy Implementation|3.5
other_elective|2616|T4|Cracking the Sales Code|3.5
other_elective|2644|T4|Sustainable Operations|3.5
other_elective|2663|T4|AI Impact on Business|3.5
other_elective|2675|T4|European Union: Governance and Crises|3.5
other_elective|2687|T4|Public Policy|3.5
other_elective|2688|T4|Curricular Internship - Trimestral|3.5
other_elective|2716|T4|Regenerative Business|3.5
other_elective|2749|T4|Management in the Public Sector|3.5
other_elective|2751|T4|Sustainable Marketing|3.5
other_elective|2757|T4|Hotel Asset Management|3.5
other_elective|2770|T4|Power and Social Change|3.5
other_elective|2776|T4|Hotel Investment and Development|3.5
other_elective|2791|T4|Advanced Product Design|3.5
other_elective|2799|T4|Extracurricular Internship - Trimestral|0
other_elective|2961|T4|Economics of Immigration|3.5
"""


def _read_subjects() -> tuple[dict, ...]:
    subjects = []
    seen = set()
    for line in _RAW_SUBJECTS.strip().splitlines():
        group, code, period, name, ects = line.split("|", 4)
        ects_value = float(ects)
        if ects_value <= 0:
            continue
        key = (group, code, period, name)
        if key in seen:
            continue
        seen.add(key)
        subjects.append({
            "program": "Master of Finance",
            "group": group,
            "code": code,
            "period": period,
            "name": name,
            "ects": ects_value,
        })
    return tuple(subjects)


SUBJECTS = _read_subjects()


def subjects_for(program: str, groups: list[str]) -> list[dict]:
    wanted = set(groups)
    return [
        subject for subject in SUBJECTS
        if subject["program"] == program and subject["group"] in wanted
    ]


def subject_key(subject: dict) -> str:
    parts = (
        subject["group"],
        subject["code"],
        subject["period"],
        subject["name"],
    )
    return "|".join(parts)


def subject_label(subject: dict) -> str:
    return (
        f"{subject['period']} - {subject['code']} | "
        f"{subject['name']} ({subject['ects']:g} ECTS)"
    )


def course_name(subject: dict) -> str:
    return f"{subject['name']} ({subject['code']}, {subject['period']})"


def period_sort_key(period: str) -> tuple[int, str]:
    return (PERIOD_ORDER.get(period, 99), period)
