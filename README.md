# USDR Unemployment Insurance Hosted Solution

## Setup
- `git clone https://github.com/usdigitalresponse/proj-dol-aa-api.git`
- `virtualenv venv`
- `source venv/bin/activate`
- `pip install -r requirements.txt`

### Python Package Importing
If you are having issues with detecting local imports in Python
- Run `pwd` from `proj-dol-aa-api` directory.
- Run `export PYTHONPATH="$PYTHONPATH:/result-from-above"`.

### Sendgrid Setup
- Go to app.sendgrid.com and login with credentials from email thread with ui-fact-finding@usdigitalresponse.org.
- Go to the [API keys page](https://app.sendgrid.com/settings/api_keys) and generate a new token. Tokens are view-once only.
- Copy token and run `echo "export SENDGRID_API_KEY='YOUR_API_KEY'" > sendgrid.env`
- Run `source ./sendgrid.env`.
- You can test whether this is working by replacing the recipients email in `tests/tests.py -> test_sengrid_client` with your email and running it.

### Bundling Lambdas
- To bundle the ingestion lambda to upload to the console, run `./bundle_ingestion_lambda.sh` from project root, and upload the resulting `ui-ingestion-lambda.zip` in the AWS lambda console.