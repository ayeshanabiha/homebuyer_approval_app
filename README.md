# Fannie Mae - Technica Challenge 
## A Beginner's Guide to Buying Homes

This project is my submission to Fannie Mae's challenge at the Technica 2022 hackathon.

The link to my webapp is [here](https://ayeshanabiha-homebuyer-approval-app-homebuyer-app-1xn7yg.streamlitapp.com/)

For first-time homebuyers, the process can often be confusing and feel overwhelming. In this web app (powered by Streamlit), users are able to learn about the basics of homebuying, check if they currently qualify to buy a home (and what they can do to improve their chances), and also learn a little about data science by looking at my analysis of previous homebuyer data!

### Intro to Homebuying

In this section, I define commonly used terms and discuss factors homebuyers should keep in mind when looking to purchase a home.

### Do I Qualify? 

In this section, users are able to put in information about the house they are looking to purchase, their monthly income, monthly debts, and payments regarding housing in order to get a detailed review of whether they are currently eligible. If a user is not eligible, the web app gives recommendations on how users can be improve to qualify in the future. 

For a user to be eligible, they must satisfy the following conditions:
- Credit score must be under 640
- LTV should be less than 80%; if it is higher, users are required to purchase a Private Mortgage Insurance which charges 1% of their appraised house value. While a high LTV value does not immediately disqualify a user, the amount you need to pay for the house will increase which may affect your DTI and FEDTI ratios
- DTI ratio should be at most 43% (it is preferred to be less than 36%)
- FEDTI ratio must be less than or equal to 28%

### A Look at Past Data
In this section, I look at data given by [Fannie Mae's github](https://github.com/FannieMaeOpenSource/technica-2022). After getting the data into a Pandas dataframe, I defined methods to calculate LTV, DTI, and FEDTI. Then, I created a method that made sure these values were in the thresholds I defined above. If they are, the the user is approved for a home purchase. If not, the conditions that caused them to be disqualfied are added for later processing. 

After getting the labels for each homebuyer, I decided to use this to train a Logistic Regression classifier as our intended output is a binary value (either approved or not approved). My model had a 92.8% accuracy. 

### Future Work
To expand upon this application I have a few things I would love to do:
- I would love to incorporate HTML/CSS to make the UI more appealing 
- I would love to test other ML models (such as decision trees) to see which one best fits the data
- I would love to optimize the current model by finetuning hyperparameters through a GridSearch 
