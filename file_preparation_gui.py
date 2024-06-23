import os
from tkinter import *
from tkinter import filedialog
from preparation.data_preparation import *
from additional.additional_commands import *
from statystical_analysis.data_analysis import *

root = Tk()
root.geometry("1280x720")
root.title("Track Record analysis")
image_path = r"assets/12-5-scaled-1920x1080.png"

bg_image = PhotoImage(file=image_path)
bg_image_set = Label(root, image=bg_image)
bg_image_set.place(relheight=1, relwidth=1)

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
    save_directory = os.path.join(os.path.dirname(__file__), 'files')
    ensure_directory(save_directory)
    save_data_csv(file_object, race_info, save_directory)
    loading_window.destroy()
    print("File has been processed!")

def analyze_file():
    root.update()
    x = filedialog.askopenfilename()
    loading_window = show_loading_window()
    root.update()
    log_date, log_time, sth, st2 = x.split("/")[-1].split("_")
    save_directory = os.path.join(os.path.dirname(__file__), 'files')
    ensure_directory(save_directory)
    data_analysis(x, save_directory, log_date, log_time)
    # file_get(?)
    # heatmap()
    loading_window.destroy()
    print("File has been processed!")

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
                 width=20, 
                 text="Clean file", 
                 font=('Georgia', 30),
                 bg='lightskyblue',
                 command=clean_file)
Button1.place(x=700, y=200)

Button2 = Button(root, 
                 height=1,
                 width=20, 
                 text="Analyze clean file", 
                 font=('Georgia', 30), 
                 bg='lightskyblue',
                 command=analyze_file)
Button2.place(x=700, y=300)

Button5 = Button(root, 
                 height=1, 
                 width=20, 
                 text="Exit", 
                 font=('Georgia', 30), 
                 bg='tomato', 
                 command=quit)
Button5.place(x=700, y=500)

root.mainloop()