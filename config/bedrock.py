from dotenv import load_dotenv
import os
load_dotenv('.keys')


def get_bedrock_config():
    config_list_bedrock = [
        {
            "api_type": "bedrock",
            "model": "anthropic.claude-3-sonnet-20240229-v1:0",
            "aws_region": "us-east-1",
            "aws_access_key": os.getenv("AWS_ACCESS_KEY_ID"),
            "aws_secret_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
            "price": [0.003, 0.015],
            "temperature": 0.1,
            "cache_seed": None,  # turn off caching
        }
    ]
    return config_list_bedrock
