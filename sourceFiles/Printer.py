import win32print
import win32ui

def print_receipt(text, printer_name=None):
    text = text + "\n\n\n\n\n\n\n\n" + b'\x1d\x56\x01'.decode('latin1')
    # Get default printer if not specified
    if not printer_name:
        printer_name = win32print.GetDefaultPrinter()

    # Open printer
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
    print_receipt(receipt_text)