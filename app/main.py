import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.workflow import socialpilot_workflow
from app.agents.human_approval import human_approval_agent
from app.agents.publishing_agent import publishing_agent
from app.agents.pre_publish_guard import pre_publish_guard
from app.agents.content_generation_agent import content_generation_agent
from app.agents.linkedin_adapter import linkedin_adapter
from app.agents.qa_agent import qa_agent


st.set_page_config(
    page_title="SocialPilot AI",
    page_icon="📱",
    layout="wide",
)

st.title("SocialPilot AI")
st.caption("Multi-Agent Social Media Management System")

st.divider()

st.subheader("Create Content")

topic = st.text_input(
    "Topic",
    placeholder="Example: AI agents in software development",
)

brand_context = st.text_area(
    "Brand / Content Context",
    placeholder="Optional context for the content strategy",
    height=120,
)

platform = st.selectbox(
    "Platform",
    ["LinkedIn"],
)

st.divider()

if st.button("Run SocialPilot", type="primary"):

    if not topic.strip():
        st.warning("Please enter a topic.")
        st.stop()

    initial_state = {
        "topic": topic.strip(),
        "brand_context": brand_context.strip(),
        "platform": platform,
        "search_query": "",
        "sources": [],
        "research_summary": "",
        "trend_signals": [],
        "trend_summary": "",
        "verified_facts": "",
        "source_count": 0,
        "content_strategy": "",
        "draft_content": "",
        "linkedin_content": "",
        "qa_report": "",
        "qa_status": "",
        "revision_count": 0,
        "human_decision": "",
        "approval_status": "",
        "approval_message": "",
        "publication_status": "",
        "publication_payload": {},
        "publication_message": "",
        "guard_status": "",
        "guard_message": "",
        "revised_content": "",
    }

    try:

        with st.spinner(
            "Running research, verification, content generation and QA..."
        ):

            result = socialpilot_workflow.invoke(
                initial_state
            )

    except Exception as e:

        st.error(
            "SocialPilot could not complete the workflow."
        )

        st.caption(
            "Please check the API configuration, quota, "
            "network connection, or application logs."
        )

        with st.expander("Technical Error"):
            st.code(str(e))

        st.stop()

    print("\n===== VERIFICATION STATE DEBUG =====")
    print("VERIFIED_FACTS:")
    print(result.get("verified_facts", "MISSING"))
    print("SOURCE_COUNT:", result.get("source_count", "MISSING"))
    print("RESULT KEYS:", list(result.keys()))
    print("===================================\n")

    st.session_state["socialpilot_result"] = result
    st.session_state["approval_complete"] = False

    st.success(
        "Content generation and QA completed."
    )

    st.rerun()


result = st.session_state.get(
    "socialpilot_result"
)


