from tkinter import *
import serial
import serial.tools.list_ports
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
from datetime import datetime

# Global variables
min_value_emg = 0
max_value_emg = 0
mean_value_emg = 0
min_value_ecg = 0
max_value_ecg = 0
mean_value_ecg = 0

emg_data = []
ecg_data = []

is_ready_emg = False
is_ready_ecg = False
add_called = False  # Flag to ensure `add()` is called only once

def deletes():
    instruction_label.destroy()
    frame_ilustr_ekg.destroy()
    frame_ilustr_emg.destroy()
    emg_label2.destroy()
    emg_label1.destroy()
    ekg_label2.destroy()

def create_csv():
    global min_value_emg, max_value_emg, mean_value_emg
    global min_value_ecg, max_value_ecg, mean_value_ecg
    file_path = r'C:\Users\Hp\Desktop\Нейро\info_csv.csv'
    fio = name_entry.get()
    name_entry.delete(0, END)
    age = age_entry.get()
    age_entry.delete(0, END)
    with open(file_path, 'a') as file:
        current_datetime = datetime.now()
        formatted_date = current_datetime.strftime('%Y-%m-%d')
        hour_data = current_datetime.strftime('%H:%M:%S')
        file.write(f'\n{fio},{age},{formatted_date},{hour_data},{min_value_emg},{mean_value_emg},{max_value_emg},'
                   f'{min_value_ecg},{mean_value_ecg},{max_value_ecg}\n')

def add():
    global ekg_min_label, ekg_max_label, ekg_sr_label, emg_min_label, emg_max_label, emg_sr_label
    global canvas1, canvas2, ani_emg, ani_ecg, add_called, info_label2, name_entry, age_entry
    root.geometry("1600x1000")

    # Ensure `add()` is called only once
    if add_called:
        return
    add_called = True

    # Stop old animations
    if 'ani_emg' in globals() and ani_emg is not None:
        ani_emg.event_source.stop()
    if 'ani_ecg' in globals() and ani_ecg is not None:
        ani_ecg.event_source.stop()

    # Destroy old canvases
    if 'canvas1' in globals() and canvas1 is not None:
        canvas1.get_tk_widget().destroy()
    if 'canvas2' in globals() and canvas2 is not None:
        canvas2.get_tk_widget().destroy()

    deletes()

    # Add operator information widgets
    info_oper = Label(frame_self_info, text='Информация о операторе',
                      borderwidth=1, relief="solid",
                      justify='left', font=('Helvetica', 14))
    info_oper.grid(row=0, column=3, sticky='nsew')

    fio_input_fr = Frame(frame_self_info, borderwidth=1, relief="solid")
    fio_input_fr.grid(row=1, column=3, sticky='nsew')

    name_label = Label(fio_input_fr, text='ФИО ', font=('Helvetica', 12))
    name_label.grid(row=0, column=0, sticky='nsew')

    name_entry = Entry(fio_input_fr)
    name_entry.grid(row=0, column=1)

    age_label = Label(fio_input_fr, text='Возраст ', font=('Helvetica', 12))
    age_label.grid(row=1, column=0, sticky='nsew')

    age_entry = Entry(fio_input_fr)
    age_entry.grid(row=1, column=1)

    save_button = Button(fio_input_fr, text='Записать', command=create_csv)
    save_button.grid(row=2, column=1, sticky='nsew')

    frame_self_info.grid_columnconfigure(0, weight=1)
    frame_self_info.grid_columnconfigure(1, weight=1)
    frame_self_info.grid_columnconfigure(2, weight=1)
    frame_self_info.grid_columnconfigure(3, weight=1)

    # Update EKG frame
    frame_ilustr_ekg = Frame(ekg_frame, highlightbackground="black", highlightthickness=1)
    frame_ilustr_ekg.grid(row=0, column=0, padx=10, pady=10)
    ekg_min_label = Label(ekg_frame, text='Мин. значение: ', font=('Helvetica', 12))
    ekg_min_label.grid(row=1, column=0, sticky='nsw', padx=10)
    ekg_sr_label = Label(ekg_frame, text='Ср. значение: ', font=('Helvetica', 12))
    ekg_sr_label.grid(row=2, column=0, sticky='nsw', padx=10)
    ekg_max_label = Label(ekg_frame, text='Макс. значение: ', font=('Helvetica', 12))
    ekg_max_label.grid(row=3, column=0, sticky='nsw', padx=10)

    # Update EMG frame
    emg_frame = Frame(output_frame, highlightbackground="black", highlightthickness=1)
    emg_frame.grid(row=0, column=1, sticky='nsew')
    frame_ilustr_emg = Frame(emg_frame, highlightbackground="black", highlightthickness=1)
    frame_ilustr_emg.grid(row=0, column=0, padx=10, pady=10)

    emg_min_label = Label(emg_frame, text='Мин. значение: ', font=('Helvetica', 12))
    emg_min_label.grid(row=1, column=0, sticky='nw', padx=10)
    emg_sr_label = Label(emg_frame, text='Ср. значение: ', font=('Helvetica', 12))
    emg_sr_label.grid(row=2, column=0, sticky='nw', padx=10)
    emg_max_label = Label(emg_frame, text='Макс. значение: ', font=('Helvetica', 12))
    emg_max_label.grid(row=3, column=0, sticky='nw', padx=10)

    info_frame = Frame(output_frame, highlightbackground="black", highlightthickness=1)
    info_frame.grid(row=1, columnspan=2, sticky='nsew')
    info_label2 = Label(info_frame, text='Пульс отсутствует', font=('Helvetica', 16), anchor='center')
    info_label2.grid(row=1, sticky='nsew')
    info_frame.grid_columnconfigure(0, weight=1)
    # info_frame.grid_rowconfigure(0, weight=1)

    video_frame = Frame(output_frame, highlightbackground="black", highlightthickness=1)
    video_frame.grid(row=0, column=2, rowspan=2, sticky='nsew')
    video_label1 = Label(video_frame, text='Видео блок', font=('Helvetica', 14))
    video_label1.grid(row=0, column=0, sticky='nsew', pady=30)
    video_block = Frame(video_frame, highlightbackground="black", highlightthickness=1, bg='white', width=400,
                        height=400)
    video_block.grid(row=1, padx=20)

    # Recreate the canvas for EMG plot
    canvas1 = FigureCanvasTkAgg(fig_emg, master=frame_ilustr_emg)
    canvas1.draw()
    canvas1.get_tk_widget().pack(fill=BOTH, expand=True)

    # Recreate the canvas for ECG plot
    canvas2 = FigureCanvasTkAgg(fig_ecg, master=frame_ilustr_ekg)
    canvas2.draw()
    canvas2.get_tk_widget().pack(fill=BOTH, expand=True)

    # Reset the data for the new plots
    global ydata_emg, ydata_ecg
    ydata_emg = np.zeros(100)  # Reset EMG data
    ydata_ecg = np.zeros(100)  # Reset ECG data
    line_emg.set_ydata(ydata_emg)  # Update the line data
    line_ecg.set_ydata(ydata_ecg)  # Update the line data

    # Restart animations
    ani_emg = FuncAnimation(fig_emg, update, blit=True, interval=50, cache_frame_data=False)
    ani_ecg = FuncAnimation(fig_ecg, update, blit=True, interval=50, cache_frame_data=False)


