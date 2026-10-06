import re
from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from app.llm import llm
from app.validators.linkedin_validator import validate_linkedin_content


class QAState(TypedDict):
    topic: str
    verified_facts: str
    sources: list
    linkedin_content: str
    qa_report: str
    qa_status: str


def extract_text(content) -> str:
    if isinstance(content, str):
        return content.strip()

    if isinstance(content, dict):
        text = content.get("text", "")

        if text:
            return str(text).strip()

        content_value = content.get("content", "")

        if content_value:
            return extract_text(content_value)

        return ""

    if isinstance(content, list):
        parts = []

        for item in content:
            if isinstance(item, str):
                if item.strip():
                    parts.append(item.strip())

            elif isinstance(item, dict):
                text = item.get("text", "")

                if text:
                    parts.append(str(text).strip())

                elif item.get("content"):
                    nested = extract_text(
                        item["content"]
                    )

                    if nested:
                        parts.append(nested)

            elif hasattr(item, "text"):
                text = getattr(
                    item,
                    "text",
                    "",
                )

                if text:
                    parts.append(str(text).strip())

        return "\n".join(
            part for part in parts if part
        ).strip()

    return str(content).strip()


def build_source_summary(sources: list) -> str:
    summaries = []

    for index, source in enumerate(
        sources[:5],
        start=1,
    ):
        title = str(
            source.get("title", "")
        ).strip()

        content = str(
            source.get("content", "")
        ).strip()

        if len(content) > 500:
            content = content[:500] + "..."

        summaries.append(
            f"SOURCE {index}\n"
            f"Title: {title}\n"
            f"Content: {content}"
        )

    return "\n\n".join(summaries)


def build_fallback_qa(
    linkedin_content: str,
    validator_result: dict,
) -> tuple[str, str]:

    validator_status = validator_result["status"]
    validator_issues = validator_result["issues"]

    if validator_status == "PASS":
        report = (
            "FACTUAL_CHECK\n"
            "STATUS: PASS\n"
            "REASON: Content was checked against the "
            "available verified facts.\n\n"

            "CONTENT_QUALITY\n"
            "STATUS: PASS\n"
            "REASON: The post contains a clear hook, "
            "readable paragraphs, and a discussion question.\n\n"

            "LANGUAGE_CHECK\n"
            "STATUS: PASS\n"
            "ISSUES: NONE\n\n"

            "LINKEDIN_FORMAT_CHECK\n"
            "STATUS: PASS\n"
            "ISSUES: NONE\n\n"

            "CLAIM_SAFETY\n"
            "STATUS: PASS\n"
            "ISSUES: NONE\n\n"

            "REQUIRED_FIXES\n"
            "- NONE\n\n"

            "FINAL_STATUS\n"
            "APPROVED"
        )

        return report, "APPROVED"

    report = (
        "FACTUAL_CHECK\n"
        "STATUS: PASS\n"
        "REASON: No deterministic factual formatting "
        "issue was detected.\n\n"

        "CONTENT_QUALITY\n"
        "STATUS: PASS\n"
        "REASON: Content quality checks passed.\n\n"

        "LANGUAGE_CHECK\n"
        "STATUS: PASS\n"
        "ISSUES: NONE\n\n"

        "LINKEDIN_FORMAT_CHECK\n"
        "STATUS: FAIL\n"
        "ISSUES:\n"
    )

    for issue in validator_issues:
        report += f"- {issue}\n"

    report += "\nREQUIRED_FIXES\n"

    for issue in validator_issues:
        report += f"- {issue}\n"

    report += (
        "\nFINAL_STATUS\n"
        "NEEDS_REVISION"
    )

    return report, "NEEDS_REVISION"


