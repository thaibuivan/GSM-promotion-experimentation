# Technical Report: Causal Inference & Synthetic Data Generation (Week 2)

## 1. Introduction and Objectives
Observational data often contains inherent biases due to confounding variables, making it unsuitable for direct causal measurement. For instance, an observed correlation between voucher usage and increased ride frequency may be confounded by external factors such as weather conditions or peak hour demand.

To establish a robust foundation for A/B testing and to evaluate the experimental pipeline, this phase focuses on constructing a Structural Causal Model (SCM) and generating a synthetic dataset. This approach allows for the introduction of a known ground-truth treatment effect, enabling the validation of the subsequent statistical testing methodologies.

## 2. Structural Causal Model (SCM) Design
The synthetic data generation process is defined in `notebooks/week2_synthetic_data/2_complex_data_generation.ipynb`. The methodology incorporates the following components:

### 2.1. User Profile Generation
User characteristics are simulated using standard probability distributions to reflect real-world demographics:
- **Age:** Generated using a Normal Distribution.
- **Income:** Generated using a Log-normal Distribution to account for right-skewness typical of income data.
- **Historical Ride Frequency:** Derived through interpolation based on age and income brackets.

### 2.2. Confounding Variables Integration
To simulate environmental factors that simultaneously affect both treatment assignment (propensity to use a voucher) and the outcome (ride frequency), the following confounders are introduced:
- **Hour Demand Multiplier:** A time-series multiplier reflecting rush hour peaks (e.g., 07:00-09:00 and 17:00-19:00).
- **Weather Conditions:** A binomial variable simulating rain probability, which acts as a positive shock to ride demand.

### 2.3. Outcome Variable Formulation
The SCM defines two primary outcome variables to isolate the causal effect:
1. **Observational Outcome (`y_obs`):** The natural number of rides, formulated as a function of the user profile and confounding variables, excluding any voucher effect.
2. **Experimental Outcome (`y_rand`):** The outcome under a Randomized Controlled Trial (RCT) setting. A predefined constant `treatment_effect` is added to `y_obs` strictly for users randomly assigned to the treatment group.

## 3. Conclusion
By engineering a synthetic dataset with a predefined causal structure, the project successfully decouples the true treatment effect from observational noise. This dataset serves as a rigorous testing ground for the segmentation and A/B testing analyses conducted in subsequent phases, ensuring that the statistical models applied are capable of accurately identifying causal impact amidst simulated confounding factors.
