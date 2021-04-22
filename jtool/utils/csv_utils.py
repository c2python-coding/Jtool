import csv
from io import StringIO

def parse_csv(data, delim):
    csvlist= []
    data_io = StringIO(data)
    csv_reader = csv.reader(data_io, delimiter=delim)
    for row in csv_reader:
        csvlist.append(row)
    return csvlist
