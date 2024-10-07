import streamlit as st
import pickle
from datetime import datetime
import json

# Load the model
model = pickle.load(open('./Model/ML_Model1.pkl', 'rb'))

# Configure the page
st.set_page_config(
    page_title="Loan Prediction System",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with improved theme support
st.markdown("""
<style>
    /* Theme Variables */
    [data-theme="light"] {
        --primary-color: #1e3c72;
        --secondary-color: #2a5298;
        --text-color: #2c3e50;
        --background-color: #f5f7fa;
        --card-background: white;
        --success-color: #28a745;
        --error-color: #dc3545;
    }
    
    [data-theme="dark"] {
        --primary-color: #3498db;
        --secondary-color: #2980b9;
        --text-color: #ecf0f1;
        --background-color: #2c3e50;
        --card-background: #34495e;
        --success-color: #2ecc71;
        --error-color: #e74c3c;
    }
    
    [data-theme="nature"] {
        --primary-color: #2ecc71;
        --secondary-color: #27ae60;
        --text-color: #2c3e50;
        --background-color: #f0f9f4;
        --card-background: white;
        --success-color: #27ae60;
        --error-color: #c0392b;
    }

    /* Apply theme to main container */
    .main {
        background-color: var(--background-color) !important;
        color: var(--text-color) !important;
    }
    
    /* Sidebar styling */
    .css-1d391kg, .css-12oz5g7 {
        background: linear-gradient(180deg, var(--primary-color) 0%, var(--secondary-color) 100%);
    }
    
    /* Cards */
    .stCard {
        background: var(--card-background);
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        transition: transform 0.3s ease;
    }
    
    .stCard:hover {
        transform: translateY(-5px);
    }
    
    /* Result Box */
    .result-box {
        background: var(--card-background);
        border-radius: 15px;
        padding: 2rem;
        margin-top: 2rem;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
        animation: slideIn 0.5s ease;
    }
    
    .result-box.success {
        border-left: 5px solid var(--success-color);
    }
    
    .result-box.error {
        border-left: 5px solid var(--error-color);
    }
    
    /* Theme-specific text colors */
    [data-theme="dark"] .stMarkdown {
        color: var(--text-color) !important;
    }
    
    /* Improved button styling */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        color: white !important;
        padding: 1rem 2rem;
        border-radius: 10px;
        border: none;
        font-weight: bold;
        width: 100%;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }

    /* Input fields styling */
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 1px solid var(--primary-color);
        padding: 8px 12px;
    }

    .stSelectbox > div > div {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'
if 'loan_history' not in st.session_state:
    st.session_state.loan_history = []

def calculate_emi(loan_amount, duration_months, interest_rate=10.0):
    monthly_rate = interest_rate / (12 * 100)
    emi = (loan_amount * monthly_rate * (1 + monthly_rate)**duration_months) / ((1 + monthly_rate)**duration_months - 1)
    return round(emi, 2)

def format_currency(amount):
    """Format amount in Indian style with ₹ symbol"""
    return f"₹{amount:,.2f}"

def run():
    # Apply theme to the main container
    st.markdown(f"""
        <div data-theme="{st.session_state.theme}">
            <script>
                document.documentElement.setAttribute('data-theme', '{st.session_state.theme}');
            </script>
        </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.title("🏦 Loan Prediction App")
        st.markdown("---")
        
        # Theme Selection with immediate effect
        st.subheader("🎨 Theme Settings")
        theme = st.radio(
            "Choose Theme",
            options=['light', 'dark', 'nature'],
            index=['light', 'dark', 'nature'].index(st.session_state.theme)
        )
        if theme != st.session_state.theme:
            st.session_state.theme = theme
            st.experimental_rerun()
        
        # EMI Calculator
        st.markdown("---")
        st.subheader("💰 EMI Calculator")
        calc_loan_amount = st.number_input("Loan Amount (₹)", min_value=0, value=100000)
        calc_duration = st.number_input("Duration (months)", min_value=1, value=12)
        calc_interest = st.number_input("Interest Rate (%)", min_value=1.0, value=10.0)
        
        if calc_loan_amount > 0:
            emi = calculate_emi(calc_loan_amount, calc_duration, calc_interest)
            st.success(f"Monthly EMI: {format_currency(emi)}")
    
    # Main content
    st.markdown("""
        <div style='text-align: center; padding: 2rem;'>
            <h1 style='color: var(--primary-color);'>🏦 Bank Loan Prediction System</h1>
            <p style='color: var(--text-color);'>Fill out the form below to check your loan eligibility</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Form columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='stCard'>", unsafe_allow_html=True)
        st.markdown("### 👤 Personal Information")
        account_no = st.text_input('Account Number 🔢', placeholder="Enter your account number")
        fn = st.text_input('Full Name 📝', placeholder="Enter your full name")
        gen = st.selectbox("Gender 👥", ('Female', 'Male'))
        mar = st.selectbox("Marital Status 💑", ('No', 'Yes'))
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='stCard'>", unsafe_allow_html=True)
        st.markdown("### 💼 Professional Information")
        emp = st.selectbox("Employment Status 💼", ('Job', 'Business'))
        edu = st.selectbox("Education 🎓", ('Not Graduate', 'Graduate'))
        dep = st.selectbox("Dependents 👨‍👩‍👧‍👦", ('No', 'One', 'Two', 'More than Two'))
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Financial Information
    st.markdown("<div class='stCard'>", unsafe_allow_html=True)
    st.markdown("### 💰 Financial Information")
    col3, col4, col5 = st.columns(3)
    
    with col3:
        mon_income = st.number_input("Monthly Income (₹) 💵", min_value=0, format="%d")
    with col4:
        co_mon_income = st.number_input("Co-Applicant's Income (₹) 💵", min_value=0, format="%d")
    with col5:
        loan_amt = st.number_input("Loan Amount (₹) 🏦", min_value=0, format="%d")
    
    col6, col7, col8 = st.columns(3)
    
    with col6:
        dur = st.selectbox("Loan Duration ⏳", ['2 Month', '6 Month', '8 Month', '1 Year', '16 Month'])
    with col7:
        cred = st.selectbox("Credit Score 📊", ['Between 300 to 500', 'Above 500'])
    with col8:
        prop = st.selectbox("Property Area 🏘️", ['Rural', 'Semi-Urban', 'Urban'])
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    
    
 # ... (previous imports and initial code remains the same until the submit button logic)

    # Submit button
    if st.button("Submit Application 📤"):
        if not account_no or not fn:
            st.error("❌ Please fill in all required fields.")
            return
        
        # Convert duration selection to months
        duration_map = {
            '2 Month': 60,
            '6 Month': 180,
            '8 Month': 240,
            '1 Year': 360,
            '16 Month': 480
        }
        duration = duration_map[dur]
        
        # Convert categorical variables to numeric
        gen_val = 1 if gen == 'Male' else 0
        mar_val = 1 if mar == 'Yes' else 0
        dep_val = {'No': 0, 'One': 1, 'Two': 2, 'More than Two': 3}[dep]
        edu_val = 1 if edu == 'Graduate' else 0
        emp_val = 1 if emp == 'Business' else 0
        cred_val = 1 if cred == 'Above 500' else 0
        prop_val = {'Rural': 0, 'Semi-Urban': 1, 'Urban': 2}[prop]
        
        # Create feature array for prediction
        features = [[gen_val, mar_val, dep_val, edu_val, emp_val, 
                    mon_income, co_mon_income, loan_amt, duration, 
                    cred_val, prop_val]]
        
        # Make prediction
        prediction = model.predict(features)
        ans = prediction[0]
        
        # Store result in history
        result = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'name': fn,
            'account_no': account_no,
            'loan_amount': loan_amt,
            'approved': ans == 1
        }
        st.session_state.loan_history.append(result)
        
        # Display result
        if ans == 0:
            st.markdown(f"""
            <div class='result-box error'>
                <h2>❌ Application Result</h2>
                <hr>
                <p><strong>Applicant:</strong> {fn} 👤</p>
                <p><strong>Account Number:</strong> {account_no} 🔢</p>
                <p><strong>Status:</strong> We regret to inform you that your loan application has not been approved at this time. 😔</p>
                <p><strong>Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 📅</p>
                <p><strong>Recommendation:</strong> Consider improving your credit score or applying for a lower loan amount. 💡</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            emi = calculate_emi(loan_amt, duration)
            st.markdown(f"""
            <div class='result-box success'>
                <h2>🎉 Application Result</h2>
                <hr>
                <p><strong>Applicant:</strong> {fn} 👤</p>
                <p><strong>Account Number:</strong> {account_no} 🔢</p>
                <p><strong>Status:</strong> Congratulations! Your loan application has been approved! 🎊</p>
                <p><strong>Loan Amount Approved:</strong> {format_currency(loan_amt)} 💰</p>
                <p><strong>Estimated Monthly EMI:</strong> {format_currency(emi)} 💵</p>
                <p><strong>Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 📅</p>
                <p><strong>Next Steps:</strong> Our representative will contact you shortly for documentation. 📋</p>
            </div>
            """, unsafe_allow_html=True)

    # ... (rest of the code remains the same)

    # Application History
    if st.session_state.loan_history:
        st.markdown("<div class='stCard'>", unsafe_allow_html=True)
        st.markdown("### 📜 Recent Application History")
        for result in reversed(st.session_state.loan_history[-5:]):
            st.markdown(f"""
            <div style='padding: 10px; margin: 5px 0; background: {'#e8f5e9' if result['approved'] else '#ffebee'}; border-radius: 5px;'>
                {result['timestamp']} - {result['name']} - {format_currency(result['loan_amount'])} - 
                {'✅ Approved' if result['approved'] else '❌ Rejected'}
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    run()