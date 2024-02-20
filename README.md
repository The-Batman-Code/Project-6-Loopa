# Loopa

# Introduction - 
This project offers a two-pronged approach to investment exploration. One, a chat interface powered by the investment-focused LLM Loopa provides personalized advice. Two, another LLM taps into Alpha Vantage's market data, allowing you to ask questions like "Give me daily forex rates in INR" and get the answer in a downloadable CSV format. You can then delve deeper using Pandas or visualize it with an auto-generated dashboard. It's your one-stop shop for investment research and analysis!

# Chat Interface - 
![](Images/loopa-1.png)

# Data Query Interface - 
![](Images/loopa-2.png)

# Architecture - 
![](Images/archi-1.png)

![](Images/archi-2.png)

# How to deploy the Data Query Interface?
1. Head over to your GCP console and create a service account json key with the following configurations - 

![](Images/config-1.png)

2. Replace the info in the file 'loopa_key.json' with you json key info in the 'Compute_Engine/V2' folder.
3. Head over to the Compute Engine section in GCP and create a VM of the following configurations - 

![](Images/config-2.png)

![](Images/config-3.png)

![](Images/config-4.png)















