# Email-to-Action Assistant for Trade Queries

A Streamlit prototype that turns unstructured trade emails into a structured workflow:

1. **Classification** — shipment, invoice, or general trade query.
2. **Prioritisation** — high, medium, or low using transparent urgency rules.
3. **Identifier extraction** — shipment and invoice references.
4. **SQL retrieval** — fetch matching demo shipment/invoice records from SQLite.
5. **Response drafting** — generate a cautious contextual reply.
6. **Human approval** — reviewer edits and approves the draft before any external action.

> This repository is a portfolio/demo implementation. It does not send email. Approval is recorded only in the current Streamlit session.

## Features

- Streamlit user interface for pasting or selecting sample trade emails.
- Rule-based classification and priority assignment that work without an API key.
- Optional OpenAI API integration for response drafting.
- Regex-based extraction of references such as `SHP-1002` and `INV-2001`.
- Parameterised SQLite queries for shipment and invoice lookup.
- Human-in-the-loop review and approval.
- Unit tests for identifier extraction and classification.

## Architecture

```text
Incoming trade email
        |
        v
Classification + prioritisation
        |
        v
Shipment / invoice ID extraction
        |
        v
SQLite record retrieval
        |
        v
Context-aware response draft
        |
        v
Human review and approval
```

## Quick start

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/email-to-action-assistant.git
cd email-to-action-assistant
```

### 2. Create and activate a virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
streamlit run app.py
```

The app creates and seeds `data/trade_demo.db` automatically on first run.

## Optional: enable OpenAI response drafting

Copy `.env.example` to `.env` and add your API key:

```env
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4o-mini
```

Restart Streamlit and enable **Use OpenAI LLM** in the sidebar. The API is used for response drafting; classification and priority are still assigned by the local rule-based component.

Never commit `.env` or expose API keys in GitHub.

## Run tests

```bash
pytest -q
```

## Project structure

```text
email-to-action-assistant/
├── app.py
├── src/
│   ├── __init__.py
│   ├── database.py
│   └── pipeline.py
├── data/
│   └── sample_emails.csv
├── tests/
│   └── test_pipeline.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Database schema

### `shipments`

| Column | Description |
|---|---|
| shipment_id | Unique shipment reference |
| exporter | Exporting organisation |
| importer | Importing organisation |
| origin | Shipment origin |
| destination | Shipment destination |
| status | Current demo status |
| eta | Estimated arrival date |

### `invoices`

| Column | Description |
|---|---|
| invoice_id | Unique invoice reference |
| shipment_id | Related shipment |
| amount | Invoice amount |
| currency | Currency code |
| status | Invoice status |
| purchase_order | Purchase order reference |

The records are fictional demo data and should not be treated as real shipment or invoice information.

## Limitations and next steps

This is a prototype, not a production email agent. Suggested extensions:

- Replace rule-based classification with a trained classifier or LLM structured-output step.
- Add labelled evaluation data and report accuracy, precision, recall, F1-score and escalation rate.
- Add authentication, role-based approval and persistent audit logs.
- Add robust document/email parsing and attachment handling.
- Add integration tests and structured logging.
- Integrate an email provider only after adding explicit approval, access controls and safe-send safeguards.

## Responsible use

- Treat incoming email content as untrusted input.
- Verify retrieved business records before using them in customer communications.
- Require human review before sending any response.
- Do not use real customer, shipment, or invoice data in this demo repository.
