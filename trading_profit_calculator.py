#!/usr/bin/env python3
"""
Trading Profit Calculator — Real TradingView Backtest Data
============================================================
HH LL + Supertrend Strategy on Silver (XAGUSD)
Backtest period: Nov 2020 – Feb 2026 | 32 trades

Scales real performance metrics to a $1,000 account with $25 risk/trade.

Usage:
  python3 trading_profit_calculator.py
"""

import math

# ============================================================================
# REAL BACKTEST DATA (TradingView Strategy Tester)
# Instrument: Silver (XAGUSD) | Period: Nov 2020 – Feb 2026
# ============================================================================
INSTRUMENT = "Silver (XAGUSD)"
PERIOD = "Nov 2020 – Feb 2026"
PERIOD_MONTHS = 63.0

BT_CAPITAL = 100_000.0
BT_NET_PROFIT = 59_965.15
BT_NET_PROFIT_PCT = 59.97
BT_TOTAL_TRADES = 32
BT_WINNERS = 7
BT_LOSERS = 25
BT_WIN_RATE = 21.88
BT_PROFIT_FACTOR = 4.556
BT_MAX_DD = 6_828.50
BT_MAX_DD_PCT = 6.63
BT_AVG_TRADE = 1_873.91
BT_AVG_BARS = 71
BT_RISK_PER_TRADE = 1_000.0  # 1% SL on $100,000 position

# Derived from backtest
BT_GROSS_PROFIT = BT_NET_PROFIT * BT_PROFIT_FACTOR / (BT_PROFIT_FACTOR - 1)
BT_GROSS_LOSS = BT_GROSS_PROFIT / BT_PROFIT_FACTOR
BT_AVG_WIN = BT_GROSS_PROFIT / BT_WINNERS
BT_AVG_LOSS = BT_GROSS_LOSS / BT_LOSERS

# R-multiples (1R = risk per trade in the backtest)
AVG_WIN_R = BT_AVG_WIN / BT_RISK_PER_TRADE
AVG_LOSS_R = BT_AVG_LOSS / BT_RISK_PER_TRADE
EXPECTANCY_R = BT_AVG_TRADE / BT_RISK_PER_TRADE
MAX_DD_R = BT_MAX_DD / BT_RISK_PER_TRADE
TRADES_PER_MONTH = BT_TOTAL_TRADES / PERIOD_MONTHS
TRADES_PER_YEAR = TRADES_PER_MONTH * 12

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


