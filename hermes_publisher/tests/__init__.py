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
    for c in CHECKS[:4]:  # 至少前 4 條必通過
        ok, _ = c["fn"](content)
        assert ok, f"必要檢查 {c['id']} 失敗"
