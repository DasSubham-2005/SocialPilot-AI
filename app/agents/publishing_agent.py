from typing import TypedDict

import requests
from langgraph.graph import StateGraph, START, END

from app.config import LINKEDIN_ACCESS_TOKEN, LINKEDIN_PERSON_URN


class PublishingState(TypedDict):
    linkedin_content: str
    approval_status: str
    guard_status: str
    publication_status: str
    publication_payload: dict
    publication_message: str


def publish_to_linkedin(state: PublishingState):

    approval_status = state["approval_status"].upper()
    guard_status = state["guard_status"].upper()

    if approval_status != "APPROVED":
        return {
            "publication_status": "BLOCKED",
            "publication_payload": {},
            "publication_message": (
                "Publishing blocked because human approval "
                "has not been granted."
            ),
        }

    if guard_status != "PASSED":
        return {
            "publication_status": "BLOCKED",
            "publication_payload": {},
            "publication_message": (
                "Publishing blocked because the pre-publish "
                "guard has not passed."
            ),
        }

    content = state["linkedin_content"].strip()

    if not content:
        return {
            "publication_status": "BLOCKED",
            "publication_payload": {},
            "publication_message": (
                "Publishing blocked because LinkedIn content is empty."
            ),
        }

    if not LINKEDIN_ACCESS_TOKEN:
        return {
            "publication_status": "BLOCKED",
            "publication_payload": {},
            "publication_message": (
                "Publishing blocked because "
                "LINKEDIN_ACCESS_TOKEN is missing."
            ),
        }

    if not LINKEDIN_PERSON_URN:
        return {
            "publication_status": "BLOCKED",
            "publication_payload": {},
            "publication_message": (
                "Publishing blocked because "
                "LINKEDIN_PERSON_URN is missing."
            ),
        }

    payload = {
        "author": f"urn:li:person:{LINKEDIN_PERSON_URN}",
        "commentary": content,
        "visibility": "PUBLIC",
        "distribution": {
            "feedDistribution": "MAIN_FEED",
            "targetEntities": [],
            "thirdPartyDistributionChannels": [],
        },
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False,
    }

    headers = {
        "Authorization": f"Bearer {LINKEDIN_ACCESS_TOKEN}",
        "X-Restli-Protocol-Version": "2.0.0",
        "Linkedin-Version": "202609",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(
            "https://api.linkedin.com/rest/posts",
            headers=headers,
            json=payload,
            timeout=30,
        )

        if response.status_code == 201:

            post_id = response.headers.get(
                "x-restli-id",
                "",
            )

            return {
                "publication_status": "PUBLISHED",
                "publication_payload": payload,
                "publication_message": (
                    "LinkedIn post published successfully."
                    + (
                        f" Post ID: {post_id}"
                        if post_id
                        else ""
                    )
                ),
            }

        return {
            "publication_status": "FAILED",
            "publication_payload": payload,
            "publication_message": (
                f"LinkedIn publishing failed. "
                f"HTTP {response.status_code}: "
                f"{response.text}"
            ),
        }

    except requests.RequestException as exc:

        return {
            "publication_status": "FAILED",
            "publication_payload": payload,
            "publication_message": (
                f"LinkedIn publishing request failed: {exc}"
            ),
        }


graph = StateGraph(PublishingState)

graph.add_node(
    "publish_to_linkedin",
    publish_to_linkedin,
)

graph.add_edge(
    START,
    "publish_to_linkedin",
)

graph.add_edge(
    "publish_to_linkedin",
    END,
)

publishing_agent = graph.compile()