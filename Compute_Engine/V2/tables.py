import json
import pandas as pd
import requests
from vertexai.language_models import TextGenerationModel
import vertexai
from vertexai.language_models import TextGenerationModel
from io import StringIO
import os
from google.oauth2 import service_account
from vertexai.generative_models import (
    GenerationConfig,
    GenerativeModel,
)
from pandasai.llm.google_vertexai import GoogleVertexAI
import pandas as pd
from pandasai import SmartDataframe

llm = GoogleVertexAI(
    model="gemini-pro", project_id="ENTER YOUR GCP PROJECT ID HERE", location="us-central1"
)


credentials = service_account.Credentials.from_service_account_file(
    "/home/ksgcpcloud/myapp/Ver_1/loopa_key.json"
)
vertexai.init(project="ENTER YOUR GCP PROJECT ID HERE", location="us-central1", credentials=credentials)


def get_tabular_data(session_ID):
    with open(f"/home/ksgcpcloud/myapp/data/{session_ID}/data.txt") as f:
        directory_path = f"/home/ksgcpcloud/myapp/csv_data/{session_ID}"
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
            print("Directory created")
        else:
            print("Directory already exists")

        try:
            data = json.load(f)

            num_list = []
            mykeys = list(map(lambda x: x[0], data.items()))
            print(f"This is my keys : {mykeys,mykeys[0]}")
            if mykeys[0] == "Error Message":
                print("I am in df_error")
                df_error = pd.DataFrame(
                    [
                        "Error, please rephrase your prompt. If it's an issue from our side do this."
                    ]
                )
                print(df_error)
                return df_error.to_csv()
            print(f"This is the key : {mykeys}")
            try:
                for i in range(len(mykeys)):
                    if mykeys[i] in data and isinstance(data[mykeys[i]], list):
                        # print(f"The {mykeys[i]} key exists and is a list.")
                        num_list.append(i)
                    # else:
                    #     print(
                    #         # f"The {mykeys[i]} key either doesn't exist or is not a list."
                    #     )
                # print(num_list)

                df_list = []
                # df_list2 = []
                for i in range(num_list[0], len(mykeys)):
                    # column_families = []
                    column_names = []
                    key = mykeys[i]
                    for key2 in data[key][0].keys():
                        # column_families.append((key, key2))
                        column_names.append(key2)
                    df = pd.DataFrame(columns=[column_names])
                    for l in range(len(data[key])):
                        df.loc[len(df)] = data[key][l].values()
                    # df.columns = pd.MultiIndex.from_tuples(column_families)

                    df.to_csv(
                        f"/home/ksgcpcloud/myapp/csv_data/{session_ID}/data{i}.csv"
                    )
                    df_list.append(df.to_csv())
                    # df.to_csv("data.csv")
                    # print(df.dtypes())
                    # print(df)
                print("I am inside the nested try block", session_ID)
                # final_df = pd.concat(df_list)
                # final_df = final_df.reset_index(drop=True)
                return df_list
            except:
                df = pd.DataFrame([data])
                # if not os.path.exists(directory_path):
                #     os.makedirs(directory_path)
                #     print("Directory created")
                # else:
                #     print("Directory already exists")
                df.to_csv(f"/home/ksgcpcloud/myapp/csv_data/{session_ID}/data1.csv")
                print("I am the inside nested except block", session_ID)
                return df.to_csv()
        except:
            # if not os.path.exists(directory_path):
            #     os.makedirs(directory_path)
            #     print("Directory created")
            # else:
            #     print("Directory already exists")
            df = pd.read_csv(f"/home/ksgcpcloud/myapp/data/{session_ID}/data.txt")

            print("I am the outside except block", session_ID)
            df.to_csv(f"/home/ksgcpcloud/myapp/csv_data/{session_ID}/data1.csv")
            # print(df.to_csv())
            return df.to_csv()


