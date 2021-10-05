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

### RDS Setup
- Talk to Advith to get contents of `rds.env` file
- Place `rds.env` file in project root and run `source ./rds.env`

### Bundling Lambdas
- To bundle the ingestion lambda to upload to the console, run `./bundle_ingestion_lambda.sh` from project root, and upload the resulting `ui-ingestion-lambda.zip` in the AWS lambda console.

## Code of Conduct

This repo falls under [U.S. Digital Response’s Code of Conduct](./CODE_OF_CONDUCT.md), and we will hold all participants in issues, pull requests, discussions, and other spaces related to this project to that Code of Conduct. Please see [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md) for the full code.


## Contributing

This project wouldn’t exist without the hard work of many people. Thanks to the following for all their contributions! Please see [`CONTRIBUTING.md`](./CONTRIBUTING.md) to find out how you can help.

<!--
Contributors are sorted alphabetically by last name. The contributions follow
All-Contributors categories and emoji. We add title attributes so people can
hover over the emoji and see what they represent.
The list is manually managed.
-->
<!-- ALL-CONTRIBUTORS-LIST:START -->
| Contributions | Name |
| ----: | :---- |
| [💻](# "Code") | [Advith Chelikani](https://github.com/AChelikani) |
| [💻](# "Code") | [Robert Eng](https://github.com/RobertEng) |
<!-- ALL-CONTRIBUTORS-LIST:END -->

(For a [key to the contribution emoji][all-contributors-key] or more info on this format, check out [“All Contributors.”][all-contributors])


## License & Copyright

Copyright (C) 2021 U.S. Digital Response (USDR)

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this software except in compliance with the License. You may obtain a copy of the License at:

[`LICENSE`](./LICENSE) in this repository or http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
