# XRP/USD Trend + Mean Reversion Strategy

## Overview
A hybrid strategy combining **trend-following** (EMA crossover) with **mean-reversion** (RSI + VWAP) entries, designed for XRP/USD on the 1-hour timeframe.

## How It Works

### Trend Filter
- **Fast EMA (21)** above **Slow EMA (55)** = uptrend → only longs
- Fast EMA below Slow EMA = downtrend → only shorts

### Entry Logic

**Long Entry (all must be true):**
1. Uptrend confirmed (fast EMA > slow EMA)
2. RSI dips below 35 (oversold pullback)
3. Price is at or below VWAP (value zone)
4. Volume above 20-period average
5. Within active session hours (8-22 UTC default)

**Short Entry (all must be true):**
1. Downtrend confirmed (fast EMA < slow EMA)
2. RSI spikes above 65 (overbought bounce)
3. Price is at or above VWAP
4. Volume above 20-period average
5. Within active session hours

### Risk Management
- **Stop Loss:** 1.5x ATR(14) from entry
- **Take Profit:** 2.5x ATR(14) from entry (1.67 R:R ratio)
- **Trend Flip Exit:** Position closed immediately if EMAs cross against the trade
- **Position Size:** 10% of equity per trade (adjustable)

## Setup in TradingView

1. Open TradingView → Pine Editor
2. Paste the contents of `xrp_usd_strategy.pine`
3. Click "Add to Chart"
4. Set chart to **XRP/USD** (or XRPUSDT) on the **1H** timeframe
5. Open Strategy Settings to adjust parameters

## Recommended Pairs
- XRPUSD (Kraken, Bitstamp)
- XRPUSDT (Binance, Bybit)

## Parameters to Tune

| Parameter | Default | Range | Notes |
|-----------|---------|-------|-------|
| Fast EMA | 21 | 10-30 | Lower = more responsive |
| Slow EMA | 55 | 40-100 | Higher = stronger trend filter |
| RSI Oversold | 35 | 25-40 | Lower = fewer but higher-quality longs |
| RSI Overbought | 65 | 60-75 | Higher = fewer but higher-quality shorts |
| ATR Stop Mult | 1.5 | 1.0-2.0 | Tighter = more stops, less risk per trade |
| ATR TP Mult | 2.5 | 2.0-4.0 | Higher = larger wins, lower win rate |

## Current Market Context (March 2026)
XRP is consolidating in the $87-90B market cap range after a sharp decline from ~$160B. The strategy is well-suited for this environment because:
- **Ranging phase:** Mean-reversion entries catch pullbacks within the range
- **Trend filter:** Prevents fighting the dominant direction
- **VWAP anchor:** Ensures entries at fair value, not at extremes
