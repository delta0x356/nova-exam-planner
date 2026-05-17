"""Built-in subject lists used by the course loader."""

MASTER_OF_FINANCE = "Master's in Finance"
MASTER_OF_ECONOMICS = "Master's in Economics"
MASTER_OF_MANAGEMENT = "Master's in Management"
MASTER_OF_BUSINESS_ANALYTICS = "Master's in Business Analytics"
BACHELOR_OF_ECONOMICS = "Bachelor's in Economics"
BACHELOR_OF_MANAGEMENT = "Bachelor's in Management"
BACHELOR_OF_OCEAN_STUDIES = "Bachelor's in Ocean Studies"

PROGRAMS = (
    MASTER_OF_FINANCE,
    MASTER_OF_ECONOMICS,
    MASTER_OF_MANAGEMENT,
    MASTER_OF_BUSINESS_ANALYTICS,
    BACHELOR_OF_ECONOMICS,
    BACHELOR_OF_MANAGEMENT,
    BACHELOR_OF_OCEAN_STUDIES,
)

PROGRAM_GROUPS = {
    MASTER_OF_FINANCE: ("mandatory", "finance_elective", "other_elective"),
    MASTER_OF_ECONOMICS: (
        "mandatory",
        "economics_elective",
        "other_elective",
    ),
    MASTER_OF_MANAGEMENT: ("mandatory", "management_elective"),
    MASTER_OF_BUSINESS_ANALYTICS: (
        "mandatory",
        "business_analytics_elective",
        "other_elective",
    ),
    BACHELOR_OF_ECONOMICS: (
        "mandatory",
        "bachelor_economics_elective",
        "general_elective",
    ),
    BACHELOR_OF_MANAGEMENT: (
        "mandatory",
        "bachelor_management_elective",
        "general_elective",
    ),
    BACHELOR_OF_OCEAN_STUDIES: ("mandatory",),
}

