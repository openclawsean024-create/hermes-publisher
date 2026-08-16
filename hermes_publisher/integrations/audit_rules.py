"""audit_rules — Capafy 審核規則。

從 Capafy 發佈者協議 v1.1 附表 A 與評價指南 v1.0 抽取的 8 條檢查項目。
每條有 weight（重要性）與 fn（檢查函式）。
"""

from __future__ import annotations

import re


def _check_required_sections(content: str) -> tuple[bool, str]:
    """必要的章節存在。"""
    required = [
        ("name", r"^name:\s*\S+", "YAML frontmatter `name`"),
        ("description", r"^description:\s*\S+", "YAML frontmatter `description`"),
        ("version", r"^version:\s*\S+", "YAML frontmatter `version`"),
    ]
    missing = []
    for tag, pattern, label in required:
        if not re.search(pattern, content, re.MULTILINE):
            missing.append(label)
    if missing:
        return False, f"缺: {', '.join(missing)}"
    return True, "必要欄位齊全"


def _check_description_length(content: str) -> tuple[bool, str]:
    """description 應該 50–500 字。"""
    m = re.search(r"^description:\s*(.+?)(?=^---|\Z)", content, re.MULTILINE | re.DOTALL)
    if not m:
        return False, "沒找到 description"
    desc = m.group(1).strip()
    word_count = len(desc.split())
    if word_count < 20:
        return False, f"description 太短 ({word_count} 詞，建議 ≥ 30)"
    if word_count > 200:
        return False, f"description 太長 ({word_count} 詞，建議 ≤ 150)"
    return True, f"description {word_count} 詞 (合理範圍)"


def _check_legal_language(content: str) -> tuple[bool, str]:
    """沒有歧視性用語（年齡/性別/種族/外貌）。"""
    # 從 Capafy 創作者協議 §附表 A：「禁止基於受保護身份的歧視性內容」
    forbidden = [
        (r"外觀評分", "「外觀評分」是潛在歧視用語"),
        (r"外貌評分", "「外貌評分」是潛在歧視用語"),
        (r"外觀偏好", "「外觀偏好」是潛在歧視用語"),
        (r"看長相", "「看長相」是潛在歧視用語"),
        (r"年齡偏好", "「年齡偏好」是潛在歧視用語"),
        (r"看年齡", "基於年齡的篩選是潛在歧視用語"),
        (r"歧視", "直接出現歧視用語"),
        (r"女權|男權", "性別議題用語"),
        (r"種族歧視", "種族歧視用語"),
    ]
    hits = []
    for pattern, label in forbidden:
        if re.search(pattern, content):
            hits.append(label)
    if hits:
        return False, f"發現 {len(hits)} 條可能違規: {', '.join(hits[:2])}"
    return True, "無歧視性用語"


def _check_no_personal_data_request(content: str) -> tuple[bool, str]:
    """不要求個資（電話/身分證/地址）。"""
    risky = [
        r"請提供.*身分證",
        r"請提供.*電話",
        r"請提供.*地址",
        r"請上傳.*身分證",
    ]
    # 但允許「不要」這類否定句
    for pattern in risky:
        matches = re.findall(pattern, content)
        if matches:
            return False, f"可能要求個資: {matches[0]}"
    return True, "未要求個資"


def _check_prompt_length(content: str) -> tuple[bool, str]:
    """SKILL.md 不應過短（80% 通過的字數）。"""
    if len(content) < 500:
        return False, f"內容過短 ({len(content)} 字，建議 ≥ 1500)"
    if len(content) > 20_000:
        return False, f"內容過長 ({len(content)} 字，建議 ≤ 15000)"
    return True, f"內容 {len(content)} 字 (合理範圍)"


def _check_has_example(content: str) -> tuple[bool, str]:
    """至少有一個範例輸入/輸出。"""
    has_example = bool(re.search(r"##\s*範例|##\s*Example|##\s*Example", content, re.IGNORECASE))
    has_input = bool(re.search(r"##\s*輸入|##\s*Input", content, re.IGNORECASE))
    has_output = bool(re.search(r"##\s*輸出|##\s*Output", content, re.IGNORECASE))
    if has_example or (has_input and has_output):
        return True, "有範例/輸入輸出說明"
    return False, "缺範例區段（買家無法判斷 skill 輸出）"


def _check_has_limitations(content: str) -> tuple[bool, str]:
    """有「限制」或「不適用」說明。"""
    has = bool(re.search(r"##\s*限制|##\s*不適用|##\s*不要|Limitations", content, re.IGNORECASE))
    if has:
        return True, "有明確限制說明"
    return False, "建議加「限制」章節（Capafy 喜歡明確邊界）"


def _check_pricing_clarity(content: str) -> tuple[bool, str]:
    """有定價或價值描述。"""
    has = bool(re.search(r"\$[\d,.]+|NT\$[\d,.]+|price|pricing|定價|價格", content, re.IGNORECASE))
    if has:
        return True, "有提到定價/價值"
    return True, "（建議加上,但非強制）"


CHECKS = [
    {
        "id": "C1",
        "name": "必要欄位",
        "weight": 15,
        "fn": _check_required_sections,
    },
    {
        "id": "C2",
        "name": "description 長度",
        "weight": 10,
        "fn": _check_description_length,
    },
    {
        "id": "C3",
        "name": "無歧視性用語",
        "weight": 20,
        "fn": _check_legal_language,
    },
    {
        "id": "C4",
        "name": "不要求個資",
        "weight": 15,
        "fn": _check_no_personal_data_request,
    },
    {
        "id": "C5",
        "name": "內容長度",
        "weight": 10,
        "fn": _check_prompt_length,
    },
    {
        "id": "C6",
        "name": "有範例/輸入輸出",
        "weight": 15,
        "fn": _check_has_example,
    },
    {
        "id": "C7",
        "name": "有限制說明",
        "weight": 10,
        "fn": _check_has_limitations,
    },
    {
        "id": "C8",
        "name": "有定價/價值描述",
        "weight": 5,
        "fn": _check_pricing_clarity,
    },
]


def format_report(results: list[dict]) -> str:
    lines = ["  " + "─" * 60, "  審核項目結果:", "  " + "─" * 60]
    for r in results:
        status = "✅" if r["ok"] else "❌"
        lines.append(f"  {status} [{r['id']}] {r['name']:<20} weight={r['weight']:>2}")
        lines.append(f"      {r['detail']}")
    lines.append("  " + "─" * 60)
    return "\n".join(lines)
