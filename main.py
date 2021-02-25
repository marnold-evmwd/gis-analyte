from tkinter import *
from tkinter import filedialog
from analyte_auto_analyze import analyte_function

filename = ''
directory = ''

def browseFiles():
    global filename
    filename = filedialog.askopenfilename()

def browseFolder():
    global directory
    directory = filedialog.askdirectory()
    window.destroy()

window = Tk()
window.geometry("500x200")

input_explore = Button(window, text='Input WTX File', command=browseFiles, height=5, width=60)
input_explore.grid(column = 1, row = 1)

output_explore = Button(window, text='Output Excel File(s)', command=browseFolder, height=5, width=60)
output_explore.grid(column = 1, row = 2)

window.mainloop()

if filename != '' and directory != '':
    analyte_function(filename, directory)
    print('ran the software')

else:
    print('did not excecute the software')