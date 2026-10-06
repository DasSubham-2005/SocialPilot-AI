
from collections import Counter
from typing import TypedDict

from langgraph.graph import StateGraph, START, END


class TrendState(TypedDict):
    topic: str
    sources: list
    trend_signals: list
    trend_summary: str


STOP_WORDS = {
    "about",
    "after",
    "again",
    "being",
    "could",
    "from",
    "have",
    "into",
    "more",
    "most",
    "other",
    "over",
    "should",
    "their",
    "there",
    "these",
    "they",
    "this",
    "through",
    "using",
    "what",
    "when",
    "where",
    "which",
    "while",
    "with",
    "would",
    "your",
    "than",
    "that",
    "will",
    "were",
    "been",
    "also",
    "only",
    "such",
    "some",
    "many",
    "much",
    "very",
    "latest",
    "development",
    "developments",
    "technology",
}


def extract_keywords(text: str) -> list[str]:
    words = (
        text.lower()
        .replace(",", " ")
        .replace(".", " ")
        .replace(":", " ")
        .replace(";", " ")
        .replace("(", " ")
        .replace(")", " ")
        .replace("/", " ")
        .replace("-", " ")
        .split()
    )

    keywords = []

    for word in words:
        word = word.strip()

        if (
            len(word) >= 4
            and word.isalpha()
            and word not in STOP_WORDS
        ):
            keywords.append(word)

    return keywords


def detect_trends(state: TrendState):

    topic = state["topic"].strip()
    sources = state["sources"]

    keyword_counter = Counter()

    source_titles = []

    for source in sources:

        title = source.get("title", "").strip()
        content = source.get("content", "").strip()

        if title:
            source_titles.append(title)

        text = f"{title} {content}"

        keywords = extract_keywords(text)

        keyword_counter.update(set(keywords))

    trend_signals = []

    for keyword, count in keyword_counter.most_common(10):

        if count >= 2:
            trend_signals.append({
                "keyword": keyword,
                "source_mentions": count,
            })

    if trend_signals:

        top_keywords = [
            signal["keyword"]
            for signal in trend_signals[:5]
        ]

        trend_summary = (
            f"Trend signals for '{topic}' are concentrated around: "
            + ", ".join(top_keywords)
            + ". These signals were identified from repeated "
              "mentions across the researched sources."
        )

    else:

        trend_summary = (
            f"No strong repeated trend signal was detected for "
            f"'{topic}' across the available research sources."
        )

    return {
        "trend_signals": trend_signals,
        "trend_summary": trend_summary,
    }


graph = StateGraph(TrendState)

graph.add_node(
    "trend_detection",
    detect_trends,
)

graph.add_edge(
    START,
    "trend_detection",
)

graph.add_edge(
    "trend_detection",
    END,
)

trend_agent = graph.compile()
