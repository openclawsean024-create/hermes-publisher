"""simulate — 模擬不同價格 × 變現模式 × LLM 成本 → 預估月收入。"""

from __future__ import annotations

# Capafy 抽成（從協議 §3.2 抽取）
PLATFORM_FEE = 0.20  # 平台 20%

# 訂閱/按小時才有平台沙箱費（LLM 成本前扣）
# 下載模式：創作者拿 100% - 平台費 = 80%
PERIODS_PER_MONTH = {
    "day": 30,
    "week": 4.33,  # 30/7
    "month": 1,
    "one-time": 1,  # 沒週期概念,給模擬用
}


def run(args) -> int:
    price = args.price
    period = args.period
    subs = args.subs
    llm_cost = args.llm_cost

    print(f"📊 收入模擬")
    print(f"   定價: ${price:.2f} / {period}")
    print(f"   預估訂閱數: {subs}")
    print(f"   LLM 成本 (每次執行): ${llm_cost:.3f}\n")

    # 不同變現模式
    rows = []
    for mode in ["訂閱", "按小時", "下載"]:
        gross_monthly = _gross_monthly(price, period, subs, mode)
        if gross_monthly == 0:
            continue
        llm_monthly = _llm_total(llm_cost, subs, mode)
        net_after_llm = gross_monthly - llm_monthly
        platform_fee = net_after_llm * PLATFORM_FEE
        creator_net = net_after_llm - platform_fee

        rows.append(
            {
                "mode": mode,
                "gross": gross_monthly,
                "llm": llm_monthly,
                "net_llm": net_after_llm,
                "platform_fee": platform_fee,
                "creator": creator_net,
            }
        )

    print(f"  {'模式':<8} {'毛收':>10} {'LLM 成本':>10} {'淨收入':>10} {'平台費':>10} {'你實拿':>10}")
    print("  " + "─" * 64)
    for r in rows:
        print(
            f"  {r['mode']:<8} "
            f"${r['gross']:>9.2f} "
            f"${r['llm']:>9.2f} "
            f"${r['net_llm']:>9.2f} "
            f"${r['platform_fee']:>9.2f} "
            f"${r['creator']:>9.2f}"
        )

    if rows:
        best = max(rows, key=lambda r: r["creator"])
        print(f"\n  💡 最佳模式: {best['mode']} (你實拿 ${best['creator']:.2f}/月)")

    # 變現點
    if rows and subs > 0:
        print(f"\n  🎯 損益兩平 (月入 $100):")
        for r in rows:
            if r["creator"] <= 0:
                continue
            needed = 100 / (r["creator"] / subs) if subs > 0 else float("inf")
            print(f"     {r['mode']:<8} 約 {needed:.0f} 個訂閱")

    return 0


def _gross_monthly(price: float, period: str, subs: int, mode: str) -> float:
    """毛收（不含 LLM 成本）"""
    if mode == "訂閱":
        # 訂閱每 sub 每月支付 = price × (30/週期天數)
        multiplier = PERIODS_PER_MONTH[period]
        return price * multiplier * subs
    elif mode == "按小時":
        # 按小時 = 一次性收 price，計算月銷量
        return price * subs
    elif mode == "下載":
        # 下載 = 一次性收 price
        return price * subs
    return 0


def _llm_total(llm_cost: float, subs: int, mode: str) -> float:
    """每月 LLM 成本（平台沙箱費）"""
    if mode == "訂閱":
        # 假設每人每月執行 5 次
        return llm_cost * subs * 5
    elif mode == "按小時":
        return llm_cost * subs
    return 0  # 下載模式沒有 LLM 成本
