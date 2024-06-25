import os
import pandas as pd
from tkinter import Tk, Button, Label, Toplevel, PhotoImage, \
                    filedialog, messagebox, Entry, IntVar
from additional.constants import sign, sections
from preparation.data_preparation import prepare_data, save_data_csv
from statystical_analysis.data_analysis import data_analysis
from graphical_visualization.heatmap_cleaned import draw_heatmap_for_file
from ai.AlgorithmAI import train_algorithm, write_data_into_file, filter_data, \
                           read_data_from_file, plot_group_of_points, \
                           plot_points_from_new_data_with_all_points

root = Tk()
root.geometry("1280x720")
root.title("Track Record analysis")
image_path = r"assets/12-5-scaled-1920x1080.png"

bg_image = PhotoImage(file=image_path)
bg_image_set = Label(root, image=bg_image)
bg_image_set.place(relheight=1, relwidth=1)

no_of_sec = len(sections.keys())


#########################  FUNCITONS USED IN PROGRAM   #########################


def ensure_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def show_loading_window():
    loading_window = Toplevel(root)
    loading_window.title("Loading")
    loading_window.geometry("200x100")
    loading_window.attributes("-topmost", True)
    loading_label = Label(loading_window, 
                          text="Processing...", 
                          font=('Georgia', 15))
    loading_label.pack(pady=20)
    return loading_window

def clean_file():
    root.update()
    x = filedialog.askopenfilename()
    loading_window = show_loading_window()
    root.update()
    race_info, file_object = prepare_data(x, verbose=True)
    save_directory = os.path.dirname(x)
    save_data_csv(file_object, race_info, save_directory)
    loading_window.destroy()
    print("File has been processed!")

def analyze_file():
    root.update()
    x = filedialog.askopenfilename()
    loading_window = show_loading_window()
    root.update()
    log_date, log_time, sth, st2 = x.split("/")[-1].split("_")
    save_directory = os.path.dirname(x)
    data_analysis(x, save_directory, log_date, log_time)
    loading_window.destroy()
    std_file = list(filter(lambda x: x.endswith("_std_each_section.csv"), 
                           os.listdir("./files")))[0]
    messagebox.showinfo("File analysis completed",
                        "File has been analyzed. Evaluations are stored in " +
                        "the same folder as the selected file - now the " +
                        "program will display a heatmap of Standard " +
                        "Deviation of time for each section")
    draw_heatmap_for_file(f"files/{std_file}")
    print("File has been processed!")

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

def __name_from_user(allowed):
    global root

    text_var = ""

    def on_submit():
        nonlocal text_var
        text_var = entry.get()
        popup.destroy()

    # Create a popup window
    popup = Toplevel(root)
    popup.title("Enter a Number")

    possible = "Enter the names of columns separated with a comma" + "\n" + \
                "\n".join(allowed)

    Label(popup, text=possible).pack(pady=10)

    entry = Entry(popup)
    entry.pack(pady=5)

    submit_button = Button(popup, text="Submit", command=on_submit)
    submit_button.pack(pady=10)

    error_label = Label(popup, text="", fg="red")
    error_label.pack()

    popup.wait_window(popup)  # Wait here until popup is destroyed
    return text_var

