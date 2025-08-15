import csv

def save_to_csv(columns, data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(columns)
        for row in data:
            writer.writerow(row)