# Long-only Strategy v1.1 Backtest Summary (2017-2025)

## 資料生成流程

### 1. 資料來源
| 來源 | 年份 | 說明 |
|------|------|------|
| `long_only_test_2017_2018_*.csv` | 2017-2018 | 歷史 LLM 分析結果 |
| `long_only_test_2019_2024_combined.csv` | 2019-2024 | 歷史 LLM 分析結果 |
| `long_only_test_2025_*.csv` | 2025 | 最新 LLM 分析結果 |

### 2. Earnings Date 補齊
- **來源**: PostgreSQL `pead_reversal.earnings_surprises` 表
- **資料量**: 415,891 筆 (2017-2025)
- **填補結果**: 1,741 筆 reaction_date 從 PostgreSQL 補齊

### 3. 價格資料
- **來源**: Whaleforce Backtest API (`https://backtest.api.whaleforce.dev`)
- **格式**: Per-symbol OHLCV CSV
- **存放**: `backtest_tools/prices/`

---

## Backtest 設定 (v1.1-live-safe)

### Entry/Exit 規則
| 參數 | 設定值 | 說明 |
|------|--------|------|
| Decision Time | Earnings reaction day close | 財報反應日收盤做決策 |
| Entry | T+1 Open | 下一交易日開盤進場 |
| Exit | T+31 Close | 進場後 30 個交易日收盤出場 |

### Position Sizing
| 參數 | 設定值 |
|------|--------|
| CAP per Quarter | 12 | 
| Max Concurrent Positions | 12 |
| Allocation | 1/12 Equal Weight |

### Costs
| 參數 | 設定值 |
|------|--------|
| Commission | 0 bps |
| Slippage | 0 bps |

### Trading Calendar
- XNYS (NYSE)

---

## Backtest 結果

### 績效指標
| 指標 | 數值 |
|------|------|
| **Total Return** | 197.27% |
| **CAGR (ARR)** | 13.47% |
| **Annual Vol** | 6.43% |
| **Sharpe Ratio** | 2.00 |
| **Sortino Ratio** | 3.63 |
| **Max Drawdown** | -5.73% |
| **Calmar Ratio** | 2.35 |

### 交易統計
| 指標 | 數值 |
|------|------|
| Total Trades | 179 |
| Win Rate | 78.77% |
| Profit Factor | 5.93 |
| Avg Win | +11.56% |
| Avg Loss | -7.23% |
| Avg Exposure | 21.05% |

### 按年份統計
| Year | Trades | Avg Return | Win Rate |
|------|--------|------------|----------|
| 2017 | 37 | +5.0% | 86.5% |
| 2018 | 30 | +4.0% | 66.7% |
| 2019 | 3 | +4.0% | 66.7% |
| 2020 | 12 | +16.0% | 91.7% |
| 2021 | 28 | +8.0% | 85.7% |
| 2022 | 25 | +7.0% | 68.0% |
| 2023 | 25 | +12.0% | 80.0% |
| 2024 | 15 | +7.0% | 80.0% |
| 2025 | 4 | +7.0% | 75.0% |

---

## 輸出文件

| 文件 | 說明 |
|------|------|
| `signals_backtest_ready.csv` | 完整 signals (3,388 樣本) |
| `long_only_signals_2017_2025_final.csv` | trade_long=True 的 signals (266 筆) |
| `backtest_trades_2017_2025_final.csv` | 實際執行的交易 (179 筆) |
| `out_backtest_complete/nav.csv` | 每日 NAV |
| `out_backtest_complete/trades.csv` | 交易明細 |
| `out_backtest_complete/metrics.json` | 績效指標 JSON |

---

## Two-Tier Selection 規則

### Tier 1: D7 CORE (Direction Score ≥ 7)
- `LONG_D7_MIN_POSITIVES=0`
- `LONG_D7_MIN_DAY_RET=1.5`
- `LONG_D7_REQUIRE_EPS_POS=1`

### Tier 2: D6 STRICT (Direction Score = 6)
- `LONG_D6_MIN_EPS_SURPRISE=0.0`
- `LONG_D6_MIN_POSITIVES=1`
- `LONG_D6_MIN_DAY_RET=1.0`

---

Generated: 2026-01-01
