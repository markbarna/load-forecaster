import argparse
import joblib

from pipeline.model import TimeSeriesModel

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Predict load for date, time, and area zone.')
    parser.add_argument('date', type=str, metavar='D', help='the date in common string format')
    parser.add_argument('time', type=str, metavar='T', help='the time in UTC 24hr HH:MM')
    parser.add_argument('--area', type=str, required=True, help='the PJM area code', choices=['PE', 'PEP'])
    parser.add_argument('--model_path', type=str, required=True, help='path to model artifact')
    args = parser.parse_args()

    model: TimeSeriesModel = joblib.load(args.model_path)
    prediction = model.predict(args.date, args.time, args.area)
    print(f"{prediction.iloc[0]:.2f} MW")
