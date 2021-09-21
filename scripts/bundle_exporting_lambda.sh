mkdir ui-exporting-lambda
cp -R ingestion/ ui-exporting-lambda/ingestion
cp -R database/ ui-exporting-lambda/database
cp -R models/ ui-exporting-lambda/models
cp -R clients/ ui-exporting-lambda/clients
cp -R utils/ ui-exporting-lambda/utils
cp exporting_lambda.py ui-exporting-lambda/
cp -R venv/lib/python3.8/site-packages/ ui-exporting-lambda
cd ui-exporting-lambda
zip -r -D ui-exporting-lambda.zip *
mv ui-exporting-lambda.zip ../
cd ..
rm -rf ui-exporting-lambda
