# Deep-Dive EDA Framework

## 1. Registered vs. Reported Accounts (The "Dormancy Gap")

**Objective:** Visualizing the discrepancy between Mobile Money Operator (MMO) reported "Registered Users" and Findex/Survey reported "Account Ownership".

### Visualization Technique: Overlaid Bar & Line Chart with Shade Area
- **X-Axis:** Year (2017 - 2024)
- **Bar Chart (Background):** `Registered Accounts (Millions)` [Source: Telebirr/M-Pesa Reports]
    - Represents the "Total Potential Addressable Market".
- **Line Chart (Foreground):** `Adult Population with Account (Millions)` [Source: Findex/NBE * Population]
    - Represents "Actual Verified Ownership".
- **Shaded Area (Red/Orange):** The gap between the Bar and Line.
    - **Label:** "Dormant / Multi-SIM Gap"
    - **Annotation:** Calculate the % of registered accounts that are likely dormant or duplicate SIMs.

### Alternative: Funnel Chart
1. **Top:** Total Mobile Connections (Sim Cards)
2. **Middle:** Registered Mobile Money Wallets
3. **Bottom:** Active (30-day) Mobile Money Wallets
*This clearly shows the drop-off at each stage of the funnel.*

---

## 2. 4G Coverage vs. Digital Payment Adoption (Dual-Axis)

*(Implemented in `src/eda_deep_dive.py`)*

---

## 3. Statistical Test: 'P2P/ATM Crossover' Impact

**Objective:** Determine if the moment P2P transaction volume exceeded ATM cash withdrawals (The "Crossover") caused a statistically significant structural break in overall usage trends.

### Methodology: Interrupted Time Series (ITS) Analysis
Since we have high-frequency data (monthly/quarterly) from NBE/EthSwitch:

1.  **Define Intervention Point ($T_0$):**
    - Date when P2P Volume > ATM Volume (e.g., Q3 2023).

2.  **Regression Model Formulation:**
    $$ Usage_t = \beta_0 + \beta_1 \times T_t + \beta_2 \times D_t + \beta_3 \times (T_t \times D_t) + \epsilon $$
    - $Usage_t$: Monthly Digital Payment Volume (Log-transformed).
    - $T_t$: Time trend (1, 2, 3...).
    - $D_t$: Dummy variable (0 before Crossover, 1 after).
    - $T_t \times D_t$: Slope change after crossover.

3.  **Hypothesis Testing:**
    - **Null Hypothesis ($H_0$):** $\beta_2 = 0$ and $\beta_3 = 0$ (No change in level or slope).
    - **Alternative ($H_1$):** $\beta_2 \neq 0$ or $\beta_3 > 0$ (Significant acceleration in usage).

4.  **Simpler Alternative (T-Test):**
    - Compare Mean Monthly Growth Rate of Usage *Before* vs. *After* the Crossover.
    - `scipy.stats.ttest_ind(growth_pre, growth_post)`

---

## 4. Gender Gap Analysis Framework

**Objective:** Assess if infrastructure rollouts (like Fayda or Telebirr) are closing the gender gap.

### Key Metrics & Ratios

#### A. The Gender Parity Index (GPI)
$$ GPI = \frac{\text{Female Value}}{\text{Male Value}} $$
- **Interpretation:**
    - GPI < 1: Disadvantage for women.
    - GPI = 1: Parity.
    - **Track GPI over time** for: Account Ownership, Digital Payment Usage, and Mobile Phone Ownership.

#### B. The "Infrastructure Reach" Ratio
To test if infrastructure benefits are equitable:
$$ Ratio = \frac{\Delta \text{Female Inclusion}}{\Delta \text{4G Coverage}} \text{ vs } \frac{\Delta \text{Male Inclusion}}{\Delta \text{4G Coverage}} $$
- **Goal:** See if 1% increase in 4G coverage converts to equal percentage points of inclusion for men and women.

#### C. Decomposition of the Gap (Blinder-Oaxaca Decomposition logic)
- **Question:** Is the gap due to *endowments* (lower income/education for women) or *coefficients* (discrimination/structural barriers)?
- **Action:** If you have microdata, run a regression:
    $$ Inclusion = \alpha + \beta_1(Female) + \beta_2(Income) + \beta_3(Education) + \beta_4(Phone) $$
    - If $\beta_1$ remains negative and significant after controlling for Income/Phone, the gap is structural (e.g., cultural norms, trust).
