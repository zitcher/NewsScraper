import csv


def parsecsv(filepath):
    with open(filepath, newline='') as csvfile:
        fileReader = csv.reader(csvfile, delimiter=',', quotechar='"')
        csv_to_array = []
        for row in fileReader:
            csv_to_array.append(row)
        return csv_to_array
