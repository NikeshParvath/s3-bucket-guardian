# s3-bucket-guardian

# S3 Bucket Guardian – Automated Cloud Security System

## Overview
S3 Bucket Guardian is a serverless cloud security automation project that detects publicly accessible Amazon S3 buckets and alerts administrators in real time. The system is designed with a monitor and enforce model to safely evaluate and remediate security misconfigurations.

## Problem Statement
Publicly exposed S3 buckets are a common cause of data breaches. Manual monitoring is unreliable and slow, leading to delayed detection and response.

## Solution
This project implements an automated detection and alerting pipeline using AWS managed services to continuously monitor S3 bucket configurations.

## Architecture
- AWS Lambda for scanning and evaluation
- Amazon S3 for target resources
- Amazon CloudWatch for logs and custom metrics
- CloudWatch Alarms for alert conditions
- Amazon SNS for email notifications
- Amazon EventBridge for scheduled execution
- IAM for secure, least-privilege access

## Key Features
- Monitor mode for safe visibility
- Enforce mode for automatic remediation
- Metric-based alerting
- Scheduled compliance scans
- Cloud-native, serverless architecture

## Technologies Used
- AWS Lambda (Python, Boto3)
- Amazon S3
- Amazon CloudWatch
- Amazon SNS
- Amazon EventBridge
- AWS IAM

## Future Enhancements
- DynamoDB audit logging
- Risk scoring for bucket exposure
- Multi-account security support
