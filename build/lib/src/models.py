"""Strict schemas for ClawGovern YAML inputs."""

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictInt, StrictStr


class StrictModel(BaseModel):
    """Base model with strict validation and no unknown fields."""

    model_config = ConfigDict(extra="forbid", strict=True)


class Agent(StrictModel):
    name: StrictStr
    model: StrictStr
    daily_budget: StrictInt = Field(ge=0)
    tools_used: list[StrictStr]
    human_in_loop: StrictBool


class AgentsFile(StrictModel):
    agents: list[Agent]


class Policy(StrictModel):
    allowed_models: list[StrictStr]
    max_daily_budget_per_agent: StrictInt = Field(ge=0)
    require_human_in_loop_for_tools: list[StrictStr]


class EnterprisePolicyFile(StrictModel):
    policy: Policy
