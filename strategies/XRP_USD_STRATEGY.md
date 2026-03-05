# XRP/USD Short-Only Strategy

## Overview
A **short-only** strategy combining **trend-following** (EMA crossover) with **mean-reversion** (RSI + VWAP) entries, designed for XRP/USD on the 1-hour timeframe.

## How It Works

### Trend Filter
- **Fast EMA (21)** below **Slow EMA (55)** = downtrend confirmed → shorts enabled
- No trades taken when trend is bullish

### Entry Logic

**Short Entry (all must be true):**
1. Downtrend confirmed (fast EMA < slow EMA)
2. RSI spikes above 65 (overbought bounce into resistance)
3. Price is at or above VWAP (selling at premium)
4. Volume above 20-period average
5. Within active session hours (8-22 UTC default)

### Risk Management
- **Stop Loss:** 1.5x ATR(14) above entry
- **Take Profit:** 2.5x ATR(14) below entry (1.67 R:R ratio)
- **Trend Flip Exit:** Short closed immediately if EMAs cross bullish
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
| RSI Overbought | 65 | 60-75 | Higher = fewer but higher-quality shorts |
| ATR Stop Mult | 1.5 | 1.0-2.0 | Tighter = more stops, less risk per trade |
| ATR TP Mult | 2.5 | 2.0-4.0 | Higher = larger wins, lower win rate |

## Current Market Context (March 2026)
XRP is consolidating in the $87-90B market cap range after a sharp decline from ~$160B. A short-only approach fits because:
- **Bearish structure:** Price dropped hard and hasn't reclaimed prior highs
- **Sell the rips:** RSI overbought bounces within a downtrend are high-probability short entries
- **VWAP premium:** Only shorting above VWAP ensures you're selling at inflated prices
