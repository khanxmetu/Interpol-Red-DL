import sys, os

sys.path.append(os.getcwd())

import json
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker
from notice_saver.repositories import ArrestWarrantRepository

db_connection_url = URL.create(
    drivername=os.environ["DB_DRIVER"],
    username=os.environ["DB_USER"],
    password=os.environ["DB_PASS"],
    host=os.environ["DB_HOST"],
    port=int(os.environ["DB_PORT"]),
    database=os.environ["DB_NAME"],
)
engine = create_engine(db_connection_url)
LocalSession = sessionmaker(bind=engine)

with LocalSession() as session:
    aw_repo = ArrestWarrantRepository(session)
    arrest_warrants = aw_repo.get_all()


FILENAME = "scripts/data_cleaning/offense_strings.json"

def main():
    """
    Retrieve saved charges/offenses strings from the database that were specified by the Interpol
    for the purpose of classification into discrete categories

    See:
    https://chatgpt.com/share/7212fdd6-b6b3-4c9b-9bdb-9233b381bad5
    notice_saver/offense_classifier.py
    """
    total_word_count = 0
    total_chars = 0

    raw_offenses = [
        arrest_warrant.charge_translation or arrest_warrant.charge
        for arrest_warrant in arrest_warrants
    ]
    offenses = list(set([offense.lower().strip() for offense in raw_offenses if offense]))

    with open(FILENAME, "w", encoding="utf-8") as f:
        json.dump(offenses, f, indent=4)

    print(f"offense strings saved in {FILENAME}")

    total_chars = sum([len(word) for offense in offenses for word in offense ])
    total_word_count = sum([len(offense.split()) for offense in offenses])
    avg_chars = total_chars / len(offenses)
    avg_word_count = total_word_count / len(offenses)

    print("Total characters count:", total_chars)
    print("Total words count:", total_word_count)

    print("Average characters count:", avg_chars)
    print("Average words count:", avg_word_count)

main()