"""
Input Validation Utility
------------------------
Provides validation and sanitization functions for all user-facing inputs
to the Agentic PPT Builder. Used by both the Streamlit UI and CLI entry points.

All validators raise ``ValidationError`` on invalid input with a descriptive
message suitable for display to end users.
"""

import re
import html
from typing import Optional

from config.settings import Config


class ValidationError(ValueError):
    """
    Raised when user input fails validation.

    Inherits from ValueError so existing ``except ValueError`` blocks
    in the codebase continue to work without modification.
    """
    pass


def sanitize_input(text: str) -> str:
    """
    Sanitize a user-provided text string by stripping dangerous content.

    Operations performed:
        1. Strip leading/trailing whitespace
        2. Escape HTML entities (prevent XSS in any web-rendered output)
        3. Remove control characters (except newlines and tabs)
        4. Collapse multiple consecutive spaces into one

    Args:
        text: Raw user input string.

    Returns:
        Sanitized string safe for processing.

    Example:
        >>> sanitize_input("  <script>alert('xss')</script>  Hello  World  ")
        "&lt;script&gt;alert(&#x27;xss&#x27;)&lt;/script&gt; Hello World"
    """
    if not isinstance(text, str):
        return str(text).strip()

    text = text.strip()
    text = html.escape(text)
    # Remove control characters except newline (\n) and tab (\t)
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text)
    # Collapse multiple spaces
    text = re.sub(r" {2,}", " ", text)
    return text


def validate_topic(topic: Optional[str]) -> str:
    """
    Validate and sanitize the presentation topic.

    Rules:
        - Must not be empty or whitespace-only
        - Must be at least ``Config.MIN_TOPIC_LENGTH`` characters (3)
        - Must be at most ``Config.MAX_TOPIC_LENGTH`` characters (200)
        - Is sanitized before length checks (post-sanitization length applies)

    Args:
        topic: The user-provided presentation topic.

    Returns:
        The sanitized topic string.

    Raises:
        ValidationError: If the topic is empty, too short, or too long.
    """
    if not topic or not topic.strip():
        raise ValidationError("Topic cannot be empty.")

    topic = sanitize_input(topic)

    if len(topic) < Config.MIN_TOPIC_LENGTH:
        raise ValidationError(
            f"Topic must be at least {Config.MIN_TOPIC_LENGTH} characters long. "
            f"Got {len(topic)} characters."
        )

    if len(topic) > Config.MAX_TOPIC_LENGTH:
        raise ValidationError(
            f"Topic must be at most {Config.MAX_TOPIC_LENGTH} characters long. "
            f"Got {len(topic)} characters."
        )

    return topic


def validate_slide_count(count: Optional[int]) -> int:
    """
    Validate the requested number of slides.

    Args:
        count: Number of slides. If None, returns the default from Config.

    Returns:
        Validated slide count as an integer.

    Raises:
        ValidationError: If count is not an integer or out of range [1, 20].
    """
    if count is None:
        return Config.DEFAULT_SLIDE_COUNT

    try:
        count = int(count)
    except (TypeError, ValueError):
        raise ValidationError(
            f"Slide count must be an integer. Got: {type(count).__name__}."
        )

    if count < Config.MIN_SLIDE_COUNT or count > Config.MAX_SLIDE_COUNT:
        raise ValidationError(
            f"Slide count must be between {Config.MIN_SLIDE_COUNT} and "
            f"{Config.MAX_SLIDE_COUNT}. Got {count}."
        )

    return count


def validate_font(font: Optional[str]) -> str:
    """
    Validate the selected font name.

    Args:
        font: Font name string. If None, defaults to "Calibri".

    Returns:
        Validated font name.

    Raises:
        ValidationError: If font is not in the allowed list.
    """
    if not font:
        return "Calibri"

    font = font.strip()
    if font not in Config.ALLOWED_FONTS:
        raise ValidationError(
            f"Font '{font}' is not supported. "
            f"Allowed fonts: {', '.join(Config.ALLOWED_FONTS)}."
        )

    return font


def validate_depth(depth: Optional[str]) -> str:
    """
    Validate the content depth setting.

    Args:
        depth: Depth string. If None, defaults to "Concise".

    Returns:
        Validated depth string.

    Raises:
        ValidationError: If depth is not in the allowed list.
    """
    if not depth:
        return "Concise"

    depth = depth.strip()
    if depth not in Config.ALLOWED_DEPTHS:
        raise ValidationError(
            f"Depth '{depth}' is not supported. "
            f"Allowed depths: {', '.join(Config.ALLOWED_DEPTHS)}."
        )

    return depth


def validate_all_inputs(
    topic: str,
    slide_count: Optional[int] = None,
    font: Optional[str] = None,
    depth: Optional[str] = None,
) -> dict:
    """
    Validate all user inputs at once and return a clean parameter dict.

    This is the primary validation entry point used by the orchestrator
    and application entry points.

    Args:
        topic: Presentation topic.
        slide_count: Number of slides (optional, defaults to Config value).
        font: Font name (optional, defaults to "Calibri").
        depth: Content depth (optional, defaults to "Concise").

    Returns:
        A dict with validated keys: ``topic``, ``slide_count``, ``font``, ``depth``.

    Raises:
        ValidationError: If any input fails validation.
    """
    return {
        "topic": validate_topic(topic),
        "slide_count": validate_slide_count(slide_count),
        "font": validate_font(font),
        "depth": validate_depth(depth),
    }
