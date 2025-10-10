#!/usr/bin/env python3
"""
Metadata Extractor
Uses Claude API to intelligently analyze prompts and extract metadata
"""

import os
import re

import requests

from utils.cli_helpers import print_status

# Load environment variables
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass


def call_claude_api(messages, max_tokens=1000):
    """Call Claude API for metadata analysis"""
    try:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            print_status(
                "No API key found. Falling back to manual metadata entry.", "warning"
            )
            return None

        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "Content-Type": "application/json",
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
            },
            json={
                "model": "claude-3-5-sonnet-20241022",
                "max_tokens": max_tokens,
                "messages": messages,
            },
            timeout=30,
        )

        if response.status_code == 200:
            data = response.json()
            return data["content"][0]["text"]
        else:
            print_status(f"API Error: {response.status_code}", "error")
            return None

    except Exception as e:
        print_status(f"API call failed: {e}", "error")
        return None


def extract_title(content):
    """Extract title from prompt content with intelligent fallbacks"""

    # Method 1: Use Claude API for intelligent title generation (PRIMARY)
    intelligent_title = generate_title_with_claude(content)
    if intelligent_title:
        return intelligent_title

    # Method 2: Look for explicit markdown heading
    lines = content.strip().split("\n")
    for line in lines[:5]:  # Check first 5 lines
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()

    # Method 3: Look for JSON-style purpose field
    try:
        import json

        # Try to parse as JSON and extract purpose/role
        json_content = json.loads(content)

        if "purpose" in json_content:
            purpose = json_content["purpose"]
            return generate_title_from_purpose(purpose)

        if "role_definition" in json_content:
            role = json_content["role_definition"]
            return generate_title_from_role(role)

    except (json.JSONDecodeError, TypeError):
        pass

    # Method 4: Look for structured purpose/role in text format
    # Look for purpose patterns
    purpose_patterns = [
        r'"purpose":\s*"([^"]+)"',
        r"purpose:\s*([^,\n}]+)",
        r"to\s+(inspire|help|guide|assist|provide|enable)\s+([^.\n,]+)",
    ]

    import re

    for pattern in purpose_patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            purpose_text = (
                match.group(1) if len(match.groups()) >= 1 else match.group(0)
            )
            return generate_title_from_purpose(purpose_text)

    # Method 5: Parse "You are a/an..." patterns (FALLBACK)
    for line in lines[:5]:
        line = line.strip()
        if line.lower().startswith("you are a ") or line.lower().startswith(
            "you are an "
        ):
            # Extract the role/title
            title = (
                line[10:].strip()
                if line.lower().startswith("you are an ")
                else line[9:].strip()
            )

            # Stop at first sentence or reasonable length
            if "." in title:
                title = title.split(".")[0]

            # Limit to reasonable length (first few key words)
            words = title.split()
            if len(words) > 8:  # If too many words, take first meaningful chunk
                title = " ".join(words[:8])

            # Clean up common endings
            if title.endswith("."):
                title = title[:-1]

            return title.title()

    # Final fallback - return None to trigger user input
    return None


def generate_title_from_purpose(purpose_text):
    """Generate a title from purpose text"""
    # Clean up the purpose text
    purpose = purpose_text.strip().strip('"').strip()

    # Extract key concepts
    if "high agency" in purpose.lower():
        return "High Agency Inspirer"
    elif "inspire" in purpose.lower() and "remind" in purpose.lower():
        return "Life Inspiration Coach"
    elif "strategic" in purpose.lower() and "performance" in purpose.lower():
        return "Strategic Performance Advisor"
    elif "coach" in purpose.lower() or "coaching" in purpose.lower():
        return "Personal Coach"
    elif "productivity" in purpose.lower():
        return "Productivity Advisor"
    else:
        # Extract first meaningful phrase
        words = purpose.split()
        if len(words) >= 3:
            # Take first few meaningful words and title case them
            key_words = [
                w
                for w in words[:5]
                if w.lower() not in ["to", "the", "a", "an", "and", "or", "but"]
            ]
            if key_words:
                return " ".join(key_words[:3]).title()

    return "Purpose-Driven Assistant"


def generate_title_from_role(role_text):
    """Generate a title from role definition text"""
    role = role_text.strip().strip('"').strip()

    # Extract role name if it follows "act as" pattern
    if "act as" in role.lower():
        parts = role.lower().split("act as")
        if len(parts) > 1:
            role_name = parts[1].strip().strip(",").title()
            return role_name

    # Look for key role indicators
    if "inspirer" in role.lower():
        return role.title()
    elif "advisor" in role.lower():
        return role.title()
    elif "coach" in role.lower():
        return role.title()
    else:
        # Take first meaningful part
        words = role.split()
        if words:
            return " ".join(words[:3]).title()

    return "AI Assistant"


