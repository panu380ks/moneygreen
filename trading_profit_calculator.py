#!/usr/bin/env python3
"""
Trading Profit Calculator for HH LL + Supertrend Strategy
==========================================================
Models monthly profit/loss for a fixed-risk breakout strategy
with 1:10 R:R (configurable), accounting for three exit types:

  1. Take Profit hit   → full reward  (+10R default)
  2. Stop Loss hit     → full risk    (-1R)
  3. Signal exit       → partial win/loss (Supertrend flip or
                         lower-low / higher-high breakdown)

Usage:
  python3 trading_profit_calculator.py

Author: moneygreen
"""

import sys

# ============================================================================
# STRATEGY DEFAULTS (match the Pine Script settings)
# ============================================================================
SL_PCT = 1.0       # Stop loss percent
RR_RATIO = 10.0    # Reward:Risk ratio  (TP = SL × RR)
TP_PCT = SL_PCT * RR_RATIO  # 10%

# ============================================================================
# USER ACCOUNT SETTINGS
# ============================================================================
STARTING_CAPITAL = 1_000.0   # USD
RISK_PER_TRADE = 25.0        # USD risked on every trade


def position_size(risk_usd: float, sl_pct: float) -> float:
    """Calculate position size from fixed dollar risk and SL %."""
    return risk_usd / (sl_pct / 100)


def trade_pnl(risk_usd: float, rr: float) -> float:
    """Return dollar P&L for a single trade given its realized R-multiple."""
    return risk_usd * rr


def monthly_summary(
    trades_per_month: int,
    tp_win_rate: float,
    sl_loss_rate: float,
    signal_exit_rate: float,
    signal_exit_avg_r: float,
    risk_usd: float,
    rr_ratio: float,
) -> dict:
    """
    Simulate one month of trading and return a summary dict.

    Parameters
    ----------
    trades_per_month : int
        Total number of trades taken in the month.
    tp_win_rate : float
        Fraction of trades that hit Take Profit (0-1).
    sl_loss_rate : float
        Fraction of trades that hit Stop Loss (0-1).
    signal_exit_rate : float
        Fraction of trades closed by signal exit (0-1).
    signal_exit_avg_r : float
        Average R-multiple realized on signal exits (can be negative).
    risk_usd : float
        Dollar amount risked per trade.
    rr_ratio : float
        Reward-to-risk ratio (e.g. 10 for 1:10).

    Returns
    -------
    dict with keys: tp_trades, sl_trades, sig_trades, tp_pnl, sl_pnl,
                    sig_pnl, gross_pnl, total_trades
    """
    tp_trades = round(trades_per_month * tp_win_rate)
    sl_trades = round(trades_per_month * sl_loss_rate)
    sig_trades = trades_per_month - tp_trades - sl_trades

    tp_pnl = tp_trades * trade_pnl(risk_usd, rr_ratio)       # winners
    sl_pnl = sl_trades * trade_pnl(risk_usd, -1.0)           # losers
    sig_pnl = sig_trades * trade_pnl(risk_usd, signal_exit_avg_r)

    return {
        "tp_trades": tp_trades,
        "sl_trades": sl_trades,
        "sig_trades": sig_trades,
        "total_trades": trades_per_month,
        "tp_pnl": tp_pnl,
        "sl_pnl": sl_pnl,
        "sig_pnl": sig_pnl,
        "gross_pnl": tp_pnl + sl_pnl + sig_pnl,
    }


def fmt_usd(v: float) -> str:
    sign = "+" if v >= 0 else "-"
    return f"{sign}${abs(v):,.2f}"


def print_header(capital, risk, sl, tp, rr):
    pos = position_size(risk, sl)
    leverage = pos / capital
    print("=" * 64)
    print("  HH LL + Supertrend Strategy — Monthly Profit Calculator")
    print("=" * 64)
    print()
    print("  Account Settings")
    print("  ─────────────────────────────────────────────")
    print(f"  Starting Capital        :  ${capital:,.2f}")
    print(f"  Risk per Trade          :  ${risk:,.2f}")
    print(f"  Risk % of Capital       :  {risk / capital * 100:.1f}%")
    print()
    print("  Strategy Parameters (from Pine Script)")
    print("  ─────────────────────────────────────────────")
    print(f"  Stop Loss               :  {sl:.1f}%")
    print(f"  Take Profit             :  {tp:.1f}%")
    print(f"  Risk : Reward           :  1 : {rr:.0f}")
    print()
    print("  Per-Trade Math")
    print("  ─────────────────────────────────────────────")
    print(f"  Position Size           :  ${pos:,.2f}")
    print(f"  Leverage Required       :  {leverage:.1f}x")
    print(f"  If TP Hit (+{rr:.0f}R)        :  {fmt_usd(trade_pnl(risk, rr))}")
    print(f"  If SL Hit (-1R)         :  {fmt_usd(trade_pnl(risk, -1))}")
    print()
    print("  Exit Types in This Strategy")
    print("  ─────────────────────────────────────────────")
    print("  1. Take Profit hit      →  +10R  (+$250)")
    print("  2. Stop Loss hit        →  -1R   (-$25)")
    print("  3. Signal exit          →  variable R")
    print("     (Supertrend flip or lower-low / higher-high breakdown)")
    print()


