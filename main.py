import json
import requests
import pandas as pd
from bs4 import BeautifulSoup
import streamlit as st

company_code = st.text_input('Stock tricker',value='AAPL')

#income statement
url = f"https://financialmodelingprep.com/api/v3/income-statement/{company_code}?limit=120&apikey=e3e1ef68f4575bca8a430996a4e11ed1"
response = requests.get(url)
income = response.json()


#Balance sheet
url = f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{company_code}?limit=120&apikey=e3e1ef68f4575bca8a430996a4e11ed1"
response = requests.get(url)
balance_sheet = response.json()
df_balance_sheet = pd.DataFrame(balance_sheet).T

#Cash Flow
url = f"https://financialmodelingprep.com/api/v3/cash-flow-statement/{company_code}?limit=120&apikey=e3e1ef68f4575bca8a430996a4e11ed1"
response = requests.get(url)
cash_flow = response.json()

#Market Cap
url = f"https://financialmodelingprep.com/api/v3/market-capitalization/{company_code}?limit=120&apikey=e3e1ef68f4575bca8a430996a4e11ed1"
response = requests.get(url)
market_cap = response.json()

#Share_outstanding
url = f"https://financialmodelingprep.com/api/v4/shares_float?symbol={company_code}&apikey=e3e1ef68f4575bca8a430996a4e11ed1"
response = requests.get(url)
share = response.json()

#Dividend 
url = f"https://financialmodelingprep.com/api/v3/historical-price-full/stock_dividend/{company_code}?apikey=e3e1ef68f4575bca8a430996a4e11ed1"
response = requests.get(url)
dividend = response.json()

#PE
url = f"https://financialmodelingprep.com/api/v3/ratios/{company_code}?period=quarter&limit=140&apikey=e3e1ef68f4575bca8a430996a4e11ed1"
response = requests.get(url)
ratio = response.json()

#To dataframe
df_income = pd.DataFrame(income).T
df_balance_sheet = pd.DataFrame(balance_sheet).T
df_cash_flow = pd.DataFrame(cash_flow).T
df_dividend = pd.DataFrame(dividend).T
df_dividend = pd.DataFrame(dividend["historical"])
df_ratio = pd.DataFrame(ratio)

share_out_standing = df_income.loc["weightedAverageShsOut",0]
st.write(f"Share Outstanding (流通股份) {share_out_standing:,}")

total_debt = df_balance_sheet.loc["totalDebt", 0]
st.write(f"Total Debt (總負債)：{total_debt:,}")

cash_on_hand = df_balance_sheet.loc["cashAndCashEquivalents", 0]
st.write(f"Cash on Hand (現金及現金等價物)：{cash_on_hand:,}")

restricted_cash = st.number_input('Restricted cash and cash equivalents (限制性現金)', value=0)

market_capital = market_cap[0]["marketCap"]
st.write(f"MarketCap (市值)：{market_capital:,}")

ev = market_capital + total_debt - (cash_on_hand + restricted_cash)
st.write(f"Enterprise Value (企業價值)：{ev:,}")

ebit = df_income.loc["ebitda", 0]  - df_income.loc["depreciationAndAmortization", 0]
st.write(f"EBIT (息稅前淨利)：{ebit:,}")

ebitda = df_income.loc["ebitda", 0] 
st.write(f"EBITDA (稅息折舊及攤銷前利潤) {ebitda:,}")

if total_debt / ebitda >= 3:
    st.write(f"Debt Warning - EV over EBITDA is equal or above 3 (債務警告) {round((total_debt / ebitda)*100, 2)}%")
 
net_interest = df_income.loc["interestIncome", 0] - df_income.loc["interestExpense", 0]
st.write(f"Net Interest Income or Expenses (淨利息) {net_interest:,}")

tax_provision = df_income.loc["incomeBeforeTax", 0] - df_income.loc["netIncome", 0] 
st.write(f"Tax Provisions (稅務負擔) {tax_provision:,}")

revenue = df_income.loc["revenue", 0]
st.write(f"Total Revenue (營收) {revenue:,}")

cost_of_sale = df_income.loc["costOfRevenue", 0] 
st.write(f"Total Cost of Sales (成本銷售) {cost_of_sale:,}") 

gross_profit = df_income.loc["grossProfit", 0] 
st.write(f"Gross Margin (毛利) {gross_profit:,}") 

gross_profit_margin = gross_profit/revenue 
st.write(f"Gross Margin Rate (毛利率) {round(gross_profit_margin*100, 2)}%") 

general_and_administrative_expenses = df_income.loc["sellingGeneralAndAdministrativeExpenses", 0] 
st.write(f"General and Administrative (總和行政費用) {general_and_administrative_expenses:,}") 

operating_expenses = df_income.loc["operatingExpenses", 0] 
st.write(f"Operating Expenses (營業費用) {operating_expenses:,}") 

operating_expenses_ratio = operating_expenses/revenue 
st.write(f"Operating Expenses Ratio (營業費用率) {round(operating_expenses_ratio*100,2)}%") 

operating_ratio = (cost_of_sale+ operating_expenses)/revenue 
st.write(f"Operating Ratio (營業比率) {round(operating_ratio,2)}x") 

operating_income_margin = df_income.loc["operatingIncome", 0]/revenue 
st.write(f"Operating Income Margin (營業收入利潤率) {round(operating_income_margin*100,2)}%")