def generate_title_with_claude(content):
    """Use Claude API to generate an intelligent title"""
    try:
        title_prompt = f"""Analyze this prompt and suggest a concise, professional title (3-5 words) that captures the main role or purpose.

Prompt content:
{content[:800]}...

Requirements:
- 3-5 words maximum
- Captures the core role/function
- Professional and clear
- No version numbers or technical details
- Examples: "Strategic Performance Advisor", "Creative Innovation Strategist", "Knowledge Assessment Coach"

Respond with ONLY the title, nothing else."""

        messages = [{"role": "user", "content": title_prompt}]

        print_status("🤖 Generating intelligent title with Claude...", "processing")
        response = call_claude_api(messages, max_tokens=30)

        if response:
            title = response.strip().strip('"').strip()
            # Clean up any extra text
            if "\n" in title:
                title = title.split("\n")[0].strip()

            # Ensure reasonable length
            words = title.split()
            if len(words) > 6:  # If still too long, take first meaningful words
                title = " ".join(words[:5])  # Allow up to 5 words to match pattern

            return title if len(title) <= 60 else title[:60].strip()

    except Exception as e:
        print_status(f"Title generation failed: {e}", "warning")

    return None


def extract_technical_notes(content):
    """Extract technical implementation notes from content"""
    technical_data = {
        "recommended_llm": None,
        "temperature": None,
        "max_tokens": None,
        "additional_notes": [],
    }

    # First try to parse as JSON to extract any technical info
    try:
        import json

        json_content = json.loads(content)

        # Look for common technical fields in JSON
        if "recommended_llm" in json_content:
            technical_data["recommended_llm"] = json_content["recommended_llm"]
        if "temperature" in json_content:
            technical_data["temperature"] = float(json_content["temperature"])
        if "max_tokens" in json_content:
            technical_data["max_tokens"] = str(json_content["max_tokens"])

        # If we found JSON data, return early
        if any(technical_data.values()):
            return technical_data

    except (json.JSONDecodeError, TypeError, ValueError):
        pass

    # Look for technical implementation patterns in text
    lines = content.split("\n")

    for line in lines[:15]:  # Check first 15 lines for tech specs
        line = line.strip()

        # LLM recommendations
        if "recommended llm" in line.lower() or "llm" in line.lower():
            if "claude" in line.lower():
                if "sonnet" in line.lower():
                    technical_data["recommended_llm"] = "Claude 3.5 Sonnet"
                elif "opus" in line.lower():
                    technical_data["recommended_llm"] = "Claude 3 Opus"
                else:
                    technical_data["recommended_llm"] = "Claude"
            elif "gpt" in line.lower():
                if "4" in line:
                    technical_data["recommended_llm"] = "GPT-4"
                else:
                    technical_data["recommended_llm"] = "GPT-3.5"

        # Temperature settings
        temp_match = re.search(r"temperature[:\s*]*([0-9.]+)", line.lower())
        if temp_match:
            try:
                technical_data["temperature"] = float(temp_match.group(1))
            except ValueError:
                pass

        # Token limits
        token_match = re.search(r"(?:max[_\s]*tokens?)[:\s*]*([0-9,-]+)", line.lower())
        if token_match:
            technical_data["max_tokens"] = token_match.group(1).replace(",", "")

    # Look for technical implementation notes section
    content_lower = content.lower()
    if (
        "technical implementation" in content_lower
        or "implementation notes" in content_lower
    ):
        # Extract the section
        start_idx = content_lower.find("technical implementation")
        if start_idx == -1:
            start_idx = content_lower.find("implementation notes")

        if start_idx != -1:
            # Find the section content
            section_content = content[
                start_idx : start_idx + 1000
            ]  # Take reasonable chunk
            technical_data["additional_notes"].append(section_content)

    # If no technical notes found, suggest defaults based on prompt complexity
    if not any(
        [
            technical_data["recommended_llm"],
            technical_data["temperature"],
            technical_data["max_tokens"],
        ]
    ):
        # Analyze content to suggest appropriate defaults
        if (
            len(content) > 2000
            or "complex" in content.lower()
            or "advanced" in content.lower()
        ):
            technical_data["additional_notes"].append(
                "Complex prompt - consider Claude 3.5 Sonnet with temperature 0.3-0.7"
            )
        elif (
            "creative" in content.lower()
            or "inspire" in content.lower()
            or "generate" in content.lower()
        ):
            technical_data["additional_notes"].append(
                "Creative prompt - consider higher temperature (0.7-0.9)"
            )
        elif (
            "analysis" in content.lower()
            or "precise" in content.lower()
            or "accurate" in content.lower()
        ):
            technical_data["additional_notes"].append(
                "Analytical prompt - consider lower temperature (0.1-0.4)"
            )

    return technical_data