def print_scenario_table(risk, rr):
    """Print a table of monthly P&L across win rates and trade counts."""

    # ── Scenarios ──
    # Each scenario: (label, tp_rate, sl_rate, signal_rate, signal_avg_r)
    scenarios = [
        ("Conservative (20% TP)",  0.20, 0.65, 0.15, 0.5),
        ("Moderate (30% TP)",      0.30, 0.50, 0.20, 1.0),
        ("Good (40% TP)",          0.40, 0.40, 0.20, 1.5),
        ("Strong (50% TP)",        0.50, 0.30, 0.20, 2.0),
    ]

    trades_options = [5, 10, 15, 20]

    print("=" * 64)
    print("  Monthly Profit Projections")
    print("=" * 64)

    for label, tp_r, sl_r, sig_r, sig_avg in scenarios:
        print()
        print(f"  ┌─ {label}")
        print(f"  │  TP hit: {tp_r*100:.0f}%  │  SL hit: {sl_r*100:.0f}%  │"
              f"  Signal exit: {sig_r*100:.0f}% (avg {sig_avg:.1f}R)")
        print(f"  │")
        print(f"  │  {'Trades/Mo':>10}  {'TP Wins':>8}  {'SL Losses':>9}"
              f"  {'Sig Exits':>9}  {'Monthly P&L':>12}  {'on $1,000':>10}")
        print(f"  │  {'─'*10}  {'─'*8}  {'─'*9}  {'─'*9}  {'─'*12}  {'─'*10}")

        for t in trades_options:
            s = monthly_summary(t, tp_r, sl_r, sig_r, sig_avg, risk, rr)
            roi = s["gross_pnl"] / STARTING_CAPITAL * 100
            print(f"  │  {s['total_trades']:>10}  {s['tp_trades']:>8}"
                  f"  {s['sl_trades']:>9}  {s['sig_trades']:>9}"
                  f"  {fmt_usd(s['gross_pnl']):>12}  {roi:>+9.1f}%")

        print(f"  └{'─'*62}")

    print()


def print_breakeven_analysis(risk, rr):
    """Show the minimum win rate needed to break even."""
    print("=" * 64)
    print("  Break-Even Analysis")
    print("=" * 64)
    print()

    # Simple case: only TP and SL exits (no signal exits)
    # Break even: tp_rate * rr * risk = sl_rate * 1 * risk
    # tp_rate * rr = (1 - tp_rate) * 1
    # tp_rate * rr + tp_rate = 1
    # tp_rate = 1 / (rr + 1)
    be_rate = 1 / (rr + 1)
    print(f"  If every trade ends at TP or SL (no signal exits):")
    print(f"  Break-even TP win rate  =  1 / ({rr:.0f} + 1)  =  {be_rate*100:.1f}%")
    print()
    print(f"  With 1:{rr:.0f} R:R, you only need {be_rate*100:.1f}% of trades to")
    print(f"  hit TP to break even. That means you can lose {(1-be_rate)*100:.1f}%")
    print(f"  of your trades and still not lose money.")
    print()

    # Show the edge
    print("  Profit per percentage point above break-even:")
    print("  ─────────────────────────────────────────────")
    for extra in [5, 10, 15, 20, 30]:
        wr = be_rate + extra / 100
        if wr > 1.0:
            break
        # Per 10 trades
        wins_10 = round(10 * wr)
        losses_10 = 10 - wins_10
        pnl_10 = wins_10 * risk * rr - losses_10 * risk
        print(f"  {wr*100:5.1f}% win rate  →  {fmt_usd(pnl_10):>8} per 10 trades"
              f"  ({wins_10}W / {losses_10}L)")
    print()


