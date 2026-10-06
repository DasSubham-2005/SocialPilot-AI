
import re


def validate_linkedin_content(content: str) -> dict:
    issues = []

    if not content or not content.strip():
        return {
            "status": "FAIL",
            "issues": ["Content is empty."],
        }

    content = content.strip()

    if "**" in content:
        issues.append("Markdown bold formatting detected.")

    if "__" in content:
        issues.append("Markdown underscore formatting detected.")

    if re.search(r"(?m)^#{1,6}\s+", content):
        issues.append("Markdown heading detected.")

    if re.search(r"https?://\S+", content):
        issues.append("Source URL detected.")

    if re.search(r"[a-z][.!?,;:](?=[A-Za-z])", content):
        issues.append("Missing space after punctuation detected.")

    hashtags = re.findall(
        r"(?<!\w)#[A-Za-z0-9]+",
        content,
    )

    if not 3 <= len(hashtags) <= 5:
        issues.append(
            f"Expected 3 to 5 hashtags, found {len(hashtags)}."
        )

    for hashtag in hashtags:
        if not re.fullmatch(
            r"#[A-Za-z0-9]+",
            hashtag,
        ):
            issues.append(
                f"Invalid hashtag format: '{hashtag}'."
            )

    return {
        "status": "FAIL" if issues else "PASS",
        "issues": issues,
    }
