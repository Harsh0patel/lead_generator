# Lead Generation Agent

## High‑Level Architecture

```
User Inputs (Streamlit)
        │
        ▼
Stage 1: Identification
        │
        ▼
Stage 2: Enrichment
        │
        ▼
Stage 3: Scoring
        │
        ▼
Ranked Leads (CSV / UI Table)
```

Each stage is isolated as a service to keep logic clean and testable.

---

## Pipeline Stages

### Stage 1 – Identification

**Purpose:** Identify relevant leads based on user‑defined filters.

**Inputs:**

* Name (optional)
* Title keywords (optional)
* Company (optional)

**Responsibilities:**

* Query source data (CSV)
* Apply text‑based filtering
* Return a structured DataFrame of candidate leads

**Output:**

* DataFrame of identified leads

---

### Stage 2 – Enrichment

**Purpose:** Find more details about lead, here in demo i use csv for demo purpose

but can change into api search or database search.

**Responsibilities:**

* Prepare data for scoring

**Output:**

* Enriched DataFrame

---

### Stage 3 – Scoring

**Purpose:** Assign a probability score to each lead indicating relevance and priority.

**Sample Scoring Logic:**

* Funding stage (Seed, Series A, Series B, etc.)
* Geographic location
* Presence in biotech hubs
* Recent publications and research focus

- Funding stage relevance
- Strategic location (Boston, Bay Area, Basel, UK Golden Triangle)
- Recent publications in target domains (e.g., Drug‑Induced Liver Injury)

**Output:**

* Final DataFrame with `probability_score`

---

## Tech Stack

* **Python 3.10+**
* **Streamlit** – UI
* **Pandas** – Data processing
* **Modular service design** (services/ directory)

---

## Project Structure

```
project_root/
│
├── app.py                     # Streamlit entry point
├── services/
│   ├── identification.py      # Stage 1 logic
│   ├── enrichment.py          # Stage 2 logic
│   └── scoring.py             # Stage 3 logic
│
├── data/
│   └── leads.csv              # Input / intermediate data
│
├── requirements.txt
└── README.md
```

---

## Installation

1. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Application

```bash
streamlit run app.py
```

Then open the provided local URL in your browser.

---

## Usage Instructions

1. Enter optional filters in the sidebar:

   * Title keywords
   * Company name
   * Person name
2. Click **Run Lead Generation**
3. The pipeline executes sequentially:

   * Identification → Enrichment → Scoring
4. Review ranked leads in the main UI

## Future Improvements

* Replace rule‑based scoring with ML ranking
* Add evaluation metrics and logging (LangSmith‑style)

NOTE: Some of the feture like search is not working since i don't work with streamlit very much so i search for it in LLM's but they are bad one's so i don't change it but beside that all are work very well thank you.