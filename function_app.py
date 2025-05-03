import logging
import azure.functions as func
import requests
import json
from azure.eventhub import EventHubProducerClient, EventData
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

app = func.FunctionApp()

@app.timer_trigger(schedule="*/60 * * * * *", arg_name="myTimer", run_on_startup=False, use_monitor=False)
def coinrankingfunctionTrigger(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function executed.')

    # Event Hub configurations
    eventhub_name = "coinrankingeventhub"
    eventhub_namespace = "coinrankingstreaming.servicebus.windows.net"

    # Initialize the Event Hub producer using Managed Identity
    credential = DefaultAzureCredential()
    producer = EventHubProducerClient(
        fully_qualified_namespace=eventhub_namespace,
        eventhub_name=eventhub_name,
        credential=credential
    )

    # Function to send events to Event Hub
    def send_eventhub_message(message):
        event_data_batch = producer.create_batch()
        event_data_batch.add(EventData(json.dumps(message)))
        producer.send_batch(event_data_batch)

    # Function to handle the API response
    def handle_api_response(response):
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Request failed with status code {response.status_code}"}

    # Function to fetch cryptocurrency data from CoinRanking API
    def fetch_coinranking_data(base_url, api_key):
        url = f"{base_url}/v2/coins"
        headers = {"x-access-token": api_key}
        response = requests.get(url, headers=headers)
        return handle_api_response(response)

    # Function to flatten and structure the CoinRanking data
    def flatten_coinranking_data(data):
        coins = data.get("data", {}).get("coins", [])
        flattened_data = [
            {
                "id": coin.get("id", ""),
                "symbol": coin.get("symbol", ""),
                "name": coin.get("name", ""),
                "price": coin.get("price", ""),
                "marketCap": coin.get("marketCap", ""),
                "change": coin.get("change", ""),
                "rank": coin.get("rank", ""),
                "volume": coin.get("24hVolume", ""),
                "btcPrice": coin.get("btcPrice", ""),
                "sparkline": coin.get("sparkline", ""),
                "lowVolume": coin.get("lowVolume", ""),
                "coinrankingUrl": coin.get("coinrankingUrl", ""),
                "color": coin.get("color", ""),
                "iconUrl": coin.get("iconUrl", ""),
                "websiteUrl": coin.get("websiteUrl", ""),
                "explorerUrl": coin.get("explorerUrl", ""),
                "twitterUrl": coin.get("twitterUrl", ""),
            }
            for coin in coins
        ]
        return flattened_data

    # Function to get the API key from Azure Key Vault
    def get_secret_from_key_vault(vault_url, secret_name):
        try:
            credential = DefaultAzureCredential()
            client = SecretClient(vault_url=vault_url, credential=credential)
            secret = client.get_secret(secret_name)
            return secret.value
        except Exception as e:
            logging.error(f"Failed to retrieve secret '{secret_name}' from Key Vault: {e}")
            return None

    # Main program
    def fetch_and_stream_coinranking_data():
        base_url = "https://api.coinranking.com"
        vault_url = "https://cryptocoinstreamingkv.vault.azure.net/"  # Replace with your Key Vault URL
        coinranking_secret_name = "coinrankingsecretKV"  # Replace with your secret name

        # Fetch the API key from Azure Key Vault
        api_key = get_secret_from_key_vault(vault_url, coinranking_secret_name)

        # Fetch data from CoinRanking API
        coinranking_data = fetch_coinranking_data(base_url, api_key)

        # Flatten and structure the data
        flattened_data = flatten_coinranking_data(coinranking_data)

        # Send data to Event Hub
        for coin_data in flattened_data:
            send_eventhub_message(coin_data)

    # Calling the Main Program
    fetch_and_stream_coinranking_data()