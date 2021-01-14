import argparse
import requests

if __name__ == '__main__':
    """
    usage: predict.py [-h] date time {PE,PEP} url
    
    Predict load for date, time, and area zone.
    
    positional arguments:
      date        the date in common string format
      time        the time in UTC 24hr HH:MM
      {PE,PEP}    the PJM area code (one of PE, PEP)
      url         POST request endpoint url
    
    optional arguments:
      -h, --help  show this help message and exit
    """
    parser = argparse.ArgumentParser(description='Predict load for date, time, and area zone.')
    parser.add_argument('date', type=str, help='the date in common string format')
    parser.add_argument('time', type=str, help='the time in UTC 24hr HH:MM')
    parser.add_argument('area', type=str, help='the PJM area code (one of PE, PEP)', choices=['PE', 'PEP'])
    parser.add_argument('url', type=str, help='POST request endpoint url')
    args = parser.parse_args()

    payload = {
        'date': args.date,
        'time': args.time,
        'area': args.area
    }
    response = requests.post(url=args.url, json=payload)
    prediction = response.text

    print(prediction)
