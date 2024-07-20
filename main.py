import tkinter
from tkinter import ttk
from tkinter import messagebox
import ttkbootstrap as ttk
import sqlite3

def enter_data():
    accepted = accept_var.get()
    
    if accepted=="Accepted":
        # User info
        nombre = Nombre_entry.get()
        apellido = Apellido_entry.get()
        cedula = cedula_entry.get()
        
        if nombre and apellido:
            title = title_combobox.get()
            age = age_spinbox.get()
            nationality = nationality_combobox.get()
            
            # Course info
            registration_status = reg_status_var.get()
            numcourses = numcourses_spinbox.get()
            numsemesters = numsemesters_spinbox.get()
            
            print("Nombre: ", nombre, "Apellido: ", apellido, "Cedula:",cedula)
            print("Title: ", title, "Age: ", age, "Nationality: ", nationality)
            print("# Courses: ", numcourses, "# Semesters: ", numsemesters)
            print("Registration status", registration_status)
            print("------------------------------------------")
            
            # Create Table
            conn = sqlite3.connect('data.db')
            table_create_query = '''CREATE TABLE IF NOT EXISTS Student_Data 
                    (nombre TEXT, apellido TEXT,cedula INT, titulo TEXT, age INT, nationality TEXT, 
                    registration_status TEXT, num_courses INT, num_semesters INT)
            '''
            conn.execute(table_create_query)
            
            # Insert Data
            data_insert_query = '''INSERT INTO Student_Data (nombre, apellido, cedula, titulo, 
            age, nationality, registration_status, num_courses, num_semesters) VALUES 
            (?, ?, ?, ?, ?, ?, ?, ?, ?)'''
            data_insert_tuple = (nombre, apellido, cedula, title,
                                  age, nationality, registration_status, numcourses, numsemesters)
            cursor = conn.cursor()
            cursor.execute(data_insert_query, data_insert_tuple)
            conn.commit()
            conn.close()

            
                
        else:
            tkinter.messagebox.showwarning(title="Error", message="Nombre y Apellido son requeridos.")
    else:
        tkinter.messagebox.showwarning(title= "Error", message="No has aceptado los terminos")

def show_additional_info():
    # Crear ventana emergente
    additional_info_window = tkinter.Toplevel(window)
    additional_info_window.title("Información Complementaria")

    # Crear tabla
    additional_info_frame = tkinter.Frame(additional_info_window)
    additional_info_frame.pack(padx=20, pady=20)

    # Crear encabezados de la tabla
    headers = ["Tamaño", "Carro", "Dirección", "Profesión", "Institución"]
    for i, header in enumerate(headers):
        header_label = tkinter.Label(additional_info_frame, text=header)
        header_label.grid(row=0, column=i)

    # Crear entradas de la tabla
    size_entry = tkinter.Entry(additional_info_frame)
    car_entry = tkinter.Entry(additional_info_frame)
    address_entry = tkinter.Entry(additional_info_frame)
    profession_entry = tkinter.Entry(additional_info_frame)
    institution_entry = tkinter.Entry(additional_info_frame)

    size_entry.grid(row=1, column=0)
    car_entry.grid(row=1, column=1)
    address_entry.grid(row=1, column=2)
    profession_entry.grid(row=1, column=3)
    institution_entry.grid(row=1, column=4)

    # Botón para guardar datos
    save_button = tkinter.Button(additional_info_frame, text="Guardar", command=lambda: save_additional_data(
        additional_info_window, size_entry.get(), car_entry.get(), address_entry.get(), profession_entry.get(), institution_entry.get()))
    save_button.grid(row=2, column=0, columnspan=5, pady=10)

def save_additional_data(additional_info_window, size, car, address, profession, institution):
    # Conectar a la base de datos
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    # Crear tabla "Complementos" si no existe
    c.execute('''CREATE TABLE IF NOT EXISTS Complementos
                 (size TEXT, car TEXT, address TEXT, profession TEXT, institution TEXT)''')

    # Insertar datos en la tabla "Complementos"
    c.execute("INSERT INTO Complementos (size, car, address, profession, institution) VALUES (?, ?, ?, ?, ?)",
              (size, car, address, profession, institution))
    conn.commit()
    conn.close()

    # Cerrar la ventana emergente
    additional_info_window.destroy()