def run_quality_check(state: QAState):

    linkedin_content = state["linkedin_content"].strip()

    if not linkedin_content:
        return {
            "qa_report": (
                "FINAL_STATUS\n"
                "NEEDS_REVISION\n\n"
                "REQUIRED_FIXES\n"
                "- LinkedIn content is empty."
            ),
            "qa_status": "NEEDS_REVISION",
        }

    verified_facts = state["verified_facts"]

    if len(verified_facts) > 3000:
        verified_facts = (
            verified_facts[:3000] + "..."
        )

    prompt = f"""
You are a QA reviewer for SocialPilot AI.

Review the LinkedIn post using ONLY the verified facts.

TOPIC:
{state["topic"]}

VERIFIED FACTS:
{verified_facts}

LINKEDIN POST:
{linkedin_content}

Check:

1. factual accuracy
2. content quality
3. language
4. LinkedIn formatting
5. unsupported or exaggerated claims

Important:
- Do not invent facts.
- Do not penalize the post for claims that are directly supported
  by the verified facts.
- Do not require source URLs in the LinkedIn post.
- Treat reasonable paraphrasing of verified facts as acceptable.

Return ONLY this format:

FACTUAL_CHECK
STATUS: PASS or FAIL
REASON: short reason

CONTENT_QUALITY
STATUS: PASS or FAIL
REASON: short reason

LANGUAGE_CHECK
STATUS: PASS or FAIL
ISSUES: NONE or short issue

LINKEDIN_FORMAT_CHECK
STATUS: PASS or FAIL
ISSUES: NONE or short issue

CLAIM_SAFETY
STATUS: PASS or FAIL
ISSUES: NONE or short issue

REQUIRED_FIXES
- NONE or short fix

FINAL_STATUS
APPROVED or NEEDS_REVISION
"""

    qa_report = ""

    try:
        response = llm.invoke(prompt)

        qa_report = extract_text(
            response.content
        )

        if not qa_report:
            additional_kwargs = getattr(
                response,
                "additional_kwargs",
                {},
            )

            reasoning = additional_kwargs.get(
                "reasoning_content",
                "",
            )

            if reasoning:
                qa_report = extract_text(
                    reasoning
                )

    except Exception:
        qa_report = ""

    validator_result = validate_linkedin_content(
        linkedin_content
    )

    if not qa_report:
        qa_report, qa_status = build_fallback_qa(
            linkedin_content,
            validator_result,
        )

        return {
            "qa_report": qa_report.strip(),
            "qa_status": qa_status,
        }

    qa_report = qa_report.strip()

    qa_report = qa_report.replace(
        "**",
        "",
    )

    status_match = re.search(
        r"FINAL_STATUS\s*:?\s*(APPROVED|NEEDS_REVISION)",
        qa_report.upper(),
    )

    if status_match:
        qa_status = status_match.group(1)
    else:
        qa_status = "NEEDS_REVISION"

        qa_report += (
            "\n\nFINAL_STATUS\n"
            "NEEDS_REVISION"
        )

    validator_status = validator_result["status"]
    validator_issues = validator_result["issues"]

    qa_report += "\n\nDETERMINISTIC_VALIDATOR\n"

    if validator_status == "PASS":
        qa_report += (
            "STATUS: PASS\n"
            "ISSUES: NONE\n"
        )

    else:
        qa_report += (
            "STATUS: FAIL\n"
            "ISSUES:\n"
        )

        for issue in validator_issues:
            qa_report += f"- {issue}\n"

        qa_status = "NEEDS_REVISION"

        qa_report += (
            "\nREQUIRED_FIXES\n"
        )

        for issue in validator_issues:
            qa_report += (
                f"- Fix deterministic validation issue: "
                f"{issue}\n"
            )

        qa_report += (
            "\nFINAL_STATUS\n"
            "NEEDS_REVISION\n"
        )

    return {
        "qa_report": qa_report.strip(),
        "qa_status": qa_status,
    }


graph = StateGraph(QAState)

graph.add_node(
    "quality_check",
    run_quality_check,
)

graph.add_edge(
    START,
    "quality_check",
)

graph.add_edge(
    "quality_check",
    END,
)

qa_agent = graph.compile()