import tkinter as tk
from time import strftime
from datetime import datetime
from tkinter import messagebox
import pygame

pygame.mixer.init()

root = tk.Tk()
root.title("Reloj Digital con Alarmas")

alarms = []
alarm_active = {}  

def update_time():
    current_time = strftime('%H:%M:%S')  
    current_date = datetime.now().strftime('%d %b %Y')
    time_label.config(text=current_time)
    date_label.config(text=current_date)
    root.after(1000, update_time) 
    check_alarms()  

def check_alarms():
    now = strftime('%H:%M')
    for alarm_time in alarms:
        if now == alarm_time:
            if alarm_time not in alarm_active or not alarm_active[alarm_time]:
                play_alarm_sound()
                messagebox.showinfo("Alarma", "¡Es hora de tu alarma!")
                alarm_active[alarm_time] = True
            alarms.remove(alarm_time)
            update_alarm_list()

def play_alarm_sound():
    try:
        pygame.mixer.music.load('lofi.mp3')
        pygame.mixer.music.play()
        root.after(30000, pygame.mixer.music.stop) 
    except Exception as e:
        print(f"Error al reproducir el sonido de alarma: {e}")

def is_valid_time(time_str):
    try:
        datetime.strptime(time_str, '%H:%M')
        return True
    except ValueError:
        return False

def set_alarm():
    alarm_time = alarm_entry.get()
    if alarm_time:
        if is_valid_time(alarm_time):
            if alarm_time not in alarms:
                alarms.append(alarm_time)
                alarm_active[alarm_time] = False  
                update_alarm_list()
                alarm_entry.delete(0, tk.END)
                messagebox.showinfo("Alarma", f"Alarma configurada para las {alarm_time}")
            else:
                messagebox.showwarning("Alarma", "Esta alarma ya está configurada.")
        else:
            messagebox.showwarning("Formato Incorrecto", "El formato debe ser HH:MM y la hora debe ser válida.")
    else:
        messagebox.showwarning("Campo Vacío", "Por favor ingrese la hora y minutos.")

def delete_alarm(alarm_list):
    selected_index = alarm_list.curselection()
    if selected_index:
        alarm_time = alarm_list.get(selected_index)
        confirm = messagebox.askyesno("Confirmar Eliminación", f"¿Deseas eliminar la alarma para las {alarm_time}?")
        if confirm:
            if alarm_time in alarms:
                alarms.remove(alarm_time)
                del alarm_active[alarm_time] 
                update_alarm_list()
                alarm_list.delete(selected_index)  
                messagebox.showinfo("Alarma Eliminada", f"Alarma para las {alarm_time} ha sido eliminada.")
            else:
                messagebox.showwarning("Error", "No se pudo encontrar la alarma para eliminar.")
    else:
        messagebox.showwarning("Selección", "Por favor, selecciona una alarma para eliminar.")

def update_alarm_list():
    alarm_list.delete(0, tk.END)
    for alarm in alarms:
        alarm_list.insert(tk.END, alarm)

def show_alarm_list():
    alarm_window = tk.Toplevel(root)
    alarm_window.title("Alarmas Configuradas")
    alarm_window.geometry("300x200")
    alarm_window.configure(bg='#1e1e1e')
    
    listbox = tk.Listbox(alarm_window, font=('Orbitron', 15), bg='#2e2e2e', fg='white', borderwidth=0)
    listbox.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
    
    for alarm in alarms:
        listbox.insert(tk.END, alarm)

    delete_button = tk.Button(alarm_window, text="Eliminar Alarma", font=('Orbitron', 15), command=lambda: delete_alarm(listbox), bg='red', fg='white', padx=20, pady=10)
    delete_button.pack(pady=10)

def on_key_press(event):
    text = alarm_entry.get()
    if len(text) == 2 and text.isdigit():
        alarm_entry.insert(tk.END, ":")
    elif len(text) > 5:
        alarm_entry.delete(5, tk.END) 

root.geometry("600x500")
root.configure(bg='#1e1e1e')

time_label = tk.Label(root, font=('Orbitron', 60, 'bold'), background='#1e1e1e', foreground='cyan', padx=20, pady=20)
time_label.pack(pady=(20, 10))

date_label = tk.Label(root, font=('Orbitron', 20), background='#1e1e1e', foreground='white', padx=20, pady=10)
date_label.pack(pady=(0, 20))

alarm_frame = tk.Frame(root, bg='#1e1e1e')
alarm_frame.pack(pady=20)

alarm_label = tk.Label(alarm_frame, text="Configurar Alarma (HH:MM):", font=('Orbitron', 15), bg='#1e1e1e', fg='white')
alarm_label.pack()

alarm_entry = tk.Entry(alarm_frame, font=('Orbitron', 20), width=10)
alarm_entry.pack(pady=10)


alarm_entry.bind('<KeyRelease>', on_key_press)

set_alarm_button = tk.Button(alarm_frame, text="Agregar Alarma", font=('Orbitron', 15), command=set_alarm, bg='cyan', fg='black', padx=20, pady=10)
set_alarm_button.pack(pady=10)

view_alarm_button = tk.Button(root, text="Ver Alarmas", font=('Orbitron', 15), command=show_alarm_list, bg='green', fg='black', padx=20, pady=10)
view_alarm_button.pack(pady=10)

alarm_list = tk.Listbox(root, font=('Orbitron', 15), bg='#2e2e2e', fg='white', width=20, height=6, borderwidth=0)
alarm_list.pack(pady=20)

update_time()

root.bind('<KeyPress-d>', lambda event: delete_alarm(alarm_list))

root.mainloop()
