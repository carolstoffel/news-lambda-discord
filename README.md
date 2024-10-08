# News to Discord Lambda Function

This repository contains an AWS Lambda function that fetches the latest news headlines related to "war" from a news API and sends the updates to a Discord channel via a webhook.

## Overview

The Lambda function uses the mediastack API to retrieve the most recent news headlines and formats them into a message that is then sent to a specified Discord channel using a webhook URL. The function is designed to be run on a schedule, such as every hour during work hours.

## Environment Variables

The following environment variables must be configured for the Lambda function to operate:

- `API_NEWS_KEY`: Your API key for accessing the News API.
- `DISCORD_WEBHOOK_URL`: The webhook URL for your Discord channel.
- `API_NEWS_URL`: The base URL for the News API (`https://mediastack.com/documentation`).

## Lambda Function

The function is written in Python and performs the following steps:

1. Retrieves sensitive data (API key, Discord webhook URL, News API URL) from environment variables set on AWS configuration.
2. Sends a request to the API to fetch news related to a specific topic, in this case "war" and "ucraine".
3. Extracts relevant data (title, description, URL, published date) from the response.
4. Formats the extracted data into a message.
5. Sends the message to a Discord channel using the specified webhook URL.
6. Returns a success or failure status based on the response from the Discord webhook.


## Deployment

To deploy the Lambda function, follow these steps:

1. Package the code and dependencies into a ZIP file.
    1.1  You'll need to run this command locally to download the requests folder into your machine ```pip install requests -t .```. 
2. Upload the ZIP file to AWS Lambda.
3. Configure the environment variables in the Lambda function settings.
4. Set up a trigger for the Lambda function, such as a CloudWatch Events rule for scheduled execution.(i.e. 0 9-19 ? * MON-FRI *)


## Images

[![Screenshot1](https://i.postimg.cc/G2hq1zTP/Captura-de-tela-2024-09-11-113924.png)](https://postimg.cc/LqwzttTh)