def get_active_ports():
    active_ports = []
    ports = serial.tools.list_ports.comports()
    for port in ports:
        try:
            ser = serial.Serial(port.device, 115200)
            active_ports.append(port.device)
            ser.close()
        except (serial.SerialException, OSError):
            continue
    return active_ports

# Set up the main Tkinter window
root = Tk()
root.geometry('1400x1000')

# Create a frame to hold the other labels
frame_self_info = Frame(root)
frame_self_info.grid(row=0, column=0, sticky='nsew')

# Create and place the first label at the top of the root window
inf_label = Label(frame_self_info, text='Информация о разработке',
                  borderwidth=1, relief="solid", justify='left', font=('Helvetica', 14))
inf_label.grid(row=0, column=0, columnspan=3, sticky='nsew')

# Create and place the other labels in the frame
prog_name_label = Label(frame_self_info, text='Название \n образовательной \n программы',
                        borderwidth=1, relief="solid", justify='left', font=('Helvetica', 14))
prog_name_label.grid(row=1, column=0, sticky='nsew')

neiro_label = Label(frame_self_info, text='Проектирование \n нейроинтерфейсов',
                    borderwidth=1, relief="solid", font=('Helvetica', 14))
neiro_label.grid(row=1, column=1, sticky='nsew')

place_label = Label(frame_self_info, text='Рабочее место №__',
                    justify='left', font=('Helvetica', 14), borderwidth=1, relief="solid")
place_label.grid(row=1, column=2, sticky='nsew')

