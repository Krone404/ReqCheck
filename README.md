# ReqCheck

A web-based tool for analysing and improving the quality of software requirement descriptions.

ReqCheck helps software engineers identify issues in requirement wording such as ambiguity, vague language, and poor structure. The system analyses written requirements using deterministic rule-based logic and provides structured feedback to help improve clarity and testability.

---

# Demo

Example workflow:

1. User enters a requirement description.
2. User selects requirement type and priority.
3. ReqCheck analyses the requirement.
4. Feedback is returned highlighting potential issues.

Example requirement:

```
The system should respond quickly to user requests.
```

ReqCheck feedback:

```
Issue: ambiguous term detected
Term: "quickly"
Suggestion: define measurable performance criteria
```

---

# Features

### Requirement Analysis

ReqCheck analyses requirement descriptions using rule-based checks derived from requirements engineering best practices.

Checks include:

* ambiguity detection
* vague language detection
* requirement testability
* structural clarity

---

### Requirement Classification

Users specify requirement attributes when submitting a requirement.

Type

* Functional
* Non-functional
* Constraint

Priority (MoSCoW)

* Must
* Should
* Could
* Won’t

These values influence the analysis rules applied.

---

### Quality Feedback

ReqCheck generates feedback including:

* detected issues
* improvement suggestions
* requirement quality indicators
* requirement clarity score

---

### SRS Export

Requirements can be exported into a simplified **Software Requirements Specification format**, including:

* requirement description
* classification
* priority
* analysis findings

---

# Architecture

ReqCheck uses a simple client-server architecture.

```
User
 │
 ▼
React Frontend
 │
 ▼
Python Backend API
 │
 ▼
Rule-Based Analysis Engine
```

Frontend handles user interaction.

Backend performs requirement analysis and returns feedback.

---

# Technology Stack

Frontend

* React
* Vite
* TypeScript
* Bootstrap

Backend

* Python
* FastAPI

Analysis Engine

* Custom rule-based requirement analysis

---

# Deployment

The system is deployed using separate frontend and backend services.

Frontend

Platform: **Vercel**

Role: hosts the React interface.

Backend

Platform: **Railway**

Role: hosts the Python API and rule engine.

Deployment architecture:

```
User
 │
 ▼
Vercel (React Frontend)
 │
 ▼
Railway (Python API)
 │
 ▼
Rule Engine
```

---

# Repository Structure

```
reqcheck
│
├── frontend
│   ├── src
│   │   ├── components
│   │   │   └── RequirementAnalyzer.tsx
│   │   │
│   │   ├── api
│   │   │   └── reqcheck.ts
│   │   │
│   │   ├── App.tsx
│   │   └── main.tsx
│   │
│   ├── package.json
│   └── vite.config.ts
│
├── backend
│   ├── app.py
│   │
│   ├── models
│   │   ├── request.py
│   │   └── result.py
│   │
│   ├── analysis
│   │   ├── ambiguity.py
│   │   ├── testability.py
│   │   ├── completeness.py
│   │   └── consistency.py
│   │
│   └── services
│       └── analyzer.py
│
└── README.md
```

---

# Local Development

## 1. Clone repository

```bash
git clone https://github.com/yourusername/reqcheck.git
cd reqcheck
```

---

# Backend Setup

Navigate to the backend directory.

```
cd backend
```

Create virtual environment.

```
python -m venv venv
```

Activate environment.

Mac/Linux

```
source venv/bin/activate
```

Windows

```
venv\Scripts\activate
```

Install dependencies.

```
pip install -r requirements.txt
```

Start backend server.

```
uvicorn app.main:app --reload
```

Backend runs at:

```
http://localhost:8000
```

---

# Frontend Setup

Navigate to frontend.

```
cd frontend
```

Install dependencies.

```
npm install
```

Start development server.

```
npm run dev
```

Frontend runs at:

```
http://localhost:5173
```

---

# API Example

Endpoint:

```
POST /api/analyse
```

Example request:

```json
{
  "text": "The system shall respond within 2 seconds.",
  "type": "functional",
  "priority": "must"
}
```

Example response:

```json
{
  "findings": [],
  "clarity_score": 100,
  "testability_score": 100
}
```

---

# Evaluation

The system will be evaluated using a mixed-methods approach including:

* requirement writing tasks
* before-and-after requirement comparison
* usability questionnaires
* participant feedback

Usability will be measured using the **System Usability Scale (SUS)**.

Participants will primarily be software engineering students and developers.

---

# Author

Cameron Cartwright
BSc (Hons) Software Engineering
Bournemouth University

Supervisor
Botao Fan

---

# Licence

Academic project – Bournemouth University.
