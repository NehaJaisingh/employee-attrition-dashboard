import pandas as pd

# ------------------ LOAD DATA ------------------

data = pd.read_csv("hr_attrition_dataset.csv")

# ------------------ CLEAN DATA ------------------

data["AttritionReason"] = data["AttritionReason"].fillna("No Attrition")
data = data.drop("EmployeeID", axis=1)

# ------------------ PREDICTION FUNCTION ------------------

def predict_employee(row, time_frame):

    score = 0
    reasons = []

    if row["MonthlyIncome"] < 3000:
        score += 2
        reasons.append("Low Salary")

    if row["WorkLifeBalance"] <= 2:
        score += 2
        reasons.append("Poor Work-Life Balance")

    if row["OverTime"] == "Yes":
        score += 2
        reasons.append("Overtime")

    if row["StressLevel"] >= 7:
        score += 2
        reasons.append("High Stress")

    if row["JobSatisfaction"] <= 2:
        score += 2
        reasons.append("Low Job Satisfaction")

    # Risk classification
    if score >= 6:
        return "High Risk | Will Leave in 3 months | Reason: " + ", ".join(reasons)

    elif score >= 3:
        return "Medium Risk | May Leave in 6 months | Reason: " + ", ".join(reasons)

    else:
        return "Low Risk | Will Stay"


# ------------------ APPLY TO DATASET ------------------

results = []

for index, row in data.iterrows():
    prediction = predict_employee(row, 6)
    results.append(prediction)

data["Prediction"] = results

# ------------------ SHOW RESULTS ------------------

print("\nEmployees at Risk:\n")
print(data[data["Prediction"].str.contains("High Risk|Medium Risk")])

# ------------------ ACCURACY CALCULATION ------------------

correct = 0
total = len(data)

for index, row in data.iterrows():

    prediction = row["Prediction"]

    # Convert prediction → Yes/No
    if "High Risk" in prediction or "Medium Risk" in prediction:
        pred_label = "Yes"
    else:
        pred_label = "No"

    actual_label = row["Attrition"]

    if pred_label == actual_label:
        correct += 1

accuracy = correct / total

print("\nAccuracy:", round(accuracy * 100, 2), "%")

# ------------------ SUMMARY ------------------

print("\nSummary:\n")

print("High Risk Employees:", len(data[data["Prediction"].str.contains("High Risk")]))
print("Medium Risk Employees:", len(data[data["Prediction"].str.contains("Medium Risk")]))
print("Low Risk Employees:", len(data[data["Prediction"].str.contains("Low Risk")]))

# ------------------ SAMPLE OUTPUT ------------------

sample = data.iloc[0]
print("\nSample Prediction:\n", predict_employee(sample, 6))