import streamlit as st
import pandas as pd

st.set_page_config(page_title= "A Beginner's Guide to Buying Homes", page_icon= "🏠", layout="wide")

def get_ltv(appraised_value, loan_amount):
    return loan_amount/appraised_value

def get_dti(gross_monthly_income, credit_card_payment, car_payment, student_loan_payment, monthly_mortgage_payment, pmi):
    monthly_debt = credit_card_payment + car_payment + student_loan_payment + monthly_mortgage_payment + pmi
    return monthly_debt/gross_monthly_income

def get_dti_app(gross_monthly_income, monthly_debt, pmi):
    return (monthly_debt+pmi)/gross_monthly_income

def get_fedti(gross_monthly_income, monthly_mortgage_payment, pmi):
    return (monthly_mortgage_payment+pmi)/gross_monthly_income

def is_buyer_approved_app(credit_score, dti, fedti, ltv):
    is_approved = True
    messages = []
    if credit_score < 640:
        messages.append("Credit Score is less than 640")
        is_approved = False     
    if dti > 0.43:
        messages.append("DTI ratio is greater than 43%")
        is_approved = False
    if fedti > 0.28:
        messages.append("FEDTI ratio is greater than 28%")
        is_approved = False
    if ltv > 0.80:
        messages.append("LTV ratio is greater than 80%")
    
    if is_approved:
        messages.append("All conditions met")
        
    return is_approved, messages

def is_buyer_approved(credit_score, dti, fedti, deny_stats):
    is_approved = True
    messages = []
    if credit_score < 640:
        messages.append("Credit Score is less than 640")
        if "credit_score" in deny_stats:
            deny_stats['credit_score'] = deny_stats['credit_score'] + 1
        else:
            deny_stats['credit_score'] = 1
        is_approved = False     
    if dti > 0.43:
        messages.append("DTI ratio is greater than 43%")
        if "dti" in deny_stats:
            deny_stats['dti'] = deny_stats['dti'] + 1
        else:
            deny_stats['dti'] = 1
        is_approved = False
        
    if fedti > 0.28:
        messages.append("FEDTI ratio is greater than 28%")
        if "fedti" in deny_stats:
            deny_stats['fedti'] = deny_stats['fedti'] + 1
        else:
            deny_stats['fedti'] = 1
        is_approved = False
    
    if is_approved:
        messages.append("All conditions met")
        
    return is_approved, messages

st.title("A Beginner's Guide to Buying Homes")
homebuyer_data = pd.read_csv("technica_2022-HomeBuyerInfo.csv")

tab1, tab2, tab3 = st.tabs(["So how do I do this?", "Do I qualify?", "Previous Data from Homebuyers"])

with tab1:
    st.header("Hey you! Are you looking to buy a home?")
    st.write("For first-time homebuyers, the process can often be confusing and feel overwhelming. Worry not! We've got all the information you need to make sure you'll be out of your parents' basement in no time!")
    
    st.write("Before we can delve into homebuying, we need to know some important terms that are commonly used:")
    with st.expander("Terms to Know"):
        st.write('- **Gross Monthly Income**: the amount of money you earn monthly prior to taxes and other deductions')
        st.write("- **Home Appraised Value**: the monetary value assigned to a property (i.e. it's market value)")
        st.write("- **Down Payment Amount**: the initial up-front payment given by a buyer when purchasing a home (i.e. typically a buyer will pay a portion of the appraised value and then take out a loan for the remainder)")
        st.write("- **Mortgage**: an agreement in which the buyer borrows money from a lender to purchase a home (typically divided into monthly installments)")
        st.write("- **Refinancing**: modifying an existing loan to either lower the interest rate, change payment schedules, etc.")
        st.write("- **Credit Score**: a numerical value to predicts how likely you are to pay a loan back on time (the higher the score, the more confidence)")
        st.write("- **LTV (Loan-to-Value)**: compares the amount of your mortagage with the appraised value of your property (i.e. what percentage of the home's value do you need a loan for)")
        st.write("- **DTI (Debt-to-Income Ratio)**: percentage of your gross monthly income that goes towards paying your monthly debt payments (such as credit cards, car, student loans, etc.)")
        st.write("- **FEDTI (Front-end debt to income)**: represents the ratio of your total monthly housing expenses debt to your monthly gross income")
    
    st.write("Here's some factors one should consider when trying to purchase a home:")

    st.info("Make sure your credit score is **640** or above")
    st.info("Your LTV should be **less than 80%**. If higher, you may face higher interest rates and will be required to purchase a Private Mortgage Insurance (which charges 1% of the appraised house price)")
    st.info("Your DTI should **less than 43%** (but it is preferred for it to be **less than 36%**) with **no more than 28%** of that debt being towards a mortgage")
    st.info("Your FEDTI should be **less than or equal to 28%**")

    st.write("Woah! I know I just threw a lot of terms and numbers at you, but hear me out. You don't have to do any of the math, just use our in-house application in the next tab to check if you're eligible to buy a home. In addition, we'll give you tips on how to improve your chances if you happen to be denied.")

