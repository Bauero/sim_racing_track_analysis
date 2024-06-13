import tkinter
from tkinter import PhotoImage
from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
from data_preparation import *
from additional_commands import *
from tkinter import Tk
from tkinter import filedialog
from additional_commands import clean
from constants import physical_columns
from race_data_extraction_display import display_track_summary, \
                                        display_laps_summary
from File_preparation_CLI import *

root=tkinter.Tk()
root.geometry("1280x720")
root.title("Track Record analysis")
image_path=r"12-5-scaled-1920x1080.png"

bg_image=PhotoImage(file=image_path)
bg_image_set=tkinter.Label(root, image=bg_image)
bg_image_set.place(relheight=1, relwidth=1)

def openNewWindow1():
     
    # Toplevel object which will 
    # be treated as a new window
    root2 = Toplevel(root)
 
    # sets the title of the
    # Toplevel widget
    root2.title("Confirmation")
 
    # sets the geometry of toplevel
    root2.geometry("1280x720")

    bg_image2=PhotoImage(file=image_path)
    bg_image2_set=tkinter.Label(root2, image=bg_image)
    bg_image2_set.place(relheight=1, relwidth=1)

    # A Label widget to show in toplevel
    root2_app_header=tkinter.Label(root2,height= 1, width=36, text = "Track Record analysis", font=('Georgia', 60))
    root2_app_header.pack(pady=30)

def openNewWindow2():
     
    # Toplevel object which will 
    # be treated as a new window
    root2 = Toplevel(root)
 
    # sets the title of the
    # Toplevel widget
    root2.title("Confirmation")
 
    # sets the geometry of toplevel
    root2.geometry("1280x720")

    bg_image2=PhotoImage(file=image_path)
    bg_image2_set=tkinter.Label(root2, image=bg_image)
    bg_image2_set.place(relheight=1, relwidth=1)

    # A Label widget to show in toplevel
    root2_app_header=tkinter.Label(root2,height= 1, width=36, text = "Track Record analysis", font=('Georgia', 60))
    root2_app_header.pack(pady=30)

def openNewWindow3():
     
    # Toplevel object which will 
    # be treated as a new window
    root3 = Toplevel(root)
 
    # sets the title of the
    # Toplevel widget
    root3.title("Confirmation")
 
    # sets the geometry of toplevel
    root3.geometry("1280x720")

    bg_image3=PhotoImage(file=image_path)
    bg_image3_set=tkinter.Label(root3, image=bg_image)
    bg_image3_set.place(relheight=1, relwidth=1)

    root3_app_header=tkinter.Label(root3,height= 1, width=36, text = "Track Record analysis", font=('Georgia', 60))
    root3_app_header.pack(pady=30)

def clean_file():
    x = filedialog.askopenfilename()
    race_info, file_object = prepare_data(x,verbose=True)
    save_data_csv(file_object, race_info, race_info["log_date"], race_info["log_time"], "")
    save_data_csv(file_object, race_info, "")
    print("File have been processed!")

app_header=tkinter.Label(root,height= 1, width=20, text = "Track Record analysis", font=('Georgia', 60))
app_header.pack(pady=30)

T=tkinter.Label(root, bg='tan' , height=10, width=40, font=('Georgia', 15), text="Welcome! \n\n Instructions: \n\n 1. Open telemetry file in motec \n 2. Export file as CSV \n 3. Use  <Clean File> and select said CSV file \n 4. Use the other options on the clean file")
T.place(x=150, y=200)

Button1=tkinter.Button(root,height= 1, width=20, text = "Clean file", font=('Georgia', 30), bg='lightskyblue',command=clean_file)
Button1.place(x=700, y=200)

Button2=tkinter.Button(root,height= 1, width=20, text = "Analyze clean file", font=('Georgia', 30), bg='lightskyblue',command=openNewWindow2)
Button2.place(x=700, y=300)

Button3=tkinter.Button(root,height= 1, width=20, text = "Compare clean file", font=('Georgia', 30), bg='lightskyblue', command=openNewWindow3)
Button3.place(x=700, y=400)

# Button4=tkinter.Checkbutton(root, height= 1, width=35, text = "Run commands with extensive descriptions", font=('Georgia', 30), bg='lightskyblue')
# Button4.pack(pady=10)

Button5=tkinter.Button(root,height= 1, width=20, text = "Exit", font=('Georgia', 30), bg='tomato', command=quit)
Button5.place(x=700, y=500)


root.mainloop()
