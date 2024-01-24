import pandas as pd
import mysql.connector
import tkinter as tk
from tkinter import Label, Entry, Button
import numpy as np
import webbrowser
from datetime import datetime
import joblib


default_font = ("Helvetica", 15) 
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mysql",
    database="healthyeni"
)
svm_model = joblib.load('model.pkl')
scaler = joblib.load('scaler.pkl') 
def laborant_login():
    def check_laborant():
        laborant_id = entry_laborant_id.get()
        laborant_password = entry_laborant_password.get()

        cursor = conn.cursor()
        query = "SELECT * FROM laborant WHERE ID = %s AND Password = %s"
        cursor.execute(query, (laborant_id, laborant_password))
        result = cursor.fetchone()

        if result:
            laborant_window.destroy()
            laborant_page()
        else:
            error_label.config(text="Wrong ID or Password!",font=default_font)

    laborant_window = tk.Toplevel(root)
    laborant_window.title("Laborant Entry")
    laborant_window.geometry("300x180")
    laborant_window.configure(bg="pink")
    icon_path = 'lab.ico'
    laborant_window.iconbitmap(icon_path)  
    window_width = 300
    window_height = 180
    x_coordinate = 600
    y_coordinate = 220

    laborant_window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

    label_laborant_id = tk.Label(laborant_window, text="Laborant ID:",bg="pink",fg="blue",font=default_font)
    label_laborant_id.pack()

    entry_laborant_id = tk.Entry(laborant_window)
    entry_laborant_id.pack()

    label_laborant_password = tk.Label(laborant_window, text="Laborant Password:",bg="pink", fg="blue",font=default_font)
    label_laborant_password.pack()

    entry_laborant_password = tk.Entry(laborant_window, show="*")
    entry_laborant_password.pack()

    login_button = tk.Button(laborant_window, text="Enter", command=check_laborant,bg="pink",fg="blue",font=default_font)
    login_button.pack()

    error_label = tk.Label(laborant_window, bg="pink",fg="red",font=default_font)
    error_label.pack()

def doctor_login():
    def check_doctor():
        doctor_id = entry_doctor_id.get()
        doctor_password = entry_doctor_password.get()

        cursor = conn.cursor()
        query = "SELECT * FROM doctor WHERE ID = %s AND Password = %s"
        cursor.execute(query, (doctor_id, doctor_password))
        result = cursor.fetchone()

        if result:
            doctor_window.destroy() 
            doctor_page()
        else:
            error_label.config(text="Wrong ID or Password!",font=default_font)

    doctor_window = tk.Toplevel(root)
    doctor_window.title("Doctor Entry")
    doctor_window.configure(bg="pink") 
    doctor_window.geometry("300x180")
    icon_path = 'doc.ico'
    doctor_window.iconbitmap(icon_path)

    window_width = 300
    window_height = 180
    x_coordinate = 600
    y_coordinate = 220

    doctor_window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

    label_doctor_id = tk.Label(doctor_window, text="Doctor ID:",bg="pink", fg="blue",font=default_font)
    label_doctor_id.pack()

    entry_doctor_id = tk.Entry(doctor_window)
    entry_doctor_id.pack()

    label_doctor_password = tk.Label(doctor_window, text="Doctor Password:",bg="pink", fg="blue",font=default_font)
    label_doctor_password.pack()

    entry_doctor_password = tk.Entry(doctor_window, show="*")
    entry_doctor_password.pack()

    login_button = tk.Button(doctor_window, text="Enter", command=check_doctor,bg="pink",fg="blue",font=default_font)
    login_button.pack()

    error_label = tk.Label(doctor_window,bg="pink", fg="red",font=default_font)
    error_label.pack()

