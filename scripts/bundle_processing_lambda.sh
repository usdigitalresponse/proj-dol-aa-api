mkdir ui-processing-lambda
cp -R ingestion/ ui-processing-lambda/ingestion
cp -R database/ ui-processing-lambda/database
cp -R models/ ui-processing-lambda/models
cp -R clients/ ui-processing-lambda/clients
cp -R utils/ ui-processing-lambda/utils
cp processing_lambda.py ui-processing-lambda/
cp -R venv/lib/python3.8/site-packages/ ui-processing-lambda
cd ui-processing-lambda
zip -r -D ui-processing-lambda.zip *
mv ui-processing-lambda.zip ../
cd ..
rm -rf ui-processing-lambda
