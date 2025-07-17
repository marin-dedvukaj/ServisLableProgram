import csv
import datetime
import os
import tempfile
class Storer:
    def __init__(self, filename,filepath = None):
        if filepath == None:
            filepath = tempfile.gettempdir()
            print(filepath)
        self.fileName = filename
        self.filePath = filepath
        self.fullPath = f"{self.filePath}/{self.fileName}"
        self.create()


    def addAllDatta(self, Name="", Phone="", Address="", Device="", Problem="", Acessories="", DateOfArrival=None):
        if DateOfArrival is None:
            DateOfArrival = datetime.datetime.now().strftime("%Y-%m-%d")
        data = [Name, Phone, Address, Device, Problem, Acessories, DateOfArrival]
        return self.add(data)

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
        return newID


    def load(self):
        with open(self.fullPath, mode='r') as file:
            reader = csv.reader(file)
            next(reader)
            return [row for row in reader]