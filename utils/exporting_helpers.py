import csv
from typing import List
from models.claim import Claim
import re

EXCLUDED_COLUMNS = ["id", "is_delivered_successfully"]
CSV_COLUMNS = [
    ("email", "Email"),
    ("weeks", "Weeks"),
    ("form_url", "Form URL"),
    ("email_attempted_at", "Email Attempted (Time)"),
    ("response_received_at", "Response Received (Time)"),
    ("covid_01_17_21", "Has Covid, Week of 1/17/21"),
    ("covid_01_24_21", "Has Covid, Week of 1/24/21"),
    ("week_01_17_21_able", "Able, Week of 1/17/21"),
    ("week_01_17_21_available", "Available, Week of 1/17/21"),
    ("week_01_24_21_able", "Able, Week of 1/24/21"),
    ("week_01_24_21_available", "Available, Week of 1/24/21"),
    ("created_at", "Created (Time)"),
    ("updated_at", "Updated (Time)"),
    ("is_always_able_and_available", "Is Always Able and Available"),
]


def row_to_csv_row(row):
    csv_row = []

    for col in CSV_COLUMNS:
        csv_row.append(row.get(col[0]))

    return csv_row


def claims_to_csv(claims: List[Claim], filepath: str):
    counter = 0
    with open(filepath, "w") as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow(map(lambda x: x[1], CSV_COLUMNS))
        for claim in claims:
            row = {}
            is_always_able_and_available = None
            for key, value in claim.__dict__.items():
                if not key.startswith("__") and not callable(key):
                    if key in EXCLUDED_COLUMNS:
                        continue
                    elif key == "response":
                        if value is None:
                            continue
                        questions, answers = clean_response_for_csv(value)
                        for q, a in zip(questions, answers):
                            if a == "No":
                                is_always_able_and_available = False
                            if a:
                                row[q] = a
                        if is_always_able_and_available is None:
                            is_always_able_and_available = True
                    else:
                        row[key] = value

            row["is_always_able_and_available"] = is_always_able_and_available

            writer.writerow(row_to_csv_row(row))
            counter += 1


def clean_response_for_csv(response):
    answers = response["answers"]

    row = []
    for answer in answers.values():
        name = answer["name"]
        if re.match(r"week_\d{1,2}_\d{2}_\d{2}_able", name) != None:
            row.append(answer)
        elif re.match(r"week_\d{1,2}_\d{2}_\d{2}_available", name) != None:
            row.append(answer)
        elif re.match(r"covid_\d{1,2}_\d{2}_\d{2}", name) != None:
            row.append(answer)

    row = sorted(row, key=lambda x: x["name"])
    header = [ans["name"] for ans in row]
    row = ["answer" in ans and ans["answer"] for ans in row]
    return [header, row]