def analyze_prompt_with_claude(content):
    """Use Claude to analyze prompt and suggest metadata including discovery info"""

    analysis_prompt = f"""Analyze this prompt and provide comprehensive metadata in JSON format:

{content[:2000]}{'...' if len(content) > 2000 else ''}

Provide your analysis as a JSON object with these fields:
{{
  "title": "3-5 word professional title capturing the main role",
  "category": "suggested category (be specific, e.g., 'Business Strategy', 'Creative Writing', 'Personal Development')",
  "tags": ["2-3", "relevant", "tags"],
  "privacy_recommendation": "public or private",
  "privacy_reasoning": "brief explanation for privacy recommendation",
  "complexity_level": "basic, intermediate, or advanced",
  "use_case": "brief description of main use case",
  "discovery": {{
    "purpose": "One clear sentence: What does this prompt help accomplish?",
    "best_for": "Specific situations, problems, or use cases this addresses",
    "session_length": "Estimated time for typical session (e.g. '10-15 minutes')",
    "interaction_style": "Communication approach (e.g. 'Direct but supportive')",
    "outcome": "What the user gets from using this prompt",
    "try_if": "One compelling reason to try this prompt, in quotes"
  }}
}}

IMPORTANT: Privacy should be based on the PROMPT CONTENT itself, not how it might be used:

PRIVATE if the prompt contains:
- Personal details, company-specific info, real names, confidential methods, proprietary frameworks
- **Personal user characteristics, personality traits, individual challenges embedded in the prompt**
- **User-specific contexts like 'You're working with someone who identifies as...', personality descriptions, individual trait lists**
- **Prompts tailored to specific personality profiles or personal situations**

PUBLIC if the prompt contains:
- General-purpose tools, universal frameworks, widely applicable methodologies
- **Generic coaching/advisory content that doesn't reveal anything about the specific user**
- **Broadly applicable systems that work for anyone without personal customization**

Examples:
- PUBLIC: "High Agency Inspirer" (universal life coaching framework)
- PUBLIC: "Strategic Performance Advisor" (general business methodology)
- PUBLIC: "Creative Writing Assistant" (widely applicable tool)
- PRIVATE: "Acme Corp Q4 Strategy Review" (company-specific)
- PRIVATE: "John's Personal Therapy Session Guide" (personal details)
- **PRIVATE: Coaching prompt with 'You're working with someone who is: calm, reserved, critical...' (personal characteristics)**
- **PRIVATE: Any prompt describing specific user traits, challenges, or personality profile**

Key principle: If the prompt reveals personal information about its creator/user, it should be PRIVATE.

Discovery examples:
- purpose: "Build proactive thinking and overcome limiting beliefs"
- best_for: "Feeling stuck, making excuses, procrastination, or avoiding action"
- session_length: "10-15 minutes"
- interaction_style: "Direct but supportive with evidence-based frameworks"
- outcome: "Specific action plan with accountability measures"
- try_if: "I know what I should do but keep procrastinating"

Respond ONLY with the JSON object, no other text."""

    messages = [{"role": "user", "content": analysis_prompt}]

    print_status("🤖 Analyzing prompt with Claude...", "info")
    response = call_claude_api(messages, max_tokens=500)

    if not response:
        return None

    try:
        # Clean up response and parse JSON
        response = response.strip()
        if response.startswith("```json"):
            response = response.replace("```json", "").replace("```", "").strip()
        elif response.startswith("```"):
            response = response.replace("```", "").strip()

        import json

        analysis = json.loads(response)
        return analysis

    except json.JSONDecodeError as e:
        print_status(f"Failed to parse Claude's analysis: {e}", "error")
        return None


def extract_all_metadata(content):
    """Extract all metadata from prompt content"""
    metadata = {}

    # Extract title
    metadata["title"] = extract_title(content)

    # Extract technical notes
    technical_data = extract_technical_notes(content)
    metadata.update(technical_data)

    # Get Claude's analysis (includes discovery info now)
    claude_analysis = analyze_prompt_with_claude(content)
    if claude_analysis:
        # Map Claude response fields to metadata
        metadata["ai_suggested_title"] = claude_analysis.get("title")
        metadata["ai_suggested_category"] = claude_analysis.get("category")
        metadata["ai_suggested_tags"] = claude_analysis.get("tags", [])
        metadata["ai_privacy_recommendation"] = claude_analysis.get(
            "privacy_recommendation"
        )
        metadata["ai_privacy_reasoning"] = claude_analysis.get("privacy_reasoning")
        metadata["complexity_level"] = claude_analysis.get("complexity_level")
        metadata["use_case"] = claude_analysis.get("use_case")
        metadata["discovery"] = claude_analysis.get("discovery", {})

        # Use Claude's title if we don't have one from extraction
        if not metadata.get("title") and claude_analysis.get("title"):
            metadata["title"] = claude_analysis["title"]

    return metadata


if __name__ == "__main__":
    # Test with the Elite Strategic Performance Advisor prompt
    test_content = """# Elite Strategic Performance Advisor

**Recommended LLM**: Claude 3.5 Sonnet | **Temperature**: 0.4 | **Max Tokens**: 4000-6000

You are an Elite Strategic Performance Advisor specializing in breakthrough performance acceleration through systems-level analysis and evidence-based strategic guidance."""

    metadata = extract_all_metadata(test_content)
    import json

    print(json.dumps(metadata, indent=2))
