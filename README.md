In today’s data-driven world, real-time insights are important especially in fast-moving markets like cryptocurrency. I recently completed an exciting project where I designed and deployed an end-to-end ETL streaming pipeline to fetch live crypto data from the CoinRanking API and visualize it in Power BI, all built on Microsoft Azure.
The Problem 
Crypto prices fluctuate by the second. Static reports and batch processing can’t keep up. Hence, the reason for the project to:
•	Automate data ingestion from a third-party API
•	Stream and process the data in near real-time
•	Enable business users to interact with insights instantly

The Solution: Azure-Powered Streaming Pipeline
Here's a high-level breakdown of the architecture:
Data Source: CoinRanking API
Fetches live market data such as price, market cap, volume, etc., every 60 seconds.
⚙️ Azure Function (Timer Trigger)
•	Acts as the ETL orchestrator.
•	Scheduled to run every 30 seconds.
•	Uses Managed Identity to authenticate securely with other Azure services like Azure EventHub.
•	Calls the API and sends it to Event Hub.
🔐 Azure Key Vault
Securely stores the API keys used by the Function App to authenticate requests.
🧵 Azure Event Hub
Serves as the real-time data ingestion service (data streaming bus) to decouple data producers and consumers. Also, used the Data Explorer feature to view the streaming events (overview).
🧩 Microsoft Fabric (Eventstream + Eventhouse)
•	Eventstream captures data in real-time.
•	Eventhouse stores structured event data for analytics in the KQL (Kusto Query Language) database.
📊 Power BI
Connected to Eventhouse to visualize and analyze data trends in real-time dashboards and reports.

💡 What Makes This Special?
•	Serverless and Scalable: Azure Function handles workload efficiently without manual scaling. 
•	Secure: Managed Identity and Key Vault ensure zero hardcoded secrets.
•	Real-time Insight: From data capture to dashboard updates in seconds.
•	Future-Ready: Modular design makes it easy to integrate more APIs or analytics tools.

🎯 What are the Use Cases for this project?
•	Financial monitoring for traders
•	Risk and volatility dashboards for FinTechs
•	Real-time analytics in investment platforms
________________________________________
👨‍💻 Technologies Used
•	Python 
•	Azure Functions
•	Azure Key Vault
•	Azure Event Hub
•	Microsoft Fabric (Eventstream, Eventhouse)
•	Power BI

📈 Final Thoughts
This project demonstrates the power of combining serverless computing, secure access management, and real-time analytics into one seamless solution. If you're looking to modernize your data pipelines or bring streaming analytics into your organization, Azure has the tools to make it happen.
