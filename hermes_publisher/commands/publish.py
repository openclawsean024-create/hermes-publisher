"""publish — 把 SKILL.md 推上 Capafy。

MVP 階段: 只做 agent-card 草稿產生 + Capafy CLI 串接。
不做: 自動 OAuth、批次上傳、Webhook 監聽。
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path

from .check import _find_skill_md


def run(args) -> int:
    skill_md = _find_skill_md(args.skill)
    if skill_md is None:
        print(f"❌ 找不到 SKILL.md: {args.skill}")
        return 1

    content = skill_md.read_text(encoding="utf-8")
    card = _parse_skill_md(content)

    print(f"📦 產生 agent-card 草稿: {skill_md.name}")
    print(f"   名稱: {card['name']}")
    print(f"   版本: {card['version']}")
    print(f"   描述: {card['description'][:80]}...")
    print()

    # 寫 agent-card.md
    skill_dir = skill_md.parent.parent if skill_md.name == "SKILL.md" else skill_md.parent
    card_path = skill_dir / "agent-card.md"
    card_path.write_text(_render_card(card), encoding="utf-8")
    print(f"✍️  已寫: {card_path}")
    print()

    if args.dry_run:
        print("🏃 dry-run 模式：不真的上傳")
        print()
        print("📄 agent-card.md 內容預覽:")
        print("─" * 60)
        print(card_path.read_text(encoding="utf-8")[:1500])
        print("─" * 60)
        return 0

    # 互動式問定價
    price = args.price
    period = args.period
    if price is None or period is None:
        price, period = _ask_pricing(price, period)

    # 確認後真的上傳
    print(f"\n📤 即將上傳到 Capafy:")
    print(f"   定價: ${price:.2f} / {period}")
    confirm = input("   確認? (y/N): ").strip().lower()
    if confirm != "y":
        print("❌ 取消")
        return 1

    # 調用 Capafy-publisher skill CLI
    capafy_cli = shutil.which("capafy-publisher")
    if capafy_cli is None:
        print("\n⚠️  找不到 capafy-publisher CLI")
        print("   請先在 Capafy 創作者後台申請 Publisher 認證")
        print("   https://capafy.ai/zh-hant/developer/doc/2.2")
        print()
        print("   agent-card.md 已寫好。請手動執行:")
        print(f"     capafy-publisher publish --card {card_path}")
        return 0

    cmd = [capafy_cli, "publish", "--card", str(card_path), "--price", str(price), "--period", period]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"✅ 上架成功!")
        print(f"   {result.stdout}")
    else:
        print(f"❌ 上架失敗: {result.stderr}")
        return 1

    return 0


def _parse_skill_md(content: str) -> dict:
    """從 YAML frontmatter 解析必要欄位。"""
    # 簡單 YAML frontmatter 解析（不依賴 PyYAML）
    m = re.match(r"^---\n(.+?)\n---", content, re.DOTALL)
    if not m:
        return {"name": "未命名", "description": "無描述", "version": "0.1.0"}

    fm = m.group(1)
    card = {"name": "", "description": "", "version": "0.1.0"}

    # name 簡單情況
    m_name = re.search(r"^name:\s*(\S+)", fm, re.MULTILINE)
    if m_name:
        card["name"] = m_name.group(1).strip()

    # description 支援 multi-line (| 開頭)
    if "description: |" in fm or "description:|" in fm:
        # 多行模式：抓 | 下面所有縮排內容
        m_desc = re.search(r"^description:\s*\|\s*\n((?:  .+\n?)+)", fm, re.MULTILINE)
        if m_desc:
            card["description"] = "\n".join(
                line.strip() for line in m_desc.group(1).split("\n") if line.strip()
            )
    else:
        m_desc = re.search(r"^description:\s*(.+)$", fm, re.MULTILINE)
        if m_desc:
            card["description"] = m_desc.group(1).strip()

    m_ver = re.search(r"^version:\s*(\S+)", fm, re.MULTILINE)
    if m_ver:
        card["version"] = m_ver.group(1).strip()

    # 從 # 標題補 name
    if not card["name"]:
        h1 = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        if h1:
            card["name"] = h1.group(1).strip()

    # 從第一段補 description
    if not card["description"]:
        first_para = re.search(r"^#\s+.+\n\n(.+?)(?:\n\n|$)", content, re.MULTILINE | re.DOTALL)
        if first_para:
            card["description"] = first_para.group(1).strip()[:200]

    return card


def _render_card(card: dict) -> str:
    """產生 Capafy agent-card.md。"""
    return f"""# {card['name']}

> {card['description']}

## 開發者資訊

- 版本: {card['version']}
- 上架時間: 自動
- 來源: hermes-publisher MVP

## 描述

{card['description']}

## 適合對象

（請填）

## 適合場景

（請填）

## 試用說明

（請填）

## 變現模式

依照 hermes-publisher 模擬結果填入

## 評價

（Capafy 自動生成）
"""


def _ask_pricing(price: float | None, period: str | None) -> tuple[float, str]:
    if price is None:
        p = input("  定價 (USD, 例 9.99): ").strip()
        price = float(p) if p else 9.99
    if period is None:
        per = input("  週期 (day/week/month/one-time) [week]: ").strip() or "week"
        period = per
    return price, period
