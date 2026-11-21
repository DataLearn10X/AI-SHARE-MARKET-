# Phase 3 – Advanced Stock Price Charting Engine

## Implemented

- Chart types: Candlestick, Line, Area
- Period filters: 1D, 1W, 1M, 3M, 6M, 1Y, 2Y, 3Y, 5Y, MAX
- Technical indicators: SMA 20/50/100/200, EMA 20, RSI 14, MACD, Bollinger Bands
- Volume bars with color by candle direction
- Benchmark comparison (Nifty 50 via ^NSEI, normalized)
- RSI and MACD sub-charts
- Range selector, zoom/pan, hover tooltips
- Source and timestamp disclosure (yfinance, delayed/unofficial)
- NaN close handling (incomplete current bar)

## Files
- `analytics/technical_indicators.py`
- `frontend/components/advanced_chart.py`
- `app.py` (Price History tab)

## Data Validation
- Uses actual historical OHLCV from yfinance
- No artificial candles
- Missing/NaN closes dropped
- Period mapping to provider-supported intervals
- Benchmark optional and normalized

## Performance
- Session-state caching of fetched DataFrame
- Indicators applied once on load
- No repeated API calls on rerun

## Limitations
- yfinance unofficial; intraday (1D) uses daily bars
- Corporate action adjustments depend on yfinance
- No real-time data
