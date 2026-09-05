# hermes-publisher

> 從 Claude Code / Codex / Hermes 一鍵把 SKILL.md 上架到 Capafy 販售。

## 為什麼

Capafy 官方 publisher skill 是「上傳介面」，但有 3 個痛點：
1. **手動填 agent-card** — 描述、定價、範例要自己寫
2. **不知道會不會過審核** — 上傳後才發現被拒要改 7 天
3. **不知道怎麼定價** — 隨便拍一個數字

`hermes-publisher` 補上這 3 件事。

## 安裝

```bash
git clone https://github.com/sean/hermes-publisher
cd hermes-publisher
pip install -e .
```

## 4 個指令

| 指令 | 用途 |
|---|---|
| `publish` | 偵測 SKILL.md 變更 → 自動產生 agent-card 草稿 → 推上 Capafy |
| `simulate` | 模擬不同價格 × 變現模式 × LLM 成本 → 預估月收入 |
| `check` | 對 Capafy 審核指南 8 條跑自檢，預測上架成功率 |
| `status` | 查你已上架 skill 的銷售狀態 |

## 範例

```bash
# 審核自檢
python -m hermes_publisher check --skill ./examples/hr-resume-screener

# 收益試算
python -m hermes_publisher simulate --price 9.99 --period week --subs 50

# 模擬上架（不真的上傳）
python -m hermes_publisher publish --skill ./examples/hr-resume-screener --dry-run

# 真的上架
python -m hermes_publisher publish --skill ./examples/hr-resume-screener

# 查狀態
python -m hermes_publisher status
```

## 範圍（明確不做）

- ❌ 鏈上結算（市場未成熟、法律複雜）
- ❌ 試用引擎（重跑 LLM 成本太高）
- ❌ 多平台抽象（目前只有 Capafy 一家）
- ❌ 網站 / Dashboard（用 Capafy 自己的後台）
- ❌ 金流（Capafy 抽 80%，你 0% 觸錢）

## 1 個月時程

| 週 | 工作 |
|---|---|
| Week 1 | 基礎建設 + 1 個真實 SKILL.md 上架 |
| Week 2 | check + simulate 指令（已完成） |
| Week 3 | publish 指令 + 親自用 3 次 |
| Week 4 | 找 5 個 Capafy creator 試用 + 收集回饋 |

## 開發

```bash
# 跑測試
pytest

# 格式化
ruff check .
```

## License

MIT


<!-- Last validated: 2026-09-06 by OpenClaw Overnight Dev -->
