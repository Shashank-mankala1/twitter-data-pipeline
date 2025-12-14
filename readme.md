# Twitter Data Engineering Pipeline

## Project Overview

This project demonstrates an end-to-end data engineering pipeline built using AWS EC2, Amazon S3, Apache Airflow, and Python.  
The pipeline extracts tweets from Twitter using the Tweepy API, performs basic transformations, and stores the processed data in a structured format.  
The entire ETL process is orchestrated using Airflow DAGs running on an EC2 instance.


## Architecture

**Tech Stack**
- AWS EC2 – Host Airflow and run scheduled jobs
- Apache Airflow – Workflow orchestration and scheduling
- Amazon S3 – Data storage layer
- Python – ETL logic
- Tweepy – Twitter API integration
- Pandas – Data transformation
- s3fs – Interface between Pandas and S3

**Pipeline Flow**
1. Airflow scheduler triggers the DAG daily
2. Python ETL script connects to Twitter API
3. Tweets are extracted and transformed into tabular format
4. Output data is stored as CSV in S3 or locally


## Project Structure
```
├── twitter_dag.py # Airflow DAG definition
├── twitter_etl.py # Twitter ETL logic
├── refined_tweets.csv # Output file
├── .env # Environment variables (excluded from Git)
└── README.md
```

## Airflow DAG Details

- DAG Name: twitter_dag  
- Schedule: Daily  
- Operator: PythonOperator  
- Task ID: complete_twitter_etl  
- Start Date: 2021-11-08  

The DAG executes a Python callable that runs the complete Twitter ETL process.

---

## ETL Process

### Extract
- Authenticates with Twitter API using OAuth
- Fetches recent tweets from a specified user
- Excludes retweets
- Retrieves full tweet text

### Transform
- Selects relevant attributes:
  - user
  - text
  - favorite_count
  - retweet_count
  - created_at
- Converts data into a Pandas DataFrame

### Load
- Saves transformed data as a CSV file
- Can be configured to write directly to an S3 bucket


## Environment Variables

Create a `.env` file in the project root:

```
ACCESS_KEY=your_access_key
ACCESS_SECRET=your_access_secret
CONSUMER_KEY=your_consumer_key
CONSUMER_SECRET=your_consumer_secret
```



## How to Run

### 1. Setup EC2
- Launch an EC2 instance
- Install Python, pip, and Apache Airflow
- Initialize Airflow metadata database

### 2. Install Dependencies
``` pip install tweepy pandas python-dotenv s3fs apache-airflow ```


### 3. Configure Airflow
- Move `twitter_dag.py` to the `dags/` directory
- Ensure `twitter_etl.py` is accessible in the Python path

### 4. Start Airflow Services

```
airflow scheduler
airflow webserver
```


### 5. Trigger the DAG
- Open Airflow UI
- Enable and trigger `twitter_dag`


## Sample Output

The pipeline generates a CSV file with structured tweet data:
```
| user | text | favorite_count | retweet_count | created_at |
```

## Key Learnings

- Building ETL pipelines using Python
- Workflow orchestration with Apache Airflow
- Integrating third-party APIs
- Using AWS EC2 and S3 for data pipelines
- Managing secrets using environment variables
