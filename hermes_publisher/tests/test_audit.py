"""Tests for hermes-publisher."""

from pathlib import Path


# 測試用 SKILL.md 範例
SAMPLE_SKILL_MD = """---
name: test-skill
description: |
  這是一個測試用的 skill。它做測試。
version: 1.0.0
---

# 測試 skill

## 輸入
- prompt: string

## 輸出
- result: string

## 範例
輸入: hello
輸出: world

## 限制
- 不處理個人資料
"""


def test_check_healthy_skill(tmp_path: Path):
    """能正確檢查一個健康的 SKILL.md。"""
    from hermes_publisher.commands.check import _find_skill_md
    from hermes_publisher.integrations.audit_rules import CHECKS

    skill_md = tmp_path / "SKILL.md"
    skill_md.write_text(SAMPLE_SKILL_MD, encoding="utf-8")

    found = _find_skill_md(tmp_path)
    assert found == skill_md

    content = skill_md.read_text(encoding="utf-8")
    # C1 必要欄位必通過
    ok, _ = CHECKS[0]["fn"](content)
    assert ok, "必要檢查 C1 失敗"
    # C3 歧視性用語必通過
    ok, _ = CHECKS[2]["fn"](content)
    assert ok, "必要檢查 C3 失敗"


def test_check_finds_in_skills_subdir(tmp_path: Path):
    """支援 /skills/SKILL.md 路徑。"""
    from hermes_publisher.commands.check import _find_skill_md

    skills_dir = tmp_path / "skills"
    skills_dir.mkdir()
    skill_md = skills_dir / "SKILL.md"
    skill_md.write_text(SAMPLE_SKILL_MD, encoding="utf-8")

    found = _find_skill_md(tmp_path)
    assert found == skill_md


def test_parse_skill_md_multiline_desc():
    """從 YAML frontmatter 抓 multi-line description。"""
    from hermes_publisher.commands.publish import _parse_skill_md

    card = _parse_skill_md(SAMPLE_SKILL_MD)
    assert card["name"] == "test-skill"
    assert "測試" in card["description"]
    assert card["version"] == "1.0.0"


def test_check_required_sections():
    """必要欄位檢查。"""
    from hermes_publisher.integrations.audit_rules import _check_required_sections

    ok, detail = _check_required_sections(SAMPLE_SKILL_MD)
    assert ok is True
    assert "齊全" in detail

    # 缺 name
    bad = "---\ndescription: test\nversion: 1.0\n---\n"
    ok, detail = _check_required_sections(bad)
    assert ok is False
    assert "name" in detail


def test_check_legal_language_flagged():
    """歧視性用語應被抓。"""
    from hermes_publisher.integrations.audit_rules import _check_legal_language

    bad = "這份工作會進行外觀評分"
    ok, _ = _check_legal_language(bad)
    assert ok is False
    assert "外觀評分" in _check_legal_language(bad)[1] or "歧視" in _check_legal_language(bad)[1]


def test_simulate_subscription_math():
    """simulate 計算邏輯正確。"""
    from hermes_publisher.commands.simulate import _gross_monthly, _llm_total

    # $9.99/週 × 50 subs = 9.99 × 4.33 × 50 = 2162.84
    gross = _gross_monthly(9.99, "week", 50, "訂閱")
    assert abs(gross - 2162.84) < 1

    # LLM: 0.05 × 50 × 5 = 12.5
    llm = _llm_total(0.05, 50, "訂閱")
    assert llm == 12.5
