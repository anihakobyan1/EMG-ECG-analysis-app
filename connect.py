from tkinter import *
import serial
import serial.tools.list_ports
import numpy as np
from datetime import datetime
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation

# Global variables for EMG and ECG statistics
min_value_emg = 0
max_value_emg = 0
mean_value_emg = 0
min_value_ecg = 0
max_value_ecg = 0
mean_value_ecg = 0
emg_data = []
ecg_data = []
age = 0  # Initialize age globally

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

def open_new_window():
    global age  # Declare age as global
    window = Toplevel()
    window.geometry('1300x800')
    window.title('Информация о разработке')

    # Create a frame to hold the other labels
    frame_self_info = Frame(window)
    frame_self_info.grid(row=0, column=0, sticky='nsew')

    # Create and place labels and entry widgets
    info_razrab = Label(frame_self_info, text='Информация о разработке', borderwidth=1, relief="solid",
                        justify='left', font=('Helvetica', 14))
    info_razrab.grid(row=0, column=0, columnspan=3, sticky='nsew')

    info_oper = Label(frame_self_info, text='Информация о операторе',
                      borderwidth=1, relief="solid",
                      justify='left', font=('Helvetica', 14))
    info_oper.grid(row=0, column=3, sticky='nsew')

    prog_name_label = Label(frame_self_info, text='Название \n образовательной \n программы',
                            borderwidth=1, relief="solid", justify='left', font=('Helvetica', 14))
    prog_name_label.grid(row=1, column=0, sticky='nsew')

    neiro_label = Label(frame_self_info, text='Проектирование \n нейроинтерфейсов',
                        borderwidth=1, relief="solid", font=('Helvetica', 14))
    neiro_label.grid(row=1, column=1, sticky='nsew')

    place_label = Label(frame_self_info, text='Рабочее место №__',
                        justify='left', font=('Helvetica', 14), borderwidth=1, relief="solid")
    place_label.grid(row=1, column=2, sticky='nsew')

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

    def create_csv():
        global min_value_emg, max_value_emg, mean_value_emg
        global min_value_ecg, max_value_ecg, mean_value_ecg
        file_path = r'C:\Users\Hp\Desktop\Нейро\info_csv.csv'
        fio = name_entry.get()
        age = age_entry.get()
        with open(file_path, 'a') as file:
            current_datetime = datetime.now()
            formatted_date = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
            file.write(f'{fio},{age},{formatted_date},{min_value_emg},{max_value_emg},{mean_value_emg},{min_value_ecg},{max_value_ecg},{mean_value_ecg},\n')

    save_button = Button(fio_input_fr, text='Записать', command=create_csv)
    save_button.grid(row=2, column=1, sticky='nsew')

    frame_self_info.grid_columnconfigure(0, weight=1)
    frame_self_info.grid_columnconfigure(1, weight=1)
    frame_self_info.grid_columnconfigure(2, weight=1)
    frame_self_info.grid_columnconfigure(3, weight=1)

    # Create the output frame to hold the EKG and EMG frames
    output_frame = Frame(window)
    output_frame.grid(row=1, sticky='nsew')

    # EKG Frame
    ekg_frame = Frame(output_frame, highlightbackground="black", highlightthickness=1)
    ekg_frame.grid(row=0, column=0, sticky='nsew')
    ekg_label1 = Label(ekg_frame, text='График ЭКГ', font=('Helvetica', 12))
    ekg_label1.grid(row=0, column=0, sticky='nsew')
    frame_ilustr_ekg = Frame(ekg_frame, highlightbackground="black", highlightthickness=1, width=300,
                             height=200)
    frame_ilustr_ekg.grid(row=1, column=0, padx=10, pady=10)
    ekg_min_label = Label(ekg_frame, text='Мин. значение: ', font=('Helvetica', 12))
    ekg_min_label.grid(row=2, column=0, sticky='nsw', padx=10)
    ekg_sr_label = Label(ekg_frame, text='Ср. значение: ', font=('Helvetica', 12))
    ekg_sr_label.grid(row=3, column=0, sticky='nsw', padx=10)
    ekg_max_label = Label(ekg_frame, text='Макс. значение: ', font=('Helvetica', 12))
    ekg_max_label.grid(row=4, column=0, sticky='nsw', padx=10)

    # EMG Frame
    emg_frame = Frame(output_frame, highlightbackground="black", highlightthickness=1)
    emg_frame.grid(row=0, column=1, sticky='nsew')
    emg_label1 = Label(emg_frame, text='График ЭМГ', font=('Helvetica', 12), justify='center')
    emg_label1.grid(row=0, column=0, sticky='nsew')
    frame_ilustr_emg = Frame(emg_frame, highlightbackground="black", highlightthickness=1, width=300, height=200)
    frame_ilustr_emg.grid(row=1, padx=10, pady=10)

    emg_min_label = Label(emg_frame, text='Мин. значение: ', font=('Helvetica', 12))
    emg_min_label.grid(row=2, column=0, sticky='nw', padx=10)
    emg_sr_label = Label(emg_frame, text='Ср. значение: ', font=('Helvetica', 12))
    emg_sr_label.grid(row=3, column=0, sticky='nw', padx=10)
    emg_max_label = Label(emg_frame, text='Макс. значение: ', font=('Helvetica', 12))
    emg_max_label.grid(row=4, column=0, sticky='nw', padx=10)

    info_frame = Frame(output_frame, highlightbackground="black", highlightthickness=1)
    info_frame.grid(row=1, columnspan=2, sticky='nsew')
    info_label2 = Label(info_frame, text='Пульс отсутствует', font=('Helvetica', 16))
    info_label2.grid(row=1, column=0, sticky='nsew')

    video_frame = Frame(output_frame, highlightbackground="black", highlightthickness=1)
    video_frame.grid(row=0, column=2, rowspan=2, sticky='nsew')
    video_label1 = Label(video_frame, text='Видео блок', font=('Helvetica', 14))
    video_label1.grid(row=0, column=0, sticky='nsew', pady=30)
    video_block = Frame(video_frame, highlightbackground="black", highlightthickness=1, bg='white', width=400,
                        height=400)
    video_block.grid(row=1, padx=20)

    output_frame.grid_columnconfigure(0, weight=1)
    output_frame.grid_columnconfigure(1, weight=1)
    output_frame.grid_rowconfigure(0, weight=1)
    output_frame.grid_rowconfigure(1, weight=1)

    window.grid_rowconfigure(0, weight =0)  # This row does not need to expand
    window.grid_rowconfigure(1, weight=1)  # This row should expand

    window.grid_columnconfigure(0, weight=1)

    # Initialize global variables for EMG and ECG data
    global min_value_emg, max_value_emg, mean_value_emg
    global min_value_ecg, max_value_ecg, mean_value_ecg
    min_value_emg = 0
    max_value_emg = 0
    mean_value_emg = 0
    min_value_ecg = 0
    max_value_ecg = 0
    mean_value_ecg = 0

    emg_data = []
    ecg_data = []

    # Serial port setup
    active_ports = get_active_ports()
    if active_ports:
        global ser
        ser = serial.Serial(active_ports[0], baudrate=115200)
    else:
        print('Порт не найден')

    # Set up the plot for EMG
    fig_emg, ax_emg = plt.subplots(figsize=(3, 3))
    xdata = np.arange(0, 100)
    ydata_emg = np.zeros(100)
    line_emg, = ax_emg.plot(xdata, ydata_emg, color='r')
    ax_emg.set_ylim(0, 255)
    ax_emg.set_xlim(0, 100)
    ax_emg.set_ylabel('Напряжение (мВ)')

    # Set up the plot for ECG
    fig_ecg, ax_ecg = plt.subplots(figsize=(3, 3))
    ydata_ecg = np.zeros(100)
    line_ecg, = ax_ecg.plot(xdata, ydata_ecg, color='g')
    ax_ecg.set_ylim(0, 255)
    ax_ecg.set_xlim(0, 100)
    ax_ecg.set_ylabel('Напряжение (мВ)')

    # Create a canvas to embed the plot in the Tkinter window
    canvas1 = FigureCanvasTkAgg(fig_emg, master=frame_ilustr_emg)
    canvas1.draw()
    canvas1.get_tk_widget().pack(fill=BOTH, expand=True)

    canvas2 = FigureCanvasTkAgg(fig_ecg, master=frame_ilustr_ekg)
    canvas2.draw()
    canvas2.get_tk_widget().pack(fill=BOTH, expand=True)

    def update(frame):
        global ydata_emg, ydata_ecg
        global min_value_emg, max_value_emg, mean_value_emg
        global min_value_ecg, max_value_ecg, mean_value_ecg
        if ser.in_waiting > 0:
            line_data = ser.readline().decode('utf-8').rstrip()
            try:
                emg_value, ecg_value = map(float, line_data.split('_'))
                ydata_emg = np.append(ydata_emg[1:], emg_value)
                ydata_ecg = np.append(ydata_ecg[1:], ecg_value)
                line_emg.set_ydata(ydata_emg)
                line_ecg.set_ydata(ydata_ecg)
                emg_data.append(emg_value)
                ecg_data.append(ecg_value)

                # Update pulse information
                if 40 < ecg_value < 220 - age:
                    info_label2.config(text='Пульс в норме.')
                elif ecg_value == 0:
                    info_label2.config(text='Пульс отсутствует.')
                else:
                    info_label2.config(text='Пульс выходит за пределы нормы.')

                # Calculate EMG statistics
                if emg_data:
                    min_value_emg = int(min(emg_data))
                    max_value_emg = int(max(emg_data))
                    mean_value_emg = int(sum(emg_data) // len(emg_data))
                    emg_min_label.config(text=f'Мин. значение: {min_value_emg}')
                    emg_max_label.config(text=f'Макс. значение: {max_value_emg}')
                    emg_sr_label.config(text=f'Ср. значение: {mean_value_emg}')

                # Calculate ECG statistics
                if ecg_data:
                    min_value_ecg = int(min(ecg_data))
                    max_value_ecg = int(max(ecg_data))
                    mean_value_ecg = int(sum(ecg_data) // len(ecg_data))
                    ekg_min_label.config(text=f'Мин. значение: {min_value_ecg}')
                    ekg_max_label.config(text=f'Макс. значение: {max_value_ecg}')
                    ekg_sr_label.config(text=f'Ср. значение: {mean_value_ecg}')
            except ValueError:
                pass  # Ignore any lines that cannot be converted to float
        ser.reset_input_buffer()
        return line_emg, line_ecg

    # Create an animation
    ani_emg = FuncAnimation(fig_emg, update, blit=True, interval=50, cache_frame_data=False)
    ani_ecg = FuncAnimation(fig_ecg, update, blit=True, interval=50, cache_frame_data=False)

    # Start the Tkinter main loop
    window.protocol("WM_DELETE_WINDOW", lambda: (ser.close(), window.destroy()))  # Close serial on exit
    window.mainloop()

# Call the function to open the new window
