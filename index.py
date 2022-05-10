from tkinter import *
from tkinter import filedialog as FileDialog
import matplotlib.pyplot as plt
import math
import json


# |------------------------------|
#  CORE | functions and variables
# |------------------------------|

data = []
numbers = []
ruta = ""


def insert_number():
    num = selected_number.get()
    if num != "":
        try:
            numbers.append(int(num))
            numbers.sort()
            list_n.set(str(numbers))
        except:
            mensaje.set("you can't insert letters")
    else:
        mensaje.set("please insert a number")
    selected_number.set("")


def delete_numbers():
    numbers.clear()
    list_n.set(str(numbers))


def create_graph():
    try:
        sample_length = len(numbers)
        lower_number = numbers[0]
        bigger_number = numbers[-1]
        range = bigger_number - lower_number
        interval_count = math.sqrt(sample_length)
        interval_count = math.ceil(interval_count)
        amplitude = range / interval_count
        intervals = []
        actual_number = lower_number
        while len(intervals) <= interval_count:
            intervals.append(actual_number)
            actual_number = actual_number + amplitude
            intervals.sort()
        plt.hist(numbers, intervals, histtype="bar", rwidth=0.8)
        plt.xlabel(selected_x_axis.get())
        plt.ylabel(selected_y_axis.get())
        plt.title(selected_name.get())
        plt.show()
    except IndexError:
        mensaje.set("you can't create an empty graph")
    except:
        mensaje.set("an error ocurred")


def create_list():
    save_table = FileDialog.asksaveasfile(
        title="save file as", mode="w", defaultextension=".txt")
    if save_table is not None:
        ruta = save_table.name
        contenido = str(numbers) + "\n" + selected_name.get() + "\n" + \
            selected_x_axis.get() + "\n" + selected_y_axis.get()  # /n == salto de linea
        save_table = open(ruta, "w+", encoding="utf8")
        save_table.write(contenido)
        save_table.close()


def read_list():
    mensaje.set("abrir fichero")
    ruta = FileDialog.askopenfilename(
        initialdir=".",
        filetype=(("ficheros de texto", "*.txt"),),
        title="open a frequency table data")

    if ruta != "":
        fichero = open(ruta, "r", encoding="utf8")
        contenido = fichero.read()
        contenido = contenido.split("\n")
        print(contenido)
        received_list = contenido[0]
        received_title = contenido[1]
        received_x = contenido[2]
        received_y = contenido[3]
        selected_name.set(received_title)
        selected_x_axis.set(received_x)
        selected_y_axis.set(received_y)
        received_list = json.loads(received_list)
        for c in received_list:
            c = int(c)
        numbers.clear()
        for c in received_list:
            numbers.append(c)
        list_n.set(str(numbers))
        fichero.close()
        root.title(ruta + "opened table data")
        create_graph()


# |-------------------------------|
# |------------ UI ---------------|
# |-------------------------------|
# root
root = Tk()
root.title("frequency table generator")
root.iconbitmap('OwO.ico')

# menu
menubar = Menu(root)
root.config(menu=menubar)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open a data list", command=read_list)
filemenu.add_command(label="Save data", command=create_list)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(menu=filemenu, label="File")

# title
label = Label(root, text="frequency table generator")
label.pack(anchor="center")
label.config(fg="#3498db", font=("Arial Bold", 24))


# entry
Label(root, text="insert numbers").pack()
selected_number = StringVar()
enter_entry = Entry(root, justify="center",
                    textvariable=selected_number).pack()


# buttons 1
list_n = StringVar()
list_n.set(str(numbers))
Label(root, textvariable=list_n).pack()
Button(root, text="enter number", command=insert_number).pack()
Button(root, text="reset numbers", command=delete_numbers).pack()
Label(root, text="---------------------------------------------").pack()


# table config

Label(root, text="configure the frequency table").pack()

selected_name = StringVar()
selected_x_axis = StringVar()
selected_y_axis = StringVar()

Label(root, text="title").pack()
name_entry = Entry(root, justify="center", textvariable=selected_name).pack()
Label(root, text="x axis' title").pack()
x_entry = Entry(root, justify="center", textvariable=selected_x_axis).pack()
Label(root, text="y axis' title").pack()
y_entry = Entry(root, justify="center", textvariable=selected_y_axis).pack()

# buttons 2
Button(root, text="create table", command=create_graph).pack()

# monitor inferior
mensaje = StringVar()
mensaje.set("Hi again")
monitor = Label(root, textvar=mensaje, justify="left")
monitor.pack(side="left")


# loop
root.mainloop()


# dedicated to the memory of JuanDi
