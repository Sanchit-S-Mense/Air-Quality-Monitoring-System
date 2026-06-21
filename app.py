import os
import csv
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)


def get_average(file_path, category):
    with open(file_path) as csvfile:
        reader = csv.DictReader(csvfile)
        total = 0
        i = 0
        for row in reader:
            try:
                # Convert to float and add to total
                total += float(row[category])
                i += 1
            except ValueError:
                pass  # Skip rows with missing or invalid data
        return round(total / i, 2) if i > 0 else 0


@app.route('/')
def index():
    # Find all CSV files in the static folder
    files = [f for f in os.listdir('static') if f.endswith('.csv')]
    return render_template('index.html', files=files)


@app.route('/get_data')
def get_data():
    # The frontend will ask for a specific file and a specific metric
    filename = request.args.get('file')
    metric = request.args.get('metric')  # 'Temperature', 'Moisture', or 'AQ'

    # Map 'Moisture' to 'Humidity' (CSV column name)
    csv_metric = 'Humidity' if metric == 'Moisture' else metric

    file_path = os.path.join('static', filename)

    # Use the average function with the mapped CSV metric name
    avg = get_average(file_path, csv_metric)

    # Read all the rows to send to the map
    data = []
    with open(file_path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Map Humidity to Moisture for the frontend if present
            if 'Humidity' in row:
                row['Moisture'] = row['Humidity']
            data.append(row)

    # Send the data back as JSON
    return jsonify({'average': avg, 'data': data, 'metric': metric})


if __name__ == '__main__':
    # Run the server
    app.run(debug=True)