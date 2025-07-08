import csv
import datetime
import os
class Storer:
    def __init__(self, filename,filepath):
        self.fileName = filename
        self.filePath = filepath
        self.fullPath = f"{self.filePath}/{self.fileName}"
        self.create()


    def addAllDatta(self, Name="", Phone="", Address="", Device="", Problem="", Acessories="", DateOfArrival=None):
        if DateOfArrival is None:
            DateOfArrival = datetime.datetime.now().strftime("%Y-%m-%d")
        data = [Name, Phone, Address, Device, Problem, Acessories, DateOfArrival]
        self.add(data)

    def create(self):
        if os.path.exists(self.fullPath):
            return
        if not os.path.exists(self.filePath):
            os.makedirs(self.filePath)
        with open(self.fullPath, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Name", "Phone"," Address", "Device","Problem","Acessories","Date Of Arrival"])


    def add(self, data):
        with open(self.fullPath, mode='r', newline='') as file:
            reader = csv.reader(file)
            next(reader)
            rows = list(reader)
            if rows:
                lastID = int(rows[-1][0])
            else:
                lastID = 0
        newID = lastID + 1
        with open(self.fullPath, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([newID] + data)


    def load(self):
        with open(self.fullPath, mode='r') as file:
            reader = csv.reader(file)
            return [row for row in reader]


if __name__ == "__main__":
    storer = Storer("test.csv", "D:/projects/ServisLableProgram/test")
    storer.create()
    for i in range(5):
        storer.addAllDatta(Name=f"User {i}", Phone=f"123456789{i}", Address=f"Address {i}", Device=f"Device {i}", Problem=f"Problem {i}", Acessories=["Accessory1", "Accessory2"])
    storer.addAllDatta(Name="John Doe", Phone="1234567890", Address="123 Main St", Device="Laptop", Problem="Not charging", Acessories=["Charger","Laptop Bag"], DateOfArrival="2023-10-01")
    data = storer.load()
    for row in data:
        print(row)  