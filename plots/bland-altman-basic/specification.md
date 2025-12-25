# bland-altman-basic: Bland-Altman Agreement Plot

## Description

A Bland-Altman plot (also known as a difference plot or Tukey mean-difference plot) visualizes the agreement between two measurement methods by plotting the difference against the average of paired observations. It displays the mean difference (bias) as a horizontal line and limits of agreement (mean ± 1.96 SD) to assess whether the methods are interchangeable within acceptable tolerances.

## Applications

- Comparing a new blood glucose meter against a laboratory reference standard in medical device validation
- Assessing inter-rater reliability between two observers measuring the same physiological parameter
- Evaluating whether two analytical chemistry methods produce equivalent results for quality control

## Data

- `method1` (numeric) - Measurements from the first method or observer
- `method2` (numeric) - Corresponding measurements from the second method or observer
- Size: 30-200 paired observations recommended for reliable limits of agreement estimation
- Example: Paired blood pressure readings from two different sphygmomanometers on the same subjects

## Notes

- The x-axis shows the mean of each pair: (method1 + method2) / 2
- The y-axis shows the difference: method1 - method2
- Include a horizontal line at the mean difference (bias)
- Include dashed horizontal lines at ±1.96 SD (95% limits of agreement)
- Annotate the mean and limits of agreement values on the plot
- Points should have moderate transparency to reveal overlapping observations
