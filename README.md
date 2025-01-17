# Weather Data Analytics Project

This project integrates the OpenWeatherMap API with AWS services to perform analytics. The project fetches data from the OpenWeatherMap API, stores it in an S3 bucket, catalogs the data using AWS Glue, and queries it using Amazon Athena.

## Project Structure

```
weather-insights
├── src
│   ├── fetch_data.py        # Main script for fetching data and uploading data in s3
│   ├── requirements.txt
|   ├── cities.json
|   └── Dockerfile           # Defines the Docker image for the application
├── terraform
│   ├── main.tf              # Main Terraform configuration for AWS resources
│   ├── variables.tf         # Variables for Terraform configuration
│   ├── output.tf           # Outputs of the Terraform configuration
|   ├── terraform.tfvars
|   ├── iam-policy.json
|   ├── Dockerfile
│   └── iam_roles.tf         # IAM roles and policies for AWS access
├── README.md                # Documentation for the project
├── .env
├── docker-compose.yaml
└── .gitignore               # Files and directories to ignore in version control

```

## Setup Instructions

### Prerequisites

1. **Docker**: Ensure Docker is installed on your machine.
2. **AWS Account**: Ensure you have an AWS account with the necessary permissions to create S3 buckets, Glue databases, and Glue crawlers.
3. **OpenWeatherMap API Key**: Ensure you have an API key from OpenWeatherMap.

### Steps

1. **Clone the Repository**:
   ```sh
   git clone https://github.com/Rene-Mayhrem/weather-insights.git
   cd weather-insights
   ```

2. **Create a .env File**: Create a `.env` file in the root directory with your AWS credentials and OpenWeatherMap API key:
   ```
   AWS_ACCESS_KEY_ID=<your-access-key-id>
   AWS_SECRET_ACCESS_KEY=<your-secret-access-key>
   AWS_REGION=us-east-1
   S3_BUCKET_NAME=<your-s3-bucket-name>
   OPENWEATHER_API_KEY=<your-openweather-api-key>
   ```

3. **Create a cities.json File**: Create a `cities.json` file in the root directory with a list of cities to study:
   ```json
   {
     "cities": [
       "London",
       "New York",
       "Tokyo",
       "Paris",
       "Berlin"
     ]
   }
   ```

4. **Using Docker Compose**: Build and run the services:
   ```sh
   docker compose run terraform init
   docker compose run python
   ```

## Usage

After running the Docker containers, follow these steps:

1. **Verify Infrastructure Setup**:
   - Ensure that Terraform has successfully created the necessary AWS resources (S3 bucket, Glue database, and Glue crawler).
   - You can check the AWS Management Console to verify that these resources have been created.

2. **Verify Data Upload**:
   - Ensure that the Python script has successfully fetched weather data for the specified cities and uploaded the data to the S3 bucket.
   - You can check the S3 bucket in the AWS Management Console to verify that the JSON files have been uploaded.

3. **Run the Glue Crawler**:
   - The Glue crawler should automatically run if it was set up correctly. This will catalog the data in the S3 bucket.
   - You can check the Glue console to verify that the crawler has run and that the data has been cataloged.

4. **Query Data with Athena**:
   - Use Amazon Athena to query the data cataloged by Glue.
   - You can access Athena through the AWS Management Console and run SQL queries on the data.

## License

This project is licensed under the MIT License. See the LICENSE file for details.