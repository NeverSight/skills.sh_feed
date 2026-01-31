#!/usr/bin/env python3
"""
Build a deterministic skill -> category index for the website to consume.

Outputs:
  data/skills_category_index.json

Notes:
- Primary categories intentionally align with the current website `SkillCategory` union:
    document-processing, development-tools, data-analysis, business-marketing,
    communication-writing, creative-media, productivity, collaboration, security
- If the website doesn't have a mapping entry for a skill, it can still fall back to
  its existing heuristic guesser.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Optional


REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"
INDEX_PATH = DATA_DIR / "skills_index.json"
OUTPUT_PATH = DATA_DIR / "skills_category_index.json"

PRIMARY_CATEGORIES = [
    "document-processing",
    "development-tools",
    "data-analysis",
    "business-marketing",
    "communication-writing",
    "creative-media",
    "productivity",
    "collaboration",
    "security",
]


def _contains_any(hay: str, needles: Iterable[str]) -> bool:
    return any(n in hay for n in needles)

def _contains_any_token(tokens: set[str], needles: Iterable[str]) -> bool:
    return any(n in tokens for n in needles)


def _contains_any_phrase(hay: str, needles: Iterable[str]) -> bool:
    # Use this only for multi-word / hyphenated / path-like phrases.
    # Avoid for short strings like "ui" / "auth" to prevent false positives.
    return any(n in hay for n in needles)


def _split_words(s: str) -> list[str]:
    # Keep it simple and fast; we mainly want keyword-ish tokens.
    return [w for w in re.split(r"[^a-z0-9]+", s.lower()) if w]


def _load_description_text(repo_relative_path: Optional[str]) -> str:
    """
    skills_index items store `description` as a repo-relative file path:
      data/skills-md/<owner>/<repo>/<skillId>/description_en.txt
    """
    if not repo_relative_path:
        return ""
    p = REPO_ROOT / repo_relative_path.lstrip("/").strip()
    try:
        # Read a small chunk; we only need keywords.
        return p.read_text(encoding="utf-8", errors="ignore")[:2000].lower()
    except Exception:
        return ""


@dataclass(frozen=True)
class Categorization:
    primary: str
    subcategory: Optional[str] = None


def categorize(source: str, skill_id: str, title: str, description_path: Optional[str]) -> Categorization:
    """
    Rule-based categorization. Designed to be:
    - deterministic
    - explainable
    - cheap to compute for ~20k skills
    """
    source_l = (source or "").lower()
    skill_l = (skill_id or "").lower()
    title_l = (title or "").lower()

    key = f"{source_l}/{skill_l} {title_l}"
    words = set(_split_words(key))

    # Strong repo-level hints first.
    if "marketingskills" in source_l or "marketing" in source_l:
        return Categorization(primary="business-marketing", subcategory="marketing")
    if "awesome-web3-security" in source_l or "web3" in source_l:
        return Categorization(primary="security", subcategory="web3-security")
    if "awesome-ai-security" in source_l:
        return Categorization(primary="security", subcategory="ai-security")

    # Document / office formats.
    doc_tokens = {
        "pdf",
        "doc",
        "docx",
        "ppt",
        "pptx",
        "xls",
        "xlsx",
        "word",
        "powerpoint",
        "excel",
        "epub",
        "latex",
        "tex",
        "ocr",
    }
    if words & doc_tokens or _contains_any_phrase(key, ["/pdf", "/docx", "/pptx", "/xlsx"]):
        return Categorization(primary="document-processing")
    if _contains_any_token(words, ["document", "documents", "slides", "spreadsheet"]) and _contains_any_phrase(
        key, ["convert", "extract", "parse", "merge", "annotat", "summariz"]
    ):
        return Categorization(primary="document-processing")

    # Security (with guardrails to not steal SEO-audit etc.).
    if "seo" in words or "serp" in words:
        # SEO-specific things tend to be marketing / analytics.
        if _contains_any_phrase(key, ["audit", "analy", "report", "keyword"]):
            return Categorization(primary="data-analysis", subcategory="seo")
        return Categorization(primary="business-marketing", subcategory="seo")

    security_tokens = {
        "security",
        "secure",
        "vuln",
        "vulnerability",
        "pentest",
        "pentesting",
        "threat",
        "forensic",
        "forensics",
        "malware",
        "exploit",
        "xss",
        "csrf",
        "sqli",
        "rce",
        "cve",
        "crypto",
        "cryptography",
        "oauth",
        "jwt",
        "auth",
        "authentication",
        "authorization",
        "sast",
        "dast",
        "appsec",
        "devsecops",
        "incident",
        "response",
        "solana",
        "mev",
        "wallet",
        "forensics",
    }
    security_phrases = {
        "sql-injection",
        "audit-website",
        "smart-contract",
        "smart-contracts",
        "web3-security",
    }
    if (words & security_tokens) or _contains_any_phrase(key, security_phrases):
        sub = None
        if ({"solana", "mev", "wallet", "web3", "ethereum"} & words) or _contains_any_phrase(
            key, ["smart-contract"]
        ):
            sub = "web3-security"
        elif {"forensic", "forensics"} & words:
            sub = "forensics"
        elif {"pentest", "pentesting", "exploit"} & words:
            sub = "pentesting"
        elif {"auth", "oauth", "jwt", "authentication", "authorization"} & words:
            sub = "identity-access"
        return Categorization(primary="security", subcategory=sub)

    # Creative / media / design.
    creative_tokens_strong = {
        "ui",
        "ux",
        "figma",
        "logo",
        "branding",
        "illustration",
        "video",
        "audio",
        "music",
        "remotion",
        "canvas",
        "animation",
        "typography",
    }
    creative_tokens_soft = {"design", "image", "images", "color", "colors", "visual", "graphics", "graphic"}
    # "design" is overloaded (system design, database design). Only treat as creative when paired with UI/visual hints.
    creative_hints_without_design = (creative_tokens_strong | creative_tokens_soft) - {"design"}
    if (words & creative_tokens_strong) or (("design" in words) and (words & creative_hints_without_design)):
        return Categorization(primary="creative-media")

    # Writing / communication.
    # Avoid substring matching like "playwright" -> "write".
    writing_tokens = {
        "copywriting",
        "blog",
        "newsletter",
        "email",
        "resume",
        "cv",
        "cover",
        "coverletter",
        "proposal",
        "grammar",
        "proofread",
        "proofreading",
        "rewrite",
        "summarize",
        "summary",
        "translation",
        "translate",
        "translated",
        "speech",
        "meeting",
        "meetingnotes",
        "docs",
        "documentation",
    }
    writing_phrases = {"cover-letter", "meeting-notes"}
    if (words & writing_tokens) or _contains_any_phrase(key, writing_phrases):
        sub = "translation" if ({"translate", "translation"} & words) else None
        return Categorization(primary="communication-writing", subcategory=sub)

    # Business / marketing (non-SEO).
    biz_tokens = {
        "marketing",
        "sales",
        "growth",
        "pricing",
        "crm",
        "funnel",
        "ads",
        "adwords",
        "tiktok",
        "linkedin",
        "twitter",
        "campaign",
        "branding",
    }
    biz_phrases = {"facebook-ads"}
    if (words & biz_tokens) or _contains_any_phrase(key, biz_phrases):
        return Categorization(primary="business-marketing")

    # Data / analytics.
    data_tokens = {
        "data",
        "analysis",
        "analytics",
        "dashboard",
        "visualization",
        "statistics",
        "forecast",
        "timeseries",
        "etl",
        "warehouse",
        "bigquery",
        "snowflake",
        "dbt",
        "pandas",
        "numpy",
        "jupyter",
        "spark",
        "kafka",
        "bi",
    }
    data_phrases = {"time-series"}
    if (words & data_tokens) or _contains_any_phrase(key, data_phrases):
        sub = None
        if {"sql", "postgres", "postgresql", "mysql", "sqlite"} & words:
            sub = "sql"
        elif {"pandas", "numpy", "jupyter"} & words:
            sub = "data-science"
        elif {"bigquery", "snowflake", "dbt", "warehouse"} & words:
            sub = "data-warehouse"
        return Categorization(primary="data-analysis", subcategory=sub)

    # Collaboration / project management.
    collab_tokens = {
        "collaboration",
        "agile",
        "scrum",
        "jira",
        "linear",
        "trello",
        "asana",
        "notion",
        "confluence",
        "slack",
        "teams",
        "discord",
    }
    collab_phrases = {"project-management"}
    if (words & collab_tokens) or _contains_any_phrase(key, collab_phrases):
        return Categorization(primary="collaboration")

    # Productivity.
    productivity_tokens = {
        "productivity",
        "workflow",
        "notes",
        "note",
        "todo",
        "task",
        "planning",
        "plan",
        "calendar",
        "pomodoro",
        "brainstorm",
        "organize",
        "focus",
        "habit",
        "routine",
    }
    productivity_phrases = {"time-management"}
    if (words & productivity_tokens) or _contains_any_phrase(key, productivity_phrases):
        return Categorization(primary="productivity")

    # Developer tooling / programming / infrastructure.
    # Keep this AFTER other categories: many skills mention "agent" / "skills" / org names, which are not categories.
    dev_tokens = {
        # Languages
        "python",
        "py",
        "javascript",
        "js",
        "typescript",
        "ts",
        "node",
        "nodejs",
        "go",
        "golang",
        "rust",
        "java",
        "kotlin",
        "swift",
        "objectivec",
        "objc",
        "c",
        "cpp",
        "cxx",
        "csharp",
        "dotnet",
        "php",
        "ruby",
        "rails",
        # Web / frameworks
        "react",
        "next",
        "nextjs",
        "vue",
        "svelte",
        "angular",
        "tailwind",
        "webpack",
        "vite",
        # Testing / QA
        "test",
        "testing",
        "playwright",
        "cypress",
        "selenium",
        "jest",
        "vitest",
        "pytest",
        "axe",
        "a11y",
        "accessibility",
        "wcag",
        # Mobile
        "ios",
        "android",
        "xcode",
        "simulator",
        # DevOps / infra
        "docker",
        "kubernetes",
        "k8s",
        "terraform",
        "ansible",
        "helm",
        "nix",
        "tmux",
        "orbstack",
        "ci",
        "cd",
        "github",
        "git",
        # Data stores (often dev best-practices)
        "postgres",
        "postgresql",
        "mysql",
        "sqlite",
        "mongodb",
        "redis",
        # Cloud
        "aws",
        "gcp",
        "azure",
        "cloudflare",
        "netlify",
        "supabase",
        # AI engineering
        "llm",
        "prompt",
        "prompts",
        "mcp",
        # General engineering words
        "api",
        "sdk",
        "cli",
        "library",
        "framework",
        "backend",
        "frontend",
        "observability",
        "logging",
        "tracing",
        "metrics",
        "debug",
        "debugging",
    }
    dev_phrases = {
        "best-practices",
        "bestpractices",
        "code-review",
        "codegen",
    }
    if (words & dev_tokens) or _contains_any_phrase(key, dev_phrases):
        sub = None
        # Lightweight subcategories (optional, safe to ignore).
        if {"playwright", "cypress", "selenium", "jest", "vitest", "pytest", "axe"} & words:
            sub = "testing"
        elif {"docker", "kubernetes", "k8s", "terraform", "ansible", "helm", "nix"} & words:
            sub = "devops"
        elif {"postgres", "postgresql", "mysql", "sqlite", "mongodb", "redis"} & words:
            sub = "databases"
        elif {"react", "next", "nextjs", "vue", "svelte", "angular", "tailwind"} & words:
            sub = "frontend"
        elif {"llm", "prompt", "mcp"} & words:
            sub = "ai-engineering"
        return Categorization(primary="development-tools", subcategory=sub)

    # If still ambiguous, peek at the short description.
    desc = _load_description_text(description_path)
    if desc:
        desc_words = set(_split_words(desc))
        if ({"pdf", "docx", "pptx", "xlsx", "spreadsheet", "presentation"} & desc_words) or _contains_any_phrase(
            desc, ["powerpoint", "spreadsheet"]
        ):
            return Categorization(primary="document-processing")
        if {"seo", "marketing", "campaign", "sales"} & desc_words:
            return Categorization(primary="business-marketing")
        if {"security", "vulnerability", "pentest", "forensics"} & desc_words or _contains_any_phrase(
            desc, ["sql-injection", "smart contract", "audit-website"]
        ):
            return Categorization(primary="security")
        # Avoid generic "writing code" phrasing used by dev skills (e.g. "Use when writing code...").
        if {"copywriting", "proofread", "proofreading", "grammar", "translate", "translation", "resume"} & desc_words:
            return Categorization(primary="communication-writing")
        if ({"ui", "ux", "figma", "video", "audio", "remotion", "canvas"} & desc_words) or _contains_any_phrase(
            desc, ["user interface", "visual design"]
        ):
            return Categorization(primary="creative-media")
        if {"data", "analysis", "analytics", "pandas", "jupyter", "dashboard"} & desc_words:
            return Categorization(primary="data-analysis")
        if {"jira", "slack", "notion", "collaboration", "scrum"} & desc_words:
            return Categorization(primary="collaboration")
        if {"productivity", "workflow", "todo", "notes", "planning", "pomodoro"} & desc_words:
            return Categorization(primary="productivity")
        if {"playwright", "pytest", "jest", "typescript", "react", "docker", "kubernetes", "ios", "android"} & desc_words:
            return Categorization(primary="development-tools")

    # Default bucket: most skills are developer adjacent.
    return Categorization(primary="development-tools")


def main() -> None:
    if not INDEX_PATH.exists():
        raise SystemExit(f"Missing {INDEX_PATH}")

    with INDEX_PATH.open("r", encoding="utf-8") as f:
        index = json.load(f)

    items = index.get("items") or []
    if not isinstance(items, list):
        raise SystemExit("skills_index.json: expected `items` to be a list")

    skill_to_category: dict[str, str] = {}
    skill_to_subcategory: dict[str, str] = {}

    for it in items:
        full_id = (it.get("id") or "").strip()
        if not full_id:
            continue

        cat = categorize(
            source=str(it.get("source") or ""),
            skill_id=str(it.get("skillId") or ""),
            title=str(it.get("title") or ""),
            description_path=it.get("description"),
        )

        primary = cat.primary
        if primary not in PRIMARY_CATEGORIES:
            # Website removed "other" bucket; default all unknowns to dev tools.
            primary = "development-tools"

        skill_to_category[full_id] = primary
        if cat.subcategory:
            skill_to_subcategory[full_id] = cat.subcategory

    out = {
        "updatedAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "sourceIndexUpdatedAt": index.get("updatedAt"),
        "version": 3,
        "primaryCategories": PRIMARY_CATEGORIES,
        "skillToCategory": dict(sorted(skill_to_category.items())),
        # Optional finer-grain label; safe for the website to ignore for now.
        "skillToSubcategory": dict(sorted(skill_to_subcategory.items())),
    }

    OUTPUT_PATH.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH} ({len(skill_to_category)} skills; {len(skill_to_subcategory)} with subcategory)")


if __name__ == "__main__":
    main()