def __show_one_specific_graph_with_points():

    selected_columns_data = ['Section', 'Time', 'Time_on_lap', 'STEERANGLE', \
                        'THROTTLE','RPMS', 'G_LAT', 'G_LON', 'SPEED', 'BRAKE', \
                        'LAP_BEACON', "Distance", "Distance_on_lap"]
    allowed_columns = ['Time_on_lap', 'STEERANGLE', 'THROTTLE', 
                        'SPEED', 'BRAKE', 'Distance', 'Distance_on_lap']
    grbycol = ['LAP_BEACON']

    Tk().withdraw()
    csv_file_path = filedialog.askopenfilename()  # Replace with your file path
    if csv_file_path == "": exit()
    
    dir = os.curdir + sign + "graphs_for_section"
    selected_section = None
    default_columns = ["Time_on_lap", "SPEED"]
    selected_columns = []

    # Selection of specific section
    while selected_section == None:
        Tk().withdraw()
        selected_section = __get_number_from_user()
        if selected_section < 0 or selected_section > no_of_sec:
            output = messagebox.askyesno("Incorrect number",
                                f"Value outside range 1 - {no_of_sec}!\n" +
                                " Do you want to retry selecting directory?",
                                parent = root)

            if output == False: return
            selected_section = None

    # Selection of columns
    while selected_columns == []:
        Tk().withdraw()
        ans = __name_from_user(allowed_columns)
        if ans.strip() == "":
            selected_columns = default_columns
        else:
            values = ans.strip().split(",")
            for v in values:
                for o in allowed_columns:
                    if v.strip().lower() == o.lower():
                        selected_columns.append(o)
            if selected_columns == []:
                output = messagebox.askyesno("Wrong column names",
                                "The columsn which you provided are not " +
                                "listed! Do you want to put names again? "+
                                "(letter size matters)",
                                parent = root)
                if output == False:
                    selected_columns = default_columns
                    break
            if len(selected_columns) < 2:
                selected_columns.append("SPEED")

    # Assing choosen columns
    col1 = selected_columns[0]
    col2 = selected_columns[1]

    processing_option = {
        'SPEED' : 'average',
        'Time_on_lap' : 'last',
        'Distance' : 'none',
        'Distance_on_lap' : 'none',
        'BRAKE' : 'none',
        'STEERANGLE' : 'highiest',
        'THROTTLE' : 'average'
    }

    col1_proc = processing_option[col1]
    col2_proc = processing_option[col2]

    concat_file = pd.read_csv("./ai/concatenated.csv")

    agg_data, kmeans = train_algorithm(concat_file,
                                       selected_section,
                                       col1 = col1,
                                       col2 = col2,
                                       col1_process = col1_proc,
                                       col2_process = col2_proc)

    data = pd.read_csv(csv_file_path, usecols = selected_columns_data)
    data_to_compare = filter_data(data, selected_section, 
                                  grbycol,
                                  col1 = col1,
                                  col2 = col2,
                                  col1_process = col1_proc,
                                  col2_process = col2_proc)

    dtc_x = data_to_compare[col1]
    dtc_y = data_to_compare[col2]

    plot_points_from_new_data_with_all_points(dtc_x, dtc_y, "red", 130, 
                                              agg_data,
                                              kmeans,
                                              selected_section,
                                              col1,
                                              col2)


########################   GUI SETUP AND ARRANGEMENT   ########################


app_header = Label(root, 
                  height=1, 
                  width=20, 
                  text="Track Record analysis", 
                  font=('Georgia', 60))
app_header.pack(pady=30)

T = Label(root, 
          bg='tan', 
          height=10, 
          width=40, 
          font=('Georgia', 15),
          text="Welcome! \n\n Instructions: \n\n 1. Open ACC file in "+\
               "motec \n 2. Export file as CSV \n 3. Use  <Clean File> "+\
               "and select said CSV file \n 4. Analyze clean file")
T.place(x=150, y=200)

Button1 = Button(root, 
                 height=1, 
                 width=30, 
                 text="Clean file", 
                 font=('Georgia', 20),
                 bg='lightskyblue',
                 command=clean_file)
Button1.place(x=700, y=200)

Button2 = Button(root, 
                 height=1,
                 width=30, 
                 text="Analyze clean file (consistency)", 
                 font=('Georgia', 20), 
                 bg='lightskyblue',
                 command=analyze_file)
Button2.place(x=700, y=280)

Button3 = Button(root, 
                 height=1,
                 width=30, 
                 text="Analyze clean file (clusterring)", 
                 font=('Georgia', 20), 
                 bg='lightskyblue',
                 command=__show_one_specific_graph_with_points)
Button3.place(x=700, y=360)

Button5 = Button(root, 
                 height=1, 
                 width=20, 
                 text="Exit", 
                 font=('Georgia', 30), 
                 bg='tomato', 
                 command=quit)
Button5.place(x=700, y=500)

root.mainloop()