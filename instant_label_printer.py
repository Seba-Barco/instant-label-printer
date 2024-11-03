import sys
import tkinter as tk
import os
import json
from tkinter import messagebox
import shutil
from tkinter import Scrollbar
import etiqueta_individual
import etiqueta_pallet
import pdf_print

# Filenames
filename_last_opened = "last_opened.json"

# Directory path variables
path_to_folder_label_editor_db = "label_editor_db"
path_to_folder_last_opened = os.path.join(path_to_folder_label_editor_db, "last_opened")
path_to_folder_label_files = os.path.join(path_to_folder_label_editor_db, "label_files")
path_to_file_last_opened = os.path.join(path_to_folder_last_opened, filename_last_opened)


# Functions
def check_and_create_directories():
    """
    ** Main Function **
    This function checks if it's the first time the app is executed
    by checking if a path to the main directory exists and if it
    doesn't, it creates the necessary directories for the app to run
    properly. It also tries to hide the main directory in the os file
    system.
    """
    if not os.path.exists(path_to_folder_label_editor_db):
        os.makedirs(path_to_folder_label_editor_db)
        os.makedirs(path_to_folder_last_opened)
        os.makedirs(path_to_folder_label_files)
        os.makedirs("Generated Labels")
    # Try to make the main app directory HIDDEN
    try:
        os.system(f'attrib +h "{path_to_folder_label_editor_db}"')
    except OSError:
        pass


def refresh_last_opened_label_file(path, filename):
    # Source filename and path
    source = os.path.join(path, filename)
    # Destination filename and path
    destination = path_to_file_last_opened
    # Use shutil to copy and replace the file
    shutil.copy(source, destination)


def open_label_file(path, filename):
    """
    ** Secondary Function **
    This function takes a path and a filename as a parameter and
    iterates over the label + input pairs to update them with the data
    inside the file.
    """
    with open(os.path.join(path, filename), "r") as f:
        label_data = json.load(f)

    # Update the input fields in the main window with the new data
    for i, key in enumerate(text_field_data):
        input_fields[i].configure(state="normal")  # Ensure field is editable
        input_fields[i].delete(0, tk.END)  # Clear the field first
        input_fields[i].insert(0, label_data.get(key, ""))  # Populate with new data
        input_fields[i].configure(state="disabled")

    # Button enabling and disabling
    button_pallet_label.configure(state="normal")
    button_modify.configure(state="normal")
    button_save.configure(state="disabled")

    input_fields[4].configure(state="normal")


def retrieve_last_opened_label_file():
    """
    ** Main Function **
    This function checks if there is a file containing data from the
    label that was opened the last, and if so, it uses the
    open_label_file function to load the data into the main window
    """
    if os.path.exists(path_to_file_last_opened):
        open_label_file(path_to_folder_last_opened, filename_last_opened)


def get_label_files(listbox_widget):
    """
    ** Secondary Function **
    This function checks if there is a path to the label files folder.
    If so, it will load all the directory filenames into a list. Then,
    for every item in the list, it will remove the .json extension by
    splitting the filename, so that the Label List window only shows
    the name of the file.
    """
    if os.path.exists(path_to_folder_label_files):
        filenames = os.listdir(path_to_folder_label_files)
        for clean_filename in filenames:
            clean_filename = os.path.splitext(clean_filename)[0]
            listbox_widget.insert(tk.END, clean_filename)


def get_selected_file_filename(listbox_widget):
    """
    ** Secondary Function **
    This function returns the filename of an item selected in a listbox
    widget without it's .json extension
    """
    # Get the selected item from the Listbox
    selected_item_index = listbox_widget.curselection()
    filename = listbox_widget.get(selected_item_index[0]) + ".json"
    return filename


def check_curselection(listbox_widget):
    """
    ** Secondary Function **
    This function checks if something is selected in a listbox widget.
    """
    selected_item_index = listbox_widget.curselection()
    if len(selected_item_index) > 0:
        return True
    else:
        return False


def make_window_responsive(window):
    """
    ** Secondary Funciton **
    This function takes a window and makes it responsive
    """
    window.attributes('-disabled', False)