if result:

    st.divider()

    st.subheader("Research")

    st.write(
        result.get(
            "research_summary",
            "",
        )
    )

    st.subheader("Research Sources")

    sources = result.get(
        "sources",
        [],
    )

    if sources:

        for index, source in enumerate(
            sources,
            start=1,
        ):

            title = source.get(
                "title",
                "Untitled source",
            )

            url = source.get(
                "url",
                "",
            )

            content = source.get(
                "content",
                "",
            )

            with st.expander(
                f"Source {index}: {title}"
            ):

                if url:
                    st.markdown(
                        f"**URL:** {url}"
                    )

                if content:
                    st.write(content)

    else:

        st.info(
            "No research sources available."
        )

    st.subheader("Trend Detection")

    trend_summary = result.get(
        "trend_summary",
        "",
    )

    if trend_summary:
        st.write(trend_summary)

    trend_signals = result.get(
        "trend_signals",
        [],
    )

    if trend_signals:

        st.write("Detected Signals")

        for signal in trend_signals:

            keyword = signal.get(
                "keyword",
                "",
            )

            mentions = signal.get(
                "source_mentions",
                0,
            )

            st.write(
                f"- {keyword} — "
                f"{mentions} source mentions"
            )

    else:

        st.info(
            "No strong repeated trend signals detected."
        )

    st.subheader("Verified Facts")

    verified_facts = result.get(
        "verified_facts",
        "",
    )

    if verified_facts:
        st.write(verified_facts)
    else:
        st.warning(
            "No verified facts were returned in the workflow state."
        )

    st.subheader("Workflow Status")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Sources",
            result.get(
                "source_count",
                len(
                    result.get(
                        "sources",
                        [],
                    )
                ),
            ),
        )

    with col2:

        st.metric(
            "Revisions",
            result.get(
                "revision_count",
                0,
            ),
        )

    with col3:

        st.metric(
            "QA Status",
            result.get(
                "qa_status",
                "N/A",
            ),
        )

    st.subheader("Content Strategy")

    st.write(
        result.get(
            "content_strategy",
            "",
        )
    )

    st.subheader("Generated LinkedIn Content")

    st.text_area(
        "LinkedIn Post",
        value=result.get(
            "linkedin_content",
            "",
        ),
        height=300,
        disabled=True,
    )

    st.subheader("QA")

    qa_status = result.get(
        "qa_status",
        "N/A",
    )

    if qa_status == "APPROVED":

        st.success(
            "QA Status: APPROVED"
        )

    elif qa_status == "NEEDS_REVISION":

        st.warning(
            "QA Status: NEEDS_REVISION"
        )

    else:

        st.info(
            f"QA Status: {qa_status}"
        )

    with st.expander("QA Report"):

        st.write(
            result.get(
                "qa_report",
                "",
            )
        )

    st.divider()

    st.subheader("Human Approval")

    st.caption(
        "Review the generated LinkedIn content. "
        "Only approved content can be published."
    )

    if qa_status != "APPROVED":

        st.warning(
            "Human approval is unavailable because "
            "the content has not passed QA."
        )

    else:

        approval_decision = st.radio(
            "Decision",
            [
                "PENDING",
                "APPROVE",
                "REJECT",
            ],
            horizontal=True,
            key="approval_decision",
        )

        if approval_decision == "PENDING":

            st.warning(
                "Content is waiting for human approval."
            )

        elif approval_decision == "REJECT":

           st.error(
               "Content rejected by human reviewer."
           )

           if st.button(
               "Reject & Regenerate",
                type="primary",
           ):

                try:

                   with st.spinner(
                       "Regenerating content using existing research..."
                   ):

                      generation_result = (
                         content_generation_agent.invoke({
                           "topic": result["topic"],
                            "brand_context": result[
                               "brand_context"
                            ],
                            "platform": result[
                                "platform"
                            ],
                            "research_summary": result[
                                "research_summary"
                            ],
                            "trend_signals": result[
                               "trend_signals"
                            ],
                            "trend_summary": result[
                               "trend_summary"
                            ],
                            "verified_facts": result[
                                "verified_facts"
                            ],
                            "sources": result[
                                "sources"
                            ],
                            "content_strategy": "",
                            "draft_content": "",
                       })
                     )

                      adapter_result = (
                        linkedin_adapter.invoke({
                            "topic": result["topic"],
                            "draft_content": generation_result[
                               "draft_content"
                           ],
                           "linkedin_content": "",
                        })
                      )

                      qa_result = (
                        qa_agent.invoke({
                            "topic": result["topic"],
                            "verified_facts": result[
                               "verified_facts"
                            ],
                            "sources": result[
                                "sources"
                            ],
                            "linkedin_content": adapter_result[
                                "linkedin_content"
                            ],
                            "qa_report": "",
                            "qa_status": "",
                        })
                      )

                   new_result = {
                   **result,
                   **generation_result,
                   **adapter_result,
                   **qa_result,
                   "revision_count": 0,
                   "human_decision": "",
                   "approval_status": "",
                   "approval_message": "",
                   "publication_status": "",
                   "publication_payload": {},
                   "publication_message": "",
                   "guard_status": "",
                   "guard_message": "",
                   "revised_content": "",
                   }

                   st.session_state[
                    "socialpilot_result"
                   ] = new_result

                   st.session_state[
                    "approval_complete"
                   ] = False

                #    st.session_state[
                #     "approval_decision"
                #    ] = "PENDING"

                   st.rerun()

                except Exception as e:

                   st.error(
                    "Content regeneration failed."
                   )

                   with st.expander(
                    "Technical Error"
                   ):
                      st.code(str(e))

        elif approval_decision == "APPROVE":

            if st.button(
                "Approve & Publish",
                type="primary",
            ):

                try:

                    approval_result = (
                        human_approval_agent.invoke({
                            "linkedin_content": result[
                                "linkedin_content"
                            ],
                            "qa_status": result[
                                "qa_status"
                            ],
                            "qa_report": result[
                                "qa_report"
                            ],
                            "human_decision": "APPROVE",
                            "approval_status": "",
                            "approval_message": "",
                        })
                    )

                    updated_result = {
                        **result,
                        **approval_result,
                    }

                    if (
                        updated_result[
                            "approval_status"
                        ]
                        != "APPROVED"
                    ):

                        st.error(
                            "Human approval was not granted."
                        )

                        st.stop()

                    content = updated_result[
                        "linkedin_content"
                    ].strip()

                    publication_payload = {
                        "platform": "linkedin",
                        "content": content,
                        "publish_mode": "manual",
                    }

                    guard_result = (
                        pre_publish_guard.invoke({
                            "linkedin_content": content,
                            "approval_status": (
                                updated_result[
                                    "approval_status"
                                ]
                            ),
                            "publication_status": "READY",
                            "publication_payload": (
                                publication_payload
                            ),
                            "guard_status": "",
                            "guard_message": "",
                        })
                    )

                    updated_result.update(
                        guard_result
                    )

                    if (
                        updated_result[
                            "guard_status"
                        ]
                        != "PASSED"
                    ):

                        st.session_state[
                            "socialpilot_result"
                        ] = updated_result

                        st.error(
                            "Publishing blocked by "
                            "the pre-publish guard."
                        )

                        st.stop()

                    publishing_result = (
                        publishing_agent.invoke({
                            "linkedin_content": content,
                            "approval_status": (
                                updated_result[
                                    "approval_status"
                                ]
                            ),
                            "guard_status": (
                                updated_result[
                                    "guard_status"
                                ]
                            ),
                            "publication_status": "",
                            "publication_payload": (
                                publication_payload
                            ),
                            "publication_message": "",
                        })
                    )

                    updated_result.update(
                        publishing_result
                    )

                    st.session_state[
                        "socialpilot_result"
                    ] = updated_result

                    st.session_state[
                        "approval_complete"
                    ] = True

                    st.rerun()

                except Exception as e:

                    st.error(
                        "The approval or publishing "
                        "process could not be completed."
                    )

                    with st.expander(
                        "Technical Error"
                    ):
                        st.code(str(e))

    if st.session_state.get(
        "approval_complete"
    ):

        st.divider()

        st.subheader("Publishing")

        publication_status = result.get(
            "publication_status",
            "N/A",
        )

        if publication_status == "PUBLISHED":

            st.success(
                "LinkedIn post published successfully."
            )

        elif publication_status == "FAILED":

            st.error(
                "LinkedIn publishing failed."
            )

        else:

            st.warning(
                f"Publication Status: "
                f"{publication_status}"
            )

        st.write(
            result.get(
                "publication_message",
                "",
            )
        )

        st.subheader("Pre-Publish Guard")

        guard_status = result.get(
            "guard_status",
            "N/A",
        )

        if guard_status == "PASSED":

            st.success(
                f"Guard Status: {guard_status}"
            )

        else:

            st.error(
                f"Guard Status: {guard_status}"
            )

        st.write(
            result.get(
                "guard_message",
                "",
            )
        )

        with st.expander(
            "Publication Payload"
        ):

            st.json(
                result.get(
                    "publication_payload",
                    {},
                )
            )