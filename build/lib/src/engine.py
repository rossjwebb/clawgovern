"""Policy auditing engine for ClawGovern."""

from src.models import AgentsFile, EnterprisePolicyFile


def audit_agents(
    agents_data: AgentsFile, policy_data: EnterprisePolicyFile
) -> list[dict[str, object]]:
    """Evaluate each agent against enterprise policy and return raw audit results."""

    policy = policy_data.policy
    allowed_models = set(policy.allowed_models)
    hitl_required_tools = set(policy.require_human_in_loop_for_tools)

    results: list[dict[str, object]] = []

    for agent in agents_data.agents:
        violation_reasons: list[str] = []

        if agent.daily_budget > policy.max_daily_budget_per_agent:
            violation_reasons.append(
                "Budget check failed: "
                f"daily_budget={agent.daily_budget} exceeds "
                f"max_daily_budget_per_agent={policy.max_daily_budget_per_agent}."
            )

        if agent.model not in allowed_models:
            violation_reasons.append(
                "Model check failed: "
                f"model='{agent.model}' is not in allowed_models."
            )

        matched_hitl_tools = [
            tool for tool in agent.tools_used if tool in hitl_required_tools
        ]
        if matched_hitl_tools and not agent.human_in_loop:
            violation_reasons.append(
                "HITL check failed: tools requiring human-in-loop found "
                f"{matched_hitl_tools}, but human_in_loop is false."
            )

        results.append(
            {
                "agent_name": agent.name,
                "passed": len(violation_reasons) == 0,
                "violation_reasons": violation_reasons,
            }
        )

    return results
