import sklearn
import os
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import joblib
from PIL import Image, ImageTk  # For background image

# Get the folder where the script is running
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Use absolute paths
csv_path = os.path.join(BASE_DIR, "heart.csv")
model_path = os.path.join(BASE_DIR, "heart_model.pkl")
scaler_path = os.path.join(BASE_DIR, "scaler.pkl")
bg_image_path = os.path.join(BASE_DIR, "background.jpg")

# Load the trained model and scaler using absolute paths
model = joblib.load(model_path)
scaler = joblib.load(scaler_path)

# Function to map display value to numeric value
def get_sex_numeric_value(sex_display_value):
    return sex_numeric_values[sex_display_values.index(sex_display_value)]

def get_cp_numeric_value(cp_display_value):
    return cp_numeric_values[cp_display_values.index(cp_display_value)]

def get_fbs_numeric_value(fbs_display_value):
    return fbs_numeric_values[fbs_display_values.index(fbs_display_value)]

def get_ecg_numeric_value(ecg_display_value):
    return ecg_numeric_values[ecg_display_values.index(ecg_display_value)]

def get_exang_numeric_value(exang_display_value):
    return exang_numeric_values[exang_display_values.index(exang_display_value)]

def get_slope_numeric_value(slope_display_value):
    return slope_numeric_values[slope_display_values.index(slope_display_value)]

# Function to make predictions
def predict_heart_disease():
    try:
        # Get user inputs
        input_data = np.array([
            int(age_var.get()), 
            get_sex_numeric_value(sex_var.get()),  
            get_cp_numeric_value(cp_var.get()), 
            int(bp_var.get()),  
            int(chol_var.get()),  
            get_fbs_numeric_value(fbs_var.get()), 
            get_ecg_numeric_value(ecg_var.get()), 
            int(hr_var.get()),  
            get_exang_numeric_value(exang_var.get()), 
            float(oldpeak_var.get()),  
            get_slope_numeric_value(slope_var.get())
        ]).reshape(1, -1)

        # Scale input and make prediction
        scaled_input = scaler.transform(input_data)
        prediction = model.predict(scaled_input)

        # Display result with styling
        result_text = "⚠ High Risk of Heart Disease" if prediction[0] == 1 else "✅ Low Risk of Heart Disease"
        result_color = "#FF4C4C" if prediction[0] == 1 else "#4CAF50"

        result_label.config(text=f"Prediction: {result_text}", fg="black", bg=result_color)

    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong: {e}")

# Function to reset all input fields
def reset_fields():
    age_var.set("")
    sex_var.set("")
    cp_var.set("")
    bp_var.set(90)  
    chol_var.set(100)  
    fbs_var.set("")
    ecg_var.set("")
    hr_var.set(60)  
    exang_var.set("")
    oldpeak_var.set(0.0)  
    slope_var.set("")
    result_label.config(text="", bg=root.cget("bg"))  

# Create Tkinter window
root = tk.Tk()
root.title("Heart Disease Prediction")  
root.geometry("1200x600")

# Load background image using absolute path
bg_image = Image.open(bg_image_path)  
bg_image = bg_image.resize((1200, 600))
bg_photo = ImageTk.PhotoImage(bg_image)

# Background label
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)

# Style
label_font = ("Arial", 13, "bold")
input_font = ("Arial", 11)

# Add a title label at the top
title_label = tk.Label(root, text="Heart Disease Prediction", font=("Arial", 15, "bold"), bg="#4CAF50", fg="black", pady=10)
title_label.pack()

# Frame for input fields
frame = tk.Frame(root, bd=0)
frame.pack(pady=10)

# Variables
age_var = tk.StringVar()
sex_var = tk.StringVar()
cp_var = tk.StringVar()
bp_var = tk.IntVar(value=90)
chol_var = tk.IntVar(value=100)
fbs_var = tk.StringVar()
ecg_var = tk.StringVar()
hr_var = tk.IntVar(value=60)
exang_var = tk.StringVar()
oldpeak_var = tk.DoubleVar(value=0.0)
slope_var = tk.StringVar()

