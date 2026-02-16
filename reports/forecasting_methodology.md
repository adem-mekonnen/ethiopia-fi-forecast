# Forecasting Methodology: Trend + Event Shocks

## 1. Why "Trend + Shocks" vs. ARIMA?

**The Limit of Small N:**
We only have 5 historical data points (Findex 2011, 2014, 2017, 2021, 2024).
- **ARIMA (Auto-Regressive Integrated Moving Average):** Requires at least 30-50 data points to identify seasonality and autocorrelation structures reliable. With N=5, ARIMA will overfit or fail to converge.
- **Trend + Shocks:** This "Structural" approach is robust for sparse data.
    - **Trend Component:** Fits a simple line/curve to the history (The "Business as Usual" path).
    - **Shock Component:** Manually superimposes the estimated impact of known future events (The "Structural Breaks").

**Formula:**
$$ Y_{2026} = (m \times 2026 + c) + \sum (\text{Event Impact}_{2026}) $$

---

## 3. Scenario Definitions (2025-2027)

We define three scenarios based on the **success rate** of key upcoming infrastructure projects.

### A. Base Case (Status Quo)
*   **Assumptions:** Projects rollout on schedule but with typical friction.
*   **Multipliers:**
    *   **2025 Interoperability (EthSwitch):** 1.0x Impact (Full effect).
    *   **Fayda Digital ID:** 0.8x Impact (80% enrollment target met).
    *   **Liberalization:** Neutral (Short term inflation balances out efficiency gains).

### B. Optimistic Case (Digital Leap)
*   **Assumptions:** Rapid adoption, seamless interoperability, and aggressive policy support.
*   **Multipliers:**
    *   **2025 Interoperability:** 1.2x Impact (Network effects kick in).
    *   **Fayda Digital ID:** 1.1x Impact (Exceeds targets).
    *   **GenAI / Fintech Innovation:** Adds a +2% unreported "Innovation Boost".

### C. Pessimistic Case (Stagflation/Instability)
*   **Assumptions:** Macroeconomic shocks (inflation > 30%), internet disruptions, or delayed projects.
*   **Multipliers:**
    *   **2025 Interoperability:** 0.5x Impact (Technical glitches or low adoption).
    *   **Fayda Digital ID:** 0.4x Impact (Rollout stalls).
    *   **Macro Shock:** Applies a flat -5% penalty to "Affordability" driven usage.
