#!/usr/bin/env python3
"""
Trading Profit Calculator — Multi-Instrument Real Backtest Data
================================================================
HH LL + Supertrend Strategy on NAS100, Silver (XAGUSD), Gold (XAUUSD)

Scales real TradingView Strategy Tester performance to a $1,000 account
with $25 risk per trade across all three instruments.

Usage:
  python3 trading_profit_calculator.py
"""


# ============================================================================
# REAL BACKTEST DATA (TradingView Strategy Tester)
# ============================================================================

INSTRUMENTS = [
    {
        "name": "NAS100",
        "period": "Mar 2006 – Feb 2026",
        "period_months": 239.0,
        "bt_capital": 100_000.0,
        "net_profit": 27_240.49,
        "net_profit_pct": 27.24,
        "total_trades": 262,
        "winners": 56,
        "losers": 206,
        "win_rate": 21.37,
        "profit_factor": 1.221,
        "max_dd": 15_013.05,
        "max_dd_pct": 13.71,
        "risk_per_trade": 1_000.0,
    },
    {
        "name": "Silver (XAGUSD)",
        "period": "Nov 2020 – Feb 2026",
        "period_months": 63.0,
        "bt_capital": 100_000.0,
        "net_profit": 59_965.15,
        "net_profit_pct": 59.97,
        "total_trades": 32,
        "winners": 7,
        "losers": 25,
        "win_rate": 21.88,
        "profit_factor": 4.556,
        "max_dd": 6_828.50,
        "max_dd_pct": 6.63,
        "risk_per_trade": 1_000.0,
    },
    {
        "name": "Gold (XAUUSD)",
        "period": "Mar 2006 – Feb 2026",
        "period_months": 239.0,
        "bt_capital": 100_000.0,
        "net_profit": 8_625.83,
        "net_profit_pct": 8.63,
        "total_trades": 69,
        "winners": 12,
        "losers": 57,
        "win_rate": 17.39,
        "profit_factor": 1.292,
        "max_dd": 8_930.40,
        "max_dd_pct": 7.60,
        "risk_per_trade": 1_000.0,
    },
]

# ============================================================================
# USER ACCOUNT SETTINGS
# ============================================================================
CAPITAL = 1_000.0
RISK = 25.0
SL_PCT = 1.0
RR = 10.0
TP_PCT = SL_PCT * RR


def fmt(v):
    """Format a dollar value with sign."""
    return f"{'+' if v >= 0 else '-'}${abs(v):,.2f}"


def derive_metrics(inst):
    """Calculate derived R-multiples and frequencies from raw backtest data."""
    r = inst["risk_per_trade"]
    pf = inst["profit_factor"]
    net = inst["net_profit"]

    gross_profit = net * pf / (pf - 1)
    gross_loss = gross_profit / pf
    avg_win = gross_profit / inst["winners"]
    avg_loss = gross_loss / inst["losers"]
    avg_trade = net / inst["total_trades"]

    return {
        "gross_profit": gross_profit,
        "gross_loss": gross_loss,
        "avg_win": avg_win,
        "avg_loss": avg_loss,
        "avg_win_r": avg_win / r,
        "avg_loss_r": avg_loss / r,
        "expectancy_r": avg_trade / r,
        "max_dd_r": inst["max_dd"] / r,
        "trades_per_month": inst["total_trades"] / inst["period_months"],
        "trades_per_year": inst["total_trades"] / inst["period_months"] * 12,
        "r_per_month": (inst["total_trades"] / inst["period_months"])
        * (avg_trade / r),
    }