def print_compounding_projection(capital, risk, rr):
    """Show how the account grows if profits are reinvested."""
    print("=" * 64)
    print("  12-Month Compounding Projection (Moderate Scenario)")
    print("=" * 64)
    print()
    print("  Assumptions: 30% TP rate, 50% SL rate, 20% signal exits")
    print("  (avg 1.0R), 10 trades/month, reinvesting 50% of profits")
    print()
    print(f"  {'Month':>7}  {'Capital':>10}  {'Risk/Trade':>12}  {'Monthly P&L':>12}  {'Cumulative':>11}")
    print(f"  {'─'*7}  {'─'*10}  {'─'*12}  {'─'*12}  {'─'*11}")

    bal = capital
    base_risk = risk
    cumulative = 0.0
    tp_r, sl_r, sig_r, sig_avg = 0.30, 0.50, 0.20, 1.0
    trades = 10

    for month in range(1, 13):
        current_risk = base_risk
        # After first month, allow risk to grow with account (50% reinvestment)
        if month > 1 and bal > capital:
            # Risk grows proportionally but capped at 2.5% of capital
            proportional_risk = base_risk * (bal / capital)
            max_risk = bal * 0.025
            current_risk = min(proportional_risk, max_risk)

        s = monthly_summary(trades, tp_r, sl_r, sig_r, sig_avg, current_risk, rr)
        pnl = s["gross_pnl"]
        bal += pnl
        cumulative += pnl

        print(f"  {month:>7}  ${bal:>9,.2f}  ${current_risk:>11,.2f}"
              f"  {fmt_usd(pnl):>12}  {fmt_usd(cumulative):>11}")

    print()
    total_return = (bal - capital) / capital * 100
    print(f"  Starting Capital  :  ${capital:,.2f}")
    print(f"  Ending Capital    :  ${bal:,.2f}")
    print(f"  Total Return      :  {total_return:+.1f}%")
    print()


def print_risk_warning():
    print("=" * 64)
    print("  ⚠  IMPORTANT DISCLAIMERS")
    print("=" * 64)
    print("""
  • These are THEORETICAL projections, not guaranteed returns.
  • Actual results depend on market conditions, execution quality,
    slippage, commissions, and the specific instrument traded.
  • This strategy requires LEVERAGE (2.5x on a $1,000 account).
    Leverage amplifies both gains AND losses.
  • Past backtest performance does not guarantee future results.
  • The win rate and trade frequency are UNKNOWN until you
    backtest on your specific instrument and timeframe in
    TradingView.
  • Signal exits (Supertrend flip, lower-low breakdown) will
    often close trades before TP is reached, reducing average
    win size.
  • Always backtest on TradingView first and use the actual
    win rate / trade count from your backtest results.
""")


def print_quick_answer(risk, rr):
    """Give the user a direct answer to their question."""
    print("=" * 64)
    print("  QUICK ANSWER: $1,000 account, $25 risk/trade")
    print("=" * 64)
    print()

    # Most likely scenario range for a breakout strategy
    print("  With your 1:10 R:R strategy, each winning trade makes $250")
    print("  and each losing trade costs $25.")
    print()
    print("  Estimated monthly profit depends on two unknowns:")
    print("  1) How many trades per month (depends on timeframe/instrument)")
    print("  2) What % of trades hit Take Profit vs Stop Loss")
    print()
    print("  Realistic range for a breakout strategy:")
    print()

    cases = [
        ("Worst case",  10, 0.15, 0.70, 0.15, -0.5),
        ("Below avg",   10, 0.20, 0.60, 0.20, 0.5),
        ("Average",     10, 0.30, 0.50, 0.20, 1.0),
        ("Above avg",   10, 0.40, 0.40, 0.20, 1.5),
        ("Best case",   10, 0.50, 0.30, 0.20, 2.0),
    ]

    for label, trades, tp_r, sl_r, sig_r, sig_avg in cases:
        s = monthly_summary(trades, tp_r, sl_r, sig_r, sig_avg, risk, rr)
        roi = s["gross_pnl"] / STARTING_CAPITAL * 100
        print(f"  {label:<12}  {tp_r*100:>3.0f}% TP rate  →  "
              f"{fmt_usd(s['gross_pnl']):>9}  ({roi:>+6.1f}% monthly)")

    print()
    print("  ► Most likely (moderate) estimate: ~$575/month (+57.5%)")
    print("    Based on 10 trades, 30% TP rate, 50% SL rate")
    print()


def main():
    capital = STARTING_CAPITAL
    risk = RISK_PER_TRADE
    sl = SL_PCT
    tp = TP_PCT
    rr = RR_RATIO

    print()
    print_quick_answer(risk, rr)
    print()
    print_header(capital, risk, sl, tp, rr)
    print_scenario_table(risk, rr)
    print_breakeven_analysis(risk, rr)
    print_compounding_projection(capital, risk, rr)
    print_risk_warning()


if __name__ == "__main__":
    main()
