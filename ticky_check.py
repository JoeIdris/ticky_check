"""
This program extracts information from a system log about errors and user usage.
It generates a two csv reports containing:
(1) the errors and their frequency
(2) user usage statistic (error and non-error frequencies)

"""



# imports
import re
import operator
import csv

def generate_report():
    """
    Populates errors & per_user dictionaries with information about errors frequency, and user usage statistics, respectively.

    Arguments:
        None

    Returns:
        A list of dictionaries
    """

    errors = {}
    per_user = {}

    with open('./syslog.log', 'r', encoding='utf-8') as file:
        for line in [line.strip("\n") for line in file.readlines()]:
            match = re.search(r"(ERROR|INFO) ([\w\s']+).*\((.*)\)", line)
            msg_type, msg_info, user = match.group(1), match.group(2), match.group(3)

            per_user[user] = per_user.get(user, {'INFO': 0, 'ERROR': 0})
            per_user[user][msg_type] += 1

            if msg_type == 'ERROR':
                errors[msg_info] = errors.get(msg_info, 0) + 1

        errors = sorted(errors.items(), key = operator.itemgetter(1), reverse=True)
        per_user = sorted(per_user.items(), key = operator.itemgetter(0))

        return errors, per_user


def to_csv(filename, data, headers):
    """
    Generates a csv file from a given dictionary

    Arguments:
        filename -> str: name of the csv file to be written to disk
        data -> dict: a dictionary containing data
        headers -> list: list of header strings as column names

    Returns:
        No return value

    """
    if not '.csv' in filename:
        filename += '.csv'

    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)

        row = []
        for x, y in data:
            if isinstance(y, dict):
                info_count, err_count = list(y.values())
                row = x, info_count, err_count
            else:
                row = x, y

            writer.writerow(row)



if __name__ == "__main__":

    errors, per_user = generate_report()
    to_csv('errors_statistics', errors, ['Error', 'Count'])
    to_csv('user_statistics.csv', per_user, ['Username', 'INFO', 'ERROR'])
