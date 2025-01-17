import requests
import json
import os
import boto3

def fetch_weather_data(api_key, city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def upload_to_s3(file_name, bucket_name):
    # Create an S3 client using boto3
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
        region_name=os.environ.get('AWS_REGION')
    )
    with open(file_name, 'r') as f:
        data = json.load(f)
    # Upload the JSON data to the specified S3 bucket
    s3_client.put_object(Bucket=bucket_name, Key=file_name, Body=json.dumps(data))
