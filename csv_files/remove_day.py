import csv
from csv import reader
# skip first line i.e. read header first and then iterate over each row od csv as a list
with open('times6_2.csv', 'r') as read_obj:
    csv_reader = reader(read_obj)
    header = next(csv_reader)
    # Check file as empty
    if header != None:
        # Iterate over each row after the header in the csv
        for row in csv_reader:
            #print(type(row[0]))
            # row variable is a list that represents a row in csv
            s2 = row[0].split(" ",1)[1]
            
            with open('temp.csv', 'a') as file:
                writer = csv.writer(file)
                writer.writerow([s2])