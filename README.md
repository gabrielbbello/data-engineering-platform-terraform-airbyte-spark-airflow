# Data Engineering Platform: AWS, Terraform, Airbyte, Spark, and Airflow for a Scalable and Managed Platform

![GitHub release (latest by date)](https://img.shields.io/github/v/release/your-username/data-engineering-platform?color=blue&label=Version&style=for-the-badge)

This repository presents a modular and scalable Data Engineering platform designed to be flexible, easy to expand, and built upon best practices of organization and implementation.

## Technologies Used

- **Amazon Web Services (AWS)**: Cloud provider for the project.
- **Terraform**: Infrastructure as Code (IaC) tool.
- **Spark with Python API (PySpark)**: Distributed processing tool with local deployment.
- **Airbyte**: Data integration tool.
- **Postgres instance on Amazon Relational Database Service (RDS)**: Initial database.

### AWS Resources

- **Amazon S3** (Data Lake)
- **Amazon Virtual Private Cloud (VPC)**
- **Subnets**
- **Internet Gateway**
- **Route Table**
- **Amazon EC2**
- **Amazon Relational Databases (RDS)**
- **Amazon Identity and Access Management (IAM)**
- **AWS Glue Data Catalog**
- **AWS Glue Crawler**
- **Amazon Athena**

---

## Table of Contents

- [Overview](#overview)
- [Repository Structure](#repository-structure)
- [Technologies](#technologies)
- [Terraform AWS Infrastructure](#terraform-aws-infrastructure)
- [Environment Setup](#environment-setup)
- [Project Execution](#project-execution)
- [Next Steps](#next-steps)
- [Contact](#contact)

---

## Overview

This project was developed to:

- Automate the creation of resources and the Data Lake infrastructure on AWS using **Terraform**.
- Process large volumes of data with **Apache Spark**.
- Use **Airbyte** on an EC2 instance to ingest data into S3.
- Provide a scalable foundation for integration with additional tools like **Airflow**.

To illustrate the project, a database was created in Postgres RDS using data from the well-known [Flights dataset](https://www.kaggle.com/datasets/mahoora00135/flights). This dataset contains information about airport flights, including departure and arrival times, delays, airline details, flight numbers, origins, destinations, duration, distance, and timestamps.

---

## Repository Structure

- **core/**: Contains Terraform configuration files to provision AWS resources.
- **spark/**: Apache Spark modules:
  - **jobs/**: Scripts for data processing and aggregation.
  - **config/**: Logger and SparkSession configuration.
  - **utils/**: Utility functions.
- **requirements.txt**: Python dependencies for the project.
- **.env** and **env.example**: Environment variable configurations.
- **.gitignore**: Specifies files to be ignored by version control.

---

## Terraform AWS Infrastructure

### Requirements
| Name | Version |
|------|---------|
|[Terraform](https://developer.hashicorp.com/terraform/docs) | >= 1.9.4 |
|[AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest) | ~> 5.63.1 |

### Providers
| Name | Version |
|------|---------|
|[AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest) | 5.63.1 |

### Resources
| Name | Status |
|------|---------|
|[aws_db_instance.rds](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/db_instance) | ready |
|[aws_db_parameter_group.rds](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/db_parameter_group) | ready |
|[aws_db_subnet_group.rds](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/db_subnet_group) | ready |
|[aws_instance.this (airbyte)](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/instance) | ready |
|[aws_key_pair.this (airbyte)](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/key_pair) | ready |
|[aws_security_group.airbyte](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/security_group) | ready |
|[aws_security_group.rds](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/security_group) | ready |
|[random_id.global](https://registry.terraform.io/providers/hashicorp/random/latest/docs/resources/id) | ready |
|[aws_s3_bucket.this (bronze-layer)](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket) | ready |
|[aws_s3_bucket.this (silver-layer)](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket) | ready |
|[aws_s3_bucket.this (gold-layer)](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket) | ready |
|[aws_internet_gateway](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/internet_gateway) | ready |
|[aws_route.public_internet_gateway](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/route) | ready |
|[aws_route_table.public](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/route_table) | ready |
|[aws_route_table_association.public](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/route_table_association) | ready |
|[aws_subnet.public](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/subnet) | ready |
|[aws_vpc](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/vpc) | ready |

---

## Environment Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/data-engineering-platform.git
   cd data-engineering-platform
   ```

2. **Create and Configure the `.env` File**
   Use the `env.example` file as a reference to create the `.env` file:
   ```bash
   cp env.example .env
   ```
   Adjust the environment variables as needed.

3. **Install Python Dependencies**
   It is recommended to use a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Create and Configure the `terraform.tfvars` File**
   Use the `terraform.example.tfvars` file as a reference to create the `terraform.tfvars` file:
   ```bash
   cp terraform.example.tfvars terraform.tfvars
   ```
   Adjust the environment variables as needed.

4. **Initialize Terraform**
   Set up Terraform to provision the infrastructure:
   ```bash
   cd core/resources
   terraform init
   terraform plan
   terraform apply
   ```

---

## Project Execution
### Run Spark Pipelines (Version 1)
In the current version (v1), data processing follows a structured pipeline using Apache Spark executed locally. Future versions will migrate this process to AWS Glue Jobs for a fully managed, serverless ETL workflow.

1. Process and load data from the bronze layer to the silver layer:
   ```bash
   spark-submit spark/jobs/bronze_to_silver.py
   ```

2. Aggregate and load data from the silver layer to the gold layer:
   ```bash
   spark-submit spark/jobs/silver_to_gold.py
   ```

---

## Upcoming Changes

The project is evolving to enhance automation, scalability, and orchestration. Key improvements planned:

🔹 AWS Glue Jobs – Replace local Spark execution with managed AWS Glue Jobs for scalable ETL workflows. Integrate Glue Crawlers and Data Catalog for schema discovery.

🔹 S3 as a Serverless Data Lake – Optimize data ingestion and transformation using Glue Crawlers for automatic schema inference and Data Catalog for metadata management.

🔹 Airflow for Orchestration – Deploy Apache Airflow in EC2 or MWAA, with DAGs stored in S3, enabling dynamic, modular workflow orchestration.

🔹 Airbyte Connection as Code – Automate Airbyte workspace, sources, and destinations using Terraform, ensuring full Infrastructure as Code (IaC) integration.

---

## Contact
- **Author**: Gabriel Bello
- **Email**: gabrielbbello@gmail.com
- **LinkedIn**: [linkedin.com/in/gabriel-brito-bello](https://linkedin.com/in/gabriel-brito-bello)

---

If you liked this project or have suggestions, feel free to open an issue or submit a pull request. Thank you for checking out my work! 🚀