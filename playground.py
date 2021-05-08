import csv

companies = []

class searchTerm:
    def __init__(self, date, name):
        self.date = date
        self.name = name

with open("/Users/Howard/Desktop/分析資料.csv", newline="", encoding= "UTF-8-sig") as compdata:
    rows = csv.reader(compdata, delimiter = ",")

    for row in rows:
        # companies.append(row[0])
        # print(row)
        # print(type(row[0]))
        # print(type(row[1]))
        # len(row)
        companies.append(searchTerm(row[0], row[1]))

for comp in companies:
    print(comp.name)
    print(comp.date)