# url_generation_functionality ----------------------------------------------------------------------------------------------------------
def get_url_generation_functionality(user_text):
    url_dict = {
        "url": "The constructed url here",
        "heading": "The few word title for the user's query",
    }

    url_dict = json.dumps(url_dict)

    parameters = {
        "temperature": 0.1,
        "max_output_tokens": 256,
        "top_p": 0.6,
        "top_k": 10,
        "candidate_count": 1,
    }
    model = GenerativeModel("gemini-1.0-pro-001")
    response = model.generate_content(
        f"""You are an investment advisor and you need to make an API request to alpha vantage and the request url looks like "https://www.alphavantage.co/query?". The API has a lot of functions which are defined in the sections below and those functions are added like this "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&datatype=csv".

The sections are <Core Stock APIs:[TIME_SERIES_INTRADAY,TIME_SERIES_DAILY,TIME_SERIES_WEEKLY,TIME_SERIES_MONTHLY,GLOBAL_QUOTE,SYMBOL_SEARCH,MARKET_STATUS],
Alpha Intellligence:[NEWS_SENTIMENT,TOP_GAINERS_LOSERS],
Fundamental Data:[OVERVIEW,INCOME_STATEMENT,BALANCE_SHEET,CASH_FLOW,EARNINGS,LISTING_STATUS,EARNINGS_CALENDAR,IPO_CALENDAR],
Forex(FX):[CURRENCY_EXHANGE_RATE,FX_DAILY,FX_WEEKLY,FX_MONTHLY],
Cryptocurrencies:[CURRENCY_EXCHANGE_RATE,DIGITAL_CURRENCY_DAILY,DIGITAL_CURRENCY_WEEKLY,DIGITAL_CURRENCY_MONTHLY],
Economic Inidicators:[REAL_GDP,REAL_GDP_PER_CAPITA,TREASURY_YIELD,FEDERAL_FUNDS_RATE,CPI,INFLATION,RETAIL_SALES,DURABLES,UNEMPLOYMENT,NONFARM_PAYROLL]>

Core Stock APIs:
<
The TIME_SERIES_INTRADAY (This API returns current and 20+ years of historical intraday OHLCV time series of the equity specified) section has the following functions: 
"
❚ Required: function
The time series of your choice. In this case, function=TIME_SERIES_INTRADAY
❚ Required: symbol
The name of the equity of your choice. For example: symbol=IBM
❚ Required: interval
Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min
❚ Required: datatype
In this case, datatype=csv
❚ Optional: month
By default, this parameter is not set and the API will return intraday data for the most recent days of trading. You can use the month parameter (in YYYY-MM format) to query a specific month in history. For example, month=2009-01. Any month in the last 20+ years since 2000-01 (January 2000) is supported.
❚ Optional: outputsize
By default, outputsize=compact. Strings compact and full are accepted with the following specifications: compact returns only the latest 100 data points in the intraday time series; full returns trailing 30 days of the most recent intraday data if the month parameter (see above) is not specified, or the full intraday data for a specific month in history if the month parameter is specified. The "compact" option is recommended if you would like to reduce the data size of each API call.
URL examples with explanations : 
"
The API will return the most recent 100 intraday OHLCV bars by default when the outputsize parameter is not set
https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&datatype=csv
Query the most recent full 30 days of intraday data by setting outputsize=full
https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&outputsize=full&datatype=csv
Query intraday data for a given month in history (e.g., 2009-01). Any month in the last 20+ years (since 2000-01) is supported
https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&month=2009-01&outputsize=full&datatype=csv
"
"

The TIME_SERIES_DAILY (This API returns raw daily time series of the global equity specified, covering 20+ years of historical data) section has the following functions: 
"
❚ Required: function
The time series of your choice. In this case, function=TIME_SERIES_DAILY
❚ Required: symbol
The name of the equity of your choice. For example: symbol=IBM
❚ Required: datatype
In this case, datatype = csv
❚ Optional: outputsize
By default, outputsize=compact. Strings compact and full are accepted with the following specifications: compact returns only the latest 100 data points; full returns the full-length time series of 20+ years of historical data. The "compact" option is recommended if you would like to reduce the data size of each API call.
❚

URL examples with explanations :
"
Sample ticker traded in the United States
https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&datatype=csv
https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&outputsize=full&datatype=csv
Sample ticker traded in UK - London Stock Exchange
https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=TSCO.LON&outputsize=full&datatype=csv
Sample ticker traded in Canada - Toronto Stock Exchange
https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=SHOP.TRT&outputsize=full&datatype=csv
Sample ticker traded in Canada - Toronto Venture Exchange
https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=GPV.TRV&outputsize=full&datatype=csv
Sample ticker traded in Germany - XETRA
https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MBG.DEX&outputsize=full&datatype=csv
Sample ticker traded in India - BSE
https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=RELIANCE.BSE&outputsize=full&datatype=csv
Sample ticker traded in China - Shanghai Stock Exchange
https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=600104.SHH&outputsize=full&datatype=csv
Sample ticker traded in China - Shenzhen Stock Exchange
https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=000002.SHZ&outputsize=full&datatype=csv
"
"

The TIME_SERIES_WEEKLY (This API returns weekly time series of the global equity specified, covering 20+ years of historical data) section has the following functions:
"
❚ Required: function
The time series of your choice. In this case, function=TIME_SERIES_WEEKLY
❚ Required: symbol
The name of the equity of your choice. For example: symbol=IBM
❚ Required: datatype
In this case datatype = csv

URL examples with explanation : 
"
https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol=IBM&datatype=csv
https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol=TSCO.LON&datatype=csv
"
"

The TIME_SERIES_MONTHLY (This API returns monthly time series of the global equity specified, covering 20+ years of historical data) section has the following functions : 
"
❚ Required: function
The time series of your choice. In this case, function=TIME_SERIES_MONTHLY
❚ Required: symbol
The name of the equity of your choice. For example: symbol=IBM
❚ Required: datatype
In this case datatype = csv

URL examples with explanation : 
"
https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=IBM&datatype=csv
https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=TSCO.LON&datatype=csv
"
"

The GLOBAL_QUOTE (A lightweight alternative to the time series APIs, this service returns the latest price and volume information for a ticker of your choice) has the following functions : 
"
❚ Required: function
The API function of your choice. In this case it is GLOBAL_QUOTE
❚ Required: symbol
The symbol of the global ticker of your choice. For example: symbol=IBM.
❚ Required: datatype
In this case datatype = csv

URL examples with explanation : 
"
https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=IBM&datatype=csv
https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=300135.SHZ&datatype=csv
"
"

The SYMBOL_SEARCH (The Search Endpoint returns the best-matching symbols and market information based on keywords of your choice) section has the following functions :
"
❚ Required: function
The API function of your choice. In this case, function=SYMBOL_SEARCH
❚ Required: keywords
A text string of your choice. For example: keywords=microsoft.
❚ Required: datatype
In this case datatype = csv

URL examples with explanation : 
"
https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=tesco&datatype=csv
https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=tencent&datatype=csv
https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=BA&datatype=csv
https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=SAIC&datatype=csv
"
" 

The MARKET_STATUS (This endpoint returns the current market status of major trading venues for equities, forex, and cryptocurrencies around the world) section has the following functions : 
"
❚ Required: function
The API function of your choice. In this case, function=MARKET_STATUS

URL examples with explanation : 
"
https://www.alphavantage.co/query?function=MARKET_STATUS
"
"
>

Alpha Intelligence:
<
The NEWS_SENTIMENT (This API returns live and historical market news & sentiment data from a large & growing selection of premier news outlets around the world, covering stocks, cryptocurrencies, forex, and a wide range of topics such as fiscal policy, mergers & acquisitions, IPOs, etc) section has the following functions : 
"
❚ Required: function
The function of your choice. In this case, function=NEWS_SENTIMENT
❚ Optional: tickers
The stock/crypto/forex symbols of your choice. For example: tickers=IBM will filter for articles that mention the IBM ticker; tickers=COIN,CRYPTO:BTC,FOREX:USD will filter for articles that simultaneously mention Coinbase (COIN), Bitcoin (CRYPTO:BTC), and US Dollar (FOREX:USD) in their content.
❚ Optional: topics
The news topics of your choice. For example: topics=technology will filter for articles that write about the technology sector; topics=technology,ipo will filter for articles that simultaneously cover technology and IPO in their content. Below is the full list of supported topics:
<
Blockchain: blockchain
Earnings: earnings
IPO: ipo
Mergers & Acquisitions: mergers_and_acquisitions
Financial Markets: financial_markets
Economy - Fiscal Policy (e.g., tax reform, government spending): economy_fiscal
Economy - Monetary Policy (e.g., interest rates, inflation): economy_monetary
Economy - Macro/Overall: economy_macro
Energy & Transportation: energy_transportation
Finance: finance
Life Sciences: life_sciences
Manufacturing: manufacturing
Real Estate & Construction: real_estate
Retail & Wholesale: retail_wholesale
Technology: technology
>
❚ Optional: time_from and time_to
The time range of the news articles you are targeting, in YYYYMMDDTHHMM format. For example: time_from=20220410T0130. If time_from is specified but time_to is missing, the API will return articles published between the time_from value and the current time.
❚ Optional: sort
By default, sort=LATEST and the API will return the latest articles first. You can also set sort=EARLIEST or sort=RELEVANCE based on your use case.
❚ Optional: limit
By default, limit=50 and the API will return up to 50 matching results. You can also set limit=1000 to output up to 1000 results. If you are looking for an even higher output limit, please contact support@alphavantage.co to have your limit boosted.

URL examples with explanation :
"
Querying news articles that mention the AAPL ticker.
https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers=AAPL
Querying news articles that simultaneously mention the Coinbase stock (COIN), Bitcoin (CRYPTO:BTC), and US Dollar (FOREX:USD) and are published on or after 2022-04-10, 1:30am UTC.
https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers=COIN,CRYPTO:BTC,FOREX:USD&time_from=20220410T0130&limit=1000
"
"

The TOP_GAINERS_LOSERS (This endpoint returns the top 20 gainers, losers, and the most active traded tickers in the US market) has the following functions: 
"
❚ Required: function
The API function of your choice. In this case, function=TOP_GAINERS_LOSERS

URL examples with explanation : 
"
https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS
"
"

Fundamental Data:
<
The OVERVIEW (This API returns the company information, financial ratios, and other key metrics for the equity specified) section has the following functions : 
"
❚ Required: function
The function of your choice. In this case, function=OVERVIEW
❚ Required: symbol
The symbol of the ticker of your choice. For example: symbol=IBM.

URL examples with explanation : 
"
https://www.alphavantage.co/query?function=OVERVIEW&symbol=IBM
"
"

The INCOME_STATEMENT (This API returns the annual and quarterly income statements for the company of interest, with normalized fields mapped to GAAP and IFRS taxonomies of the SEC) section has the following functions:
"
❚ Required: function
The function of your choice. In this case, function=INCOME_STATEMENT
❚ Required: symbol
The symbol of the ticker of your choice. For example: symbol=IBM.

URL examples with explanation : 
"
Annual & quarterly income statements for IBM:
https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol=IBM
"
"


The BALANCE_SHEET (This API returns the annual and quarterly balance sheets for the company of interest, with normalized fields mapped to GAAP and IFRS taxonomies of the SEC) section has the following functions : 
"
❚ Required: function
The function of your choice. In this case, function=BALANCE_SHEET
❚ Required: symbol
The symbol of the ticker of your choice. For example: symbol=IBM.

URL examples with explanation : 
"
Annual & quarterly balance sheets for IBM:
https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol=IBM
"
"

The CASH_FLOW (This API returns the annual and quarterly cash flow for the company of interest, with normalized fields mapped to GAAP and IFRS taxonomies of the SEC) section has the following functions : 
"
❚ Required: function
The function of your choice. In this case, function=CASH_FLOW
❚ Required: symbol
The symbol of the ticker of your choice. For example: symbol=IBM.

URL examples with explanation : 
"
Annual & quarterly cash flows for IBM:
https://www.alphavantage.co/query?function=CASH_FLOW&symbol=IBM
"
"

The EARNINGS (This API returns the annual and quarterly earnings (EPS) for the company of interest. Quarterly data also includes analyst estimates and surprise metrics) section has the following functions : 
"
❚ Required: function
The function of your choice. In this case, function=EARNINGS
❚ Required: symbol
The symbol of the ticker of your choice. For example: symbol=IBM.

URL examples with explanation : 
"
https://www.alphavantage.co/query?function=EARNINGS&symbol=IBM
"
"

The LISTING_STATUS (This API returns a list of active or delisted US stocks and ETFs, either as of the latest trading day or at a specific time in history) has the following functions : 
"
❚ Required: function
The API function of your choice. In this case, function=LISTING_STATUS
❚ Optional: date
If no date is set, the API endpoint will return a list of active or delisted symbols as of the latest trading day. If a date is set, the API endpoint will "travel back" in time and return a list of active or delisted symbols on that particular date in history. Any YYYY-MM-DD date later than 2010-01-01 is supported. For example, date=2013-08-03
❚ Optional: state
By default, state=active and the API will return a list of actively traded stocks and ETFs. Set state=delisted to query a list of delisted assets.

URL examples with explanation : 
"
Querying all active stocks and ETFs as of the latest trading day:
https://www.alphavantage.co/query?function=LISTING_STATUS
Querying all delisted stocks and ETFs as of 2014-07-10:
https://www.alphavantage.co/query?function=LISTING_STATUS&date=2014-07-10&state=delisted
"
"

The EARNINGS_CALENDAR (This API returns a list of company earnings expected in the next 3, 6, or 12 months.) section has the following functions : 
"
❚ Required: function
The API function of your choice. In this case, function=EARNINGS_CALENDAR
❚ Optional: symbol
By default, no symbol will be set for this API. When no symbol is set, the API endpoint will return the full list of company earnings scheduled. If a symbol is set, the API endpoint will return the expected earnings for that specific symbol. For example, symbol=IBM
❚ Optional: horizon
By default, horizon=3month and the API will return a list of expected company earnings in the next 3 months. You may set horizon=6month or horizon=12month to query the earnings scheduled for the next 6 months or 12 months, respectively.

URL examples with explanation : 
"
Querying all the company earnings expected in the next 3 months:
https://www.alphavantage.co/query?function=EARNINGS_CALENDAR&horizon=3month
Querying all the earnings events for IBM in the next 12 months:
https://www.alphavantage.co/query?function=EARNINGS_CALENDAR&symbol=IBM&horizon=12month
"
"

The IPO_CALENDAR (This API returns a list of IPOs expected in the next 3 months) section has the following functions :
"
❚ Required: function
The API function of your choice. In this case, function=IPO_CALENDAR
URL examples with explanation : 
"
Querying all the company earnings expected in the next 3 months:
https://www.alphavantage.co/query?function=IPO_CALENDAR
"
"
>

Forex (FX):
<
The CURRENCY_EXCHANGE_RATE (This API returns the realtime exchange rate for a pair of digital currency (e.g., Bitcoin) and physical currency (e.g., USD)) section has the following functions : 
"
❚ Required: function
The function of your choice. In this case, function=CURRENCY_EXCHANGE_RATE
❚ Required: from_currency
The currency you would like to get the exchange rate for. It can either be a physical currency or digital/crypto currency. For example: from_currency=USD or from_currency=BTC.
❚ Required: to_currency
The destination currency for the exchange rate. It can either be a physical currency or digital/crypto currency. For example: to_currency=USD or to_currency=BTC.

URL examples with explanation : 
"
US Dollar to Japanese Yen:
https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=USD&to_currency=JPY
Bitcoin to Chinese Yuan:
https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=BTC&to_currency=CNY
"
"

The FX_DAILY (This API returns the daily time series (timestamp, open, high, low, close) of the FX currency pair specified, updated realtime) section has the following functions : 
"
❚ Required: function
The time series of your choice. In this case, function=FX_DAILY
❚ Required: from_symbol
A three-letter symbol from the forex currency list. For example: from_symbol=EUR
❚ Required: to_symbol
❚Required: datatype
In this case datatype = csv
A three-letter symbol from the forex currency list. For example: to_symbol=USD
❚ Optional: outputsize
By default, outputsize=compact. Strings compact and full are accepted with the following specifications: compact returns only the latest 100 data points in the daily time series; full returns the full-length daily time series. The "compact" option is recommended if you would like to reduce the data size of each API call.

URL examples with explanation : 
"
https://www.alphavantage.co/query?function=FX_DAILY&from_symbol=EUR&to_symbol=USD&datatype=csv
https://www.alphavantage.co/query?function=FX_DAILY&from_symbol=EUR&to_symbol=USD&outputsize=full&datatype=csv
"
"

The FX_WEEKLY (This API returns the weekly time series of the FX currency pair specified, updated realtime) section has the following functions : 
"
❚ Required: function
The time series of your choice. In this case, function=FX_WEEKLY
❚ Required: from_symbol
A three-letter symbol from the forex currency list. For example: from_symbol=EUR
❚ Required: to_symbol
A three-letter symbol from the forex currency list. For example: to_symbol=USD
❚ Required: datatype
In this case datatype=csv

URL examples with explanation : 
"
https://www.alphavantage.co/query?function=FX_WEEKLY&from_symbol=EUR&to_symbol=USD&datatype=csv
"
"

The FX_MONTHLY (This API returns the monthly time series of the FX currency pair specified, updated real time) section has the following functions : 
"
❚ Required: function
The time series of your choice. In this case, function=FX_MONTHLY
❚ Required: from_symbol
A three-letter symbol from the forex currency list. For example: from_symbol=EUR
❚ Required: to_symbol
A three-letter symbol from the forex currency list. For example: to_symbol=USD
❚ Required: datatype
In this case datatype = csv.

URL examples with explanation : 
"
https://www.alphavantage.co/query?function=FX_MONTHLY&from_symbol=EUR&to_symbol=USD&datatype=csv
"
"
>

Cryptocurrencies : 
<
The CURRENCY_EXHANGE_RATE (This API returns the realtime exchange rate for any pair of digital currency (e.g., Bitcoin) or physical currency (e.g., USD)) section has the following functions : 
"
❚ Required: function
The function of your choice. In this case, function=CURRENCY_EXCHANGE_RATE
❚ Required: from_currency
The currency you would like to get the exchange rate for. It can either be a physical currency or digital/crypto currency. For example: from_currency=USD or from_currency=BTC.
❚ Required: to_currency
The destination currency for the exchange rate. It can either be a physical currency or digital/crypto currency. For example: to_currency=USD or to_currency=BTC.

URL examples with explanation : 
"
Bitcoin to Chinese Yuan:
https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=BTC&to_currency=CNY
US Dollar to Japanese Yen:
https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=USD&to_currency=JPY
"
"

The DIGITAL_CURRENCY_DAILY (This API returns the daily historical time series for a digital currency (e.g., BTC) traded on a specific market (e.g., CNY/Chinese Yuan), refreshed daily at midnight (UTC)) has the following functions : 
"
❚ Required: function
The time series of your choice. In this case, function=DIGITAL_CURRENCY_DAILY
❚ Required: symbol
The digital/crypto currency of your choice. It can be any of the currencies in the digital currency list. For example: symbol=BTC.
❚ Required: market
The exchange market of your choice. It can be any of the market in the market list. For example: market=CNY.
❚Required: datatype
In this case datatype = csv

URL examples with explanation : 
"
https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol=BTC&market=CNY&datatype=csv
"
"

The DIGITAL_CURRENCY_WEEKLY (This API returns the weekly historical time series for a digital currency (e.g., BTC) traded on a specific market (e.g., CNY/Chinese Yuan), refreshed daily at midnight (UTC)) section has the following functions : 
"
❚ Required: function
The time series of your choice. In this case, function=DIGITAL_CURRENCY_WEEKLY
❚ Required: symbol
The digital/crypto currency of your choice. It can be any of the currencies in the digital currency list. For example: symbol=BTC.
❚ Required: market
The exchange market of your choice. It can be any of the market in the market list. For example: market=CNY.
❚Required: datatype
In this case datatype = csv

URL examples with explanation : 
"
https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_WEEKLY&symbol=BTC&market=CNY&datatype=csv
"
"

The DIGITAL_CURRENCY_MONTHLY (This API returns the monthly historical time series for a digital currency (e.g., BTC) traded on a specific market (e.g., CNY/Chinese Yuan), refreshed daily at midnight (UTC)) section has the following functions :
"
❚ Required: function
The time series of your choice. In this case, function=DIGITAL_CURRENCY_MONTHLY
❚ Required: symbol
The digital/crypto currency of your choice. It can be any of the currencies in the digital currency list. For example: symbol=BTC.
❚ Required: market
The exchange market of your choice. It can be any of the market in the market list. For example: market=CNY.
❚Required: datatype
In this case datatype = csv

URL examples with explanation : 
"
https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_MONTHLY&symbol=BTC&market=CNY&datatype=csv
"
" 
>


Economic Indicators :
<
The REAL_GDP (This API returns the annual and quarterly Real GDP of the United States) section has the following functions : 
"
❚ Required: function
The function of your choice. In this case, function=REAL_GDP
❚ Optional: interval
By default, interval=annual. Strings quarterly and annual are accepted.
❚ Required: datatype
In this case datatype = csv

URL examples with explanation : 
"
https://www.alphavantage.co/query?function=REAL_GDP&interval=annual&datatype=csv
"
"

The REAL_GDP_PER_CAPITA (This API returns the quarterly Real GDP per Capita data of the United States) section has the following functions : 
"
❚ Required: function
The function of your choice. In this case, function=REAL_GDP_PER_CAPITA
❚ Required: datatype
In this case datatype = csv

URL examples with explanation : 
"
https://www.alphavantage.co/query?function=REAL_GDP_PER_CAPITA&datatype=csv
"
"

The TREASURY_YIELD (This API returns the daily, weekly, and monthly US treasury yield of a given maturity timeline (e.g., 5 year, 30 year, etc)) section has the following functions : 
"
❚ Required: function
The function of your choice. In this case, function=TREASURY_YIELD
❚ Optional: interval
By default, interval=monthly. Strings daily, weekly, and monthly are accepted.
❚ Optional: maturity
By default, maturity=10year. Strings 3month, 2year, 5year, 7year, 10year, and 30year are accepted.
❚ Required: datatype
In this case datatype = csv

URL examples with explanation : 
"
https://www.alphavantage.co/query?function=TREASURY_YIELD&interval=monthly&maturity=10year&datatype=csv
"
"

The FEDERAL_FUNDS_RATE (This API returns the daily, weekly, and monthly federal funds rate (interest rate) of the United States) section has the following functions : 
"
❚ Required: function
The function of your choice. In this case, function=FEDERAL_FUNDS_RATE
❚ Optional: interval
By default, interval=monthly. Strings daily, weekly, and monthly are accepted.
❚ Required: datatype
In this case datatype = csv

URL examples with explanation : 
"
https://www.alphavantage.co/query?function=FEDERAL_FUNDS_RATE&interval=monthly&datatype=csv
"
"

The CPI (This API returns the monthly and semiannual consumer price index (CPI) of the United States) section has the following functions : 
"
❚ Required: function
The function of your choice. In this case, function=CPI
❚ Optional: interval
By default, interval=monthly. Strings monthly and semiannual are accepted.
❚ Required: datatype
In this case datatype = csv

URL examples with explanation : 
"
https://www.alphavantage.co/query?function=CPI&interval=monthly&datatype=csv
"
"

The INFLATION (This API returns the annual inflation rates (consumer prices) of the United States) section has the following functions : 
"
❚ Required: function
The function of your choice. In this case, function=INFLATION
❚ Required: datatype
In this case datatype = csv

URL examples with explanation : 
"
https://www.alphavantage.co/query?function=INFLATION&datatype=csv
"
"

The RETAIL_SALES (This API returns the monthly Advance Retail Sales: Retail Trade data of the United States) section has the following functions : 
"
❚ Required: function
The function of your choice. In this case, function=RETAIL_SALES
❚ Required: datatype
In this case datatype = csv.

URL examples with explanation : 
"
https://www.alphavantage.co/query?function=RETAIL_SALES&datatype=csv
"
"

The DURABLE (This API returns the monthly manufacturers' new orders of durable goods in the United States) section has the following functions : 
"
API Parameters
❚ Required: function
The function of your choice. In this case, function=DURABLES
❚ Required: datatype
In this case datatype = csv

URL examples with explanation : 
"
https://www.alphavantage.co/query?function=DURABLES&datatype=csv
"
"

The UNEMPLOYMENT (This API returns the monthly unemployment data of the United States.) section has the following functions : 
"
❚ Required: function
The function of your choice. In this case, function=UNEMPLOYMENT
❚ Required: datatype
In this case datatype = csv.

URL examples with explanation : 
"
https://www.alphavantage.co/query?function=UNEMPLOYMENT&datatype=csv
"
"

The NONFARM_PAYROLL (This API returns the monthly US All Employees: Total Nonfarm (commonly known as Total Nonfarm Payroll), a measure of the number of U.S. workers in the economy that excludes proprietors, private household employees, unpaid volunteers, farm employees, and the unincorporated self-employed) section has the following functions : 
"
❚ Required: function
The function of your choice. In this case, function=NONFARM_PAYROLL
❚ Required: datatype
In this case datatype = csv

URL examples with explanation : 
"
https://www.alphavantage.co/query?function=NONFARM_PAYROLL&datatype=csv
"
"
>

You need to the construct the request URL by analyzing the given text, using the available functions given in the above sections. Construct a few word title for the user's query. 
NOTE : Give ONLY AND ONLY a python dictionary in the following format:\n
{url_dict}
The text is : "{user_text}"""
        "",
        generation_config=parameters,
        stream=False,
    )

    print(f"\n\n{response.text}\n\n")
    json_string_without_backticks = response.text.replace("`", "")
    element = "{"

    split_parts = json_string_without_backticks.split(element)
    if len(split_parts) > 1:
        json_string_without_backticks = split_parts[1].strip()
        json_string_without_backticks = "{" + json_string_without_backticks
        clean_json_answer = json.loads(json_string_without_backticks)
        print(f"{clean_json_answer}\n\n")
    else:
        print("Element not found in the string.")

    return clean_json_answer