GROUP_LABELS = {
    MASTER_OF_FINANCE: {
        "mandatory": "Mandatory",
        "finance_elective": "Finance electives",
        "other_elective": "Other electives",
    },
    MASTER_OF_ECONOMICS: {
        "mandatory": "Mandatory",
        "economics_elective": "Economics electives",
        "other_elective": "Other electives",
    },
    MASTER_OF_MANAGEMENT: {
        "mandatory": "Mandatory",
        "management_elective": "Management electives",
    },
    MASTER_OF_BUSINESS_ANALYTICS: {
        "mandatory": "Mandatory",
        "business_analytics_elective": "Business Analytics electives",
        "other_elective": "Other electives",
    },
    BACHELOR_OF_ECONOMICS: {
        "mandatory": "Mandatory",
        "bachelor_economics_elective": "Economics electives",
        "general_elective": "General electives",
    },
    BACHELOR_OF_MANAGEMENT: {
        "mandatory": "Mandatory",
        "bachelor_management_elective": "Management electives",
        "general_elective": "General electives",
    },
    BACHELOR_OF_OCEAN_STUDIES: {
        "mandatory": "Mandatory",
    },
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
Master's in Economics|mandatory|2174|Fall|Macroeconomic Analysis|7
Master's in Economics|mandatory|2188|Fall|Microeconomic Analysis|7
Master's in Economics|mandatory|2175|Fall|Econometrics|7
Master's in Economics|mandatory|2578|Fall|Mastering Your Career|2
Master's in Economics|mandatory|2168|Spring|Macroeconometrics|7
Master's in Economics|mandatory|2165|Spring|Microeconometrics|7
Master's in Economics|economics_elective|2206|S1|Banking|7
Master's in Economics|economics_elective|2652|S1|Fundamentals on Environment and Sustainability|7
Master's in Economics|economics_elective|2477|S1|Introduction to Programming|7
Master's in Economics|economics_elective|2229|S1|Investments|7
Master's in Economics|economics_elective|2176|S1|Development Economics|7
Master's in Economics|economics_elective|2128|T1|Competition Policy|3.5
Master's in Economics|economics_elective|2783|T1|Corporate Financial Risk Management|3.5
Master's in Economics|economics_elective|2218|T1|Derivatives|3.5
Master's in Economics|economics_elective|2277|T1|Impact Investments|3.5
Master's in Economics|economics_elective|2193|T1|Behavioral Economics and Finance|3.5
Master's in Economics|economics_elective|2233|T1|Macroeconomics of Financial Markets|3.5
Master's in Economics|economics_elective|2238|T1|Financial Reporting|3.5
Master's in Economics|economics_elective|2621|T2|Algorithmic Governance|3.5
Master's in Economics|economics_elective|2222|T2|Financial Statement Analysis|3.5
Master's in Economics|economics_elective|2215|T2|Auditing|3.5
Master's in Economics|economics_elective|2622|T2|Blockchain Fundamentals|3.5
Master's in Economics|economics_elective|2491|T2|Data Visualization|3.5
Master's in Economics|economics_elective|2277|T2|Impact Investments|3.5
Master's in Economics|economics_elective|2649|T2|Energy and Climate Change|3.5
Master's in Economics|economics_elective|2493|T2|Marketing Analytics|3.5
Master's in Economics|economics_elective|2236|T2|Private Equity|3.5
Master's in Economics|economics_elective|2691|T2|Climate Finance|3.5
Master's in Economics|economics_elective|2745|T2|Politics for Policy|3.5
Master's in Economics|economics_elective|2194|T2|History of Economic Analysis|3.5
Master's in Economics|economics_elective|2796|T2|Economics of the European Union|3.5
Master's in Economics|economics_elective|2206|S2|Banking|7
Master's in Economics|economics_elective|2652|S2|Fundamentals on Environment and Sustainability|7
Master's in Economics|economics_elective|2695|S2|Introduction to Machine Learning|7
Master's in Economics|economics_elective|2477|S2|Introduction to Programming|7
Master's in Economics|economics_elective|2214|T3|Asset Management|3.5
Master's in Economics|economics_elective|2215|T3|Auditing|3.5
Master's in Economics|economics_elective|2622|T3|Blockchain Fundamentals|3.5
Master's in Economics|economics_elective|2218|T3|Derivatives|3.5
Master's in Economics|economics_elective|2134|T3|Economics of Education|3.5
Master's in Economics|economics_elective|2135|T3|Economics of Health and Health Care|3.5
Master's in Economics|economics_elective|2273|T3|Fintech Ventures|3.5
Master's in Economics|economics_elective|2196|T3|International Migration|3.5
Master's in Economics|economics_elective|2635|T3|Organizing for Good in the digital age|3.5
Master's in Economics|economics_elective|2770|T3|Power and Social Change|3.5
Master's in Economics|economics_elective|2236|T3|Private Equity|3.5
Master's in Economics|economics_elective|2668|T3|Sustainability Evaluation of Policies, Plans and Projects|3.5
Master's in Economics|economics_elective|2226|T3|Hedge Funds|3.5
Master's in Economics|economics_elective|2278|T3|Sustainable Finance|3.5
Master's in Economics|economics_elective|2243|T3|Real Estate Finance|3.5
Master's in Economics|economics_elective|2755|T3|Advanced Financial Transactions in M&A|3.5
Master's in Economics|economics_elective|2691|T3|Climate Finance|3.5
Master's in Economics|economics_elective|2772|T3|Research Methods for Finance|3.5
Master's in Economics|economics_elective|2138|T3|Environmental Policy|3.5
Master's in Economics|economics_elective|2145|T3|Labor Economics|3.5
Master's in Economics|economics_elective|2173|T3|Macroeconomic Theory|3.5
Master's in Economics|economics_elective|2181|T3|Policy Evaluation|3.5
Master's in Economics|economics_elective|2184|T3|Political Economy|3.5
Master's in Economics|economics_elective|2248|T3|Fixed Income|3.5
Master's in Economics|economics_elective|2238|T3|Financial Reporting|3.5
Master's in Economics|economics_elective|2215|T4|Auditing|3.5
Master's in Economics|economics_elective|2218|T4|Derivatives|3.5
Master's in Economics|economics_elective|2236|T4|Private Equity|3.5
Master's in Economics|economics_elective|2158|T4|Economics of Health Systems|3.5
Master's in Economics|economics_elective|2675|T4|European Union: Governance and Crises|3.5
Master's in Economics|economics_elective|2491|T4|Data Visualization|3.5
Master's in Economics|economics_elective|2676|T4|Finance and the transition to net zero|3.5
Master's in Economics|economics_elective|2623|T4|Network Analytics|3.5
Master's in Economics|economics_elective|2635|T4|Organizing for Good in the digital age|3.5
Master's in Economics|economics_elective|2770|T4|Power and Social Change|3.5
Master's in Economics|economics_elective|2961|T4|Economics of Immigration|3.5
Master's in Economics|economics_elective|2131|T4|Economic Growth|3.5
Master's in Economics|economics_elective|2243|T4|Real Estate Finance|3.5
Master's in Economics|economics_elective|2225|T4|Risk Management|3.5
Master's in Economics|economics_elective|2226|T4|Hedge Funds|3.5
Master's in Economics|economics_elective|2282|T4|Sovereign Advisory|3.5
Master's in Economics|economics_elective|2240|T4|Financial Intermediation|3.5
Master's in Economics|economics_elective|2736|T4|Numerical Methods for Economics and Finance|3.5
Master's in Economics|economics_elective|2737|T4|Private Sector Development|3.5
Master's in Economics|economics_elective|2755|T4|Advanced Financial Transactions in M&A|3.5
Master's in Economics|economics_elective|2141|T4|Global Energy Markets|3.5
Master's in Economics|economics_elective|2197|T4|Advanced Behavioral Economics|3.5
Master's in Economics|economics_elective|2233|T4|Macroeconomics of Financial Markets|3.5
Master's in Economics|economics_elective|2281|T4|Behavioral Finance|3.5
Master's in Economics|economics_elective|2235|T4|Credit Risk|3.5
Master's in Economics|economics_elective|2687|T4|Public Policy|3.5
Master's in Economics|other_elective|2232|S1|Applied Corporate Finance|7
Master's in Economics|other_elective|2421|S1|Applied Entrepreneurship|7
Master's in Economics|other_elective|2483|S1|Applied Social Entrepreneurship|7
Master's in Economics|other_elective|2582|S1|Competitive Strategy: An Analytical Approach|7
Master's in Economics|other_elective|2484|S1|Corporate Strategy and Transformation|7
Master's in Economics|other_elective|2648|S1|Diversity & Inclusion|7
Master's in Economics|other_elective|2386|S1|Persuasion and Negotiation|7
Master's in Economics|other_elective|2460|S1|Strategy Consulting|7
Master's in Economics|other_elective|2784|S1|Curricular Internship - Semestral|7
Master's in Economics|other_elective|2800|S1|Extracurricular Internship - Semestral|0
Master's in Economics|other_elective|2613|T1|Asian Brands|3.5
Master's in Economics|other_elective|2329|T1|Consumer and Managerial Decision Making|3.5
Master's in Economics|other_elective|2375|T1|Corporate Social Responsibility|3.5
Master's in Economics|other_elective|2389|T1|Customer Relationship Management|3.5
Master's in Economics|other_elective|2454|T1|Doing Business in China|3.5
Master's in Economics|other_elective|2639|T1|Entrepreneurial Strategy|3.5
Master's in Economics|other_elective|2332|T1|Entrepreneurship|3.5
Master's in Economics|other_elective|2416|T1|Family Business|3.5
Master's in Economics|other_elective|2490|T1|Geoeconomics and International Relations|3.5
Master's in Economics|other_elective|2388|T1|Leadership and Change Management|3.5
Master's in Economics|other_elective|2473|T1|Negotiation|3.5
Master's in Economics|other_elective|2481|T1|Product Design and Development|3.5
Master's in Economics|other_elective|2376|T1|Project Management|3.5
Master's in Economics|other_elective|2352|T1|Quality Management|3.5
Master's in Economics|other_elective|2446|T1|Small Business Management|3.5
Master's in Economics|other_elective|2643|T1|Social Media Marketing|3.5
Master's in Economics|other_elective|2496|T1|Strategic Foresight and Scenario Planning|3.5
Master's in Economics|other_elective|2468|T1|Technology Strategy|3.5
Master's in Economics|other_elective|2364|T1|Venture Simulation|3.5
Master's in Economics|other_elective|2688|T1|Curricular Internship - Trimestral|3.5
Master's in Economics|other_elective|2799|T1|Extracurricular Internship - Trimestral|0
Master's in Economics|other_elective|2440|T2|Big Data Analysis|3.5
Master's in Economics|other_elective|2448|T2|Business Model Innovation|3.5
Master's in Economics|other_elective|2329|T2|Consumer and Managerial Decision Making|3.5
Master's in Economics|other_elective|2217|T2|Corporate Governance|3.5
Master's in Economics|other_elective|2441|T2|Digital Marketing|3.5
Master's in Economics|other_elective|2346|T2|Modeling Business Decisions|3.5
Master's in Economics|other_elective|2359|T2|Operations Management|3.5
Master's in Economics|other_elective|2468|T2|Technology Strategy|3.5
Master's in Economics|other_elective|2590|T2|Leading Social Enterprises with Impact in International Development|3.5
Master's in Economics|other_elective|2500|T2|Performance and Progress|3.5
Master's in Economics|other_elective|2588|T2|Science-Based Entrepreneurship and Innovation|3.5
Master's in Economics|other_elective|2446|T2|Small Business Management|3.5
Master's in Economics|other_elective|2688|T2|Curricular Internship - Trimestral|3.5
Master's in Economics|other_elective|2799|T2|Extracurricular Internship - Trimestral|0
Master's in Economics|other_elective|2232|S2|Applied Corporate Finance|7
Master's in Economics|other_elective|2421|S2|Applied Entrepreneurship|7
Master's in Economics|other_elective|2483|S2|Applied Social Entrepreneurship|7
Master's in Economics|other_elective|2484|S2|Corporate Strategy and Transformation|7
Master's in Economics|other_elective|2438|S2|Cross-Cultural Issues for Marketing|7
Master's in Economics|other_elective|2638|S2|Design Thinking for Social Innovation|7
Master's in Economics|other_elective|2220|S2|Entrepreneurial Finance & Venture Capital|7
Master's in Economics|other_elective|2485|S2|Innovation and Value Creation Wheel|7
Master's in Economics|other_elective|2460|S2|Strategy Consulting|7
Master's in Economics|other_elective|2580|S2|Value-Based Health Care|7
Master's in Economics|other_elective|2784|S2|Curricular Internship - Semestral|7
Master's in Economics|other_elective|2800|S2|Extracurricular Internship - Semestral|0
Master's in Economics|other_elective|2613|T3|Asian Brands|3.5
Master's in Economics|other_elective|2636|T3|Brands and Marketing in Asia's Emerging Markets|3.5
Master's in Economics|other_elective|2448|T3|Business Model Innovation|3.5
Master's in Economics|other_elective|2371|T3|CIRCULAR ECONOMY: Eliminate, Circulate and Regenerate|3.5
Master's in Economics|other_elective|2217|T3|Corporate Governance|3.5
Master's in Economics|other_elective|2239|T3|Corporate Valuation|3.5
Master's in Economics|other_elective|2616|T3|Cracking the Sales Code|3.5
Master's in Economics|other_elective|2389|T3|Customer Relationship Management|3.5
Master's in Economics|other_elective|2332|T3|Entrepreneurship|3.5
Master's in Economics|other_elective|2416|T3|Family Business|3.5
Master's in Economics|other_elective|2490|T3|Geoeconomics and International Relations|3.5
Master's in Economics|other_elective|2338|T3|International Business|3.5
Master's in Economics|other_elective|2465|T3|Open Innovation|3.5
Master's in Economics|other_elective|2481|T3|Product Design and Development|3.5
Master's in Economics|other_elective|2352|T3|Quality Management|3.5
Master's in Economics|other_elective|2614|T3|Revenue Management|3.5
Master's in Economics|other_elective|2667|T3|Service Excellence|3.5
Master's in Economics|other_elective|2643|T3|Social Media Marketing|3.5
Master's in Economics|other_elective|2699|T3|Sports Club Management|3.5
Master's in Economics|other_elective|2646|T3|Strategic Costing|3.5
Master's in Economics|other_elective|2496|T3|Strategic Foresight and Scenario Planning|3.5
Master's in Economics|other_elective|2633|T3|System Change|3.5
Master's in Economics|other_elective|2752|T3|Team Dynamics in Organizations|3.5
Master's in Economics|other_elective|2656|T3|Work & Family|3.5
Master's in Economics|other_elective|2688|T3|Curricular Internship - Trimestral|3.5
Master's in Economics|other_elective|2799|T3|Extracurricular Internship - Trimestral|0
Master's in Economics|other_elective|2239|T4|Corporate Valuation|3.5
Master's in Economics|other_elective|2332|T4|Entrepreneurship|3.5
Master's in Economics|other_elective|2351|T4|Pricing Strategies|3.5
Master's in Economics|other_elective|2359|T4|Operations Management|3.5
Master's in Economics|other_elective|2448|T4|Business Model Innovation|3.5
Master's in Economics|other_elective|2397|T4|Innovation Management|3.5
Master's in Economics|other_elective|2417|T4|Management of Non-Profit Organizations|3.5
Master's in Economics|other_elective|2441|T4|Digital Marketing|3.5
Master's in Economics|other_elective|2458|T4|Talent Development|3.5
Master's in Economics|other_elective|2465|T4|Open Innovation|3.5
Master's in Economics|other_elective|2475|T4|Sales and Retailing|3.5
Master's in Economics|other_elective|2375|T4|Corporate Social Responsibility|3.5
Master's in Economics|other_elective|2588|T4|Science-Based Entrepreneurship and Innovation|3.5
Master's in Economics|other_elective|2338|T4|International Business|3.5
Master's in Economics|other_elective|2616|T4|Cracking the Sales Code|3.5
Master's in Economics|other_elective|2500|T4|Performance and Progress|3.5
Master's in Economics|other_elective|2473|T4|Negotiation|3.5
Master's in Economics|other_elective|2716|T4|Regenerative Business|3.5
Master's in Economics|other_elective|2663|T4|AI Impact on Business|3.5
Master's in Economics|other_elective|2592|T4|Strategy Implementation|3.5
Master's in Economics|other_elective|2749|T4|Management in the Public Sector|3.5
Master's in Economics|other_elective|2751|T4|Sustainable Marketing|3.5
Master's in Economics|other_elective|2647|T4|Strategic Planning and Control|3.5
Master's in Economics|other_elective|2757|T4|Hotel Asset Management|3.5
Master's in Economics|other_elective|2644|T4|Sustainable Operations|3.5
Master's in Economics|other_elective|2791|T4|Advanced Product Design|3.5
Master's in Economics|other_elective|2279|T4|Islamic Finance|3.5
Master's in Economics|other_elective|2688|T4|Curricular Internship - Trimestral|3.5
Master's in Economics|other_elective|2799|T4|Extracurricular Internship - Trimestral|0
Master's in Management|mandatory|2414|S1|Financial Management|7
Master's in Management|mandatory|2581|S1|Advanced Financial Management|7
Master's in Management|mandatory|2431|S1|Marketing Management|7
Master's in Management|mandatory|2430|S1|Advanced Marketing|7
Master's in Management|mandatory|2584|S1|Strategy|7
Master's in Management|mandatory|2459|S1|Advanced Strategy|7
Master's in Management|mandatory|2578|S1|Mastering Your Career|2
Master's in Management|mandatory|2435|T1|Statistics III|3.5
Master's in Management|mandatory|2786|T1|Research Methods in Management|3.5
Master's in Management|mandatory|2336|T1|Human Resources Management|3.5
Master's in Management|mandatory|2336|T2|Human Resources Management|3.5
Master's in Management|mandatory|2463|T2|Advanced Topics in Human Resources Management|3.5
Master's in Management|mandatory|2434|T2|Statistics II|3.5
Master's in Management|mandatory|2435|T2|Statistics III|3.5
Master's in Management|mandatory|2786|T2|Research Methods in Management|3.5
Master's in Management|mandatory|2414|S2|Financial Management|7
Master's in Management|mandatory|2581|S2|Advanced Financial Management|7
Master's in Management|mandatory|2431|S2|Marketing Management|7
Master's in Management|mandatory|2430|S2|Advanced Marketing|7
Master's in Management|mandatory|2584|S2|Strategy|7
Master's in Management|mandatory|2459|S2|Advanced Strategy|7
Master's in Management|mandatory|2578|S2|Mastering Your Career|2
Master's in Management|mandatory|2336|T3|Human Resources Management|3.5
Master's in Management|mandatory|2463|T3|Advanced Topics in Human Resources Management|3.5
Master's in Management|mandatory|2435|T3|Statistics III|3.5
Master's in Management|mandatory|2786|T3|Research Methods in Management|3.5
Master's in Management|mandatory|2434|T4|Statistics II|3.5
Master's in Management|mandatory|2435|T4|Statistics III|3.5
Master's in Management|mandatory|2786|T4|Research Methods in Management|3.5
Master's in Business Analytics|mandatory|2766|T1|Introduction to Python for Data Analysis|3.5
Master's in Business Analytics|mandatory|2771|T1|Research Methods for Business Analytics|3.5
Master's in Business Analytics|mandatory|2762|T1|Digital Strategy and Markets|3.5
Master's in Business Analytics|mandatory|2659|T2|Data Curation for Business Analytics|3.5
Master's in Business Analytics|mandatory|2609|T2|Data Visualization for Business Analytics|3.5
Master's in Business Analytics|mandatory|2773|T2|Optimization|3.5
Master's in Business Analytics|mandatory|2578|S1|Mastering Your Career|2
Master's in Business Analytics|mandatory|2606|T3|Data Ecosystems and Governance in Organizations|3.5
Master's in Business Analytics|mandatory|2767|T3|Machine Learning|3.5
Master's in Business Analytics|mandatory|2761|T3|Digital Experimentation & Causal Analysis|3.5
Master's in Business Analytics|business_analytics_elective|2599|T1|Project Scoping|3.5
Master's in Business Analytics|business_analytics_elective|2610|S2|Business Analytics Special Project|7
Master's in Business Analytics|business_analytics_elective|2612|T3|Advanced Programming for Data Science|3.5
Master's in Business Analytics|business_analytics_elective|2615|T3|Web and Cloud Computing|3.5
Master's in Business Analytics|business_analytics_elective|2758|T4|Advanced Topics in Machine Learning|3.5
Master's in Business Analytics|business_analytics_elective|2442|T4|Design and Construction of Data Centric Apps|3.5
Master's in Business Analytics|business_analytics_elective|2779|T4|Engineering of Data Analysis|3.5
Master's in Business Analytics|business_analytics_elective|2421|S1|Applied Entrepreneurship|7
Master's in Business Analytics|business_analytics_elective|2582|S1|Competitive Strategy: An Analytical Approach|7
Master's in Business Analytics|business_analytics_elective|2484|S1|Corporate Strategy and Transformation|7
Master's in Business Analytics|business_analytics_elective|2128|T1|Competition Policy|3.5
Master's in Business Analytics|business_analytics_elective|2783|T1|Corporate Financial Risk Management|3.5
Master's in Business Analytics|business_analytics_elective|2389|T1|Customer Relationship Management|3.5
Master's in Business Analytics|business_analytics_elective|2218|T1|Derivatives|3.5
Master's in Business Analytics|business_analytics_elective|2639|T1|Entrepreneurial Strategy|3.5
Master's in Business Analytics|business_analytics_elective|2481|T1|Product Design and Development|3.5
Master's in Business Analytics|business_analytics_elective|2352|T1|Quality Management|3.5
Master's in Business Analytics|business_analytics_elective|2496|T1|Strategic Foresight and Scenario Planning|3.5
Master's in Business Analytics|business_analytics_elective|2468|T1|Technology Strategy|3.5
Master's in Business Analytics|business_analytics_elective|2621|T2|Algorithmic Governance|3.5
Master's in Business Analytics|business_analytics_elective|2440|T2|Big Data Analysis|3.5
Master's in Business Analytics|business_analytics_elective|2622|T2|Blockchain Fundamentals|3.5
Master's in Business Analytics|business_analytics_elective|2448|T2|Business Model Innovation|3.5
Master's in Business Analytics|business_analytics_elective|2778|T2|Cybersecurity in Organizations|3.5
Master's in Business Analytics|business_analytics_elective|2441|T2|Digital Marketing|3.5
Master's in Business Analytics|business_analytics_elective|2649|T2|Energy and Climate Change|3.5
Master's in Business Analytics|business_analytics_elective|2185|T2|Game Theory|3.5
Master's in Business Analytics|business_analytics_elective|2493|T2|Marketing Analytics|3.5
Master's in Business Analytics|business_analytics_elective|2359|T2|Operations Management|3.5
Master's in Business Analytics|business_analytics_elective|2785|T2|Product Management in Technology|3.5
Master's in Business Analytics|business_analytics_elective|2588|T2|Science-Based Entrepreneurship and Innovation|3.5
Master's in Business Analytics|business_analytics_elective|2793|T2|Supply Chain Management|3.5
Master's in Business Analytics|business_analytics_elective|2468|T2|Technology Strategy|3.5
Master's in Business Analytics|business_analytics_elective|2421|S2|Applied Entrepreneurship|7
Master's in Business Analytics|business_analytics_elective|2484|S2|Corporate Strategy and Transformation|7
Master's in Business Analytics|business_analytics_elective|2638|S2|Design Thinking for Social Innovation|7
Master's in Business Analytics|business_analytics_elective|2220|S2|Entrepreneurial Finance & Venture Capital|7
Master's in Business Analytics|business_analytics_elective|2214|T3|Asset Management|3.5
Master's in Business Analytics|business_analytics_elective|2622|T3|Blockchain Fundamentals|3.5
Master's in Business Analytics|business_analytics_elective|2448|T3|Business Model Innovation|3.5
Master's in Business Analytics|business_analytics_elective|2371|T3|CIRCULAR ECONOMY: Eliminate, Circulate and Regenerate|3.5
Master's in Business Analytics|business_analytics_elective|2616|T3|Cracking the Sales Code|3.5
Master's in Business Analytics|business_analytics_elective|2389|T3|Customer Relationship Management|3.5
Master's in Business Analytics|business_analytics_elective|2218|T3|Derivatives|3.5
Master's in Business Analytics|business_analytics_elective|2134|T3|Economics of Education|3.5
Master's in Business Analytics|business_analytics_elective|2135|T3|Economics of Health and Health Care|3.5
Master's in Business Analytics|business_analytics_elective|2273|T3|Fintech Ventures|3.5
Master's in Business Analytics|business_analytics_elective|2196|T3|International Migration|3.5
Master's in Business Analytics|business_analytics_elective|2465|T3|Open Innovation|3.5
Master's in Business Analytics|business_analytics_elective|2635|T3|Organizing for Good in the digital age|3.5
Master's in Business Analytics|business_analytics_elective|2481|T3|Product Design and Development|3.5
Master's in Business Analytics|business_analytics_elective|2352|T3|Quality Management|3.5
Master's in Business Analytics|business_analytics_elective|2496|T3|Strategic Foresight and Scenario Planning|3.5
Master's in Business Analytics|business_analytics_elective|2791|T4|Advanced Product Design|3.5
Master's in Business Analytics|business_analytics_elective|2663|T4|AI Impact on Business|3.5
Master's in Business Analytics|business_analytics_elective|2448|T4|Business Model Innovation|3.5
Master's in Business Analytics|business_analytics_elective|2616|T4|Cracking the Sales Code|3.5
Master's in Business Analytics|business_analytics_elective|2778|T4|Cybersecurity in Organizations|3.5
Master's in Business Analytics|business_analytics_elective|2218|T4|Derivatives|3.5
Master's in Business Analytics|business_analytics_elective|2441|T4|Digital Marketing|3.5
Master's in Business Analytics|business_analytics_elective|2961|T4|Economics of Immigration|3.5
Master's in Business Analytics|business_analytics_elective|2185|T4|Game Theory|3.5
Master's in Business Analytics|business_analytics_elective|2397|T4|Innovation Management|3.5
Master's in Business Analytics|business_analytics_elective|2623|T4|Network Analytics|3.5
Master's in Business Analytics|business_analytics_elective|2465|T4|Open Innovation|3.5
Master's in Business Analytics|business_analytics_elective|2359|T4|Operations Management|3.5
Master's in Business Analytics|business_analytics_elective|2635|T4|Organizing for Good in the digital age|3.5
Master's in Business Analytics|business_analytics_elective|2716|T4|Regenerative Business|3.5
Master's in Business Analytics|business_analytics_elective|2588|T4|Science-Based Entrepreneurship and Innovation|3.5
Master's in Business Analytics|business_analytics_elective|2644|T4|Sustainable Operations|3.5
Master's in Business Analytics|other_elective|2232|S1|Applied Corporate Finance|7
Master's in Business Analytics|other_elective|2483|S1|Applied Social Entrepreneurship|7
Master's in Business Analytics|other_elective|2206|S1|Banking|7
Master's in Business Analytics|other_elective|2784|S1|Curricular Internship - Semestral|7
Master's in Business Analytics|other_elective|2652|S1|Fundamentals on Environment and Sustainability|7
Master's in Business Analytics|other_elective|2386|S1|Persuasion and Negotiation|7
Master's in Business Analytics|other_elective|2460|S1|Strategy Consulting|7
Master's in Business Analytics|other_elective|2613|T1|Asian Brands|3.5
Master's in Business Analytics|other_elective|2193|T1|Behavioral Economics and Finance|3.5
Master's in Business Analytics|other_elective|2375|T1|Corporate Social Responsibility|3.5
Master's in Business Analytics|other_elective|2688|T1|Curricular Internship - Trimestral|3.5
Master's in Business Analytics|other_elective|2454|T1|Doing Business in China|3.5
Master's in Business Analytics|other_elective|2416|T1|Family Business|3.5
Master's in Business Analytics|other_elective|2490|T1|Geoeconomics and International Relations|3.5
Master's in Business Analytics|other_elective|2277|T1|Impact Investments|3.5
Master's in Business Analytics|other_elective|2388|T1|Leadership and Change Management|3.5
Master's in Business Analytics|other_elective|2233|T1|Macroeconomics of Financial Markets|3.5
Master's in Business Analytics|other_elective|2473|T1|Negotiation|3.5
Master's in Business Analytics|other_elective|2376|T1|Project Management|3.5
Master's in Business Analytics|other_elective|2446|T1|Small Business Management|3.5
Master's in Business Analytics|other_elective|2643|T1|Social Media Marketing|3.5
Master's in Business Analytics|other_elective|2215|T2|Auditing|3.5
Master's in Business Analytics|other_elective|2217|T2|Corporate Governance|3.5
Master's in Business Analytics|other_elective|2688|T2|Curricular Internship - Trimestral|3.5
Master's in Business Analytics|other_elective|2491|T2|Data Visualization|3.5
Master's in Business Analytics|other_elective|2651|T2|Digital Transformation in Hospitality|3.5
Master's in Business Analytics|other_elective|2194|T2|History of Economic Analysis|3.5
Master's in Business Analytics|other_elective|2277|T2|Impact Investments|3.5
Master's in Business Analytics|other_elective|2590|T2|Leading Social Enterprises with Impact in International Development|3.5
Master's in Business Analytics|other_elective|2500|T2|Performance and Progress|3.5
Master's in Business Analytics|other_elective|2236|T2|Private Equity|3.5
Master's in Business Analytics|other_elective|2446|T2|Small Business Management|3.5
Master's in Business Analytics|other_elective|2232|S2|Applied Corporate Finance|7
Master's in Business Analytics|other_elective|2483|S2|Applied Social Entrepreneurship|7
Master's in Business Analytics|other_elective|2206|S2|Banking|7
Master's in Business Analytics|other_elective|2438|S2|Cross-Cultural Issues for Marketing|7
Master's in Business Analytics|other_elective|2784|S2|Curricular Internship - Semestral|7
Master's in Business Analytics|other_elective|2652|S2|Fundamentals on Environment and Sustainability|7
Master's in Business Analytics|other_elective|2485|S2|Innovation and Value Creation Wheel|7
Master's in Business Analytics|other_elective|2460|S2|Strategy Consulting|7
Master's in Business Analytics|other_elective|2580|S2|Value-Based Health Care|7
Master's in Business Analytics|other_elective|2613|T3|Asian Brands|3.5
Master's in Business Analytics|other_elective|2215|T3|Auditing|3.5
Master's in Business Analytics|other_elective|2217|T3|Corporate Governance|3.5
Master's in Business Analytics|other_elective|2239|T3|Corporate Valuation|3.5
Master's in Business Analytics|other_elective|2688|T3|Curricular Internship - Trimestral|3.5
Master's in Business Analytics|other_elective|2138|T3|Environmental Policy|3.5
Master's in Business Analytics|other_elective|2416|T3|Family Business|3.5
Master's in Business Analytics|other_elective|2248|T3|Fixed Income|3.5
Master's in Business Analytics|other_elective|2490|T3|Geoeconomics and International Relations|3.5
Master's in Business Analytics|other_elective|2338|T3|International Business|3.5
Master's in Business Analytics|other_elective|2145|T3|Labor Economics|3.5
Master's in Business Analytics|other_elective|2173|T3|Macroeconomic Theory|3.5
Master's in Business Analytics|other_elective|2181|T3|Policy Evaluation|3.5
Master's in Business Analytics|other_elective|2184|T3|Political Economy|3.5
Master's in Business Analytics|other_elective|2770|T3|Power and Social Change|3.5
Master's in Business Analytics|other_elective|2236|T3|Private Equity|3.5
Master's in Business Analytics|other_elective|2243|T3|Real Estate Finance|3.5
Master's in Business Analytics|other_elective|2614|T3|Revenue Management|3.5
Master's in Business Analytics|other_elective|2667|T3|Service Excellence|3.5
Master's in Business Analytics|other_elective|2643|T3|Social Media Marketing|3.5
Master's in Business Analytics|other_elective|2699|T3|Sports Club Management|3.5
Master's in Business Analytics|other_elective|2646|T3|Strategic Costing|3.5
Master's in Business Analytics|other_elective|2633|T3|System Change|3.5
Master's in Business Analytics|other_elective|2752|T3|Team Dynamics in Organizations|3.5
Master's in Business Analytics|other_elective|2215|T4|Auditing|3.5
Master's in Business Analytics|other_elective|2281|T4|Behavioral Finance|3.5
Master's in Business Analytics|other_elective|2375|T4|Corporate Social Responsibility|3.5
Master's in Business Analytics|other_elective|2239|T4|Corporate Valuation|3.5
Master's in Business Analytics|other_elective|2235|T4|Credit Risk|3.5
Master's in Business Analytics|other_elective|2688|T4|Curricular Internship - Trimestral|3.5
Master's in Business Analytics|other_elective|2491|T4|Data Visualization|3.5
Master's in Business Analytics|other_elective|2683|T4|E-Commerce and Metaverse|3.5
Master's in Business Analytics|other_elective|2158|T4|Economics of Health Systems|3.5
Master's in Business Analytics|other_elective|2676|T4|Finance and the transition to net zero|3.5
Master's in Business Analytics|other_elective|2141|T4|Global Energy Markets|3.5
Master's in Business Analytics|other_elective|2757|T4|Hotel Asset Management|3.5
Master's in Business Analytics|other_elective|2338|T4|International Business|3.5
Master's in Business Analytics|other_elective|2279|T4|Islamic Finance|3.5
Master's in Business Analytics|other_elective|2233|T4|Macroeconomics of Financial Markets|3.5
Master's in Business Analytics|other_elective|2749|T4|Management in the Public Sector|3.5
Master's in Business Analytics|other_elective|2417|T4|Management of Non-Profit Organizations|3.5
Master's in Business Analytics|other_elective|2473|T4|Negotiation|3.5
Master's in Business Analytics|other_elective|2500|T4|Performance and Progress|3.5
Master's in Business Analytics|other_elective|2770|T4|Power and Social Change|3.5
Master's in Business Analytics|other_elective|2351|T4|Pricing Strategies|3.5
Master's in Business Analytics|other_elective|2236|T4|Private Equity|3.5
Master's in Business Analytics|other_elective|2687|T4|Public Policy|3.5
Master's in Business Analytics|other_elective|2243|T4|Real Estate Finance|3.5
Master's in Business Analytics|other_elective|2475|T4|Sales and Retailing|3.5
Master's in Business Analytics|other_elective|2647|T4|Strategic Planning and Control|3.5
Master's in Business Analytics|other_elective|2751|T4|Sustainable Marketing|3.5
Master's in Business Analytics|other_elective|2458|T4|Talent Development|3.5
Bachelor's in Economics|mandatory|1117|S1|Principles of Microeconomics|7
Bachelor's in Economics|mandatory|1117|S2|Principles of Microeconomics|7
Bachelor's in Economics|mandatory|1118|S1|Principles of Macroeconomics|7
Bachelor's in Economics|mandatory|1118|S2|Principles of Macroeconomics|7
Bachelor's in Economics|mandatory|1119|S1|Microeconomics|7
Bachelor's in Economics|mandatory|1119|S2|Microeconomics|7
Bachelor's in Economics|mandatory|1120|S1|Macroeconomics|7
Bachelor's in Economics|mandatory|1120|S2|Macroeconomics|7
Bachelor's in Economics|mandatory|1121|S1|Seminar in European Economics|7
Bachelor's in Economics|mandatory|1121|S2|Seminar in European Economics|7
Bachelor's in Economics|mandatory|1124|T1|Economic History|3.5
Bachelor's in Economics|mandatory|1124|T3|Economic History|3.5
Bachelor's in Economics|mandatory|1125|S1|Advanced Microeconomics|7
Bachelor's in Economics|mandatory|1125|S2|Advanced Microeconomics|7
Bachelor's in Economics|mandatory|1217|S1|Financial Accounting|7
Bachelor's in Economics|mandatory|1217|S2|Financial Accounting|7
Bachelor's in Economics|mandatory|1219|S1|Finance|7
Bachelor's in Economics|mandatory|1219|S2|Finance|7
Bachelor's in Economics|mandatory|1309|S1|Calculus I|7
Bachelor's in Economics|mandatory|1309|S2|Calculus I|7
Bachelor's in Economics|mandatory|1310|S1|Calculus II|7
Bachelor's in Economics|mandatory|1310|S2|Calculus II|7
Bachelor's in Economics|mandatory|1311|S1|Linear Algebra with Programming|7
Bachelor's in Economics|mandatory|1311|S2|Linear Algebra with Programming|7
Bachelor's in Economics|mandatory|1312|S1|Data Analysis and Probability|7
Bachelor's in Economics|mandatory|1312|S2|Data Analysis and Probability|7
Bachelor's in Economics|mandatory|1313|S1|Statistics for Economics and Management|7
Bachelor's in Economics|mandatory|1313|S2|Statistics for Economics and Management|7
Bachelor's in Economics|mandatory|1314|S1|Econometrics|7
Bachelor's in Economics|mandatory|1314|S2|Econometrics|7
Bachelor's in Economics|mandatory|1317|S1|Data Handling|3.5
Bachelor's in Economics|mandatory|1317|S2|Data Handling|3.5
Bachelor's in Economics|mandatory|1318|S1|Computer Programming|7
Bachelor's in Economics|mandatory|1318|S2|Computer Programming|7
Bachelor's in Economics|mandatory|1462|S1|Communication and Leadership|4
Bachelor's in Economics|mandatory|1462|S2|Communication and Leadership|4
Bachelor's in Economics|mandatory|1463|T1|Ethics|3.5
Bachelor's in Economics|mandatory|1463|T2|Ethics|3.5
Bachelor's in Economics|mandatory|1463|T3|Ethics|3.5
Bachelor's in Economics|mandatory|1463|T4|Ethics|3.5
Bachelor's in Economics|mandatory|1465|T1|Introduction to Modern and Contemporary History|3.5
Bachelor's in Economics|mandatory|1465|T2|Introduction to Modern and Contemporary History|3.5
Bachelor's in Economics|mandatory|1465|T3|Introduction to Modern and Contemporary History|3.5
Bachelor's in Economics|mandatory|1465|T4|Introduction to Modern and Contemporary History|3.5
Bachelor's in Economics|mandatory|1466|S1|Managing Impactful Projects|4
Bachelor's in Economics|mandatory|1466|S2|Managing Impactful Projects|4
Bachelor's in Economics|mandatory|1469|T1|Human Behavior and Decision Making|3.5
Bachelor's in Economics|mandatory|1469|T2|Human Behavior and Decision Making|3.5
Bachelor's in Economics|mandatory|1469|T3|Human Behavior and Decision Making|3.5
Bachelor's in Economics|mandatory|1469|T4|Human Behavior and Decision Making|3.5
Bachelor's in Economics|mandatory|1471|S1|Careers with Impact|4
Bachelor's in Economics|mandatory|1471|S2|Careers with Impact|4
Bachelor's in Economics|bachelor_economics_elective|1123|S1|Development Economics|7
Bachelor's in Economics|bachelor_economics_elective|1126|S1|Industrial Organization|7
Bachelor's in Economics|bachelor_economics_elective|1126|S2|Industrial Organization|7
Bachelor's in Economics|bachelor_economics_elective|1129|S1|Public Economics|7
Bachelor's in Economics|bachelor_economics_elective|1129|S2|Public Economics|7
Bachelor's in Economics|bachelor_economics_elective|1130|T1|Behavioral Economics|3.5
Bachelor's in Economics|bachelor_economics_elective|1130|T3|Behavioral Economics|3.5
Bachelor's in Economics|bachelor_economics_elective|1131|T3|Environment and Natural Resources Economics|3.5
Bachelor's in Economics|bachelor_economics_elective|1132|T3|History of Economic Thought|3.5
Bachelor's in Economics|bachelor_economics_elective|1133|S1|International Macroeconomics|7
Bachelor's in Economics|bachelor_economics_elective|1133|S2|International Macroeconomics|7
Bachelor's in Economics|bachelor_economics_elective|1134|S1|International Trade|7
Bachelor's in Economics|bachelor_economics_elective|1134|S2|International Trade|7
Bachelor's in Economics|bachelor_economics_elective|1135|S1|Research in Economics - Project|7
Bachelor's in Economics|bachelor_economics_elective|1135|S2|Research in Economics - Project|7
Bachelor's in Economics|bachelor_economics_elective|1136|T3|Economic History of Portuguese Speaking Countries|3
Bachelor's in Economics|bachelor_economics_elective|1137|T3|Macroeconomic Policies|3.5
Bachelor's in Economics|bachelor_economics_elective|1231|S2|Topics in Finance|7
Bachelor's in Economics|bachelor_economics_elective|1233|S2|Financial Markets|3.5
Bachelor's in Economics|general_elective|1216|S2|Principles of Management|7
Bachelor's in Economics|general_elective|1218|S1|Management Accounting|7
Bachelor's in Economics|general_elective|1218|S2|Management Accounting|7
Bachelor's in Economics|general_elective|1220|S1|Marketing|7
Bachelor's in Economics|general_elective|1220|S2|Marketing|7
Bachelor's in Economics|general_elective|1221|S1|Operations Management|7
Bachelor's in Economics|general_elective|1221|S2|Operations Management|7
Bachelor's in Economics|general_elective|1222|S1|Organizational Behavior|7
Bachelor's in Economics|general_elective|1222|S2|Organizational Behavior|7
Bachelor's in Economics|general_elective|1223|S1|Strategy|7
Bachelor's in Economics|general_elective|1223|S2|Strategy|7
Bachelor's in Economics|general_elective|1224|S1|Information Systems|7
Bachelor's in Economics|general_elective|1224|S2|Information Systems|7
Bachelor's in Economics|general_elective|1226|S1|Entrepreneurship|7
Bachelor's in Economics|general_elective|1226|S2|Entrepreneurship|7
Bachelor's in Economics|general_elective|1227|S1|International Management|7
Bachelor's in Economics|general_elective|1227|S2|International Management|7
Bachelor's in Economics|general_elective|1228|S1|Global Business Environment|7
Bachelor's in Economics|general_elective|1228|S2|Global Business Environment|7
Bachelor's in Economics|general_elective|1229|S1|Business Seminar|7
Bachelor's in Economics|general_elective|1229|S2|Business Seminar|7
Bachelor's in Economics|general_elective|1232|A|Cultural Diversity Management|3
Bachelor's in Economics|general_elective|1319|S1|Multivariate Statistics|7
Bachelor's in Economics|general_elective|1319|S2|Multivariate Statistics|7
Bachelor's in Economics|general_elective|1464|T1|Law in Economics and Business|3.5
Bachelor's in Economics|general_elective|1464|T2|Law in Economics and Business|3.5
Bachelor's in Economics|general_elective|1464|T4|Law in Economics and Business|3.5
Bachelor's in Economics|general_elective|1467|S1|European Law|7
Bachelor's in Economics|general_elective|1467|S2|European Law|7
Bachelor's in Economics|general_elective|1472|T1|Business Law|3.5
Bachelor's in Economics|general_elective|1472|T3|Business Law|3.5
Bachelor's in Economics|general_elective|1473|S1|Long-term Internship|7
Bachelor's in Economics|general_elective|1473|S2|Long-term Internship|7
Bachelor's in Economics|general_elective|1492|S1|Short-term Internship|3.5
Bachelor's in Economics|general_elective|1492|S2|Short-term Internship|3.5
Bachelor's in Management|mandatory|1117|S1|Principles of Microeconomics|7
Bachelor's in Management|mandatory|1118|S2|Principles of Macroeconomics|7
Bachelor's in Management|mandatory|1217|S1|Financial Accounting|7
Bachelor's in Management|mandatory|1216|T4|Business Principles|3.5
Bachelor's in Management|mandatory|1218|S1|Management Accounting|7
Bachelor's in Management|mandatory|1219|S1|Finance|7
Bachelor's in Management|mandatory|1220|S2|Marketing|7
Bachelor's in Management|mandatory|1221|S1|Operations Management|7
Bachelor's in Management|mandatory|1222|S2|Organizational Behavior|7
Bachelor's in Management|mandatory|1223|S1|Strategy|7
Bachelor's in Management|mandatory|1309|S1|Calculus I|7
Bachelor's in Management|mandatory|1310|S2|Calculus II|7
Bachelor's in Management|mandatory|1311|S1|Linear Algebra with Programming|7
Bachelor's in Management|mandatory|1312|S2|Data Analysis and Probability|7
Bachelor's in Management|mandatory|1313|S2|Statistics for Economics and Management|7
Bachelor's in Management|mandatory|1317|S1|Data Handling|3.5
Bachelor's in Management|mandatory|1317|S2|Data Handling|3.5
Bachelor's in Management|mandatory|1318|S2|Computer Programming|7
Bachelor's in Management|mandatory|1462|S1|Communication and Leadership|4
Bachelor's in Management|mandatory|1463|T3|Ethics|3.5
Bachelor's in Management|mandatory|1464|T1|Law in Economics and Business|3.5
Bachelor's in Management|mandatory|1469|T3|Human Behavior and Decision Making|3.5
Bachelor's in Management|mandatory|1471|S1|Careers with Impact|4
Bachelor's in Management|mandatory|1471|S2|Careers with Impact|4
Bachelor's in Management|bachelor_management_elective|1224|S1|Information Systems|7
Bachelor's in Management|bachelor_management_elective|1224|S2|Information Systems|7
Bachelor's in Management|bachelor_management_elective|1225|S1|Business History|7
Bachelor's in Management|bachelor_management_elective|1226|S1|Entrepreneurship|7
Bachelor's in Management|bachelor_management_elective|1226|S2|Entrepreneurship|7
Bachelor's in Management|bachelor_management_elective|1227|S1|International Management|7
Bachelor's in Management|bachelor_management_elective|1227|S2|International Management|7
Bachelor's in Management|bachelor_management_elective|1228|S1|Global Business Environment|7
Bachelor's in Management|bachelor_management_elective|1228|S2|Global Business Environment|7
Bachelor's in Management|bachelor_management_elective|1229|S1|Business Seminar|7
Bachelor's in Management|bachelor_management_elective|1229|S2|Business Seminar|7
Bachelor's in Management|bachelor_management_elective|1315|S1|Modeling and Optimization|7
Bachelor's in Management|bachelor_management_elective|1473|S1|Long-term Internship|7
Bachelor's in Management|bachelor_management_elective|1473|S2|Long-term Internship|7
Bachelor's in Management|bachelor_management_elective|1492|S1|Short-term Internship|3.5
Bachelor's in Management|bachelor_management_elective|1492|S2|Short-term Internship|3.5
Bachelor's in Management|general_elective|1121|S1|Seminar in European Economics|7
Bachelor's in Management|general_elective|1123|S1|Development Economics|7
Bachelor's in Management|general_elective|1125|S1|Advanced Microeconomics|7
Bachelor's in Management|general_elective|1125|S2|Advanced Microeconomics|7
Bachelor's in Management|general_elective|1126|S1|Industrial Organization|7
Bachelor's in Management|general_elective|1126|S2|Industrial Organization|7
Bachelor's in Management|general_elective|1129|S1|Public Economics|7
Bachelor's in Management|general_elective|1129|S2|Public Economics|7
Bachelor's in Management|general_elective|1130|T1|Behavioral Economics|3.5
Bachelor's in Management|general_elective|1130|T3|Behavioral Economics|3.5
Bachelor's in Management|general_elective|1131|T3|Environment and Natural Resources Economics|3.5
Bachelor's in Management|general_elective|1132|T3|History of Economic Thought|3.5
Bachelor's in Management|general_elective|1133|S1|International Macroeconomics|7
Bachelor's in Management|general_elective|1133|S2|International Macroeconomics|7
Bachelor's in Management|general_elective|1134|S1|International Trade|7
Bachelor's in Management|general_elective|1134|S2|International Trade|7
Bachelor's in Management|general_elective|1314|S1|Econometrics|7
Bachelor's in Management|general_elective|1314|S2|Econometrics|7
Bachelor's in Management|general_elective|1319|S1|Multivariate Statistics|7
Bachelor's in Management|general_elective|1319|S2|Multivariate Statistics|7
Bachelor's in Management|general_elective|1467|S1|European Law|7
Bachelor's in Management|general_elective|1467|S2|European Law|7
Bachelor's in Management|general_elective|1472|T1|Business Law|3.5
Bachelor's in Management|general_elective|1472|T3|Business Law|3.5
Bachelor's in Ocean Studies|mandatory|1700|T1|Biology Fundamentals|7
Bachelor's in Ocean Studies|mandatory|1701|S1|Principles of Oceanography|7
Bachelor's in Ocean Studies|mandatory|1702|T4|Fundamentals of Geology|7
Bachelor's in Ocean Studies|mandatory|1703|S2|Marine Ecosystems and Sustainable Development|7
Bachelor's in Ocean Studies|mandatory|1708|T3|Interdisciplinary Ocean Challenges|7
Bachelor's in Ocean Studies|mandatory|1709|T4|Ocean Challenges of Coastal Cities|7
Bachelor's in Ocean Studies|mandatory|1117|S1|Principles of Microeconomics|7
Bachelor's in Ocean Studies|mandatory|1131|T1|Environment and Natural Resources Economics|7
Bachelor's in Ocean Studies|mandatory|1312|S1|Data Analysis and Probability|7
Bachelor's in Ocean Studies|mandatory|1313|S1|Statistics for Economics and Management|7
Bachelor's in Ocean Studies|mandatory|1494|S1|Introduction to Law|7
Bachelor's in Ocean Studies|mandatory|1495|S2|International Law of the Sea|7
Bachelor's in Ocean Studies|mandatory|1496|T3|Geopolitics and International Relations|7
Bachelor's in Ocean Studies|mandatory|1497|T3|Oceans and History|7
Bachelor's in Ocean Studies|mandatory|1498|T4|Ocean Policies, Sustainability and Governance|7
Bachelor's in Ocean Studies|mandatory|500001|T1|Aquaculture and Fisheries Economics|7
Bachelor's in Ocean Studies|mandatory|500002|T3|Blue Infrastructures Planning and Nature-based Solutions|7
Bachelor's in Ocean Studies|mandatory|500003|S1|Climate Change and Ocean|7
Bachelor's in Ocean Studies|mandatory|500004|S1|Data Analysis, AI and Integrated Systems|7
Bachelor's in Ocean Studies|mandatory|500005|S2|Field LAB|7
Bachelor's in Ocean Studies|mandatory|500006|S1|Geographical Information Systems|7
Bachelor's in Ocean Studies|mandatory|500007|S2|Law and Sustainability|7
Bachelor's in Ocean Studies|mandatory|500008|T3|Living-Resources Protection and Restoration|7
Bachelor's in Ocean Studies|mandatory|500009|S1|Marine and Maritime Spatial Planning and Management|7
Bachelor's in Ocean Studies|mandatory|500010|T3|Marine Litter and Waste Management|7
Bachelor's in Ocean Studies|mandatory|500011|S1|Marine Technologies and Innovation|7
Bachelor's in Ocean Studies|mandatory|500012|T4|Maritime Security and International Relations|7
Bachelor's in Ocean Studies|mandatory|500013|T4|Ocean and Arts|7
Bachelor's in Ocean Studies|mandatory|500014|T1|Ocean Energy|7
Bachelor's in Ocean Studies|mandatory|500015|S2|Ocean Seminar|7
Bachelor's in Ocean Studies|mandatory|500016|S2|Shipping and International Commercial and Maritime Law|7
Bachelor's in Ocean Studies|mandatory|500017|T4|The Ocean's Heritage|7
"""


def _read_subjects() -> tuple[dict, ...]:
    subjects = []
    seen = set()
    for line in _RAW_SUBJECTS.strip().splitlines():
        parts = line.split("|")
        if len(parts) == 5:
            program = MASTER_OF_FINANCE
            group, code, period, name, ects = parts
        else:
            program, group, code, period, name, ects = parts
        if code.upper() == "MODULES" or name.strip().lower() == "modules":
            continue
        ects_value = float(ects)
        if ects_value <= 0:
            continue
        key = (program, group, code, period, name)
        if key in seen:
            continue
        seen.add(key)
        subjects.append({
            "program": program,
            "group": group,
            "code": code,
            "period": period,
            "name": name,
            "ects": ects_value,
        })
    return tuple(subjects)


SUBJECTS = _read_subjects()

VIRTUAL_GROUP_SOURCES = {
    (MASTER_OF_MANAGEMENT, "management_elective"): (
        MASTER_OF_FINANCE,
        "other_elective",
    ),
}


def groups_for(program: str) -> tuple[str, ...]:
    return PROGRAM_GROUPS.get(program, PROGRAM_GROUPS[MASTER_OF_FINANCE])


def group_label(program: str, group: str) -> str:
    labels = GROUP_LABELS.get(program, GROUP_LABELS[MASTER_OF_FINANCE])
    return labels.get(group, group.replace("_", " ").title())


def subjects_for(program: str, groups: list[str]) -> list[dict]:
    out = []
    for group in groups:
        source = VIRTUAL_GROUP_SOURCES.get((program, group))
        if source:
            source_program, source_group = source
            out.extend(
                {**subject, "program": program, "group": group}
                for subject in SUBJECTS
                if subject["program"] == source_program
                and subject["group"] == source_group
            )
        else:
            out.extend(
                subject for subject in SUBJECTS
                if subject["program"] == program and subject["group"] == group
            )
    return out


def subject_key(subject: dict) -> str:
    parts = (
        subject["program"],
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
