---
name: hermes-publisher
description: |
  從 Claude Code / Codex / Hermes Agent 內一鍵把 SKILL.md 上架到 Capafy 販售。
  包含 4 個指令：publish / simulate / check / status。
  Use when user 寫好 SKILL.md 並說「上架」、「賣」、「發布」到 Capafy 時。
version: 0.1.0
author: Sean
license: MIT
---

# hermes-publisher

從你的 agent client（Claude Code / Codex / Hermes）出發，**一個指令**把
本地 SKILL.md 包裝成 Capafy 可販售的 Agent。

## 為什麼需要這個工具

Capafy 官方提供的 publisher skill 是「上傳介面」，但有 3 個痛點：
1. **手動填 agent-card** — 描述、定價、範例要自己寫
2. **不知道會不會過審核** — 上傳後才發現被拒要改 7 天
3. **不知道怎麼定價** — 隨便拍一個數字

`hermes-publisher` 補上這 3 件事。

## 指令

| 指令 | 用途 |
|---|---|
| `publish` | 偵測 SKILL.md 變更 → 自動產生 agent-card 草稿 → 推上 Capafy |
| `simulate` | 模擬不同價格 × 變現模式 × LLM 成本 → 預估月收入 |
| `check` | 對 Capafy 審核指南 8 條跑一遍，預測上架成功率 |
| `status` | 查你已上架 skill 的銷售狀態 |

## 安裝

```bash
git clone https://github.com/sean/hermes-publisher
cd hermes-publisher
pip install -e .
```

## 設定

需要 Capafy 帳號 + Capafy-publisher skill 已安裝。
第一次使用會引導你授權。

## 範例

```bash
# 檢查我的 SKILL.md 會不會通過 Capafy 審核
python -m hermes_publisher check --skill ./my-skills/hr-screener

# 模擬「$9.99/週」訂閱的收入
python -m hermes_publisher simulate --price 9.99 --period week --subs 50

# 真的上架
python -m hermes_publisher publish --skill ./my-skills/hr-screener

# 看銷售狀態
python -m hermes_publisher status
```

## 範圍限制

- 只支援 Capafy 一家（目前全球唯一在營運的 skill 市集）
- 不碰金流（Capafy 抽 80%，你 0% 觸錢）
- 不做鏈上結算（市場未成熟）
- 不做試用引擎（重跑 LLM 成本太高）

## 6 個月後擴展

- 第 2 家平台出現時，加 adapter
- 鏈上結算成本下降時，加可選 feature
- 100 個 creator 後，加 dashboard + Discord community
