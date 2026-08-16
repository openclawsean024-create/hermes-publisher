"""check — 對 Capafy 審核指南 8 條跑一遍，預測上架成功率。

資料來源:
- Capafy 評價指南 v1.0 (2026-05-06)
- Capafy 發佈者協議 v1.1 (2026-08-14) 附表 A 技能內容標準
"""

from __future__ import annotations

import re
from pathlib import Path

from ..integrations.audit_rules import CHECKS, format_report


def run(args) -> int:
    skill_md = _find_skill_md(args.skill)
    if skill_md is None:
        print(f"❌ 找不到 SKILL.md: {args.skill}")
        return 1

    content = skill_md.read_text(encoding="utf-8")
    print(f"📋 檢查: {skill_md.relative_to(args.skill.resolve().parent)}")
    print(f"   路徑: {skill_md}")
    print(f"   大小: {len(content):,} 字元\n")

    results = []
    for check in CHECKS:
        ok, detail = check["fn"](content)
        results.append(
            {
                "id": check["id"],
                "name": check["name"],
                "weight": check["weight"],
                "ok": ok,
                "detail": detail,
            }
        )

    print(format_report(results))
    print(_verdict(results))
    return 0 if all(r["ok"] for r in results) else 1


def _find_skill_md(skill_path: Path) -> Path | None:
    """找 SKILL.md 檔案。

    支援:
    - skill_path 是目錄 → 找 /SKILL.md 或 /skills/SKILL.md
    - skill_path 是檔案 → 直接用
    """
    if skill_path.is_file():
        return skill_path
    if skill_path.is_dir():
        for candidate in [skill_path / "SKILL.md", skill_path / "skills" / "SKILL.md"]:
            if candidate.exists():
                return candidate
    return None


def _verdict(results: list[dict]) -> str:
    total_weight = sum(r["weight"] for r in results)
    passed_weight = sum(r["weight"] for r in results if r["ok"])
    pct = (passed_weight / total_weight) * 100 if total_weight else 0

    if pct == 100:
        return f"✅ 預測可上架 ({pct:.0f}% 通過)"
    elif pct >= 80:
        return f"⚠️  預測可上架但建議修補 ({pct:.0f}% 通過)"
    elif pct >= 50:
        return f"🟡 預測可能被拒 ({pct:.0f}% 通過)"
    else:
        return f"❌ 預測會被拒 ({pct:.0f}% 通過)"
