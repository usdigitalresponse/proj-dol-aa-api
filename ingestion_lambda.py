"""
This lambda function will trigger when a new CSV is uploaded to the ui-claimant-imports bucket.

It will consume the CSV and store all the claims to-be-processed into the database.
"""
from ingestion.csv_processor import CSVProcessor
import boto3
import urllib.parse
import json
from database.db_connection import DatabaseConnection

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

        db_connection = DatabaseConnection(is_test=False)

        csv_processor = CSVProcessor(db_connection)
        csv_processor.ingest(body=body)

        db_connection.close()

        return {
            "statusCode": 200,
            "body": json.dumps("Success. Processed {}/{}".format(bucket, key)),
        }
    except Exception as e:
        print(e)
        print("Bucket: {}, Key: {}".format(bucket, key))
        raise e
