"""Utility helpers shared across the project.

Current contents:
- extract_json_block(text) -> Optional[str]: find and return the first JSON object/array substring
- get_ppt_download_link(ppt_filename) -> str: return a base64 download link for a PPTX file
"""
import base64
import os
from typing import Optional


def extract_json_block(s: str) -> Optional[str]:
    """Try to extract the first JSON object or array from the given string.

    Handles fenced code blocks like ```json ... ``` and plain JSON printed by the model.
    Returns the JSON substring if found, otherwise None.
    """
    import re

    fence_re = re.compile(r"```(?:json)?\s*(.*?)\s*```", re.DOTALL | re.IGNORECASE)
    m = fence_re.search(s)
    if m:
        return m.group(1).strip()

    # Otherwise, search for the first occurrence of an object or array by scanning for '{' or '['
    start = None
    for i, ch in enumerate(s):
        if ch in '{[':
            start = i
            break
    if start is None:
        return None

    # Balanced-brace scan to find the matching end
    stack = []
    end = None
    for i in range(start, len(s)):
        ch = s[i]
        if ch == '{' or ch == '[':
            stack.append(ch)
        elif ch == '}' or ch == ']':
            if not stack:
                # unmatched closing
                return None
            stack.pop()
            if not stack:
                end = i + 1
                break
    if end is None:
        return None
    return s[start:end].strip()

def get_ppt_download_link(ppt_filename):
    if not os.path.exists(ppt_filename):
        raise FileNotFoundError(f"PPTX file not found: {ppt_filename}")

    with open(ppt_filename, "rb") as file:
        ppt_contents = file.read()
    b64_ppt = base64.b64encode(ppt_contents).decode()
    return f'<a href="data:application/vnd.openxmlformats-officedocument.presentationml.presentation;base64,{b64_ppt}" download="{os.path.basename(ppt_filename)}">Download the PowerPoint Presentation</a>'
