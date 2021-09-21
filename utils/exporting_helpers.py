import csv
from typing import List
from models.claim import Claim


def claims_to_csv(claims: List[Claim], filepath: str):
    counter = 0
    with open(filepath, "w") as csvfile:
        writer = csv.writer(csvfile)
        row = {}
        for claim in claims:
            for key, value in claim.__dict__.items():
                if not key.startswith("__") and not callable(key):
                    row[key] = value

            # For first row, print out values too as header row.
            if counter == 0:
                writer.writerow(row.keys())
            writer.writerow(row.values())
            counter += 1