def make_window_unresponsive(window):
    """
    ** Secondary Funciton **
    This function takes a window and makes it unresponsive
    """
    window.attributes('-disabled', True)


def open_selected_file(listbox_widget):
    """
    ** Secondary Function **
    This function takes a selected file from a listbox widget and opens
    it.
    """
    if check_curselection(listbox_widget):
        filename = get_selected_file_filename(listbox_widget)
        open_label_file(path_to_folder_label_files, filename)
        # Close the label list window
        listbox_widget.winfo_toplevel().destroy()
        refresh_last_opened_label_file(path_to_folder_label_files, filename)


def delete_selected_file(listbox_widget):
    """
    ** Secondary Function **
    This function takes a selected file from a listbox widget and
    deletes it
    """
    if check_curselection(listbox_widget):
        filename_to_delete = get_selected_file_filename(listbox_widget)

        # Get the parent window of the listbox_widget and make it unresponsive
        label_list_window = listbox_widget.winfo_toplevel()
        make_window_unresponsive(label_list_window)

        # Ask for confirmation before deleting
        base_filename = filename_to_delete.split(".")[0]
        confirm_delete = messagebox.askokcancel(
            "Confirmación", f"¿Está seguro de que desea borrar la etiqueta {base_filename}?")

        # Make the label_list_window responsive again
        make_window_responsive(label_list_window)

        # Bring the label_list_window to the front and set focus
        label_list_window.lift()

        if confirm_delete:
            # Delete the file from the directory
            file_path = os.path.join(path_to_folder_label_files, filename_to_delete)
            if os.path.exists(file_path):
                os.remove(file_path)

            # Clear the Listbox and refresh the list
            listbox_widget.delete(listbox_widget.curselection())


def center_window(window, width, height):
    """
    ** Secondary Function **
    This function centers a window vertically and horizontally in the
    middle of a screen.
    """
    # Get the screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate the x and y coordinates to center the window
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    # Set the window's position
    window.geometry(f"{width}x{height}+{x}+{y}")


def enable_all_entries():
    for entry in input_fields:
        entry.configure(state="normal")


def disable_all_entries():
    # Disable all entries except the last one
    for entry in input_fields[:-1]:
        entry.configure(state="disabled")


def clear_all_entries():
    # Entries can't be cleared unless they are previously enabled
    for entry in input_fields:
        entry.delete(0, tk.END)


def save():
    data_to_save = {}

    # Collect data from the Entry widgets
    for i in range(4):
        key_entry = text_field_data[i]
        value_data = input_fields[i].get()
        data_to_save[key_entry] = value_data

    # Get the filename from the data_to_save dictionary
    filename = data_to_save[text_field_data[0]] + ".json"

    new_name = input_fields[0].get()

    # if old_name != new_name:

    # Save the data to a JSON file
    with open(os.path.join(path_to_folder_label_files, filename), "w") as f:
        json.dump(data_to_save, f)
    messagebox.showinfo("Guardado Exitoso", "Etiqueta guardada correctamente. Ya se pueden generar los archivos PDF.")

    new_name = input_fields[0].get() + ".json"
    old_file_path = os.path.join(path_to_folder_label_files, old_name[0])
    new_file_path = os.path.join(path_to_folder_label_files, new_name)
    if os.path.exists(old_file_path) and old_file_path != new_file_path:
        print("Borrar archivo viejo")

    disable_all_entries()

    refresh_last_opened_label_file(path_to_folder_label_files, filename)
    old_name[0] = ""

    # Button enabling and disabling
    button_label_list.configure(state="normal")
    button_pallet_label.configure(state="normal")
    button_modify.configure(state="normal")
    button_save.configure(state="disabled")


def new_label():
    enable_all_entries()
    # Entires have to be enabled in order to clear them
    clear_all_entries()
    old_name[0] = "invalid_direction"

    # Button enabling and disabling

    button_pallet_label.configure(state="disabled")
    button_modify.configure(state="disabled")
    button_save.configure(state="disabled")


