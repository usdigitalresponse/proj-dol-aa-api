import csv
from typing import List
from models.claim import Claim
import re

EXCLUDED_COLUMNS = ["id", "is_delivered_successfully"]


def claims_to_csv(claims: List[Claim], filepath: str):
    counter = 0
    with open(filepath, "w") as csvfile:
        writer = csv.writer(csvfile)
        row = {}
        for claim in claims:
            for key, value in claim.__dict__.items():
                if not key.startswith("__") and not callable(key):
                    if key in EXCLUDED_COLUMNS:
                        continue
                    elif key == 'response':
                        questions, answers = response_to_csv(value)
                        for q, a in zip(questions, answers):
                            row[q] = a
                    else:
                        row[key] = value

            # For first row, print out values too as header row.
            if counter == 0:
                writer.writerow(row.keys())
            writer.writerow(row.values())
            counter += 1


def response_to_csv(response):
    answers = response['answers']
    
    row = []
    for answer in answers.values():
        name = answer['name']
        if re.match(r"week_\d{1,2}_\d{2}_\d{2}_able", name) != None:
            row.append(answer)
        elif re.match(r"week_\d{1,2}_\d{2}_\d{2}_available", name) != None:
            row.append(answer)
        elif re.match(r"covid_\d{1,2}_\d{2}_\d{2}", name) != None:
            row.append(answer)
        
    row = sorted(row, key=lambda x: x['name'])
    header = [ans['name'] for ans in row]
    row = ['answer' in ans and ans['answer'] for ans in row]

    return [header, row]
