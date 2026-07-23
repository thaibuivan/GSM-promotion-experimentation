# Statistical Foundations for A/B Testing (Week 4)

## 1. Hypothesis Testing Framework
A/B testing relies on the frequentist hypothesis testing framework to determine the statistical significance of observed differences between two groups. 

- **Null Hypothesis ($H_0$):** Assumes no difference between the Treatment and Control groups (i.e., the treatment effect is zero).
- **Alternative Hypothesis ($H_1$):** Assumes a statistically significant difference exists.

The decision to reject $H_0$ is based on the **P-value**, which represents the probability of observing a difference as extreme as the one measured, assuming $H_0$ is true. A pre-defined significance level ($\alpha = 0.05$) is used as the threshold. If the P-value < $\alpha$, $H_0$ is rejected.

## 2. Evaluation Criteria in A/B Testing
The analytical pipeline evaluates two distinct statistical requirements depending on the objective:

### 2.1. Sanity Checks (System Validation)
- **Objective:** To verify that the randomization algorithm evenly distributed users across groups, ensuring comparability.
- **Null Hypothesis ($H_0$):** Groups are perfectly balanced (Difference = 0).
- **Desired Outcome:** We expect to fail to reject $H_0$. Therefore, a **P-value > 0.05** is required to confirm the absence of bias or Sample Ratio Mismatch (SRM).

### 2.2. Overall Evaluation Criterion (OEC)
- **Objective:** To measure the true causal impact of the treatment (e.g., voucher promotion) on the primary metric (e.g., incremental rides).
- **Null Hypothesis ($H_0$):** The treatment has no effect (Difference = 0).
- **Desired Outcome:** We aim to reject $H_0$ to prove the treatment's efficacy. Therefore, a **P-value < 0.05** is required to conclude that the observed uplift is statistically significant and not due to random variance.

## 3. Financial Guardrails
In addition to statistical significance, practical significance is evaluated using financial guardrails. The **Return on Investment (ROI)** metric is calculated by netting the incremental gross revenue against the cost of the promotion (e.g., voucher issuance cost). A statistically significant OEC is only actionable if the corresponding ROI is positive, satisfying business profitability constraints.
