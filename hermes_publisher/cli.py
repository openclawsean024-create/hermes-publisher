"""hermes-publisher CLI 入口。

用法:
  python -m hermes_publisher <command> [options]

指令:
  publish    — 把 SKILL.md 推上 Capafy
  simulate   — 模擬不同價格 × 變現模式 × LLM 成本 → 預估月收入
  check      — 對 Capafy 審核指南 8 條跑自檢
  status     — 查已上架 skill 的銷售狀態
"""

import argparse
import sys
from pathlib import Path

from .commands import check, publish, simulate, status


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="hermes-publisher",
        description="從 Claude Code / Codex / Hermes 一鍵把 SKILL.md 上架到 Capafy。",
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # publish
    p_publish = subparsers.add_parser("publish", help="上架 SKILL.md 到 Capafy")
    p_publish.add_argument(
        "--skill",
        type=Path,
        required=True,
        help="包含 SKILL.md 的目錄路徑",
    )
    p_publish.add_argument(
        "--dry-run",
        action="store_true",
        help="只產生 agent-card 草稿，不真的上傳",
    )
    p_publish.add_argument(
        "--price",
        type=float,
        default=None,
        help="定價 (USD)。省略時互動式詢問",
    )
    p_publish.add_argument(
        "--period",
        choices=["day", "week", "month", "one-time"],
        default=None,
        help="變現週期。省略時互動式詢問",
    )

    # simulate
    p_sim = subparsers.add_parser("simulate", help="預估月收入")
    p_sim.add_argument("--price", type=float, required=True, help="定價 (USD)")
    p_sim.add_argument(
        "--period",
        choices=["day", "week", "month", "one-time"],
        default="week",
        help="變現週期（預設: week）",
    )
    p_sim.add_argument(
        "--subs",
        type=int,
        default=50,
        help="預估訂閱數（預設: 50）",
    )
    p_sim.add_argument(
        "--llm-cost",
        type=float,
        default=0.05,
        help="每次執行的 LLM 成本 (USD)，預設 0.05",
    )

    # check
    p_check = subparsers.add_parser("check", help="審核自檢")
    p_check.add_argument(
        "--skill",
        type=Path,
        required=True,
        help="包含 SKILL.md 的目錄路徑",
    )

    # status
    subparsers.add_parser("status", help="查已上架 skill 的銷售狀態")

    args = parser.parse_args()

    if args.command == "publish":
        return publish.run(args)
    elif args.command == "simulate":
        return simulate.run(args)
    elif args.command == "check":
        return check.run(args)
    elif args.command == "status":
        return status.run(args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
