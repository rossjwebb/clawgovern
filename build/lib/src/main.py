"""Typer CLI entrypoint for ClawGovern."""

from pathlib import Path
from typing import Any

import typer
import yaml

from src.engine import audit_agents
from src.models import AgentsFile, EnterprisePolicyFile

app = typer.Typer()


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
) -> None:
    agents_data, policy_data = _load_validated_files(agents_file, policy_file)
    print(audit_agents(agents_data, policy_data))


def main() -> None:
    app()


if __name__ == "__main__":
    main()
