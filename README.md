# InvestBuddy 💬📈

InvestBuddy is a prototype **chat-based investment assistant**.  
It collects a user’s basic financial profile, pulls live market data, and uses an AI model to generate a simple, JSON-based investment suggestion that can be rendered as friendly chat responses.

This repository contains all backend, simple frontend, data access, and retrieval-augmented generation (RAG) logic needed to run the prototype locally.

---

## Key Capabilities

- Chat-style interaction (via `frontend.py` + `backend.py`)
- Collection of user inputs:
  - Income / salary
  - Monthly expenses
  - Savings and debts
  - Goals & time horizon
  - Investment budget
- Rule-based **investment-eligibility & allocation logic** (`investment_logic.py`)
- Integration with **live market data APIs** (`financial_api.py`, `live_etf_data.py`)
- Use of **OpenAI-style prompts** to:
  - Turn numeric allocations into natural language explanations
  - Produce JSON plans that the UI can render (`prompts.py`)
- Basic **ETF knowledge base + RAG**:
  - Vector store for ETFs (`vector_store.py`, `etf_embeddings.pkl`)
  - Human-readable ETF metadata (`etf_knowledge.py`)
- Lightweight storage using a local database (`investbuddy.db`, `database.py`)
- Scripts to quickly start backend and frontend (`start_backend.sh`, `start_frontend.sh`)

---

## Tech Stack

- **Language:** Python 3
- **APIs:**
  - OpenAI-compatible chat API (for plan & explanation generation)
  - Market data API(s) such as Finnhub / Alpha Vantage / Yahoo Finance (via `financial_api.py`)
- **Data & Storage:**
  - Local database file `investbuddy.db`
  - Local ETF embeddings `etf_embeddings.pkl` and retrieval helpers
- **Shell scripts:** Bash helpers for running the app
- **Dependencies:** Listed in `requirements.txt`

---

## Repository Structure

| File / Folder                  | Description                                                                 |
|-------------------------------|-----------------------------------------------------------------------------|
| `.gitignore`                  | Git ignore rules for Python, venv, DB files, etc.                          |
| `requirements.txt`            | Python dependencies for backend, frontend, and RAG components.             |
| `backend.py`                  | Core backend server / business logic orchestration.                        |
| `frontend.py`                 | Simple web/chat frontend that talks to the backend API.                    |
| `investment_logic.py`         | Functions to compute safe investable amounts and portfolio allocations.    |
| `financial_api.py`            | Wrapper for external market data APIs (e.g., Finnhub/Yahoo/Alpha Vantage). |
| `live_etf_data.py`            | Helpers for fetching and normalizing live ETF data.                        |
| `investment_platforms.py`     | Additional logic for scenario-style analysis (e.g., business cases).       |
| `prompts.py`                  | Prompt templates and helpers for the AI model (JSON plans, explanations).  |
| `database.py`                 | Simple database access layer (`investbuddy.db`).                           |
| `investbuddy.db`              | Local database file used by the prototype.                                 |
| `etf_knowledge.py`            | Static ETF metadata and utility functions for ETF descriptions.            |
| `etf_embeddings.pkl`          | Precomputed embeddings for ETF descriptions (used in RAG).                 |
| `vector_store.py`             | Minimal vector store / retrieval logic for ETF embeddings.                 |
| `BEGINNER_FRIENDLY_UPDATE.md` | Notes on making the UX more beginner-friendly.                             |
| `LIVE_DATA_UPDATE.md`         | Notes on behavior when live data sources are integrated.                   |
| `QUICK_TEST.md`               | Quick sanity test instructions for the main flow.                          |
| `RAG_IMPLEMENTATION.md`       | Design notes for the ETF RAG layer.                                        |
| `start_backend.sh`            | Convenience script to run the backend service.                             |
| `start_frontend.sh`           | Convenience script to run the frontend UI.                                 |

---

## High-Level Architecture

### 1. Frontend (`frontend.py`)

- Exposes a lightweight web/chat interface.
- Sends user messages and profile data to the backend over HTTP.
- Displays AI responses and structured investment plans.

### 2. Backend (`backend.py`)

- Receives requests from the frontend.
- Coordinates:
  - User profile parsing
  - Eligibility & allocation logic (`investment_logic.py`)
  - Market data fetches (`financial_api.py`, `live_etf_data.py`)
  - RAG lookups for ETF descriptions (`vector_store.py`, `etf_knowledge.py`)
  - Prompt construction and calls to the AI model (`prompts.py`)
- Returns structured responses (e.g., JSON with allocations + explanations) to the frontend.

### 3. Investment Logic (`investment_logic.py`)

- Implements simple rules such as:
  - How much of income/savings can be safely allocated.
  - Basic segmentation by time horizon (short / medium / long).
- Produces percentage allocations and target tickers that later get priced via the market-data layer.

### 4. Market Data Layer (`financial_api.py`, `live_etf_data.py`)

- Talks to external market data APIs using configured API keys.
- Fetches:
  - Current stock/ETF prices
  - Potentially additional metadata depending on the provider.
- Used to show approximate quantities (e.g. how many ETF units can be bought).

### 5. RAG / Knowledge Layer (`etf_knowledge.py`, `vector_store.py`, `etf_embeddings.pkl`)

- Stores ETF-related text descriptions and embeddings.
- Retrieves the most relevant ETF descriptions based on user context / selected tickers.
- Supplies this information into prompts so the AI model can give more concrete, human-readable explanations.

### 6. Persistence (`database.py`, `investbuddy.db`)

- Basic storage for sessions, user inputs, or logs (depending on configuration).
- Currently implemented as a local DB file for easy demo and prototyping.

---

## 🔐 Repository History & Security Note

This repository is a **second, clean version** of the InvestBuddy project.

As a team, we initially created a different GitHub repository where we accidentally pushed an `.env` file with a private API key to a public repo. As soon as we noticed this, we:

1. **Revoked and rotated** the exposed key  
2. **Stopped using** the original repository  
3. **Migrated the project** into this new, clean repository **without any sensitive data**

Because of this, the **number of commits in this repo is lower** than the total work we actually did. The shorter history is the result of a **security-first reset**, not because the project is small or recently started.

We now keep all secrets and API keys out of Git (via environment variables and ignored `.env` files) and treat this as a concrete example of improving our security practices as a team.


## Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/smehraliyev404/InvestBuddy.git
cd InvestBuddy
