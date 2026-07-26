# Titanic Survival Prediction — Logistic Regression

A binary classification model predicting passenger survival on the Titanic, built end-to-end: data cleaning, feature encoding, model training, and evaluation.

## Dataset
[Titanic dataset](https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv) — 891 passengers, 12 original features (class, sex, age, fare, family aboard, port of embarkation, etc.).

## Approach
1. **Data cleaning**
   - Filled missing `Age` with median age
   - Filled missing `Embarked` with the most common port
   - Dropped `Cabin` (77% missing), `PassengerId`, `Name`, `Ticket` (no predictive value)
2. **Feature encoding**
   - Label-encoded `Sex` (male=0, female=1)
   - One-hot encoded `Embarked` (`Embarked_Q`, `Embarked_S`)
3. **Modeling**
   - 80/20 train/test split
   - Logistic Regression (scikit-learn)

## Results
- **Accuracy:** 81.01%
- **Precision (survived):** 0.79
- **Recall (survived):** 0.74
- **F1-score (survived):** 0.76

## Key Insight
The model's learned coefficients confirm real historical patterns:
- **Sex** was the strongest predictor (+2.59) — women had far higher survival odds ("women and children first").
- **Pclass** was the second strongest (-0.94) — passengers in lower classes had significantly worse survival odds.
- Other features (fare, age, embarkation port, family size) contributed comparatively little.

## Tech Stack
`pandas` · `NumPy` · `scikit-learn`

## Next Steps
- Try tree-based models (Random Forest, XGBoost) for comparison
- Feature engineer titles extracted from `Name` (Mr/Mrs/Miss/Master)
- Hyperparameter tuning with cross-validation
