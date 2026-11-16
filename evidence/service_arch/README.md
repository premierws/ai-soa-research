# Service Architecture Platform

Service Architecture Platform collects SOA facts from versioned repositories,
normalizes modules, service instances, RPC relationships, and deployment data,
then presents the result through an engineering-focused Module Board.

## Repository Layout

- `platform/backend/`: FastAPI APIs, parsers, normalization, graph projection,
  persistence, migrations, and backend tests.
- `platform/frontend/`: React Module Board, configuration workflow, advanced
  search, UI tests, and design mockups.
- `platform/docs/`: Architecture documents, product specifications, and
  implementation plans.
- `docs/project/`: Original platform-level design and implementation plan.
- `docs/assets/history/`: Selected early visualization artifacts retained for
  design history.

## Local Development

Backend:

```bash
cd platform/backend
python -m venv .venv
.venv/bin/pip install -e '.[dev]'
.venv/bin/python -m pytest -q
```

Frontend:

```bash
cd platform/frontend
npm ci
npm test -- --run
npm run build
```

See `platform/README.md` for API and workflow details.

## Runtime Inputs

Real Proto definitions, SOA deployment repositories, deployment tables,
repository checkouts, local databases, credentials, and environment files are
not stored in this repository. Configure repository locations and versions at
runtime. Tests use small synthetic fixtures under
`platform/backend/tests/fixtures/`.

## Security

Do not commit credentials, access tokens, private keys, local `.env` files, or
real internal input repositories. Repository URLs shown in tests and documents
must use non-routable example domains.
