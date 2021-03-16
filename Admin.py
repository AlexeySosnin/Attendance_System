from tkinter import *
import tkinter.ttk as ttk
import csv

root = Tk()
root.title("Admin Panel")
width = 500
height = 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width / 2) - (width / 2)
y = (screen_height / 2) - (height / 2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0, 0)

#save table
def save():
    with open("Student_Details/Student_details.csv", "w", newline='') as myfile:
        csvwriter = csv.writer(myfile, delimiter=',')
        header = ["Id","Name","IntakeCode"]
        csvwriter.writerow(header)
        for row_id in tree.get_children():
            row = tree.item(row_id)['values']
            print('save row:', row)
            csvwriter.writerow(row)
button_save = Button(root, text="Save Table", command=save)
button_save.pack()

#delete row
def delete():
    selected_item = tree.selection()[0] ## get selected item
    tree.delete(selected_item)
    
button_del = Button(root, text="Delete Row", command=delete)
button_del.pack()

#drwaing header
TableMargin = Frame(root, width=500)
TableMargin.pack(side=TOP)

scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
tree = ttk.Treeview(TableMargin, columns=("ID", "Name", "IntakeCode"), height=400, selectmode="extended",
                    yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
scrollbary.config(command=tree.yview)
scrollbary.pack(side=RIGHT, fill=Y)
scrollbarx.config(command=tree.xview)
scrollbarx.pack(side=BOTTOM, fill=X)
tree.heading('ID', text="Student ID", anchor=W)
tree.heading('Name', text="Name", anchor=W)
tree.heading('IntakeCode', text="Intake Code", anchor=W)
tree.column('#0', stretch=NO, minwidth=0, width=0)
tree.column('#1', stretch=NO, minwidth=0, width=120)
tree.column('#2', stretch=NO, minwidth=0, width=120)
tree.column('#3', stretch=NO, minwidth=0, width=120)
tree.pack()
#drwaing table
student_array = {}
i = 0
with open('Student_Details/Student_details.csv') as f:
  reader = csv.DictReader(f, delimiter=',')
  for row in reader:
    emp_id = row['Id']
    name = row['Name']
    code = row['IntakeCode']
    student_array[i] = [emp_id, name, code]
    i = i + 1
for x in reversed(student_array.values()):
  tree.insert("", 0, values=(x[0],x[1],x[2]))
#editing row
def set_cell_value(event):
    for item in tree.selection():
        item_text = tree.item(item, "values")
        column = tree.identify_column(event.x)
        row = tree.identify_row(event.y)
    cn = int(str(column).replace('#', ''))
    entryedit = Text(root, width=3 + (cn - 1) * 5, height=1)
    entryedit.place(x=70 + (cn - 1) * 110, y=80)

    def saveedit():
        tree.set(item, column=column, value=entryedit.get(0.0,"end"))
        entryedit.destroy()
        okb.destroy()

    okb = ttk.Button(root, text='OK', width=4, command=saveedit)
    okb.place(x=97 + (cn - 1) * 150, y=77)
tree.bind('<Double-1>', set_cell_value)

root.mainloop()
