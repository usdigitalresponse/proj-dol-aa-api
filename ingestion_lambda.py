"""
This lambda function will trigger when a new CSV is uploaded to the ui-claimant-imports bucket.

It will consume the CSV and store all the claims to-be-processed into the database.
"""
from ingestion.csv_processor import CSVProcessor
import boto3
import urllib.parse
import json

IMPORTS_BUCKET = "ui-claimant-imports"

s3 = boto3.client("s3")


def lambda_handler(event, context):
    # Get the bucket and key from event.
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = urllib.parse.unquote_plus(
        event["Records"][0]["s3"]["object"]["key"], encoding="utf-8"
    )

    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        body = response["Body"]  # botocore.response.StreamingBody

        csv_processor = CSVProcessor()
        csv_processor.ingest(body=body)

        return {
            "statusCode": 200,
            "body": json.dumps("Success. Processed {}/{}".format(bucket, key)),
        }
    except Exception as e:
        print(e)
        print("Bucket: {}, Key: {}".format(bucket, key))
        raise e
