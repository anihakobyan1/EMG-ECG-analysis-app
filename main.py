from tkinter import *
import serial
# import serial.tools.list_ports
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
from connect import open_new_window

# Set up the main Tkinter window
root = Tk()
root.geometry('1100x1000')

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


# Create a frame to hold the other labels
frame_self_info = Frame(root)
frame_self_info.grid(row=0, column=0, sticky='nsew')  # Use grid to place it in row 0

# Create and place the first label at the top of the root window
name_label = Label(frame_self_info, text='Информация о разработке',
                   borderwidth=1, relief="solid", justify='left', font=('Helvetica', 14))
name_label.grid(row=0, column=0, columnspan=3, sticky='nsew')  # Use grid to place it in row 0

# Create and place the other labels in the frame
name_label1 = Label(frame_self_info, text='Название \n образовательной \n программы',
                     borderwidth=1, relief="solid", justify='left', font=('Helvetica', 14))
name_label1.grid(row=1, column=0, sticky='nsew')

name_label2 = Label(frame_self_info, text='Проектирование \n нейроинтерфейсов',
                     borderwidth=1, relief="solid", font=('Helvetica', 14))
name_label2.grid(row=1, column=1, sticky='nsew')

place_label = Label(frame_self_info, text='Рабочее место №__ \n',
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
output_frame.grid(row=1, column=0, sticky='nsew')  # Use grid to place it in row 1

# EKG Frame
ekg_frame = Frame(output_frame, highlightbackground="black", highlightthickness=1)
ekg_frame.grid(row=0, column=0, sticky='nsew')
ekg_label1 = Label(ekg_frame, text='Выполнить подключение электродов для \nисследования ЭКГ согласно примеру:', font=('Helvetica', 14))
ekg_label1.pack()
ekg_label2 = Label(ekg_frame, text='Пульс не определен проверьте подключение', font=('Helvetica', 14))
ekg_label2.pack()
test_button = Button(ekg_frame, text='Новое окно', command=open_new_window)
test_button.pack()

# EMG Frame
emg_frame = Frame(output_frame, highlightbackground="black", highlightthickness=1)
emg_frame.grid(row=1, column=0, sticky='nsew')
emg_label1 = Label(emg_frame, text='Выполнить подключение электродов для \nисследования ЭМГ согласно примеру:', font=('Helvetica', 14))
emg_label1.pack()
emg_label2 = Label(emg_frame, text='Пульс не определен проверьте подключение', font=('Helvetica', 14))
emg_label2.pack()

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
root.grid_columnconfigure(0, weight=1)  # This column should expand to fill the horizontal space



try:
    # Set up the plot for EMG
    active_ports = get_active_ports()
    if active_ports:
        ser = serial.Serial(active_ports[0], baudrate=115200)
    matplotlib.use('TkAgg')  # Use TkAgg backend
    plt.style.use('ggplot')
    fig_emg, ax_emg = plt.subplots(figsize=(3, 3))
    xdata = np.arange(0, 100)  # X-axis data (time)
    ydata_emg = np.zeros(100)  # Initialize Y-axis data (EMG values)
    line_emg, = ax_emg.plot(xdata, ydata_emg, color='r')
    ax_emg.set_ylim(0, 255)
    ax_emg.set_xlim(0, 100)
    ax_emg.set_ylabel('Напряжение (мВ)')
    ax_emg.set_title('График ЭМГ')

    matplotlib.use('TkAgg')  # Use TkAgg backend
    plt.style.use('ggplot')
    fig_ecg, ax_ecg = plt.subplots(figsize=(3, 3))
    xdata = np.arange(0, 100)  # X-axis data (time)
    ydata_ecg = np.zeros(100)  # Initialize Y-axis data (EMG values)
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

    is_ready_emg = False
    is_ready_ecg = False


    # Update function for animation
    def update(frame):
        global ydata_emg
        global ydata_ecg
        global is_ready_emg
        global is_ready_ecg

        if ser.in_waiting > 0:
            line_data = ser.readline().decode('utf-8').rstrip()  # Read a line from the serial
            try:
                emg_value, ecg_value = map(float, line_data.split('_'))  # Convert to float
                ydata_emg = np.append(ydata_emg[1:], emg_value)  # Shift data and append new value
                ydata_ecg = np.append(ydata_ecg[1:], ecg_value)  # Shift data and append new value
                line_emg.set_ydata(ydata_emg)  # Update the line data
                line_ecg.set_ydata(ydata_ecg)  # Update the line data

                # Check EMG value
                if np.all(ydata_emg[1:100] > 60) and np.all(ydata_emg[1:100] < 200):
                    emg_label2.config(text='Пульс определен, перейдите к подключению \nэлектродов для исследования ЭМГ')
                    is_ready_emg = True
                else:
                    emg_label2.config(text='Пульс не определен, проверьте подключение')
                    is_ready_emg = False  # Reset if condition is not met

                # Check ECG value
                if np.all(ydata_ecg[1:100] > 5) and np.all(ydata_ecg[1:100] < 200):
                    ekg_label2.config(text='Пульс определен, перейдите к подключению \nэлектродов для исследования ЭКГ')
                    is_ready_ecg = True
                else:
                    ekg_label2.config(text='Пульс не определен, проверьте подключение')
                    is_ready_ecg = False  # Reset if condition is not met

                # Check if both conditions are met
                if is_ready_emg == False or is_ready_ecg == False:
                    open_new_window()  # Call the function to open the new window
                    root.destroy()
            except ValueError:
                pass  # Ignore any lines that cannot be converted to float

        ser.reset_input_buffer()
        return line_emg, line_ecg


    ani_emg = FuncAnimation(fig_emg, update, blit=True, interval=50, cache_frame_data=False)  # Update every 50 ms
    ani_ecg = FuncAnimation(fig_ecg, update, blit=True, interval=50, cache_frame_data=False)  # Update every 50 ms

    # # Start the Tkinter main loop
    root.protocol("WM_DELETE_WINDOW", lambda: (ser.close(), root.destroy()))  # Close serial on exit
except:
    print('Порт не найден')
    # exit()



root.mainloop()




