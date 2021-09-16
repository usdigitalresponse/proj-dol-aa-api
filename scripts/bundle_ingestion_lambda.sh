mkdir ui-ingestion-lambda
cp -R ingestion/ ui-ingestion-lambda/ingestion
cp -R database/ ui-ingestion-lambda/database
cp -R models/ ui-ingestion-lambda/models
cp ingestion_lambda.py ui-ingestion-lambda/
cp -R venv/lib/python3.8/site-packages/ ui-ingestion-lambda
cd ui-ingestion-lambda
zip -r -D ui-ingestion-lambda.zip *
mv ui-ingestion-lambda.zip ../
cd ..
rm -rf ui-ingestion-lambda
