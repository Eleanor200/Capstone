import pandas as pd
import numpy as np
import pickle

# Load the model
model_path = 'logistic_regression_model.pkl'
with open(model_path, 'rb') as file:
    model = pickle.load(file)

def preprocess_input(data):
    df = pd.DataFrame(data, index=[0])
    
    # Convert to numeric and handle any missing values or strings that cannot be converted
    for column in ['LoanAmount', 'ApplicantIncome', 'CoapplicantIncome']:
        df[column] = pd.to_numeric(df[column], errors='coerce').fillna(0)
        
    # Preprocessing the binary Credit_History feature
    df['Credit_History'] = 1.0 if data['Credit_History'] == 'Yes' else 0.0
    
    # Log transformation of LoanAmount and Total_Income to normalize their distribution
    df['LoanAmount_log'] = np.log(data['LoanAmount'] + 1)
    df['Total_Income_log'] = np.log((data['ApplicantIncome'] + data['CoapplicantIncome']) + 1)
    
    # EMI calculation assuming 'LoanAmount' is in thousands and 'Loan_Amount_Term' is in months
    df['EMI'] = data['LoanAmount'] / data['Loan_Amount_Term']
    
    # Calculating balance income after subtracting the EMI (considering EMI in the same units as Income)
    df['Balance Income'] = (data['ApplicantIncome'] + data['CoapplicantIncome']) - (df['EMI'] * 1000)
    
    # One-hot encoding for categorical features based on the user input
    df['Gender_Male'] = 1 if data['Gender'] == 'Male' else 0
    df['Married_Yes'] = 1 if data['Married'] == 'Yes' else 0
    df['Education_Graduate'] = 1 if data['Education'] == 'Graduate' else 0
    df['Self_Employed_Yes'] = 1 if data['Self_Employed'] == 'Yes' else 0

    # One-hot encoding for 'Property_Area' feature
    df['Property_Area_Rural'] = 1 if data['Property_Area'] == 'Rural' else 0
    df['Property_Area_Semiurban'] = 1 if data['Property_Area'] == 'Semiurban' else 0
    df['Property_Area_Urban'] = 1 if data['Property_Area'] == 'Urban' else 0

    # Dropping original columns that were used for one-hot encoding
    columns_to_drop = ['Gender', 'Married', 'Education', 'Self_Employed', 'ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term', 'Property_Area']
    df = df.drop(columns=columns_to_drop)
    
    return df

# def predict_loan_status(data):
#     preprocessed_data = preprocess_input(data)
#     prediction = model.predict(preprocessed_data)
#     probability = model.predict_proba(preprocessed_data)[:, 1]  # Taking probability of the positive class
    
#     # Placeholder for loan acceptance rate
#     acceptance_rate = 0.65  # Example value, adjust based on your data
    
#     feedback = ""
#     reasons = []
    
#     # Analyze reasons for ineligibility
#     if prediction == 0:  # Assuming 0 represents 'Not Eligible'
#         if data['Credit_History'] == 'No':
#             reasons.append("poor credit history")
#         if data['LoanAmount'] / (data['ApplicantIncome'] + data['CoapplicantIncome'] + 1) > 0.6:  # Example threshold
#             reasons.append("high loan amount relative to income")
#         # You can add more conditions based on your analysis
        
#         if reasons:
#             feedback = "Unfortunately, you're not eligible for a loan due to " + ", ".join(reasons) + "."
#         else:
#             feedback = "You're not eligible for a loan based on the criteria."
#     else:
#         feedback = f"Congratulations! You are eligible for a loan. The current acceptance rate is {acceptance_rate*100:.2f}%."

#     return prediction[0], probability[0], feedback

def predict_loan_status(data):
    preprocessed_data = preprocess_input(data)
    prediction = model.predict(preprocessed_data)
    probability = model.predict_proba(preprocessed_data)[:, 1]  # Taking probability of the positive class
    
    reasons = []

    # Example: High Debt-to-Income Ratio
    total_income = data['ApplicantIncome'] + data['CoapplicantIncome']
    if total_income != 0 and data['LoanAmount'] / total_income > 0.4:  # Check if total_income is not zero
        reasons.append(("High debt-to-income ratio.", 
                        "Your debt-to-income ratio is high, which means a significant portion of your income goes towards debt payments. Lenders may see this as risky. Consider reducing existing debt or increasing your income."))

    # Example: Poor Credit History
    if data['Credit_History'] == 'No':
        reasons.append(("Poor credit history.", 
                        "Having a poor credit history suggests difficulties managing credit in the past. This can affect your ability to qualify for new credit. Improve your credit by addressing outstanding issues and establishing a positive payment history."))

    # Example: High Loan Amount
    if np.log(data['LoanAmount'] + 1) > 5.5:  # Example threshold on log scale
        reasons.append(("High loan amount relative to typical loan amounts.",
                        "The loan amount you're requesting is higher than usual, which may be seen as riskier by lenders. Consider adjusting the loan amount or exploring alternative financing options."))

    # Example: Short Loan Term for High Loan Amount
    if data['LoanAmount'] != 0 and data['Loan_Amount_Term'] != 0 and data['LoanAmount'] / data['Loan_Amount_Term'] > 0.05:  # Check if both values are not zero
        reasons.append(("High monthly payment relative to loan term.",
                        "Your monthly payment relative to the loan term is high, which could strain your finances and increase the risk of default. Consider extending the loan term or reducing the loan amount to lower your monthly payments."))

    feedback = "Eligible" if prediction == 1 else "Not Eligible"
    if prediction == 0:
        feedback += ". Reasons for ineligibility:\n"
        for reason, explanation in reasons:
            feedback += f"- {reason}\n  - {explanation}\n"

        # Add contact us section
        feedback += "\nIf you have any questions or need assistance, please feel free to contact us. We're here to help!"

    return prediction[0], probability[0], feedback
