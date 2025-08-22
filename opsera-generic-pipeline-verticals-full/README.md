# Opsera Generic DevOps Pipeline – Sample Microservices (Basic)

This repo is a **turnkey starter** to demo an end-to-end DevOps pipeline in Opsera and later generate MCP servers via CodeGlide.

It includes:
- 4 FastAPI microservices: **inventory, orders, billing, scheduling**
- Consistent **OpenAPI** specs (one per service)
- **Helm** charts for Kubernetes deploys
- **Terraform** skeleton for AWS (ECR stubs) – fill in variables and apply
- **GitHub Actions** CI (build, unit test, SBOM with Syft, Trivy scan)
- Basic **security** configs (Semgrep ruleset stub, ZAP baseline)
- **k6** smoke/API test and simple **pytest** unit tests
- `docker-compose.yml` for local dev

## Quickstart (local dev)
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r services/requirements.txt

# run one service (example: inventory on :8001)
uvicorn services.inventory.app:app --reload --port 8001
```

Send `X-API-Key: demo-key` with requests to auth the protected endpoints.

## Docker (local)
```bash
docker compose up --build
```

## Kubernetes (Helm)
```bash
# assumes a kubecontext is configured
helm upgrade --install inventory   helm/inventory   -n demo --create-namespace
helm upgrade --install orders      helm/orders      -n demo
helm upgrade --install billing     helm/billing     -n demo
helm upgrade --install scheduling  helm/scheduling  -n demo
```

## Terraform (AWS skeleton)
Edit `deploy/terraform/terraform.tfvars` and fill in values. Then:
```bash
cd deploy/terraform
terraform init
terraform plan
# terraform apply      # applies infra (use with caution)
```

## GitHub Actions CI
Workflow under `.github/workflows/ci.yml` builds, tests, generates an SBOM, and scans images (matrix for all services).
By default it **does not push** to a registry; pushing is typically handled by Opsera.


---

## Auth modes
This starter supports **two auth modes** (choose one per deploy):

- **API Key (default)**: send `X-API-Key: demo-key`
- **Bearer JWT**: set env `AUTH_MODE=jwt` and `DEMO_JWT_SECRET=<secret>` on services.
  - Generate a test token:
    ```bash
    python scripts/generate_jwt.py --secret demo-secret --sub demo-user --scopes "inventory:read orders:write scheduling:read scheduling:write billing:read"
    ```
  - Use header: `Authorization: Bearer <token>`

In JWT mode, simple scope checks are enforced per endpoint.

## Vertical demo data
Toggle vertical sample data via `VERTICAL` env var per service:
- `VERTICAL=healthcare` → Scheduling slots for doctors (Dr. Kim, Dr. Lee)
- `VERTICAL=retail` → Inventory with retail SKUs + low-stock filtering
- `VERTICAL=fintech` → Billing invoices with masked account hints
(Default fixtures remain if unset.)
