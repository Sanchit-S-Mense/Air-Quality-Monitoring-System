import csv
from datetime import datetime

now = datetime.now()
print(now.strftime('%H:%M:%S'))

def unpackData(data):
    temp, humidity, aq = data.split(",")
    return float(temp),float(humidity), float(aq)

a = '32.40 , 45.70 , 98725.67 '
headers = ["Temperature", "Humidity", "AQ"]
with open("abc.csv","w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(headers)
    data = unpackData(a)
    writer.writerow(data)