eps = df_income.loc["epsdiluted",0]
st.write(f"EPS (每股收益) {eps}")

operating_cash_flow = df_cash_flow.loc["operatingCashFlow",0]
st.write(f"Cash Flow from Operation (營業現金流) {operating_cash_flow:,}")

capital_expenditure  = df_cash_flow.loc["capitalExpenditure",0]
st.write(f"Capital Expenditure or Property, Plant & Equipment PPE (資本支出) {capital_expenditure:,}")

free_cash_flows = df_cash_flow.loc["freeCashFlow",0]
st.write(f"Free Cash Flows (FCF) (自由現金流) {free_cash_flows:,}")

fcf_share = free_cash_flows/share_out_standing
st.write(f"FCF/share (每股自由現金流) {round(fcf_share,2)}")


growth_rate_revenue_5 = (revenue/df_income.loc["revenue",5])**(1/5)-1
growth_rate_revenue_8 = (revenue/df_income.loc["revenue",8])**(1/8)-1
growth_rate_revenue_10 = (revenue/df_income.loc["revenue",10])**(1/10)-1
st.write(f"Growth Rate - Revenue (5年營收成長率) {round(growth_rate_revenue_5*100,2)}%")
st.write(f"Growth Rate - Revenue (8年營收成長率) {round(growth_rate_revenue_8*100,2)}%")
st.write(f"Growth Rate - Revenue (10年營收成長率) {round(growth_rate_revenue_10*100,2)}%")

if (eps >0 ):
    growth_rate_eps_5 = (eps/df_income.loc["epsdiluted",5])**(1/5)-1
    growth_rate_eps_8 = (eps/df_income.loc["epsdiluted",8])**(1/8)-1
    growth_rate_eps_10 = (eps/df_income.loc["epsdiluted",10])**(1/10)-1
    st.write(f"EPS (5年每股盈餘成長率) {round(growth_rate_eps_5*100,2)}%")
    st.write(f"EPS (8年每股盈餘成長率) {round(growth_rate_eps_8*100,2)}%")
    st.write(f"EPS (10年每股盈餘成長率) {round(growth_rate_eps_10*100,2)}%")

if(fcf_share>0):
    growth_fcf_share_5 = (fcf_share/(df_cash_flow.loc["freeCashFlow",5]/df_income.loc["weightedAverageShsOut",5]))**(1/5)-1
    growth_fcf_share_8 = (fcf_share/(df_cash_flow.loc["freeCashFlow",8]/df_income.loc["weightedAverageShsOut",8]))**(1/8)-1
    growth_fcf_share_10 = (fcf_share/(df_cash_flow.loc["freeCashFlow",10]/df_income.loc["weightedAverageShsOut",10]))**(1/10)-1

    st.write(f"FCF/share (5年每股自由現金流成長率) {round(growth_fcf_share_5*100,2)}%")
    st.write(f"FCF/share (8年每股自由現金流成長率) {round(growth_fcf_share_8*100,2)}%")
    st.write(f"FCF/share (10年每股自由現金流成長率) {round(growth_fcf_share_10*100,2)}%")

headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'}
response = requests.get("https://ycharts.com/indicators/3_month_t_bill" ,headers=headers)
soup = BeautifulSoup(response.text,"html.parser")
mth_treasury_rate = float(soup.find_all("td",{"class":"col-6"})[5].text.replace("%", ""))
st.write(f"3-month US Treasury Yield (3個月美國國債利率) {mth_treasury_rate}%")

discount_rate = mth_treasury_rate *2
st.write(f"Discount Rate (折現率) {discount_rate}%")
print(f"29. discount_rate {discount_rate}")

dividendsPaid = df_cash_flow.loc["dividendsPaid",0]
st.write(f"Dividend payout(股利支出) {dividendsPaid:,}")
print(f"30. dividendsPaid {dividendsPaid}")

if dividendsPaid > 0:
    dividend_yield = dividendsPaid/share_out_standing
    st.write(f"Dividend Yield (股利殖利率) {round(dividend_yield*100,2)}%")
    print(f"30. dividend_yield {dividend_yield}")
    dividend_per_share =  df_dividend.loc[0,"dividend"]
    st.write(f"Dividend per share (每股股利) {dividend_per_share}")
    print(f"31. dividend_per_share {dividend_per_share}")

pe_5y = df_ratio.loc[:,"priceEarningsRatio"].head(20).describe()
pe_10y = df_ratio.loc[:,"priceEarningsRatio"].head(40).describe()
#display pe_5y in streamlit
st.write("PE Ratio (5年平均股價淨值比)")
st.write(pe_5y)

#display pe_10y in streamlit
st.write("PE Ratio (10年平均股價淨值比)")
st.write(pe_10y)

total_asset = df_balance_sheet.loc["totalAssets",0]
st.write(f"Total Asset (資產總額) {total_asset:,}")

total_liabilities = df_balance_sheet.loc["totalLiabilities",0]
st.write(f"Total Liabilities (負債總額 ){total_liabilities:,}")

Shareholder_equity  = df_balance_sheet.loc["totalStockholdersEquity",0]
st.write(f"Shareholders’ Equity (股東權益總額) {Shareholder_equity:,}")

net_income  = df_income.loc["netIncome",0]
st.write(f"Net Income (淨利) {net_income:,}")

roe  = net_income/Shareholder_equity
st.write(f"ROE {round(roe,2)}%")


print("32.")
print(pe_5y)
print(pe_10y)
