# Real-Time Stock Market Data Pipeline

End-to-end real-time data pipeline that streams live stock market data using Apache Kafka and AWS — ingesting, storing, cataloging, and querying ticker events at scale.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Apache Kafka](https://img.shields.io/badge/Apache_Kafka-231F20?style=flat&logo=apachekafka&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-232F3E?style=flat&logo=amazonaws&logoColor=white)
![Amazon S3](https://img.shields.io/badge/Amazon_S3-569A31?style=flat&logo=amazons3&logoColor=white)
![AWS Glue](https://img.shields.io/badge/AWS_Glue-FF9900?style=flat&logo=amazonaws&logoColor=white)
![Amazon Athena](https://img.shields.io/badge/Amazon_Athena-232F3E?style=flat&logo=amazonaws&logoColor=white)
![CI](https://github.com/saisudhagondi19/kafka-stock-market-pipeline/actions/workflows/ci.yml/badge.svg)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)

---

## Architecture

```
Stock Market Dataset (CSV / Financial API)
          │
          ▼
  Python Producer (Boto3 SDK)
  Fetches data → Publishes to Kafka topic
          │
          ▼
  Apache Kafka (on AWS EC2)
  Topic: stock_market_data
          │
          ▼
  Python Consumer
  Subscribes → Reads events → Writes to S3
          │
          ▼
  Amazon S3 (Raw Storage)
  Stores JSON/CSV per event
          │
          ▼
  AWS Glue Crawler
  Auto-infers schema → Updates Glue Data Catalog
          │
          ▼
  Amazon Athena
  SQL queries on S3 data via Glue Catalog
```

---

## Tech Stack

| Component | Technology |
|---|---|
| Streaming backbone | Apache Kafka (EC2-hosted) |
| Producer / Consumer | Python + Boto3 SDK |
| Compute | AWS EC2 |
| Storage | Amazon S3 |
| Schema discovery | AWS Glue Crawler + Glue Data Catalog |
| Ad-hoc querying | Amazon Athena (standard SQL) |
| ETL | AWS Glue |

---

## How It Works

**1. Data Production**
A Python producer reads stock market data and publishes events to a Kafka topic (`stock_market_data`) at ~1,000 events/second. The producer runs on an EC2 instance using the Boto3 SDK for AWS integration.

**2. Kafka Streaming**
Apache Kafka, deployed on EC2, acts as the distributed messaging layer. It decouples the producer and consumer, ensures fault tolerance, and handles high-throughput data streams reliably.

**3. Data Consumption & Storage**
A Python consumer subscribes to the Kafka topic, reads events in real time, and writes them to an Amazon S3 bucket partitioned by date and ticker symbol for efficient querying.

```
s3://your-bucket/
└── stock-data/
    └── year=2024/
        └── month=06/
            └── day=01/
                └── AAPL_events.json
```

**4. Schema Discovery**
An AWS Glue Crawler scans the S3 bucket, automatically infers the schema, and updates the Glue Data Catalog — no manual schema definition required.

**5. Ad-hoc Analysis**
Amazon Athena queries the cataloged data directly from S3 using standard SQL — no data movement, no ETL required for analysis.

```sql
-- Example: Average closing price by ticker
SELECT ticker, AVG(price) AS avg_price
FROM stock_market_data
WHERE date = '2024-06-01'
GROUP BY ticker
ORDER BY avg_price DESC;
```

---

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/saisudhagondi19/kafka-stock-market-pipeline.git
cd kafka-stock-market-pipeline
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Start Kafka on EC2**
```bash
# Start Zookeeper
bin/zookeeper-server-start.sh config/zookeeper.properties

# Start Kafka broker
bin/kafka-server-start.sh config/server.properties

# Create topic
bin/kafka-topics.sh --create --topic stock_market_data \
  --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1
```

**4. Configure AWS credentials**

Store your AWS credentials using environment variables — never hardcode them:
```bash
export AWS_REGION=us-east-1
export S3_BUCKET=your-bucket-name
```

**5. Run the producer**
```bash
python producer.py
```

**6. Run the consumer**
```bash
python consumer.py
```

**7. Trigger Glue Crawler** via AWS Console or CLI:
```bash
aws glue start-crawler --name stock-market-crawler
```

**8. Query with Athena**

Open Amazon Athena in the AWS Console → select the Glue catalog database → run SQL queries on your stock data.

---

## Project Structure

```
kafka-stock-market-pipeline/
├── producer.py          # Kafka producer — reads data, publishes to topic
├── consumer.py          # Kafka consumer — reads topic, writes to S3
├── requirements.txt
├── config/
│   └── kafka_config.py  # Broker and topic configuration (no secrets)
└── README.md
```

---

## Requirements

```
kafka-python
boto3
pandas
```

---

## Key Features

- Real-time ingestion at ~1,000 events/second
- Fault-tolerant Kafka setup with 3 partitions and replication
- S3 storage partitioned by date and ticker for optimized Athena queries
- Schema auto-discovery via Glue Crawler — zero manual schema management
- Serverless querying with Athena — pay only per query, no cluster needed

---

## Future Work

- Add Kafka consumer group for parallel processing across multiple consumers
- Integrate AWS Lambda to trigger downstream alerts on price anomalies
- Replace CSV source with live financial API (Yahoo Finance, Alpha Vantage)
- Add Grafana or QuickSight dashboard for real-time visualization
- Implement dead-letter queue for failed Kafka messages

---

## License

MIT License — see [LICENSE](LICENSE) for details.
