import os
import win32print

def send_pdf_to_printer():

    # Specify the printer name as it appears in "Printers & scanners"
    # Include a printer dropdown list in the future
    printer_name = "ZDesigner GK420t"

    # Build the path to the pdf file
    directory = "Generated Labels"
    filename = "Etiqueta INDIVIDUAL.pdf"
    file_path = os.path.join(directory, filename)

    # Get the current default printer name
    default_printer = win32print.GetDefaultPrinter()

    try:
        # Set the specified Zebra printer as the default printer
        win32print.SetDefaultPrinter(printer_name)

        # Send the PDF file to the printer using os.startfile
        os.startfile(file_path, "print")
    finally:
        # Restore the original default printer
        win32print.SetDefaultPrinter(default_printer)