# Define display and numeric values for each field
sex_display_values = ["Female", "Male"]
sex_numeric_values = [0, 1]

cp_display_values = ["Asymptomatic", "Atypical Angina", "Non-Angina Pain", "Typical Angina"]
cp_numeric_values = [0, 1, 2, 3]

fbs_display_values = ["Normal", "High"]
fbs_numeric_values = [0, 1]

ecg_display_values = ["Normal", "Abnormal", "Hypertrophy"]
ecg_numeric_values = [0, 1, 2]

exang_display_values = ["No", "Yes"]
exang_numeric_values = [0, 1]

slope_display_values = ["Up", "Flat", "Down"]
slope_numeric_values = [0, 1, 2]

# Left column inputs
left_column = tk.Frame(frame)
left_column.grid(row=0, column=0, padx=20, pady=10)
tk.Label(left_column, text="Age:", font=label_font, fg="black").pack()
ttk.Entry(left_column, textvariable=age_var, font=input_font).pack(pady=3)

tk.Label(left_column, text="Sex:", font=label_font, fg="black").pack()
ttk.Combobox(left_column, textvariable=sex_var, values=sex_display_values, font=input_font).pack(pady=3)

tk.Label(left_column, text="Chest Pain (0-3):", font=label_font, fg="black").pack()
ttk.Combobox(left_column, textvariable=cp_var, values=cp_display_values, font=input_font).pack(pady=3)

tk.Label(left_column, text="Resting BP:", font=label_font, fg="black").pack()
tk.Scale(left_column, from_=90, to=200, orient="horizontal", variable=bp_var, length=250, font=input_font).pack(pady=3)

tk.Label(left_column, text="Cholesterol:", font=label_font, fg="black").pack()
tk.Scale(left_column, from_=100, to=600, orient="horizontal", variable=chol_var, length=250, font=input_font).pack(pady=3)

# Right column inputs
right_column = tk.Frame(frame)
right_column.grid(row=0, column=1, padx=20, pady=10)
tk.Label(right_column, text="Fasting BS:", font=label_font, fg="black").pack()
ttk.Combobox(right_column, textvariable=fbs_var, values=fbs_display_values, font=input_font).pack(pady=3)

tk.Label(right_column, text="Resting ECG:", font=label_font, fg="black").pack()
ttk.Combobox(right_column, textvariable=ecg_var, values=ecg_display_values, font=input_font).pack(pady=3)

tk.Label(right_column, text="Max HR:", font=label_font, fg="black").pack()
tk.Scale(right_column, from_=60, to=220, orient="horizontal", variable=hr_var, length=250, font=input_font).pack(pady=3)

tk.Label(right_column, text="Exercise Angina:", font=label_font, fg="black").pack()
ttk.Combobox(right_column, textvariable=exang_var, values=exang_display_values, font=input_font).pack(pady=3)

tk.Label(right_column, text="Oldpeak:", font=label_font, fg="black").pack()
tk.Scale(right_column, from_=0.0, to=6.0, orient="horizontal", resolution=0.1, variable=oldpeak_var, length=250, font=input_font).pack(pady=3)

tk.Label(right_column, text="ST Slope:", font=label_font, fg="black").pack()
ttk.Combobox(right_column, textvariable=slope_var, values=slope_display_values, font=input_font).pack(pady=3)

# Frame for buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=5)

predict_btn = tk.Button(button_frame, text="Predict", command=predict_heart_disease, font=("Arial", 13, "bold"), bg="#4CAF50", fg="black", padx=20, pady=5)
predict_btn.pack(side="left", padx=10)

reset_btn = tk.Button(button_frame, text="Reset", command=reset_fields, font=("Arial", 13, "bold"), bg="#FF5733", fg="black", padx=20, pady=5)
reset_btn.pack(side="left", padx=10)

result_label = tk.Label(root, text="", font=("Arial", 14, "bold"), fg="black", pady=10)
result_label.pack()

root.mainloop()