# Configure the columns of the frame to expand equally
frame_self_info.grid_columnconfigure(0, weight=1)
frame_self_info.grid_columnconfigure(1, weight=1)
frame_self_info.grid_columnconfigure(2, weight=1)

# Create and place the instruction label below the first row
instruction_label = Label(frame_self_info, text='Инструкция для операторов',
                          font=('Helvetica', 14), borderwidth=1, relief="solid")
instruction_label.grid(row=2, column=0, columnspan=3, sticky='nsew')

# Create the output frame to hold the EKG and EMG frames
output_frame = Frame(root)
output_frame.grid(row=1, column=0, sticky='nsew')

# EKG Frame
ekg_frame = Frame(output_frame, highlightbackground="black", highlightthickness=1)
ekg_frame.grid(row=0, column=0, sticky='nsew')
ekg_label1 = Label(ekg_frame, text='Выполнить подключение электродов для \nисследования ЭКГ согласно примеру:', font=('Helvetica', 16))
ekg_label1.grid(row=0, sticky='nsew', pady=20)
ekg_label2 = Label(ekg_frame, text='Пульс не определен проверьте подключение', font=('Helvetica', 18))
ekg_label2.grid(row=1, sticky='nsew')
ekg_frame.grid_columnconfigure(0, weight=1)  # Make the column expand
# ekg_frame.grid_rowconfigure(1, weight=1)
# EMG Frame
emg_frame = Frame(output_frame, highlightbackground="black", highlightthickness=1)
emg_frame.grid(row=1, column=0, sticky='nsew')
emg_label1 = Label(emg_frame, text='Выполнить подключение электродов для \nисследования ЭМГ согласно примеру:', font=('Helvetica', 16), anchor='center')
emg_label1.grid(row=0, sticky='nsew', pady=20)
emg_label2 = Label(emg_frame, text='Пульс не определен проверьте подключение', font=('Helvetica', 18), anchor='center')
emg_label2.grid(row=1, sticky='nsew')

emg_frame.grid_columnconfigure(0, weight=1)  # Make the column expand
# Illustration Frames
frame_ilustr_ekg = Frame(output_frame, highlightbackground="black", highlightthickness=1)
frame_ilustr_ekg.grid(row=0, column=1, sticky='nsew')

frame_ilustr_emg = Frame(output_frame, highlightbackground="black", highlightthickness=1)
frame_ilustr_emg.grid(row=1, column=1, sticky='nsew')

# Configure the output frame to expand equally
output_frame.grid_columnconfigure(0, weight=1)
output_frame.grid_columnconfigure(1, weight=1)
output_frame.grid_rowconfigure(0, weight=1)
output_frame.grid_rowconfigure(1, weight=1)

# Configure the root window to expand the first row
root.grid_rowconfigure(0, weight=0)  # This row does not need to expand
root.grid_rowconfigure(1, weight=1)  # This row should expand

# Configure the root window to expand the first column
root.grid_columnconfigure(0, weight=1)

# Set up the plot for EMG
active_ports = get_active_ports()
if active_ports:
    ser = serial.Serial(active_ports[0], baudrate=9600)
else:
    print('Порт не найден')
    exit()

plt.style.use('ggplot')
fig_emg, ax_emg = plt.subplots(figsize=(2, 2))
xdata = np.arange(0, 100)  # X-axis data (time)
ydata_emg = np.zeros(100)  # Initialize Y-axis data (EMG values)
line_emg, = ax_emg.plot(xdata, ydata_emg, color='r')
ax_emg.set_ylim(0, 255)
ax_emg.set_xlim(0, 100)
ax_emg.set_ylabel('Напряжение (мВ)')
ax_emg.set_title('График ЭМГ')

fig_ecg, ax_ecg = plt.subplots(figsize=(2, 2))
ydata_ecg = np.zeros(100)  # Initialize Y-axis data (ECG values)
line_ecg, = ax_ecg.plot(xdata, ydata_ecg, color='g')
ax_ecg.set_ylim(0, 255)
ax_ecg.set_xlim(0, 100)
ax_ecg.set_ylabel('Напряжение (мВ)')
ax_ecg.set_title('График ЭКГ')

# Create a canvas to embed the plot in the Tkinter window
canvas1 = FigureCanvasTkAgg(fig_emg, master=frame_ilustr_emg)
canvas1.draw()
canvas1.get_tk_widget().pack(fill=BOTH, expand=True)

