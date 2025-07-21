import win32print
import win32ui

class Printables:
    def __init__(self):
        pass
    def FormatPhone(self, phone):
        if phone is None:
            return None
        phone = phone.replace(" ", "").replace("-", "")
        phone = phone.lstrip("+355").lstrip("0")
        if len(phone) == 10:
            return f"+355 {phone[:3]} {phone[3:6]} {phone[6:]}"
        elif len(phone) == 9:
            return f"+355 {phone[:2]} {phone[2:5]} {phone[5:]}"
        elif len(phone) == 8:
            return f"+355 {phone[:2]} {phone[2:4]} {phone[4:]}"
        else:
            return phone
    
    def Formaterer(self,ID = None, Name = None, Phone = None, Address = None, Device = None, Problem = None, Acessories = None, DateOfArrival = None):
        Text = ""
        Text += f"ID: {ID}          Arrival Date: {DateOfArrival}\n"
        Text += "-----------------------------------------------\n"
        if Name is not None:  
            Text += f"Name: {Name}\n"
        if Phone is not None:
            Text += f"Phone Number: {self.FormatPhone(Phone)}\n"
        if Address is not None and Address != "":
            Text += f"Address: {Address}\n"
        if Device is not None:
            Text += f"Device: {Device}\n"
        if Problem is not None:
            Text += f"Problem: {Problem}\n"
        if Acessories is not None:
            i = 1
            Text += "Aksesories:\n"
            for accessory in Acessories:
                Text += f"  {i}) {accessory}\n"
                i+= 1
        Text += "-----------------------------------------------\n"
        for i in [Name, Phone, Address, Device, Problem]:
            if i is not None:
                return Text
        return None
    
    def printOnPaper(self, text, printer_name=None):
        if text is None:
            return None
        text = text + "\n\n\n\n\n\n\n\n" + b'\x1d\x56\x01'.decode('latin1')
        if not printer_name:
            printer_name = win32print.GetDefaultPrinter()
        hprinter = win32print.OpenPrinter(printer_name)
        try:
            # Start a print job
            hjob = win32print.StartDocPrinter(hprinter, 1, ("Receipt", None, "RAW"))
            win32print.StartPagePrinter(hprinter)
            # Encode text as bytes (most thermal printers expect ascii or utf-8)
            win32print.WritePrinter(hprinter, text.encode('utf-8'))
            win32print.EndPagePrinter(hprinter)
            win32print.EndDocPrinter(hprinter)
        finally:
            win32print.ClosePrinter(hprinter)


if __name__ == "__main__":
    # Example usage
    receipt_text = "L41310001P"
    printer = Printables()
    printer.printOnPaper(receipt_text)