def modify():
    enable_all_entries()
    #disable the input field for the name
    input_fields[0].configure(state="disabled")
    old_name[0] = input_fields[0].get() + ".json"

    # todo: add the dictionary comparing function to confirm cancelation of modification
    # todo: also add a cancel button

    # Button enabling and disabling
    button_label_list.configure(state="disabled")
    button_pallet_label.configure(state="disabled")
    button_modify.configure(state="disabled")
    button_save.configure(state="normal")


def open_label_list():
    """
    ** Main Function **
    This function builds a window for the label list. It sets the main
    window as the transient master of label_list_window. This makes it
    so that the main window appears behind the label list window while
    the label list window is open. Then it also binds the destroy event
    of the label list window to make the main window responsive agian.
    """
    # Temporarily make the main window unresponsive
    make_window_unresponsive(root)

    # Build the window
    label_list_window = tk.Toplevel(root)
    label_list_window.title("Lista de Etiquetas")
    width = 400
    height = 450
    label_list_window.geometry(f"{width}x{height}")
    label_list_window.resizable(False, False)
    center_window(label_list_window, width, height)

    # Set the main window as the transient master of label_list_window
    label_list_window.transient(root)

    # Bind the destroy event of the label_list_window to make it responsive
    label_list_window.bind('<Destroy>', lambda event: make_window_responsive(root))

    # WIDGETS
    frame = tk.Frame(label_list_window)
    scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
    listbox = tk.Listbox(frame, height=20, yscrollcommand=scrollbar.set)  # Associate scrollbar with listbox
    scrollbar.config(command=listbox.yview)  # Associate listbox with scrollbar
    open_button = tk.Button(label_list_window, text="Abrir", command=lambda: open_selected_file(listbox))
    delete_button = tk.Button(label_list_window, text="Eliminar", command=lambda: delete_selected_file(listbox))

    # POSITIONING
    frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    open_button.pack(side=tk.LEFT, padx=60, pady=(0, 20))
    delete_button.pack(side=tk.RIGHT, padx=60, pady=(0, 20))

    # Configure column 0 to expand to the Toplevel window's width
    label_list_window.columnconfigure(0, weight=1)

    # Populate the list
    get_label_files(listbox)


# Create the tkinter main window and set the title
root = tk.Tk()
root.title("Instant Label Printer")
check_and_create_directories()


# Ugly code below
# After finishing the program, check which buttons enable and disable together and make a function for that


# This function has been modified to not theck the last entry item, because it is dedicated
# to the individual label generation.
def check_and_enable_save_button(*args):
    # Check if all Entry fields except the last one have data
    all_fields_have_data = all(entry.get() for entry in input_fields[:-1])

    # Enable the "Guardar" button accordingly
    if all_fields_have_data:
        button_save.configure(state="normal")
        print("Tienen data los primeros 4")
    else:
        button_save.configure(state="disabled")
        print("No tienen data los primeros 4")


def check_and_enable_individual_label_button(*args):
    # Check if all the first 3 Entry fields have data
    all_first_three_fields_have_data = all(entry.get() for entry in input_fields[:3])

    # Check if the last Entry field has data
    last_field_has_data = input_fields[-1].get() != ""

    # Check if the modify button is disabled
    modify_button_enabled = button_modify.cget("state") == "normal"

    # Check if the save button is disabled
    save_button_disabled = button_save.cget("state") == "disabled"

    # Enable the individual label button accordingly
    if all_first_three_fields_have_data and last_field_has_data and save_button_disabled and modify_button_enabled:
        button_individual_label.configure(state="normal")
        root.bind('<Return>', lambda event: generate_individual_label())
    else:
        button_individual_label.configure(state="disabled")
        root.unbind('<Return>')


def generate_pallet_label():
    data_codigo = input_fields[1].get()
    data_descripcion = input_fields[2].get()
    data_cables_por_pallet = input_fields[3].get()
    #data_longitud_cables = input_fields[4].get()

    # Image path
    image_path = resource_path("logo.png")

    #label_individual = [data_codigo,
    #                    data_descripcion,
    #                    "BRAND         " + data_longitud_cables + " metros"]

    label_pallet = [image_path,
                    "Proveedor: BRAND",
                    data_codigo,
                    data_descripcion,
                    "Cantidad: " + str(data_cables_por_pallet) + " unidades"]

    #claro_etiqueta_individual.create_individual_label_pdf(label_individual)
    etiqueta_pallet.create_pallet_label_pdf(label_pallet)

    messagebox.showinfo("Generación Exitosa",
                        "El archivo se ha generado con éxito.")

