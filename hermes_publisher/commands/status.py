"""status — 查已上架 skill 的銷售狀態。

MVP 階段: 用 Capafy 創作者後台 API 抓資料。
若沒裝 capafy-publisher CLI，回報「需要先 OAuth 認證」。
"""

from __future__ import annotations

import shutil
import subprocess


def run(args) -> int:
    capafy_cli = shutil.which("capafy-publisher")
    if capafy_cli is None:
        print("⚠️  找不到 capafy-publisher CLI")
        print()
        print("請先安裝 Capafy Publisher Skill:")
        print("  https://capafy.ai/zh-hant/developer/doc/2.2")
        return 1

    result = subprocess.run([capafy_cli, "status"], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ 抓取狀態失敗: {result.stderr}")
        return 1

    print("📊 你的 Capafy 銷售狀態:")
    print()
    print(result.stdout)
    return 0
