"""Typer CLI entrypoint for ClawGovern."""

from pathlib import Path
from typing import Any

import typer
import yaml

from src.models import AgentsFile, EnterprisePolicyFile

app = typer.Typer()


def _load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


@app.callback()
def root() -> None:
    """ClawGovern enterprise policy CLI."""


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
    AgentsFile.model_validate(_load_yaml(agents_file))
    EnterprisePolicyFile.model_validate(_load_yaml(policy_file))
    typer.echo("Files loaded successfully")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
