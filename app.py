# Import the prediction function from prediction.py
from prediction import predict_loan_status
from chatbot import show_chatbot_page
import streamlit as st

# Set page config with page title and layout
st.set_page_config(page_title='SwiftBank', layout='wide')

# Custom styles
st.markdown(
    """
    <style>
    /* Main content area */
    .reportview-container .main {
        color: #4F8A8B;
        background-color: #F9F9F9;
    }
    /* Sidebar */
    .sidebar .sidebar-content {
        background-color: #1b8a5a;
    }
    /* Radio buttons in the sidebar */
    .sidebar .stRadio > label {
        background-color: #137547;
        padding: 10px 15px;
        border-radius: 10px;
        border: 2px solid #137547;
    }
    /* Radio buttons options (circles) */
    .sidebar .stRadio > label > span:first-child {
        background-color: #fff;
        border-color: #eee;
    }
    /* Radio buttons text */
    .sidebar .stRadio > label > span:last-child {
        color: #fff;
    }
    /* Titles and text */
    h1, h2, h3, h4, h5, h6, .font {
        color: #1b8a5a;
        font-family: 'sans-serif';
    }
    /* Button styles */
    .stButton > button {
        color: #FFFFFF;
        background-color: #1b8a5a;
        border-radius: 5px;
        border: 1px solid #137547;
    }
    .stButton > button:hover {
        background-color: #137547;
        border-color: #0f5132;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Define the Home page
def home():
    st.title("About Us")
    
    st.markdown("""
    ## Welcome to SwiftBank - Where Speed Meets Reliability!
    
    **Established in 1995**
    
    At SwiftBank, we take pride in our rich history and unwavering commitment to providing fast and reliable banking services. Established in 1995, we embarked on a journey to redefine the banking experience by focusing on efficiency, innovation, and unparalleled customer service.
    
    ### Mission Statement
    
    Our mission is simple yet powerful: to be the benchmark for fast and reliable banking services. We understand that in today's fast-paced world, time is of the essence. That's why we've made it our mission to deliver financial solutions swiftly and reliably, meeting the diverse needs of our customers with precision.
    
    ### Why SwiftBank?
    
    **Speed in Every Transaction:** We've invested in cutting-edge technology to ensure that your transactions are processed swiftly. Whether it's a fund transfer, payment, or any banking activity, we make sure it happens in the blink of an eye.
    

    **SwiftBank - Your Partner in Progress.**
    """, unsafe_allow_html=True)


# Define the Prediction page
def show_prediction_page():
    st.title('Loan Eligibility Prediction System')

    # User Inputs
    col1, col2 = st.columns(2)

    with col1:
        gender = st.selectbox('Gender', ['Male', 'Female'])
        married = st.selectbox('Marital Status', ['Yes', 'No'])
        #dependents = st.selectbox('Dependents', ['0', '1', '2', '3+'])
        education = st.selectbox('Education', ['Graduate', 'Not Graduate'])
        self_employed = st.selectbox('Self Employed', ['Yes', 'No'])
        applicant_income = st.number_input('Applicant Monthly Income', value=0)
        coapplicant_income = st.number_input('Coapplicant Monthly Income', value=0)
        
    with col2:
        loan_amount = st.number_input('Loan Amount', value=0)
        loan_amount_term = st.number_input('Loan Amount Term (in months)', value=360)
        credit_history = st.selectbox('Credit History', ['Yes', 'No'])
        property_area = st.selectbox('Property Area', ['Urban', 'Semiurban', 'Rural'])
    
    submit_button = st.button('Predict Loan Status')

    if submit_button:
        input_data = {
            'Gender': gender,
            'Married': married,
            #'Dependents': dependents,
            'Education': education,
            'Self_Employed': self_employed,
            'ApplicantIncome': applicant_income,
            'CoapplicantIncome': coapplicant_income,
            'LoanAmount': loan_amount,
            'Loan_Amount_Term': loan_amount_term,
            'Credit_History': credit_history,
            'Property_Area': property_area
        }

        prediction, probability, feedback = predict_loan_status(input_data)
        st.write(feedback) 
    
        #if prediction is not None:
        if prediction == 1:
            st.success(f'Congratulations! You are eligible for a loan with a probability of {probability:.2f}.')
        else:
            st.error(f'Sorry, you are not eligible for a loan. Probability: {probability:.2f}')



# Sidebar navigation
st.sidebar.title("Swift Bank")
page_options = ["Home", "Prediction", "Chat With Us"]

# Using session_state to store the current page
if 'page' not in st.session_state:
    st.session_state['page'] = 'Home'

# Sidebar radio buttons for page navigation
st.session_state['page'] = st.sidebar.radio("Choose a page:", page_options, index=page_options.index(st.session_state['page']))

# Display the selected page
if st.session_state['page'] == "Home":
    home()
elif st.session_state['page'] == "Prediction":
    show_prediction_page()
elif st.session_state['page'] == "Chat With Us":
    show_chatbot_page()
