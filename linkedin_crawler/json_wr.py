import json
import datetime


def create_json():
    NEW_JSON = {
        'request_start_no': 0,
        'request_end_no': 0,
        'total_previously_msged': 0,
        'total_newly_msged': 0,
        'today_date': '',
        'today_send': 0,
        'totak_sent': 0

    }
    with open('status.json', 'w') as f:
        json.dump(NEW_JSON, f)

def read_status_json():
    # import sys
    # print(sys.path)

    with open('status.json', 'r') as f:
        data = json.load(f)
    return dict(data)


def write_status(data):
    with open('status.json', 'w') as f:
        json.dump(data, f)

if __name__ == '__main__':
    print(read_status_json())

