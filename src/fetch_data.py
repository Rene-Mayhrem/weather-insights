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

def create_glue_table(database_name, table_name, s3_location):
    # Create a Glue client using boto3
    glue_client = boto3.client(
        'glue',
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
        region_name=os.environ.get('AWS_REGION')
    )
    # Create a table in the specified Glue database
    glue_client.create_table(
        DatabaseName=database_name,
        TableInput={
            'Name': table_name,
            'StorageDescriptor': {
                'Columns': [
                    {'Name': 'city', 'Type': 'string'},
                    {'Name': 'weather', 'Type': 'array<struct<main:string,description:string,icon:string>>'},
                    {'Name': 'main', 'Type': 'struct<temp:double,feels_like:double,temp_min:double,temp_max:double,pressure:int,humidity:int>'},
                    {'Name': 'wind', 'Type': 'struct<speed:double,deg:int>'},
                    {'Name': 'clouds', 'Type': 'struct<all:int>'},
                    {'Name': 'dt', 'Type': 'int'},
                    {'Name': 'sys', 'Type': 'struct<country:string,sunrise:int,sunset:int>'},
                    {'Name': 'timezone', 'Type': 'int'},
                    {'Name': 'id', 'Type': 'int'},
                    {'Name': 'name', 'Type': 'string'},
                    {'Name': 'cod', 'Type': 'int'}
                ],
                'Location': s3_location,
                'InputFormat': 'org.apache.hadoop.mapred.TextInputFormat',
                'OutputFormat': 'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat',
                'SerdeInfo': {
                    'SerializationLibrary': 'org.openx.data.jsonserde.JsonSerDe'
                }
            },
            'TableType': 'EXTERNAL_TABLE'
        }
    )

def main():
    api_key = os.environ.get('OPENWEATHER_API_KEY')
    
    # Load the list of cities from a JSON file
    with open('cities.json', 'r') as f:
        cities = json.load(f)['cities']
    
    os.makedirs('data', exist_ok=True)
    
    bucket_name = os.environ.get('S3_BUCKET_NAME')
    database_name = 'weather_database'  # This should match the database created in Terraform
    table_name = 'weather_data'
    s3_location = f's3://{bucket_name}/data/'
    
    for city in cities:
        data = fetch_weather_data(api_key, city)
        file_name = f'data/weather_data_{city}.json'
        with open(file_name, 'w') as f:
            json.dump(data, f)
        
        # Upload data to S3
        upload_to_s3(file_name, bucket_name)

    # Create Glue table
    create_glue_table(database_name, table_name, s3_location)

if __name__ == "__main__":
    main()