# Create a canvas to embed the plot in the Tkinter window
canvas2 = FigureCanvasTkAgg(fig_ecg, master=frame_ilustr_ekg)
canvas2.draw()
canvas2.get_tk_widget().pack(fill=BOTH, expand=True)

x = 0
def update(frame):
    global min_value_emg, max_value_emg, min_value_ecg, mean_value_ecg, mean_value_emg, max_value_ecg
    global ydata_emg, ydata_ecg, is_ready_emg, is_ready_ecg, add_called
    global emg_data, ecg_data  # Ensure we can access the data lists
    global x

    if ser.in_waiting > 0:
        line_data = ser.readline().decode('utf-8').rstrip()  # Read a line from the serial
        try:
            # Parse the serial data
            parts = line_data.split('_')
            if len(parts) == 2:
                emg_value, ecg_value = map(float, parts)
            else:
                return line_emg, line_ecg

            # Update EMG and ECG data
            ydata_emg = np.append(ydata_emg[1:], emg_value)  # Shift data and append new value
            ydata_ecg = np.append(ydata_ecg[1:], ecg_value)  # Shift data and append new value
            line_emg.set_ydata(ydata_emg / 4)  # Update the line data
            line_ecg.set_ydata(ydata_ecg / 4)  # Update the line data

            # Limit the size of emg_data and ecg_data to avoid memory overflow
            if len(emg_data) > 100:
                emg_data.pop(0)
            if len(ecg_data) > 100:
                ecg_data.pop(0)

            # Append new data
            emg_data.append(emg_value/4)
            ecg_data.append(ecg_value/4)

            match x:
                case 0:
                    # Check EMG and ECG values
                    if np.all(ydata_emg[1:100] / 4 > 5) and np.all(ydata_emg[1:100] / 4 < 220):
                        emg_label2.config(text='Пульс определен, перейдите к подключению \nэлектродов для исследования ЭМГ')
                        is_ready_emg = True
                    if np.all(ydata_ecg[1:100] / 4 > 5) and np.all(ydata_ecg[1:100] / 4 < 220):
                        ekg_label2.config(text='Пульс определен, перейдите к подключению \nэлектродов для исследования ЭКГ')
                        is_ready_ecg = True
                    if is_ready_emg or is_ready_ecg:
                        x = 1
                case 1:
                    if (is_ready_emg or is_ready_ecg) and not add_called:
                        add()

                    if len(ecg_data) >= 100:  # Ensure there are enough data points
                        if np.all(np.array(ecg_data[-100:]) > 40) and np.all(np.array(ecg_data[-100:]) < 220):
                            info_label2.config(text='Пульс в норме.', fg='green')
                        else:
                            info_label2.config(text='Пульс выходит за пределы нормы.', fg='red')
                    else:
                        info_label2.config(text='Пульс отсутствует.', fg='yellow')

                    # Calculate EMG statistics
                    if emg_data:
                        min_value_emg = int(min(emg_data))
                        max_value_emg = int(max(emg_data))
                        mean_value_emg = int(sum(emg_data) // len(emg_data))
                        emg_min_label.config(text=f'Мин. значение: {min_value_emg}')
                        emg_max_label.config(text=f'Макс. значение: {max_value_emg}')
                        emg_sr_label.config(text=f'Ср. значение: {mean_value_emg}')
                    else:
                        print("EMG data is empty.")

                    # Calculate ECG statistics
                    if ecg_data:
                        min_value_ecg = int(min(ecg_data))
                        max_value_ecg = int(max(ecg_data))
                        mean_value_ecg = int(sum(ecg_data) // len(ecg_data))
                        ekg_min_label.config(text=f'Мин. значение: {min_value_ecg}')
                        ekg_max_label.config(text=f'Макс. значение: {max_value_ecg}')
                        ekg_sr_label.config(text=f'Ср. значение: {mean_value_ecg}')
                    else:
                        print("ECG data is empty.")
        except Exception as e:
            # print(f"Ошибка при обновлении: {str(e)}")
            pass
    ser.reset_input_buffer()
    return line_emg, line_ecg

# Start animations
ani_emg = FuncAnimation(fig_emg, update, blit=True, interval=50, cache_frame_data=False)
ani_ecg = FuncAnimation(fig_ecg, update, blit=True, interval=50, cache_frame_data=False)

# Start the Tkinter main loop
root.protocol("WM_DELETE_WINDOW", lambda: (ser.close(), root.destroy()))  # Close serial on exit
root.mainloop()