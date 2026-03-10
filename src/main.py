"""Typer CLI entrypoint for ClawGovern."""

import sys
from pathlib import Path
from typing import Any

import typer
import yaml
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from src.engine import audit_agents
from src.models import AgentsFile, EnterprisePolicyFile

app = typer.Typer()
console = Console(record=True)


def _load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


@app.callback()
def root() -> None:
    """ClawGovern enterprise policy CLI."""


def _load_validated_files(
    agents_file: Path, policy_file: Path
) -> tuple[AgentsFile, EnterprisePolicyFile]:
    agents_data = AgentsFile.model_validate(_load_yaml(agents_file))
    policy_data = EnterprisePolicyFile.model_validate(_load_yaml(policy_file))
    return agents_data, policy_data


@app.command()
def parse(
    agents_file: Path = typer.Option(
        Path("example_agents.yaml"), "--agents-file", help="Path to example agents YAML."
    ),
    policy_file: Path = typer.Option(
        Path("enterprise_policy.yaml"),
        "--policy-file",
        help="Path to enterprise policy YAML.",
    ),
) -> None:
    _load_validated_files(agents_file, policy_file)
    typer.echo("Files loaded successfully")


@app.command()
def audit(
    agents_file: Path = typer.Option(
        Path("example_agents.yaml"), "--agents-file", help="Path to example agents YAML."
    ),
    policy_file: Path = typer.Option(
        Path("enterprise_policy.yaml"),
        "--policy-file",
        help="Path to enterprise policy YAML.",
    ),
    export_report: bool = typer.Option(
        False, "--export-report", help="Export audit output as compliance_report.html."
    ),
) -> None:
    agents_data, policy_data = _load_validated_files(agents_file, policy_file)
    results = audit_agents(agents_data, policy_data)

    table = Table(title="ClawGovern Compliance Audit")
    table.add_column("Agent Name")
    table.add_column("Status")
    table.add_column("Violations")

    failed_count = 0

    for result in results:
        agent_name = str(result["agent_name"])
        passed = bool(result["passed"])
        violation_reasons = result["violation_reasons"]

        if passed:
            status = "[green]✅ PASS[/green]"
            violations = "None"
        else:
            failed_count += 1
            status = "[red]❌ FAIL[/red]"
            violations = "\n".join(f"• {reason}" for reason in violation_reasons)

        table.add_row(agent_name, status, violations)

    console.print(table)
    console.print(
        Panel(
            f"Audit Complete: {len(results)} Agents Scanned, {failed_count} Failed.",
            title="Summary",
        )
    )

    if export_report:
        console.save_html("compliance_report.html")

    if failed_count > 0:
        sys.exit(1)

    sys.exit(0)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
