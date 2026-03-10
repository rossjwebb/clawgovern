# ClawGovern
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)

Zero-Trust Policy Enforcement and FinOps Engine for OpenClaw Agents.

## The Problem
OpenClaw agents are high-leverage automation, but unmanaged agents create immediate enterprise risk:

- FinOps risk: runaway token spend, unbounded daily budgets, and model drift.
- Security and compliance risk: unsafe tool execution without mandatory Human-in-the-Loop (HITL) controls.
- Release risk: policy violations discovered too late, after deployment pressure is already high.

If policy is not enforced before merge, your controls are optional.

## The Solution (ClawGovern)
ClawGovern is a CI/CD-native, offline, pure-Python policy engine that enforces hard controls before code reaches production.

- Zero-trust policy gate for OpenClaw agent configs.
- Deterministic pass/fail audits for budget, model allowlists, and HITL requirements.
- No database, no external service dependency, no heavyweight framework.
- Built for PR gating in GitHub Actions and GitLab CI.

## Quickstart
Run a full policy audit:

```bash
uv run clawgovern audit
```

If violations exist, the command fails the process with exit code `1`.

## CI/CD Integration
ClawGovern is designed to block non-compliant changes automatically.

- Returns `sys.exit(1)` when any agent fails policy checks.
- Returns `sys.exit(0)` only when all agents pass.
- This makes it a direct merge gate in CI pipelines.

Example GitHub Actions workflow: `.github/workflows/clawgovern.yml`

```yaml
name: ClawGovern Policy Gate

on:
  pull_request:
  push:
    branches: [main]

jobs:
  clawgovern-audit:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup uv
        uses: astral-sh/setup-uv@v4

      - name: Enforce OpenClaw policy
        run: uv run clawgovern audit --export-report

      - name: Upload compliance report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: clawgovern-compliance-report
          path: compliance_report.html
```

## Policy as Code
ClawGovern enforces policy from YAML, not tribal knowledge.

Enterprise policy (`enterprise_policy.yaml`):

```yaml
policy:
  allowed_models:
    - gpt-4.5-turbo
    - claude-3.5-sonnet
  max_daily_budget_per_agent: 50
  require_human_in_loop_for_tools:
    - stripe_refund
    - db_drop
```

Agent definitions (`example_agents.yaml`):

```yaml
agents:
  - name: SupportBot
    model: gpt-4.5-turbo
    daily_budget: 500
    tools_used: [zendesk_read, stripe_refund]
    human_in_loop: false
  - name: InternalResearchBot
    model: open-mixtral-8x22b
    daily_budget: 10
    tools_used: [web_search]
    human_in_loop: true
```

What gets enforced:

- Budget Check: fail when `daily_budget > max_daily_budget_per_agent`.
- Model Check: fail when `model` is outside `allowed_models`.
- HITL Check: fail when restricted tools are used without `human_in_loop: true`.

## HTML Reporting
For audit trail and stakeholder visibility, export a rendered report:

```bash
uv run clawgovern audit --export-report
```

This generates:

- `compliance_report.html`

Use it for compliance reviews, security sign-off, and FinOps governance evidence.
