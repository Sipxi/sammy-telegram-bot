from services.parsers import vut_parser





for subject in vut_parser.get_data():
    if subject["subject"] == "ISJ – Skriptovací jazyky":
        print(subject)