def generate_individual_label():
    data_codigo = input_fields[1].get()
    data_descripcion = input_fields[2].get()
    data_longitud_cables = input_fields[4].get()

    label_individual = [data_codigo,
                        data_descripcion,
                        "BRAND         " + data_longitud_cables + " metros"]

    etiqueta_individual.create_individual_label_pdf(label_individual)
    # Send pdf file to the printer and print directly
    pdf_print.send_pdf_to_printer()

    # Clear the last entry field
    input_fields[4].delete(0, tk.END)
    input_fields[4].focus_set()

    # Re-check and enable/disable the print button as necessary
    check_and_enable_individual_label_button()


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller
    Without this, the png image won't bundle properly into the exe file """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# ----- Widget Creation -----


button_label_list = tk.Button(root, text="Lista de Etiquetas", command=open_label_list)
button_new_label = tk.Button(root, text="Nueva Etiqueta", command=new_label)
button_pallet_label = tk.Button(root, text="Generar Etiqueta Pallet", state="disabled", command=generate_pallet_label)

# Create 4 text fields with input fields to the right
text_field_data = [
    "Nombre Etiqueta (interno):",
    "Código:",
    "Descripción:",
    "Cables por pallet:",
    "Longitud del cable"
]

text_fields = []
input_fields = []
# The range has to be N because of the N text fields. We count from 1
for i in range(5):
    text_field = tk.Label(root, text=text_field_data[i])
    input_field = tk.Entry(root)
    text_fields.append(text_field)
    input_fields.append(input_field)

    # Bind the appropriate function based on the index
    if i < 4:
        # Bind to KeyRelease event for the first 4 entry fields
        input_field.bind("<KeyRelease>", check_and_enable_save_button)
    else:
        # Bind to KeyRelease event for the last entry field
        input_field.bind("<KeyRelease>", check_and_enable_individual_label_button)

    # Set the disabled text & background colors once
    if i == 0:
        input_fields[i].configure(disabledforeground="black", background="#D0E7D2", disabledbackground="#D0E7D2")
    else:
        input_fields[i].configure(disabledforeground="black", disabledbackground="white")

# Modify button
button_modify = tk.Button(root, text="Modificar", state="disabled", command=modify)

button_save = tk.Button(root, text="Guardar", state="disabled", command=save)

button_individual_label = tk.Button(root, text="Imprimir etiqueta individual", state="disabled", command=generate_individual_label)

# ----- Widget placement -----
# Buttons
button_label_list.grid(row=0, column=0, pady=(10, 10))
button_new_label.grid(row=0, column=1, pady=(10, 10))
button_pallet_label.grid(row=0, column=2, pady=(10, 10))

# Labels + Input Fields
for i in range(5):
    text_fields[i].grid(row=i + 1, column=0, padx=(10, 5), pady=10)
    input_fields[i].grid(row=i + 1, column=1, padx=(5, 10), pady=10, columnspan=2, sticky="EW")

# Buttons
button_modify.grid(row=10, column=0, pady=(10, 10))
button_save.grid(row=10, column=1, pady=(10, 10))
button_individual_label.grid(row=10, column=2, pady=(10, 10))

root.columnconfigure(0, minsize=170)
root.columnconfigure(1, minsize=170)
root.columnconfigure(2, minsize=170)

# Set the window size
main_window_width = 530
main_window_height = 320
root.geometry(f"{main_window_width}x{main_window_height}")
# Center the main window
center_window(root, main_window_width, main_window_height)
# Make the window non-resizable
root.resizable(width=False, height=False)

"""
Use Mutable Data Types: You can wrap the variable in a mutable data type,
like a list or dictionary, and then modify its contents. This is a bit of
a hack and not very readable, but it works because, as mentioned earlier,
you can modify the contents of a mutable object from within a function
without the global keyword.
"""
old_name = ["invalid_direction"]
retrieve_last_opened_label_file()

root.mainloop()