def laborant_page():
    def button_click():
        global laborant_window_ref 
        laborant_window_ref = frame 
        TC = int(entry_TC.get())
        Age = int(entry_Age.get())
        Sex = int(entry_Sex.get())
        ChestPainType = int(entry_ChestPainType.get())
        RestingBP = int(entry_RestingBP.get())
        Cholesterol = int(entry_Cholesterol.get())
        FastingBS = int(entry_FastingBS.get())
        RestingECG = entry_RestingECG.get()
        MaxHR = int(entry_MaxHR.get())
        ExerciseAngina = int(entry_ExerciseAngina.get())
        Oldpeak = float(entry_Oldpeak.get())
        ST_Slope = entry_ST_Slope.get()
        datalist = [Age, Sex, ChestPainType, RestingBP, Cholesterol, FastingBS,
                    RestingECG, MaxHR, ExerciseAngina, Oldpeak, ST_Slope]

        datalist = np.array(datalist).reshape(1, -1) 
        datalist = scaler.transform(datalist)

        prediction = svm_model.predict(datalist)
        predicted_value = float(prediction[0])

        mycursor = conn.cursor()
        mycursor.execute("SELECT * FROM lab_veri WHERE TC = %s", (TC,))
        existing_record = mycursor.fetchone()

        if existing_record:
            sql = "UPDATE lab_veri SET Age=%s, Sex=%s, ChestPainType=%s, RestingBP=%s, Cholesterol=%s, FastingBS=%s, RestingECG=%s, MaxHR=%s, ExerciseAngina=%s, Oldpeak=%s, ST_Slope=%s, HeartDisease=%s WHERE TC=%s"
            update_data = (Age, Sex, ChestPainType, RestingBP, Cholesterol, FastingBS,
                           RestingECG, MaxHR, ExerciseAngina, Oldpeak, ST_Slope, predicted_value, TC)
            mycursor.execute(sql, update_data)
        else:
            sql = "INSERT INTO lab_veri (TC, Age, Sex, ChestPainType, RestingBP, Cholesterol, FastingBS, RestingECG, MaxHR, ExerciseAngina, Oldpeak, ST_Slope, HeartDisease) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            insert_data = (TC, Age, Sex, ChestPainType, RestingBP, Cholesterol, FastingBS,
                           RestingECG, MaxHR, ExerciseAngina, Oldpeak, ST_Slope, predicted_value)
            mycursor.execute(sql, insert_data)

        conn.commit()
        for widget in frame.winfo_children():
            widget.destroy()

        message_label = Label(frame, text="Data added into the system", bg="pink", fg="blue", font=default_font)
        message_label.pack(pady=10)
        return_button = Button(frame, text="Return to Laborant Page", command=lambda: [laborant_window_ref.destroy(), laborant_page()], bg="pink", fg="red", font=default_font)
        return_button.pack(pady=10)
        quit_button = Button(frame, text="Quit", command=lambda: [laborant_window_ref.destroy()], bg="pink", fg="red", font=default_font)
        quit_button.pack(pady=10)

    frame = tk.Toplevel(root)
    frame.title("Laborant Page")
    frame.configure(bg="pink") 
    frame.geometry("440x800")

    window_width = 440
    window_height = 800
    x_coordinate = 530
    y_coordinate = 10

    frame.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

    label_TC = Label(frame, text="ID:", bg="pink", fg="red", font=default_font)
    label_TC.grid(row=0, column=0, sticky="n", pady=10)
    entry_TC = Entry(frame)
    entry_TC.grid(row=0, column=1)

    label_Age = Label(frame, text="Age:", bg="pink", fg="red", font=default_font)
    label_Age.grid(row=1, column=0, sticky="n", pady=10)
    entry_Age = Entry(frame)
    entry_Age.grid(row=1, column=1)

    label_Sex = Label(frame, text="Sex:\n(0: Male, 1: Female)", bg="pink", fg="red", font=default_font)
    label_Sex.grid(row=2, column=0, sticky="n", pady=10)
    entry_Sex = Entry(frame)
    entry_Sex.grid(row=2, column=1)

    label_ChestPainType = Label(frame, text="Chest Pain Type:\n(0: ASY, 1: ATA, 2: NAP, 3: TA)", bg="pink", fg="red", font=default_font)
    label_ChestPainType.grid(row=3, column=0, sticky="n", pady=10)
    entry_ChestPainType = Entry(frame)
    entry_ChestPainType.grid(row=3, column=1)

    label_RestingBP = Label(frame, text="Resting BP:", bg="pink", fg="red", font=default_font)
    label_RestingBP.grid(row=4, column=0, sticky="n", pady=10)
    entry_RestingBP = Entry(frame)
    entry_RestingBP.grid(row=4, column=1)

    label_Cholesterol = Label(frame, text="Cholesterol:", bg="pink", fg="red", font=default_font)
    label_Cholesterol.grid(row=5, column=0, sticky="n", pady=10)
    entry_Cholesterol = Entry(frame)
    entry_Cholesterol.grid(row=5, column=1)

    label_FastingBS = Label(frame, text="Fasting BS:\n(0: False, 1: True)", bg="pink", fg="red", font=default_font)
    label_FastingBS.grid(row=6, column=0, sticky="n", pady=10)
    entry_FastingBS = Entry(frame)
    entry_FastingBS.grid(row=6, column=1)

    label_RestingECG = Label(frame, text="Resting ECG:\n(0: LVH, 1: Normal, 2: ST)", bg="pink", fg="red", font=default_font)
    label_RestingECG.grid(row=7, column=0, sticky="n", pady=10)
    entry_RestingECG = Entry(frame)
    entry_RestingECG.grid(row=7, column=1)

    label_MaxHR = Label(frame, text="Max HR:", bg="pink", fg="red", font=default_font)
    label_MaxHR.grid(row=8, column=0, sticky="n", pady=10)
    entry_MaxHR = Entry(frame)
    entry_MaxHR.grid(row=8, column=1)

    label_ExerciseAngina = Label(frame, text="Exercise Angina:\n(0: No, 1: Yes)", bg="pink", fg="red", font=default_font)
    label_ExerciseAngina.grid(row=9, column=0, sticky="n", pady=10)
    entry_ExerciseAngina = Entry(frame)
    entry_ExerciseAngina.grid(row=9, column=1)

    label_Oldpeak = Label(frame, text="Oldpeak:", bg="pink", fg="red", font=default_font)
    label_Oldpeak.grid(row=10, column=0, sticky="n", pady=10)
    entry_Oldpeak = Entry(frame)
    entry_Oldpeak.grid(row=10, column=1)

    label_ST_Slope = Label(frame, text="ST Slope:\n(0: Down, 1: Flat, 2: Up)", bg="pink", fg="red", font=default_font)
    label_ST_Slope.grid(row=11, column=0, sticky="n", pady=10)
    entry_ST_Slope = Entry(frame)
    entry_ST_Slope.grid(row=11, column=1)

    predict_button = Button(frame, text="Predict", command=button_click, bg="pink", fg="red", font=default_font)
    predict_button.grid(row=12, columnspan=2, pady=10)  


    root.mainloop()