with tab2:
   st.header("Do I Qualify?")
   st.write("Check to see if you qualify today to purchase a home!")
   gross_monthly_income = st.number_input("What is your gross monthly income?")
   debt_payments = st.number_input("What is the total amount of loan payments do you have per month (i.e. credit card, car, student loans, etc.)?")
   credit_score = st.number_input("What is your credit score?")
   home_appraised_value = st.number_input("How much is the house you are looking at appraised for?")
   down_payment = st.number_input("How much are you willing to give for a down payment?")
   monthly_mortgage_payment = st.number_input("What is your monthly mortgage payment?")
   if st.button("Calculate!"):
    loan_amount = home_appraised_value - down_payment
    ltv = get_ltv(home_appraised_value, loan_amount)
    if ltv > 0.8:
        pmi = (0.01 * home_appraised_value)/12
    else:
        pmi = 0
    dti = get_dti_app(gross_monthly_income, debt_payments, pmi)
    fedti = get_fedti(gross_monthly_income, monthly_mortgage_payment, pmi)
    decision, messages = is_buyer_approved_app(credit_score, dti, fedti, ltv)

    if decision == True:
        st.success("Congratulations! You qualify to purchase a home!")

        with st.expander(f"Quick Stats on your Application: "):
            st.write(f"LTV percentage: {(ltv * 100):.2f}%")
            st.write(f"DTI percentage: {(dti * 100):.2f}%")
            st.write(f"FEDTI percentage: {(fedti * 100):.2f}%")
        
        for msg in messages:
            if msg == "LTV ratio is greater than 80%":
                st.info("While you were still approved, it is important to note that your LTV ratio was greater than 80%. This means that you are required to purchase Private Mortgage Insurance (which is 1% of the appraised value of the house you want to buy). You may want to consider increasing your down payment amount.")
    else:
        st.error(f"Unfortunately, you do not qualify :(")

        col1, col2 = st.columns(2)

        with col1:
            with st.expander("Quick Stats on your Application:"):
                st.write(f"LTV percentage: {(ltv * 100):.2f}%")
                st.write(f"DTI percentage: {(dti * 100):.2f}%")
                st.write(f"FEDTI percentage: {(fedti * 100):.2f}%")
        
        with col2:
            with st.expander("Factors that Disqualified You:"):
                for msg in messages:
                    st.write(f"- {msg}")
        
        st.write("However, all is not lost! Here are some things you can do to improve your opportunity to buy a home in the future:")
        for msg in messages:
            if msg == "Credit Score is less than 640":
                st.info("To improve your credit score, try to stay under your credit utilization limit (30% of your total available credit). The highest scorers stay under 7%. Try to keep your balance low when the card issuer reports it to the credit bureaus. If you can, review your credit reports, try to limit requests for new credit, and prioritize paying your bills on time.")
            
            if msg == "DTI ratio is greater than 43%":
                st.info("You can try to lower your DTI score by transfering high interest loans to a low interest credit card (although be wary of having too many credit catds as this can impact your ability to purchase a home). If possible, try to increase the amount you pay monthly towards your debt as that can lower the total amount more quickly. Try to also avoid taking on more debt (i.e. hold off on large purchases) until your DTI score is lower.")
            
            if msg == "FEDTI ratio is greater than 28%":
                st.info("If your FEDTI score is too high, this means your monthly housing debt takes up a large portion of your gross monthly income. If possible, you may consider renting (if it is cheaper than a monthly payment) or looking for a less expensive home.")

            if msg == "LTV ratio is greater than 80%":
                st.info("While this by itself is not reason to disqualify you, since your LTV ratio was greater than 80%, you are required to purchase Private Mortgage Insurance (which is 1% of the appraised value of the house). You may want to consider increasing your down payment amount.")
