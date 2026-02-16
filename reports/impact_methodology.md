# Association Matrix & Impact Methodology

## 1. Assigning "Impact Magnitudes" (Sparse Data)

**Problem:** We lack historical data for many Ethiopian events (e.g., liberalization).
**Solution:** Use "Comparable Country Evidence" to estimate coefficients (Impact Magnitudes).

### Methodology: The Proxy Transfer Function
$$ \text{Impact}_{ETH} = \text{Impact}_{PROXY} \times \text{Adjustment Factor} $$

#### Step-by-Step Guide
1.  **Identify Proxy Event:** Find a similar event in a country with robust data (e.g., Kenya M-Pesa 2007, India Aadhaar 2010).
2.  **Extract Base Magnitude:** Key metric change in the first 12-24 months.
    *   *Example:* M-Pesa lifted Kenya's inclusion by ~15pp in 3 years. Annualized impact $\approx 5pp/year$.
3.  **Apply Adjustment Factors:**
    *   **infrastructure_readiness:** Is Ethiopia's 4G/Agent network better or worse than the proxy country at launch? (e.g., Ethiopia 2021 > Kenya 2007, Factor = 1.2)
    *   **regulatory_friction:** Is the policy environment stricter? (e.g., KYC tiers, Factor = 0.8)
4.  **Final Estimate:**
    *   $5pp \times 1.2 \times 0.8 = 4.8pp$ lift over the adoption curve.

---

## 2. Event-Indicator Matrix Template

This matrix maps which events affect which indicators and by how much (predicted).

| Event ID | Event Name | Target Indicator | Predicted Lift (Total) | Duration (Months) | Proxy Case | Confidence |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **EVT_001** | Telebirr Launch | `USG_DIGITAL_PAYMENT` | +15% | 36 | Kenya (M-Pesa) | High |
| **EVT_002** | EthSwitch Interop | `USG_P2P_CTX` | +8% | 12 | Tanzania (Interoperability) | Med |
| **EVT_003** | Fayda ID Rollout | `ACC_OWNERSHIP` | +6% | 24 | India (Aadhaar) | High |
| **EVT_004** | FX Liberalization | `AFF_COST` | -10% (Cost decrease) | 6 | Nigeria (Float) | Low |

---

## 3. Modeling Lag Effects (The "Adoption Curve")

Impact is rarely immediate. We use a **Lag Distribution Function** (implemented in Python) to spread the "Total Lift" over time.

**Common Curves:**
*   **Linear Ramp:** Steady growth until maturity (Simple).
*   **S-Curve (Sigmoid):** Slow start -> Rapid Growth -> Saturation (Realistic for products).
*   **Decay:** Immediate shock -> Fade out (Realistic for one-time policy shocks like demonetization).

**Default Approach (Rolling Window):**
Distribute the total impact over a `window` of months using a weighted moving average or specific curve function.