def doctor_page():
    heart_disease_result = None
    control = None
    def check_TC():
        patient_TC = int(entry_patient_TC.get())
        nonlocal heart_disease_result
        nonlocal control
        if heart_disease_result:
            heart_disease_result.destroy()
        if control:
            control.destroy()
        cursor = conn.cursor()
        query = "SELECT HeartDisease, Age, Sex, ChestPainType, RestingBP, Cholesterol, FastingBS, RestingECG, MaxHR, ExerciseAngina, Oldpeak, ST_Slope FROM lab_veri WHERE TC = %s"
        cursor.execute(query, (patient_TC,))
        result = cursor.fetchone()

        if result:
            heart_disease = result[0]
            if heart_disease == 1:
                heart_disease_result = tk.Label(doctor_window, text="", bg="pink", fg="red",font=default_font)
                heart_disease_result.pack()
                heart_disease_result.config(text="Patient possibly has a heart disease!")
            else:
                heart_disease_result = tk.Label(doctor_window, text="", bg="pink", fg="blue",font=default_font)
                heart_disease_result.pack()
                heart_disease_result.config(text="Patient possibly does not have a heart disease.")

            for widget in data_frame.winfo_children():
                widget.destroy()

            data_labels = [
                "Age:", "Sex:\n(0: Male, 1: Female)", "ChestPainType:\n(0: ASY, 1: ATA, 2: NAP, 3: TA)", "RestingBP:", "Cholesterol:",
                "FastingBS:\n(0: False, 1: True)", "RestingECG:\n(0: LVH, 1: Normal, 2: ST)", "MaxHR:", "ExerciseAngina:\n(0: No, 1: Yes)", "Oldpeak:",
                "ST_Slope:\n(0: Down, 1: Flat, 2: Up)"
            ]

            for i in range(len(data_labels)):
                label = tk.Label(data_frame, text=data_labels[i], bg="pink", fg="blue")
                label.grid(row=i, column=0, padx=10, pady=5)
                value_label = tk.Label(data_frame, text=result[i + 1], bg="pink", fg="blue")
                value_label.grid(row=i, column=1, padx=10, pady=5)
        else:
            control = tk.Label(doctor_window, text="", bg="pink", fg="red",font=default_font)
            control.pack()
            control.config(text="There is no patient with this ID!")

        

    doctor_window = tk.Toplevel(root)
    doctor_window.title("Doctor Page")
    doctor_window.configure(bg="pink") 
    doctor_window.geometry("440x680")
    icon_path = 'doc.ico'
    doctor_window.iconbitmap(icon_path)

    window_width = 440
    window_height = 680
    x_coordinate = 530
    y_coordinate = 100

    doctor_window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

    label_patient_TC = tk.Label(doctor_window, text="Patient ID:", bg="pink", fg="blue", font=default_font)
    label_patient_TC.pack()

    entry_patient_TC = tk.Entry(doctor_window)
    entry_patient_TC.pack()

    check_button = tk.Button(doctor_window, text="Enter", command=check_TC, bg="pink", fg="blue", font=default_font)
    check_button.pack()

    quit_button = Button(doctor_window, text="Quit", command=lambda: [doctor_window.destroy()], bg="pink", fg="red", font=default_font)
    quit_button.pack()

    data_frame = tk.Frame(doctor_window, bg="pink")
    data_frame.pack(pady=20)

    

