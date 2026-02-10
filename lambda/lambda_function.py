import boto3
import json

s3 = boto3.client('s3')
sns = boto3.client('sns')
cloudwatch = boto3.client('cloudwatch')


TOPIC_ARN = "arn:aws:sns:ap-south-1:665012226678:S3GuardianAlerts"

def lambda_handler(event, context):
    print("Event received:", event)

    # -------------------------------
    # Decide mode
    # -------------------------------
    mode = "monitor"  # default (safe)

    if isinstance(event, dict):
        mode = event.get("mode", "monitor")

    print(f"Running in {mode.upper()} mode")

    public_buckets = []
    fixed_buckets = []

    buckets = s3.list_buckets()["Buckets"]

    for bucket in buckets:
        bucket_name = bucket["Name"]

        try:
            status = s3.get_bucket_policy_status(
                Bucket=bucket_name
            )["PolicyStatus"]["IsPublic"]

            if status:
                public_buckets.append(bucket_name)

                if mode == "enforce":
                    try:
                        s3.delete_bucket_policy(Bucket=bucket_name)
                    except:
                        pass

                    s3.put_public_access_block(
                        Bucket=bucket_name,
                        PublicAccessBlockConfiguration={
                            "BlockPublicAcls": True,
                            "IgnorePublicAcls": True,
                            "BlockPublicPolicy": True,
                            "RestrictPublicBuckets": True
                        }
                    )

                    fixed_buckets.append(bucket_name)

        except:
            # No policy or access issue
            continue

    # -------------------------------
    # Send alert if needed
    # -------------------------------
    # Send custom CloudWatch metric
    cloudwatch.put_metric_data(
        Namespace="S3BucketGuardian",
        MetricData=[
            {
                "MetricName": "PublicBucketsDetected",
                "Value": len(public_buckets),
                "Unit": "Count"
            }
        ]
    )

    if public_buckets:
        if mode == "monitor":
            subject = "S3 Bucket Guardian Alert (Monitor Mode)"
            message = (
                "Public S3 buckets detected:\n\n" +
                "\n".join(public_buckets) +
                "\n\nNo auto-fix applied."
            )
        else:
            subject = "S3 Bucket Guardian Alert (Enforce Mode)"
            message = (
                "Public S3 buckets detected and fixed:\n\n" +
                "\n".join(fixed_buckets)
            )

        sns.publish(
            TopicArn=TOPIC_ARN,
            Subject=subject,
            Message=message
        )

    return {
        "statusCode": 200,
        "body": json.dumps({
            "mode": mode,
            "publicBuckets": public_buckets,
            "fixedBuckets": fixed_buckets
        })
    }
