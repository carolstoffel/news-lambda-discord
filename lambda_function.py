import json
import requests
import os


def lambda_handler(event, context):
    # Get sensitive data from environment variables
    api_news_key = os.getenv("API_NEWS_KEY")
    discord_webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    api_news_url = os.getenv("API_NEWS_URL")

    # Query used to fetch news data from API
    query = "country=ua&sources=en&keywords=war&sort=published_desc&limit=1"

    try:
        news_data_req = requests.get(
            f"{api_news_url}?access_key={api_news_key}&{query}"
        )
        news_data_req.raise_for_status()

        # Extract relevant data from the response
        news_data = {}
        news_data["title"] = news_data_req.json()["data"][0]["title"]
        news_data["description"] = news_data_req.json()["data"][0]["description"]
        news_data["url"] = news_data_req.json()["data"][0]["url"]
        news_data["published_at"] = news_data_req.json()["data"][0]["published_at"]

        message_content = (
            f"**Headline:** {news_data['title']}\n\n"
            f"**Description:** {news_data['description']}\n\n"
            f"**URL:** [Read more here]({news_data['url']})\n\n"
            f"**Published At:** {news_data['published_at']}\n"
        )

    except requests.exceptions.RequestException as e:
        message_content = f"It was not possible to get news data due to: {str(e)}"

    payload = {"content": message_content}

    # Send the message to the Discord channel using the webhook
    response = requests.post(discord_webhook_url, json=payload)

    # Check if the request was successful
    if response.status_code == 204:
        return {"statusCode": 200, "body": json.dumps("Message sent successfully!")}
    else:
        return {
            "statusCode": response.status_code,
            "body": json.dumps("Failed to send message."),
        }