def send_email():
    recipient = "help@healthospital.com"  
    subject = "Help Needed About Heart Failure Application" 
    body = "Hello, I have an issue with the Heart Failure Application."  

    mailto_link = f"mailto:{recipient}?subject={subject}&body={body}"
    webbrowser.open_new(mailto_link)

def update_clock():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    clock_label.config(text="Time: " + current_time)
    clock_label.after(1000, update_clock)

root = tk.Tk()
root.title('Heart Failure Prediction')
icon_path = 'pulse.ico'
root.iconbitmap(icon_path)
root.geometry("500x470") 
window_width = 500
window_height = 470
x_coordinate = 500
y_coordinate = 100

root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")


bg_image = tk.PhotoImage(file='kalp.gif')


background_label = tk.Label(root, image=bg_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)  


laborant_button = tk.Button(root, text="Laborant Entry", command=laborant_login,bg="pink",fg="red",font=default_font,width=15, height=1)
laborant_button.place(x=150, y=175)  

doctor_button = tk.Button(root, text="Doctor Entry", command=doctor_login,bg="pink",fg="red",font=default_font,width=15, height=1)
doctor_button.place(x=150, y=235) 

help_button = tk.Button(root, text="Contact", command=send_email,bg="pink",fg="red",width=7, height=1)
help_button.pack()
help_button.place(x=425, y=425)

date_today = datetime.today().strftime("%d.%m.%Y")

date_label = tk.Label(root, text="Date: " + date_today,bg="white",fg="red")
date_label.pack()
date_label.place(x=375, y=10)

clock_label = tk.Label(root, text="Time: ",bg="white",fg="red")
clock_label.pack()
clock_label.place(x=385, y=30)
update_clock() 




root.mainloop()