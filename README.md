# ReqCheck

A web-based tool for analysing and improving the quality of software requirement descriptions.

ReqCheck helps software engineers identify issues in requirement wording such as ambiguity, vague language, and poor structure. The system analyses written requirements using deterministic rule-based logic — grounded in ISO/IEC/IEEE 29148:2018 — and optionally generates AI-powered improvement suggestions via a local LLM (Ollama + Mistral).

---

## Demo

Example workflow:

1. User enters a requirement description.
2. User selects requirement type and MoSCoW priority.
3. Optionally enable AI suggestions.
4. ReqCheck analyses the requirement and returns structured feedback.

Example requirement:

```
The system should respond quickly to user requests.
```

Example findings:

```
[AMB001] Vague terms detected: "quickly". Replace with precise, measurable language.
[AMB002] Weak modal verb(s) detected: "should". Use 'shall' for mandatory requirements.
[TEST001] Requirement lacks measurable criteria.
```

---

## Features

### Requirement Analysis

ReqCheck analyses requirement descriptions using rule-based checks derived from ISO/IEC/IEEE 29148:2018.

| Rule ID  | Category       | Description                                                                 | Severity |
|----------|----------------|-----------------------------------------------------------------------------|----------|
| AMB001   | Ambiguity      | Vague terms detected (e.g. "fast", "simple", "user-friendly")               | Medium   |
| AMB002   | Ambiguity      | Weak modal verbs detected (e.g. "may", "might", "can", "could")             | High     |
| AMB003   | Ambiguity      | Open-ended quantifiers detected (e.g. "etc", "some", "various")             | Medium   |
| AMB004   | Ambiguity      | Comparative terms detected (e.g. "better", "improved", "faster")            | Medium   |
| COMP001  | Completeness   | Deferred or placeholder language present (e.g. TBD, TBS, "as needed")       | High     |
| STR001   | Structure      | Requirement does not use "shall"                                             | Low      |
| TEST001  | Testability    | No measurable criteria present (numeric value, unit, or percentage)          | Low      |
| SING001  | Singularity    | Requirement may express multiple behaviours and should be split              | Medium   |
| MOSC001  | MoSCoW         | Won't-Have requirement incorrectly uses "shall"                              | Medium   |
| MOSC002  | MoSCoW         | Must-Have requirement uses a weak modal instead of "shall"                  | High     |
| TYPE001  | Type           | Non-functional requirement lacks a recognised quality attribute keyword      | Medium   |
| TYPE002  | Type           | Constraint requirement lacks a specific standard, regulation, or bound       | Medium   |
| TYPE003  | Type           | Functional requirement uses a state verb after "shall" instead of an action | Low      |

---

### Requirement Classification

Users specify requirement attributes when submitting a requirement.

**Type**
- Functional
- Non-functional
- Constraint

**Priority (MoSCoW)**
- Must
- Should
- Could
- Won't

These values influence which rules are applied and how scoring penalties are weighted.

---

### Quality Scoring

ReqCheck produces two scores (0–100) for each requirement:

- **Clarity score** — penalised by the severity of each finding. High severity findings deduct 20 points, medium 10, and low 5. Penalties are scaled by a priority multiplier (Must = 1.0, Should = 0.85, Could = 0.70, Won't = 0.55).
- **Testability score** — penalised for missing "shall", missing measurable criteria (TEST001), compound obligations (SING001), and ambiguity findings (AMB001, AMB003, AMB004).

---

### AI Suggestions (RAG Pipeline)

When enabled, ReqCheck sends the requirement and its findings to a locally running Ollama instance (Mistral model). The pipeline retrieves relevant ISO 29148 guidance from a built-in knowledge base and constructs a prompt that asks the model to produce a single improved requirement. The rewritten requirement is returned as a suggestion.

See [AI Setup](#ai-setup-ollama) for installation instructions.

---

### Requirement History

The frontend stores up to 20 analysed requirements in browser local storage. A use-case diagram is generated from the history, extracting actors and actions from requirement text and rendering them as an SVG diagram in the interface.

---

### SRS Export

Requirements can be exported in a simplified Software Requirements Specification format, including:

- requirement description
- classification and priority
- analysis findings
- quality scores

---

## Architecture

```
User
 │
 ▼
React Frontend (Vite + TypeScript)
 │
 ▼
FastAPI Backend
 │
 ├── Rule-Based Analysis Engine
 │
 └── RAG Pipeline (optional)
      │
      └── Ollama (Mistral) — runs locally
```

---

## Technology Stack

**Frontend**
- React
- Vite
- TypeScript
- Bootstrap

**Backend**
- Python
- FastAPI
- Uvicorn

**Analysis Engine**
- Custom rule-based engine (ISO/IEC/IEEE 29148:2018)

**AI (optional)**
- Ollama
- Mistral

---

## Repository Structure

```
ReqCheck
├── backend
│   ├── app
│   │   ├── api
│   │   │   ├── analysis.py
│   │   │   └── __init__.py
│   │   ├── models
│   │   │   ├── schemas.py
│   │   │   └── __init__.py
│   │   ├── preprocessing
│   │   │   ├── preprocessor.py
│   │   │   └── __init__.py
│   │   ├── rag
│   │   │   ├── data
│   │   │   │   └── guidelines.json
│   │   │   ├── generator.py
│   │   │   ├── pipeline.py
│   │   │   └── query.py
│   │   ├── rules
│   │   │   ├── dictionaries
│   │   │   │   └── ambiguity_terms.json
│   │   │   ├── ambiguity_rules.py
│   │   │   ├── base_rule.py
│   │   │   ├── completeness_rules.py
│   │   │   ├── moscow_rules.py
│   │   │   ├── singularity_rules.py
│   │   │   ├── structure_rules.py
│   │   │   ├── testability_rules.py
│   │   │   ├── type_rules.py
│   │   │   └── __init__.py
│   │   ├── services
│   │   │   ├── analysis_engine.py
│   │   │   └── __init__.py
│   │   └── main.py
│   ├── tests
│   │   ├── test_analysis_engine.py
│   │   └── test_rules.py
│   ├── pytest.ini
│   └── requirements.txt
├── frontend
│   ├── public
│   │   └── vite.svg
│   ├── src
│   │   ├── api
│   │   │   └── reqcheck.ts
│   │   ├── components
│   │   │   ├── ExportButton.tsx
│   │   │   ├── FindingsList.tsx
│   │   │   ├── RequirementInput.tsx
│   │   │   ├── ScoreDisplay.tsx
│   │   │   ├── SuggestionsList.tsx
│   │   │   └── UseCaseDiagram.tsx
│   │   ├── hooks
│   │   │   └── useRequirementHistory.ts
│   │   ├── types
│   │   │   └── analysis.ts
│   │   ├── App.tsx
│   │   ├── index.css
│   │   └── main.tsx
│   ├── eslint.config.js
│   ├── index.html
│   ├── package-lock.json
│   ├── package.json
│   ├── tsconfig.app.json
│   ├── tsconfig.json
│   ├── tsconfig.node.json
│   ├── vercel.json
│   └── vite.config.ts
├── .gitignore
└── README.md
```

---

## Local Development

### 1. Clone the repository

```bash
git clone https://github.com/krone404/reqcheck.git
cd reqcheck
```

---

### Backend Setup

Navigate to the backend directory.

```bash
cd backend
```

Create a virtual environment.

```bash
python -m venv venv
```

Activate the environment.

**Mac/Linux**
```bash
source venv/bin/activate
```

**Windows**
```bash
venv\Scripts\activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

Start the backend server.

```bash
uvicorn app.main:app --reload
```

The backend runs at:

```
http://localhost:8000
```

Environment variables (optional):

| Variable          | Default                     | Description                              |
|-------------------|-----------------------------|------------------------------------------|
| `ALLOWED_ORIGINS` | `http://localhost:5173`     | Comma-separated list of allowed CORS origins |

---

### Frontend Setup

Navigate to the frontend directory.

```bash
cd frontend
```

Install dependencies.

```bash
npm install
```

Start the development server.

```bash
npm run dev
```

The frontend runs at:

```
http://localhost:5173
```

---

### AI Setup (Ollama)

AI suggestions are powered by a locally running Ollama instance. This feature is **optional** — the rule-based analysis works without it.

**1. Install Ollama**

Download and install Ollama from [https://ollama.com](https://ollama.com).

**2. Pull the Mistral model**

```bash
ollama pull mistral
```

**3. Start Ollama**

Ollama typically starts automatically after installation. To start it manually:

```bash
ollama serve
```

**4. Verify it is running**

```bash
ollama run mistral "Hello"
```

Once Ollama is running with the Mistral model available, toggle **AI Suggestions** in the ReqCheck interface to enable the RAG pipeline. If Ollama is not running, the analysis will still complete — the suggestions field will be empty and a `rag_error` message will be returned indicating the model is unavailable.

---

### Running Tests

From the `backend` directory with the virtual environment active:

```bash
pytest
```

---

## API Reference

### Health Check

```
GET /health
```

Response:

```json
{ "status": "ok" }
```

---

### Analyse Requirement

```
POST /api/analyse
```

Request body:

```json
{
  "text": "The system shall respond within 2 seconds.",
  "type": "functional",
  "priority": "must",
  "use_rag": false
}
```

| Field      | Type    | Values                                        | Default        |
|------------|---------|-----------------------------------------------|----------------|
| `text`     | string  | 1–1000 characters, non-blank                  | required       |
| `type`     | string  | `functional`, `non_functional`, `constraint`  | `functional`   |
| `priority` | string  | `must`, `should`, `could`, `wont`             | `must`         |
| `use_rag`  | boolean | `true` / `false`                              | `false`        |

Response:

```json
{
  "findings": [
    {
      "rule_id": "TEST001",
      "message": "Requirement lacks measurable criteria.",
      "severity": "low"
    }
  ],
  "clarity_score": 95.0,
  "testability_score": 85.0,
  "suggestions": [],
  "rag_error": null
}
```

`rag_error` is `null` on success or when `use_rag` is `false`. When the AI pipeline fails (e.g. Ollama is not running), it contains a human-readable error string and the rest of the response is still returned normally.

---

## Evaluation

The system will be evaluated using a mixed-methods approach including:

- requirement writing tasks
- before-and-after requirement comparison
- usability questionnaires
- participant feedback

Usability will be measured using the **System Usability Scale (SUS)**.

Participants will primarily be software engineering students and developers.

---

## Author

Cameron Cartwright  
BSc (Hons) Software Engineering  
Bournemouth University

Supervisor: Botao Fan

---

## Licence

Academic project — Bournemouth University.