st.cache()
with tab3:
    st.header("Previous Data from Homebuyers")
    st.write("Using data provided by Fannie Mae for the Technica Hackathon Challenge, I evaluated if each buyer is qualified to purchase a home.")
    st.subheader("Part 1: Data Acquisition")
    st.write("Below is the data at a glance:")
    st.dataframe(homebuyer_data)

    st.subheader("Part 2: Define Methods for Conditions of Approval")
    st.write("In order to determine whether a particular buyer qualified, I first defined methods to calculate LTV, DTI, and FEDTI. Using these values and their credit score, I then determined their eligibility. Below are the functions I wrote:")

    st.code("def get_ltv(appraised_value, loan_amount): \n return loan_amount/appraised_value", language='python')
    st.code("def get_dti(gross_monthly_income, credit_card_payment, car_payment, student_loan_payment, monthly_mortgage_payment, pmi): \n monthly_debt = credit_card_payment + car_payment + student_loan_payment + monthly_mortgage_payment + pmi \n return monthly_debt/gross_monthly_income", language='python')
    st.code("def get_fedti(gross_monthly_income, monthly_mortgage_payment, pmi): \n return (monthly_mortgage_payment+pmi)/gross_monthly_income", language='python')

    st.subheader("Part 3: Apply Methods to Data")

    ltv = []
    dti = []
    fedti = []

    for index, row in homebuyer_data.iterrows():
        ltv_val = get_ltv(row["AppraisedValue"], row["LoanAmount"])
        if ltv_val > 0.8:
            pmi = (0.01 * row["AppraisedValue"])/12
        else:
            pmi = 0
        ltv.append(ltv_val)
        dti.append(get_dti(row["GrossMonthlyIncome"], row["CreditCardPayment"], row["CarPayment"], row["StudentLoanPayments"], row["MonthlyMortgagePayment"], pmi))
        fedti.append(get_fedti(row["GrossMonthlyIncome"], row["MonthlyMortgagePayment"], pmi))

    homebuyer_data["LTV"] = ltv
    homebuyer_data["DTI_Ratio"] = dti
    homebuyer_data["FEDTI_Ratio"] = fedti

    is_approved = []
    messages = []
    deny_stats = {}
    statuses = {}

    for index, row in homebuyer_data.iterrows():
        status, msg = is_buyer_approved(row["CreditScore"], row["DTI_Ratio"], row["FEDTI_Ratio"], deny_stats)
        if status:
            if "Y" in statuses:
                statuses["Y"] = statuses["Y"] + 1
            else:
                statuses["Y"] = 1
            is_approved.append("Y")
        else:
            if "N" in statuses:
                statuses["N"] = statuses["N"] + 1
            else:
                statuses["N"] = 1
            is_approved.append("N")
        messages.append(msg)
            
    homebuyer_data["Is_Approved"] = is_approved
    homebuyer_data["Message"] = messages

    updated_data = homebuyer_data.copy()
    updated_data = updated_data.drop(['GrossMonthlyIncome', 'CreditCardPayment', 'CarPayment', 
    'StudentLoanPayments', 'AppraisedValue', 'DownPayment', 'LoanAmount', 'MonthlyMortgagePayment'], axis = 1)

    st.write("Here is the updated dataframe after applying the methods: ")
    st.dataframe(updated_data)

    st.subheader("Part 4: Results")
    per_dti = (deny_stats["dti"]/10000)*100
    per_fedti = (deny_stats["fedti"]/10000)*100
    per_cs = (deny_stats["credit_score"]/10000)*100
    per_denied = (statuses["N"]/10000)*100
    per_accepted = (statuses["Y"]/10000)*100

    st.write(f"Out of 10,000 homeowners, **{per_accepted:.2f}%** were accepted and **{per_denied:.2f}%** were denied.\n")
    st.write(f"Out of the homeowners that were denied, ")
    st.write(f"- **{per_dti:.2f}%** were denied because their DTI ratio was greater than 43%")
    st.write(f"- **{per_fedti:.2f}%** were denied because their FEDTI ratio was greater than 28%")
    st.write(f"- **{per_cs:.2f}%** were denied because their credit score was less than 640")

    st.write("Below are some visualizations to better show the data analyzed:")

    col1, col2 = st.columns(2)

    with col1:
        st.image("income_vs_dti.png")
        st.write("In the scatterplot above, you can see that as gross monthly income increases, the DTI ratio decreases. This makes sense as the greater your income, the less percentage of it is taken out for mortgage related payments.")
    
    with col2:
        st.image("pie_chart_denials.png")
        st.write("In the pie chart above, you can see that there is pretty much a uniform distribution of reasons that led to some buyers not being approved for a loan.")
    
    st.subheader("Part 5: Applying Machine Learning to Data")
    st.write("Since we now had labels for each row classifying whether a loan was accepted or denied, I decided to use this to train an ML classification model. I thought it would be interesting to compare the results of the model to the manual approach I took when labelling the rows. I decided to use a logistic regression model as the outcome we want to predict is binary (either approved or denied)")
    st.write("I first split my data for training (75% of data) and testing (25% of data). I then trained a Logistic Regression model through `sklearn` for up to 1000 iterations. Finally, I tested my model on the test data and found the model to have **92.8%** accuracy.")
