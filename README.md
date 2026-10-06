# Translation AI Workflow Demo

A small, API-key-free prototype of an AI-assisted translation-project intake workflow. It is designed as a portfolio example for a localization or translation-services company: it uses fictional projects and linguists only.

## What it demonstrates

- Project-intake validation and enrichment
- Transparent routing by language pair, specialty, capacity, and deadline
- A pluggable LLM interface with a deterministic offline implementation
- Generated project brief, QA checklist, and client acknowledgement
- Clear separation between workflow logic, data, and the AI provider

## Workflow

```text
Translation request (JSON)
        |
        v
Validate + classify domain/urgency
        |
        v
Find eligible linguists and rank candidates
        |
        v
Create project brief + QA checklist + client email
        |
        v
Structured workflow result (JSON)
```

## Quick start

Requires Python 3.10+ and no third-party packages.

```bash
python -m app.cli --request examples/technical_en_de.json
```

To save the workflow output:

```bash
python -m app.cli --request examples/marketing_en_hu.json --output result.json
```

## Example output

The command selects an eligible fictional linguist, produces a score explanation, and prints a project brief, QA checklist, and draft acknowledgement email. See `examples/` for sample requests.

## Claude integration point

The demo defaults to `OfflineLLM`, a deterministic provider so reviewers can run it immediately. `app/llm.py` defines the minimal provider contract. In a production setup, implement `ClaudeLLM` there and inject it into `WorkflowService`; keep credentials only in environment variables, never in source control.

```python
# Illustrative only — no API key is included in this repository.
# service = WorkflowService(llm=ClaudeLLM(api_key=os.environ["ANTHROPIC_API_KEY"]))
```

## Design notes

- **No proprietary material:** all people, requests, pricing signals, and rules are fictional.
- **Human-in-the-loop:** the output is a recommendation, not an automatic assignment.
- **Explainability:** the selected linguist includes an auditable score breakdown.
- **Safe fallback:** when no candidate qualifies, the workflow flags the request for manual coordination rather than inventing a match.

## Repository layout

```text
app/            Workflow code
examples/       Fictional input requests
tests/          Standard-library unit tests
```

## Run tests

```bash
python -m unittest discover -s tests -v
```

The repository intentionally contains no generated `__pycache__` files or credentials.

## Potential next steps

1. Swap `OfflineLLM` for an Anthropic Claude adapter.
2. Add a database-backed linguist directory and availability feed.
3. Add PII redaction before sending source material to an LLM.
4. Send reviewed email drafts to a TMS/CRM via an approval step.

## License

MIT
