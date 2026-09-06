# hermes-publisher · 變更日誌

---

## v3.0.2 — 2026-09-07

> v3.0.2 Fleet Alignment Upgrade by **Sean 10-repo-fleet** Worker

### Added
- `PRD/SPEC.md` — 從無到有建立 12 章規格書（§1–§9 標準 + §10 深度市調 + §11 技術債 + §12 Fleet 對齊摘要）
- `PRD/CHANGELOG.md` — 本檔
- `.github/workflows/ci.yml` — 4-job CI（ruff lint / pytest / compileall build / PyPI optional deploy）

### Validation
- `pytest -q` → ✅ **6/6 pass**（test_audit.py：test_check_healthy_skill / test_check_finds_in_skills_subdir / test_parse_skill_md_multiline_desc / test_check_required_sections / test_check_legal_language_flagged / test_simulate_subscription_math）
- Python 3.11.15 環境執行
- 既有 4 個指令（publish / simulate / check / status）全部可用

### Preserved
- `pyproject.toml` — 完整保留（setuptools + ruff + pytest config）
- `hermes_publisher/cli.py` + 4 commands — 不動
- `hermes_publisher/integrations/audit_rules.py` — Capafy 8 條規則不動
- `hermes_publisher/tests/test_audit.py` — 6 個 test case 不動
- `examples/hr-resume-screener/` — 不動
- `SKILL.md` + `README.md` — 不動
- `dashboard.html` — fleet 統一儀表板不動

### Notes
- Default branch = `main`
- 部署目標 = PyPI（手動，預留 `publish-pypi` job，需 `PYPI_TOKEN` secret）
- pre-existing ruff 11 warnings（unused `re`/`json`/`Path` + I001 + F541）— 不在 v3.0.2 範圍，預留 v3.0.3 修補
- 無 token 寫入 repo

---

## v0.1.0 — 2026-XX-XX (initial)

- MVP 初版（Sophia / Hermes）
- 4 個指令：publish / simulate / check / status
- Capafy 8 條審核規則（從 Capafy 發佈者協議 v1.1 附表 A + 評價指南 v1.0 抽取）
- 1 個範例 SKILL.md（hr-resume-screener）
- 6 個 pytest case（5 個 check + 1 個 simulate math）
- License: MIT