def main():
    w = 66

    # Scale backtest R-multiples to user's $25 risk
    avg_win = AVG_WIN_R * RISK
    avg_loss = AVG_LOSS_R * RISK
    per_trade = EXPECTANCY_R * RISK
    max_dd = MAX_DD_R * RISK
    pos_size = RISK / (SL_PCT / 100)

    print()
    print("=" * w)
    print("  HH LL + SUPERTREND — REAL BACKTEST RESULTS")
    print("=" * w)
    print()

    # ── Source Data ──
    print(f"  Source     : TradingView Strategy Tester")
    print(f"  Strategy   : HH LL + ST Strategy")
    print(f"  Instrument : {INSTRUMENT}")
    print(f"  Period     : {PERIOD} ({PERIOD_MONTHS:.0f} months)")
    print()

    print("  Backtest Performance ($100,000 test capital)")
    print("  " + "─" * (w - 2))
    print(f"  Net Profit            {fmt(BT_NET_PROFIT):>14}   ({BT_NET_PROFIT_PCT:+.2f}%)")
    print(f"  Total Trades          {BT_TOTAL_TRADES:>14}")
    print(f"  Win Rate              {BT_WIN_RATE:>13.2f}%   ({BT_WINNERS}W / {BT_LOSERS}L)")
    print(f"  Profit Factor         {BT_PROFIT_FACTOR:>14.3f}")
    print(f"  Max Drawdown          {fmt(-BT_MAX_DD):>14}   ({BT_MAX_DD_PCT:.2f}%)")
    print(f"  Avg Trade             {fmt(BT_AVG_TRADE):>14}")
    print(f"  Avg Bars in Trade     {BT_AVG_BARS:>14}")
    print()
    print(f"  Avg Winning Trade     {fmt(BT_AVG_WIN):>14}   ({AVG_WIN_R:+.2f}R)")
    print(f"  Avg Losing Trade      {fmt(-BT_AVG_LOSS):>14}   ({-AVG_LOSS_R:+.2f}R)")
    print(f"  Expectancy/Trade      {EXPECTANCY_R:>+13.3f}R")
    print(f"  Trade Frequency       {TRADES_PER_MONTH:>10.2f}/month   ({TRADES_PER_YEAR:.1f}/year)")
    print()

    # ── Your Account ──
    print("=" * w)
    print("  YOUR ACCOUNT: $1,000 / $25 risk per trade")
    print("=" * w)
    print()

    print("  Position Sizing")
    print("  " + "─" * (w - 2))
    print(f"  Capital               ${CAPITAL:>13,.2f}")
    print(f"  Risk per Trade        ${RISK:>13,.2f}   ({RISK/CAPITAL*100:.1f}% of capital)")
    print(f"  Position Size         ${pos_size:>13,.2f}")
    print(f"  Leverage              {pos_size/CAPITAL:>13.1f}x")
    print(f"  Stop Loss             {SL_PCT:>13.1f}%")
    print(f"  Take Profit           {TP_PCT:>13.1f}%   (1:{RR:.0f} R:R)")
    print()

    print("  Per-Trade Economics (scaled from real data)")
    print("  " + "─" * (w - 2))
    print(f"  When you WIN          {fmt(avg_win):>14}   (avg {AVG_WIN_R:.2f}R)")
    print(f"  When you LOSE         {fmt(-avg_loss):>14}   (avg {AVG_LOSS_R:.2f}R)")
    print(f"  Expected per trade    {fmt(per_trade):>14}   ({EXPECTANCY_R:.3f}R)")
    print()

    sl_saving = RISK - avg_loss
    print(f"  Signal Exit Insight:")
    print(f"  Avg loss is only {AVG_LOSS_R:.2f}R, not the full -1R (-${RISK:.0f}).")
    print(f"  Signal exits cut losers early, saving ${sl_saving:.2f} per loss vs full SL.")
    print()

    # ── Projections ──
    monthly_pnl = TRADES_PER_MONTH * per_trade
    annual_pnl = TRADES_PER_YEAR * per_trade

    print("=" * w)
    print("  PROFIT PROJECTIONS")
    print("=" * w)
    print()

    print(f"  Monthly ({TRADES_PER_MONTH:.2f} trades/month avg)")
    print("  " + "─" * (w - 2))
    print(f"  Expected P&L          {fmt(monthly_pnl):>14}   ({monthly_pnl/CAPITAL*100:+.2f}%)")
    print()
    print(f"  Realistic month-to-month variation:")
    print(f"    No trade month      {'$0.00':>14}   (most common)")
    print(f"    1 loss month        {fmt(-avg_loss):>14}")
    print(f"    1 win month         {fmt(avg_win):>14}")
    print()

    print(f"  Annual ({TRADES_PER_YEAR:.1f} trades/year avg)")
    print("  " + "─" * (w - 2))
    print(f"  Expected P&L          {fmt(annual_pnl):>14}   ({annual_pnl/CAPITAL*100:+.1f}%)")
    print(f"  Wins per year         {TRADES_PER_YEAR * BT_WIN_RATE / 100:>14.1f}")
    print(f"  Losses per year       {TRADES_PER_YEAR * (100 - BT_WIN_RATE) / 100:>14.1f}")
    print(f"  Max expected DD       {fmt(-max_dd):>14}   ({BT_MAX_DD_PCT:.1f}% of capital)")
    print()

    # ── Break-Even ──
    be_rate = 1 / (RR + 1) * 100

    print("  Break-Even Analysis")
    print("  " + "─" * (w - 2))
    print(f"  Break-even win rate   {be_rate:>13.1f}%")
    print(f"  Your actual win rate  {BT_WIN_RATE:>13.2f}%")
    print(f"  Edge                  {BT_WIN_RATE - be_rate:>+13.2f}pp")
    print()
    print(f"  With {RR:.0f}:1 R:R, you need just {be_rate:.1f}% wins to break even.")
    print(f"  Your {BT_WIN_RATE:.1f}% rate is {BT_WIN_RATE - be_rate:.1f}pp above that threshold.")
    print(f"  Each winner covers ~{avg_win/avg_loss:.0f} losers — that's why you profit")
    print(f"  despite losing {100 - BT_WIN_RATE:.0f}% of trades.")
    print()

    # ── 5-Year Compounding Projection ──
    print("=" * w)
    print("  5-YEAR COMPOUNDING PROJECTION")
    print("=" * w)
    print()
    print(f"  Reinvest 50% of profits, increase risk proportionally")
    print(f"  Cap risk at 2.5% of account balance")
    print()
    print(f"  {'Year':>6}  {'Capital':>10}  {'Risk/Trade':>12}"
          f"  {'Trades':>7}  {'P&L':>11}  {'ROI':>7}")
    print(f"  {'─' * 6}  {'─' * 10}  {'─' * 12}"
          f"  {'─' * 7}  {'─' * 11}  {'─' * 7}")

    bal = CAPITAL
    base_risk = RISK

    for year in range(1, 6):
        current_risk = base_risk
        if bal > CAPITAL:
            growth = (bal - CAPITAL) / CAPITAL
            current_risk = base_risk * (1 + 0.5 * growth)
            max_risk = bal * 0.025
            current_risk = min(current_risk, max_risk)

        yr_pnl = TRADES_PER_YEAR * EXPECTANCY_R * current_risk
        roi = yr_pnl / bal * 100
        bal += yr_pnl

        print(f"  {year:>6}  ${bal:>9,.0f}  ${current_risk:>11,.2f}"
              f"  {TRADES_PER_YEAR:>7.1f}  {fmt(yr_pnl):>11}  {roi:>+6.1f}%")

    print()
    total_return = (bal - CAPITAL) / CAPITAL * 100
    print(f"  Starting   :  ${CAPITAL:,.2f}")
    print(f"  After 5yr  :  ${bal:,.2f}")
    print(f"  Return     :  {total_return:+.1f}%")
    print()

    # ── Key Takeaways ──
    print("=" * w)
    print("  KEY TAKEAWAYS")
    print("=" * w)
    print()
    print(f"  1. PROFITABLE: {fmt(annual_pnl)}/year on $1,000"
          f" ({annual_pnl / CAPITAL * 100:+.1f}% annual)")
    print()
    print(f"  2. LOW FREQUENCY: ~{TRADES_PER_YEAR:.0f} trades/year"
          f" ({TRADES_PER_MONTH:.1f}/month)")
    print(f"     Expect weeks or months between trades. Patience is essential.")
    print()
    print(f"  3. LOW WIN RATE ({BT_WIN_RATE:.0f}%) IS BY DESIGN")
    print(f"     7 wins out of 32 trades — but winners are"
          f" {avg_win / avg_loss:.0f}x larger.")
    print(f"     You WILL have long losing streaks. This is normal.")
    print()
    print(f"  4. MANAGEABLE RISK: {BT_MAX_DD_PCT:.1f}% max drawdown")
    print(f"     On $1,000 = -${CAPITAL * BT_MAX_DD_PCT / 100:,.2f} worst case"
          f" from backtest.")
    print()
    print(f"  5. SIGNAL EXITS HELP: Avg loss = {AVG_LOSS_R:.2f}R (not full -1R)")
    print(f"     The Supertrend filter protects capital on losing trades.")
    print()

    # ── Disclaimers ──
    print("=" * w)
    print("  DISCLAIMERS")
    print("=" * w)
    print()
    print("  - Based on 32 trades over 5+ years. Small sample size.")
    print("  - Past backtest performance does NOT guarantee future results.")
    print("  - Real trading includes slippage, spread, and commissions")
    print("    which may reduce returns vs backtest.")
    print("  - Requires 2.5x leverage on a $1,000 account.")
    print("  - Low trade frequency = lumpy, uneven income.")
    print("  - Consider paper trading first to validate live performance.")
    print()


if __name__ == "__main__":
    main()