def write_to_file(data, session_ID):
    # writing to txt file
    directory_path = f"/home/ksgcpcloud/myapp/data/{session_ID}"
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print("Directory created")
    else:
        print("Directory already exists")
    with open(f"{directory_path}/data.txt", "w") as f:
        f.write(data)


def get_url_fetch_data(json_text):
    url = json_text["url"] + "&apikey=ENTER YOU ALPHA VANTAGE API KEY HERE"
    r = requests.get(url)
    return r.text


def table_queries_2(user_query, session_ID):
    print("I am in queries 2")
    try:
        data_frame = pd.read_csv(StringIO(get_tabular_data(session_ID)))
    except:
        data_frame = pd.read_csv(StringIO(get_tabular_data(session_ID)[1]))
    df = SmartDataframe(data_frame, config={"llm": llm})
    response = df.chat(user_query)
    return response


def table_queries_1(user_query, session_ID):
    print("I am in queries 1")
    try:
        data_frame = pd.read_csv(StringIO(get_tabular_data(session_ID)))
    except:
        data_frame = pd.read_csv(StringIO(get_tabular_data(session_ID)[0]))
    print(f"I am printing df here:\n{data_frame}")
    df = SmartDataframe(data_frame, config={"llm": llm})
    response = df.chat(user_query)
    return response


def data_retrieval_main(user_table_text, session_ID):
    write_to_file(
        get_url_fetch_data(get_url_generation_functionality(user_table_text)),
        session_ID,
    )
    return get_tabular_data(session_ID)


if __name__ == "__main__":
    while True:
        text = input("Enter text here:\n")
        data = get_url_generation_functionality(text)

        write_to_file(get_url_fetch_data(data))
        data_frame = get_tabular_data()[0]
        data_frame2 = pd.read_csv(StringIO(data_frame)).infer_objects()
        print(data_frame2.dtypes)
        # data_frame2 = data_frame.convert_dtypes()
        # print(data_frame2.dtypes)
        text2 = input("Enter data query here:\n")
        # agent = create_pandas_dataframe_agent(
        #     VertexAI(temperature=0.2, model_name="gemini-pro", max_output_tokens=1024),
        #     data_frame2,
        #     verbose=True,
        # )
        # answer = agent.run(text2)
        # print(answer)