def main():
    w = 72

    # Pre-compute derived metrics for each instrument
    metrics = []
    for inst in INSTRUMENTS:
        m = derive_metrics(inst)
        metrics.append(m)

    print()
    print("=" * w)
    print("  HH LL + SUPERTREND — MULTI-INSTRUMENT REAL BACKTEST RESULTS")
    print("=" * w)
    print()
    print("  Source   : TradingView Strategy Tester")
    print("  Strategy : HH LL + ST Strategy")
    print(f"  Account  : ${CAPITAL:,.0f} capital / ${RISK:.0f} risk per trade")
    print()

    # ══════════════════════════════════════════════════════════════════════
    # PER-INSTRUMENT BREAKDOWN
    # ══════════════════════════════════════════════════════════════════════
    for inst, m in zip(INSTRUMENTS, metrics):
        print("─" * w)
        print(f"  {inst['name']}")
        print(f"  Period: {inst['period']} ({inst['period_months']:.0f} months)")
        print("─" * w)
        print()

        # Raw backtest stats
        print(f"  Net Profit            {fmt(inst['net_profit']):>14}"
              f"   ({inst['net_profit_pct']:+.2f}%)")
        print(f"  Total Trades          {inst['total_trades']:>14}")
        print(f"  Win Rate              {inst['win_rate']:>13.2f}%"
              f"   ({inst['winners']}W / {inst['losers']}L)")
        print(f"  Profit Factor         {inst['profit_factor']:>14.3f}")
        print(f"  Max Drawdown          {fmt(-inst['max_dd']):>14}"
              f"   ({inst['max_dd_pct']:.2f}%)")
        print()

        # R-multiples
        print(f"  Avg Winning Trade     {fmt(m['avg_win']):>14}"
              f"   ({m['avg_win_r']:+.2f}R)")
        print(f"  Avg Losing Trade      {fmt(-m['avg_loss']):>14}"
              f"   ({-m['avg_loss_r']:+.2f}R)")
        print(f"  Expectancy/Trade      {m['expectancy_r']:>+13.3f}R")
        print(f"  Trade Frequency       {m['trades_per_month']:>10.2f}/month"
              f"   ({m['trades_per_year']:.1f}/year)")
        print()

        # Scaled to $25 risk
        per_trade_usd = m["expectancy_r"] * RISK
        r_mo = m["r_per_month"]
        r_3mo = r_mo * 3
        pnl_mo = r_mo * RISK
        pnl_3mo = r_3mo * RISK

        print(f"  ┌─ Scaled to ${RISK:.0f} risk")
        print(f"  │  Per trade            {fmt(per_trade_usd):>14}"
              f"   ({m['expectancy_r']:+.3f}R)")
        print(f"  │  Per month            {fmt(pnl_mo):>14}"
              f"   ({r_mo:+.3f}R)")
        print(f"  │  Per 3 months         {fmt(pnl_3mo):>14}"
              f"   ({r_3mo:+.3f}R)")
        print(f"  └─")
        print()

    # ══════════════════════════════════════════════════════════════════════
    # COMBINED TOTALS
    # ══════════════════════════════════════════════════════════════════════
    total_r_month = sum(m["r_per_month"] for m in metrics)
    total_r_3mo = total_r_month * 3
    total_r_year = total_r_month * 12
    total_trades_month = sum(m["trades_per_month"] for m in metrics)
    total_trades_year = total_trades_month * 12

    total_pnl_month = total_r_month * RISK
    total_pnl_3mo = total_r_3mo * RISK
    total_pnl_year = total_r_year * RISK

    print("=" * w)
    print("  COMBINED TOTALS — ALL 3 INSTRUMENTS")
    print("=" * w)
    print()

    # Summary table header
    hdr = f"  {'':>20}  {'R':>10}  {'P&L ($25)':>12}  {'Trades':>8}"
    sep = f"  {'─' * 20}  {'─' * 10}  {'─' * 12}  {'─' * 8}"
    print(hdr)
    print(sep)

    # Per-instrument rows
    for inst, m in zip(INSTRUMENTS, metrics):
        label = inst["name"][:20]
        print(f"  {label:>20}  {m['r_per_month']:>+10.3f}  "
              f"{fmt(m['r_per_month'] * RISK):>12}  "
              f"{m['trades_per_month']:>8.2f}")

    print(sep)
    print(f"  {'TOTAL / MONTH':>20}  {total_r_month:>+10.3f}  "
          f"{fmt(total_pnl_month):>12}  {total_trades_month:>8.2f}")
    print()

    # 3-month and annual
    print(f"  {'TOTAL / 3 MONTHS':>20}  {total_r_3mo:>+10.3f}  "
          f"{fmt(total_pnl_3mo):>12}  {total_trades_month * 3:>8.1f}")
    print(f"  {'TOTAL / YEAR':>20}  {total_r_year:>+10.3f}  "
          f"{fmt(total_pnl_year):>12}  {total_trades_year:>8.1f}")
    print()

    # Monthly ROI
    print(f"  Monthly ROI on ${CAPITAL:,.0f}   :  {total_pnl_month / CAPITAL * 100:+.2f}%")
    print(f"  Annual ROI on ${CAPITAL:,.0f}    :  {total_pnl_year / CAPITAL * 100:+.1f}%")
    print()

    # ══════════════════════════════════════════════════════════════════════
    # MONTHLY BREAKDOWN — WHAT TO EXPECT
    # ══════════════════════════════════════════════════════════════════════
    print("=" * w)
    print("  MONTHLY BREAKDOWN — WHAT TO EXPECT")
    print("=" * w)
    print()
    print(f"  Combined trade frequency: {total_trades_month:.2f} trades/month"
          f" ({total_trades_year:.0f}/year)")
    print()

    for inst, m in zip(INSTRUMENTS, metrics):
        print(f"  {inst['name']:.<25} {m['trades_per_month']:.2f}/month"
              f"  (1 trade every {1/m['trades_per_month']:.0f} months)"
              if m['trades_per_month'] < 1 else
              f"  {inst['name']:.<25} {m['trades_per_month']:.2f}/month"
              f"  (~{m['trades_per_month']:.1f} trades/month)")

    print()
    print(f"  Across all 3 instruments you get ~{total_trades_month:.1f} trades/month")
    print(f"  combined, which means more consistent monthly activity.")
    print()

    # ══════════════════════════════════════════════════════════════════════
    # INSTRUMENT COMPARISON
    # ══════════════════════════════════════════════════════════════════════
    print("=" * w)
    print("  INSTRUMENT COMPARISON")
    print("=" * w)
    print()

    hdr2 = (f"  {'Metric':<22}  {'NAS100':>10}  {'Silver':>10}  {'Gold':>10}")
    sep2 = (f"  {'─' * 22}  {'─' * 10}  {'─' * 10}  {'─' * 10}")
    print(hdr2)
    print(sep2)

    labels = [
        ("Win Rate", lambda m, i: f"{INSTRUMENTS[i]['win_rate']:.1f}%"),
        ("Profit Factor", lambda m, i: f"{INSTRUMENTS[i]['profit_factor']:.3f}"),
        ("Avg Win (R)", lambda m, i: f"{m['avg_win_r']:+.2f}R"),
        ("Avg Loss (R)", lambda m, i: f"{-m['avg_loss_r']:+.2f}R"),
        ("Expectancy (R)", lambda m, i: f"{m['expectancy_r']:+.3f}R"),
        ("R/Month", lambda m, i: f"{m['r_per_month']:+.3f}R"),
        ("Trades/Year", lambda m, i: f"{m['trades_per_year']:.1f}"),
        ("Max DD %", lambda m, i: f"{INSTRUMENTS[i]['max_dd_pct']:.1f}%"),
    ]

    for label, fn in labels:
        vals = [fn(metrics[i], i) for i in range(3)]
        print(f"  {label:<22}  {vals[0]:>10}  {vals[1]:>10}  {vals[2]:>10}")

    print()

    # Best performer callout
    best_r = max(range(3), key=lambda i: metrics[i]["r_per_month"])
    print(f"  Best R/month: {INSTRUMENTS[best_r]['name']}"
          f" ({metrics[best_r]['r_per_month']:+.3f}R)")
    most_trades = max(range(3), key=lambda i: metrics[i]["trades_per_year"])
    print(f"  Most active:  {INSTRUMENTS[most_trades]['name']}"
          f" ({metrics[most_trades]['trades_per_year']:.1f} trades/year)")
    best_pf = max(range(3), key=lambda i: INSTRUMENTS[i]["profit_factor"])
    print(f"  Best PF:      {INSTRUMENTS[best_pf]['name']}"
          f" ({INSTRUMENTS[best_pf]['profit_factor']:.3f})")
    print()

    # ══════════════════════════════════════════════════════════════════════
    # BREAK-EVEN ANALYSIS
    # ══════════════════════════════════════════════════════════════════════
    be_rate = 1 / (RR + 1) * 100

    print("=" * w)
    print("  BREAK-EVEN ANALYSIS")
    print("=" * w)
    print()
    print(f"  Theoretical break-even with {RR:.0f}:1 R:R = {be_rate:.1f}% win rate")
    print()

    for inst, m in zip(INSTRUMENTS, metrics):
        edge = inst["win_rate"] - be_rate
        status = "ABOVE" if edge > 0 else "BELOW"
        print(f"  {inst['name']:<20}  {inst['win_rate']:>5.1f}% win rate"
              f"  →  {edge:+.1f}pp {status} break-even")

    print()
    print(f"  All three instruments beat the {be_rate:.1f}% break-even threshold.")
    print(f"  The 10:1 R:R means you can lose 90% of trades and still break even.")
    print()

    # ══════════════════════════════════════════════════════════════════════
    # 5-YEAR COMPOUNDING PROJECTION (Combined)
    # ══════════════════════════════════════════════════════════════════════
    combined_expectancy_r = total_r_month / total_trades_month if total_trades_month > 0 else 0

    print("=" * w)
    print("  5-YEAR COMPOUNDING PROJECTION (All 3 Combined)")
    print("=" * w)
    print()
    print(f"  Reinvest 50% of profits, cap risk at 2.5% of balance")
    print(f"  Combined: {total_trades_year:.0f} trades/year,"
          f" {combined_expectancy_r:+.3f}R avg expectancy")
    print()
    print(f"  {'Year':>6}  {'Capital':>10}  {'Risk/Trade':>12}"
          f"  {'Trades':>7}  {'P&L':>12}  {'ROI':>7}")
    print(f"  {'─' * 6}  {'─' * 10}  {'─' * 12}"
          f"  {'─' * 7}  {'─' * 12}  {'─' * 7}")

    bal = CAPITAL
    base_risk = RISK

    for year in range(1, 6):
        current_risk = base_risk
        if bal > CAPITAL:
            growth = (bal - CAPITAL) / CAPITAL
            current_risk = base_risk * (1 + 0.5 * growth)
            max_risk = bal * 0.025
            current_risk = min(current_risk, max_risk)

        yr_pnl = total_trades_year * combined_expectancy_r * current_risk
        roi = yr_pnl / bal * 100
        bal += yr_pnl

        print(f"  {year:>6}  ${bal:>9,.0f}  ${current_risk:>11,.2f}"
              f"  {total_trades_year:>7.0f}  {fmt(yr_pnl):>12}  {roi:>+6.1f}%")

    print()
    total_return = (bal - CAPITAL) / CAPITAL * 100
    print(f"  Starting   :  ${CAPITAL:,.2f}")
    print(f"  After 5yr  :  ${bal:,.2f}")
    print(f"  Return     :  {total_return:+.1f}%")
    print()

    # ══════════════════════════════════════════════════════════════════════
    # KEY TAKEAWAYS
    # ══════════════════════════════════════════════════════════════════════
    print("=" * w)
    print("  KEY TAKEAWAYS")
    print("=" * w)
    print()
    print(f"  1. COMBINED: {fmt(total_pnl_year)}/year on $1,000"
          f" ({total_pnl_year / CAPITAL * 100:+.1f}% annual)")
    print(f"     {total_r_year:+.2f}R per year across all 3 instruments")
    print()
    print(f"  2. SILVER IS THE STAR: {metrics[1]['r_per_month']:+.3f}R/month")
    print(f"     Highest expectancy per trade ({metrics[1]['expectancy_r']:+.3f}R)"
          f" and best profit factor ({INSTRUMENTS[1]['profit_factor']:.3f})")
    print()
    print(f"  3. NAS100 ADDS VOLUME: {metrics[0]['trades_per_year']:.0f} trades/year")
    print(f"     Lower R per trade ({metrics[0]['expectancy_r']:+.3f}R) but many more"
          f" opportunities")
    print()
    print(f"  4. GOLD IS MODEST: {metrics[2]['r_per_month']:+.3f}R/month")
    print(f"     Lowest win rate ({INSTRUMENTS[2]['win_rate']:.1f}%) and fewest trades,"
          f" but still profitable")
    print()
    print(f"  5. DIVERSIFICATION HELPS: {total_trades_month:.1f} combined trades/month")
    print(f"     vs 0.5/month with Silver alone — much more consistent activity")
    print()

    # ══════════════════════════════════════════════════════════════════════
    # DISCLAIMERS
    # ══════════════════════════════════════════════════════════════════════
    print("=" * w)
    print("  DISCLAIMERS")
    print("=" * w)
    print()
    print("  - NAS100 & Gold backtests span 20 years; Silver only 5 years.")
    print("    Different sample sizes may affect reliability of comparisons.")
    print("  - Past backtest performance does NOT guarantee future results.")
    print("  - Real trading includes slippage, spread, and commissions")
    print("    which may reduce returns vs backtest.")
    print("  - Requires 2.5x leverage on a $1,000 account.")
    print("  - Trading 3 instruments simultaneously requires managing")
    print("    multiple positions — total risk exposure may overlap.")
    print("  - Consider paper trading first to validate live performance.")
    print()


if __name__ == "__main__":
    main()
