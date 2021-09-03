mkdir ui-ingestion-lambda
cp -R ingestion/ ui-ingestion-lambda/ingestion
cp ingestion_lambda.py ui-ingestion-lambda/
cp -R venv/lib/python3.8/site-packages/ ui-ingestion-lambda
cd ui-ingestion-lambda
zip -r -D ui-ingestion-lambda.zip *
mv ui-ingestion-lambda.zip ../
cd ..
rm -rf ui-ingestion-lambda