def open_data_window():
    # Crear ventana emergente
    data_window = tkinter.Toplevel(window)
    data_window.title("Consulta de Datos")

    # Crear tabla
    data_frame = tkinter.Frame(data_window)
    data_frame.pack(padx=20, pady=20)

    # Conectar a la base de datos
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    # Obtener los datos de la tabla "Student_Data"
    c.execute("SELECT * FROM Student_Data")
    data = c.fetchall()

    # Crear encabezados de la tabla
    headers = ["Nombre", "Apellido", "Cedula", "Titulo", "Edad", "Nacionalidad", "Estado Registro", "# Cursos", "# Semestres"]
    for i, header in enumerate(headers):
        header_label = tkinter.Label(data_frame, text=header)
        header_label.grid(row=0, column=i)

    # Mostrar los datos en la tabla
    for row_index, row in enumerate(data, start=1):
        for col_index, value in enumerate(row):
            data_label = tkinter.Label(data_frame, text=str(value))
            data_label.grid(row=row_index, column=col_index)

    # Cerrar conexión a la base de datos
    conn.close()

window = ttk.Window(themename='journal')  
window.title("Registro Personal")

frame = ttk.Frame(window)
frame.pack()

# Saving User Info
user_info_frame = ttk.LabelFrame(frame, text="Informacion Empleado")
user_info_frame.grid(row= 0, column=0, padx=20, pady=10)

Nombre_label = ttk.Label(user_info_frame, text="Nombre")
Nombre_label.grid(row=0, column=0)
Apellido_label = ttk.Label(user_info_frame, text="Apellido")
Apellido_label.grid(row=0, column=1)
cedula_label = ttk.Label(user_info_frame, text="Cedula")
cedula_label.grid(row=2, column=2)

Nombre_entry = ttk.Entry(user_info_frame)
Apellido_entry = ttk.Entry(user_info_frame)
cedula_entry = ttk.Entry(user_info_frame)
Nombre_entry.grid(row=1, column=0)
Apellido_entry.grid(row=1, column=1)
cedula_entry.grid(row=3, column=2)

title_label = ttk.Label(user_info_frame, text="Titulo")
title_combobox = ttk.Combobox(user_info_frame, values=["", "Sr.", "Sra.", "Dr."])
title_label.grid(row=0, column=2)
title_combobox.grid(row=1, column=2)

age_label = ttk.Label(user_info_frame, text="Age")
age_spinbox = ttk.Spinbox(user_info_frame, from_=18, to=110)
age_label.grid(row=2, column=0)
age_spinbox.grid(row=3, column=0)

nationality_label = ttk.Label(user_info_frame, text="Nationality")
nationality_combobox = ttk.Combobox(user_info_frame, values=["Africa", "Antarctica", "Asia", "Europe", "North America", "Oceania", "South America"])
nationality_label.grid(row=2, column=1)
nationality_combobox.grid(row=3, column=1)

for widget in user_info_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# Saving Course Info
courses_frame = tkinter.LabelFrame(frame)
courses_frame.grid(row=1, column=0, sticky="news", padx=20, pady=10)

registered_label = tkinter.Label(courses_frame, text="Registration Status")

reg_status_var = tkinter.StringVar(value="Not Registered")
registered_check = tkinter.Checkbutton(courses_frame, text="Currently Registered",
                                       variable=reg_status_var, onvalue="Registered", offvalue="Not registered")

registered_label.grid(row=0, column=0)
registered_check.grid(row=1, column=0)

numcourses_label = tkinter.Label(courses_frame, text= "# Completed Courses")
numcourses_spinbox = tkinter.Spinbox(courses_frame, from_=0, to='infinity')
numcourses_label.grid(row=0, column=1)
numcourses_spinbox.grid(row=1, column=1)

numsemesters_label = tkinter.Label(courses_frame, text="# Semesters")
numsemesters_spinbox = tkinter.Spinbox(courses_frame, from_=0, to="infinity")
numsemesters_label.grid(row=0, column=2)
numsemesters_spinbox.grid(row=1, column=2)

for widget in courses_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# Accept terms
terms_frame = tkinter.LabelFrame(frame, text="Terms & Conditions")
terms_frame.grid(row=2, column=0, sticky="news", padx=20, pady=10)

accept_var = tkinter.StringVar(value="Not Accepted")
terms_check = tkinter.Checkbutton(terms_frame, text= "I accept the terms and conditions.",
                                  variable=accept_var, onvalue="Accepted", offvalue="Not Accepted")
terms_check.grid(row=0, column=0)

# Button
button = tkinter.Button(frame, text="Enviar", command= enter_data)
button.grid(row=3, column=0, sticky="news", padx=20, pady=10)

button = tkinter.Button(frame, text="Información Complementaria", command=show_additional_info)
button.grid(row=4, column=0, sticky="news", padx=20, pady=10)

button = tkinter.Button(frame, text="Consulta", command=open_data_window)
button.grid(row=5, column=0, sticky="news", padx=20, pady=10)
 
 
window.mainloop()
