import os
import pandas as pd
from additional.additional_commands import *
from additional.constants import sign, sections
from tkinter import Tk, Button, Label, Toplevel, PhotoImage, \
                    filedialog, messagebox, Entry, IntVar
from ai.AlgorithmAI import train_algorithm, write_data_into_file, \
                           read_data_from_file, plot_group_of_points


####################  GUI WINDOW CREATION AND CONTSTANTS   ####################


# Constants for windows setup

btnH = 1
btnW = 20
font1 = ('Georgia', 30)
font2 = ('Georgia', 60)
font3 = ('Georgia', 15)

no_of_sec = len(sections.keys())

# Main window

root = Tk()
root.geometry("1280x720")
root.title("Track Record analysis")
image_path = r"assets/12-5-scaled-1920x1080.png"

bg_image = PhotoImage(file=image_path)
bg_image_set = Label(root, image=bg_image)
bg_image_set.place(relheight=1, relwidth=1)


#########################  FUNCITONS USED IN PROGRAM   #########################


def __ensure_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def __verify_graphs_exist(directory, file_no):
    files = list(os.walk(directory))[0][2]
    filtered_files = list(filter(lambda x: x.endswith(".pickle"), files))
    
    return f"ai_data_{file_no}.pickle" in filtered_files


def __show_loading_window():
    loading_window = Toplevel(root)
    loading_window.title("Loading")
    loading_window.geometry("200x100")
    loading_window.attributes("-topmost", True)
    loading_label = Label(loading_window, 
                          text = "Processing...", 
                          font = font3)
    loading_label.pack(pady = 20)
    return loading_window


def __get_number_from_user():
    global root

    number_var = IntVar()
    number_var.set(None)

    def on_submit():
        try:
            number = int(entry.get())
            number_var.set(number)
            popup.destroy()
        except ValueError:
            error_label.config(text="Please enter a valid number")

    # Create a popup window
    popup = Toplevel(root)
    popup.title("Enter a Number")

    Label(popup, text="Please enter a number:").pack(pady=10)

    entry = Entry(popup)
    entry.pack(pady=5)

    submit_button = Button(popup, text="Submit", command=on_submit)
    submit_button.pack(pady=10)

    error_label = Label(popup, text="", fg="red")
    error_label.pack()

    popup.wait_window(popup)  # Wait here until popup is destroyed
    return number_var.get()


def __generate_new_ai_graphs():

    global root
    global no_of_sec

    cdir = os.curdir
    fol_for_data = cdir + sign + "graphs_for_section"
    __ensure_directory(fol_for_data)

    selected_file = ""

    while not selected_file:
        Tk().withdraw()
        selected_file = filedialog.askopenfilename(initialdir = cdir)
        if not selected_file:
            output = messagebox.askyesno("No directory selected !",
                                "Do you want to retry selecting directory?",
                                parent = root)

            if output == False: break
    
    df = None

    try:
        df = pd.read_csv(selected_file)
    except Exception as e:
        messagebox.showerror("Reading csv failed",
                            f"File which you selected ({selected_file}) " +
                            f"created this error - {e}")
        return
    
    
    for section in range(1, no_of_sec + 1):
        aggregated_data, kmeans = train_algorithm(df, section)
        write_data_into_file(fol_for_data,
                             f"ai_data_{section}.pickle",
                             aggregated_data,
                             kmeans)

    messagebox.showinfo("Processing status", "All section have beeen processed")

    return


def __show_one_specific_graph():
    
    dir = os.curdir + sign + "graphs_for_section"

    selected_section = None

    while selected_section == None:
        Tk().withdraw()
        selected_section = __get_number_from_user()
        if selected_section == None:
            output = messagebox.askyesno("No directory selected !",
                                "Do you want to retry selecting directory?",
                                parent = root)

            if output == False: return
        if selected_section < 0 or selected_section > no_of_sec:
            output = messagebox.askyesno("Incorrect number",
                                f"Value outside range 1 - {no_of_sec}!\n" +
                                " Do you want to retry selecting directory?",
                                parent = root)

            if output == False: return
            selected_section = None            

    sel_file = dir + sign + f"ai_data_{selected_section}.pickle"
    agg_data, kmeans = read_data_from_file(sel_file)

    plot_group_of_points(agg_data, kmeans, selected_section)


########################   GUI SETUP AND ARRANGEMENT   ########################

# Buttons and elements inside window

app_header = Label(root, 
                  height = btnH, 
                  width = btnW, 
                  text = "Track Record AI Analysis", 
                  font = font2)

T = Label(root, 
          bg = 'tan', 
          height = 10, 
          width = 40, 
          font = font3,
          text = "This program allows for update and ")

Button1 = Button(root, 
                 height = btnH, 
                 width = btnW, 
                 text = "Do analysis for all section", 
                 font = font1,
                 bg = 'lightskyblue',
                 command = __generate_new_ai_graphs)

Button2 = Button(root, 
                 height = btnH, 
                 width = btnW, 
                 text = "Show graph for one section", 
                 font = font1,
                 bg = 'lightskyblue',
                 command = __show_one_specific_graph)

Button5 = Button(root, 
                 height = btnH, 
                 width = btnW, 
                 text="Exit", 
                 font = font1,
                 bg = 'tomato', 
                 command = quit)

# App arangement

app_header.pack(pady=30)
T.place(x=150, y=200)
Button1.place(x=700, y=200)
Button2.place(x=700, y=280)
Button5.place(x=700, y=500)

root.mainloop()

exit()