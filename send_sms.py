import tkinter.messagebox
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from twilio.rest import Client
import csv
from datetime import datetime
from datetime import timedelta
import time
import twilio



# Declare constants
# Enter personal SID and Token here
ACCOUNT_SID = "ACa322fd7d9a65b915a9a33c706e105a68"
TEST_SID = "AC31201564899f64d0c6ce6f10a92e4585"
ACCOUNT_TOKEN = "301e0c8514d516a8a96a75cb4f4cc878"
TEST_TOKEN = "7bd910da178cf2959ac4787db6b2b912"
TEST_MODE = False


# Function to declare sid and token based on choice of test mode or not
def test_choice(test_mode):
    # pass twilio credentials with option to run a test mode
    if test_mode:
        sid = TEST_SID
        token = TEST_TOKEN
    else:
        sid = ACCOUNT_SID
        token = ACCOUNT_TOKEN
    return sid, token

# function to display balance on the screen
# def show_balance():
#     balance = float(client.api.v2010.balance.fetch().balance)
#     print(balance)
#     currency = "${:,.2f}". format(balance)
#     print(currency)
#     balance_label = tk.Label(root, text=f"Balance: {currency}")
#     balance_label.place(relx=.65, rely=.85, anchor="center")
#     balance_label.config(font=("", 15), width=12, bg="#A4A4A4")


# function to open directory and return file path
# uploads csv file into Treeview as well
def browse_file():
    count = 0
    root.filename = filedialog.askopenfilename(initialdir="/", title="Select a file",
                                               filetypes=(("csv files", "*.csv"),))
    entry_box.delete('1.0', END)
    entry_box.insert(INSERT, root.filename)
    my_tree.delete(*my_tree.get_children())
    # open file and load into treeview
    try:
        with open(root.filename, encoding='utf-8-sig') as csv_file:
            csv_reader = csv.reader(csv_file)
            # skip first line of csv that contains headings and assign to first_row make all lowercase
            first_row = [x.lower() for x in next(csv_reader)]
            print(first_row)
            fname_column = first_row.index("fname")
            phone_column = first_row.index("phone1")
            for line in csv_reader:
                firstname = line[fname_column]
                phone_number = line[phone_column]
                if phone_number != "":
                    phone_number = ''.join(c for c in phone_number if c.isdigit())
                    phone_number = "+1" + phone_number
                    status = "Pending"
                    my_tree.insert("", "end", values=(firstname, phone_number, status))
                else:
                    pass
    except OSError as e:
        pass


# function to check status of each sms using
# a +-1 minute interval from current time to get correct data
def check_status(now, file):
    count = 0
    status = []
    # gets all the data from specified time into a list
    with open(file, 'r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.reader(csv_file)
        # skip first line of csv that contains headings and assign to first_row make all lowercase
        first_row = [x.lower() for x in next(csv_reader)]
        phone_column = first_row.index("phone1")
        for x, line in enumerate(csv_reader):
            phone_number = line[phone_column]
            # if the phone number cell is not empty check status else pass to next cell
            if phone_number != "":
                phone_number = ''.join(c for c in phone_number if c.isdigit())
                phone_number = "+1" + phone_number
                messages = client.messages \
                    .list(
                    date_sent_after=datetime(now.year, now.month, now.day, now.hour, now.minute, now.second),
                    to=phone_number
                )
                timer = 0
                while (not messages) and timer != 15:
                    print("waiting for data")
                    messages = client.messages \
                        .list(
                        date_sent_after=datetime(now.year, now.month, now.day, now.hour, now.minute, now.second),
                        to=phone_number
                    )
                    time.sleep(.25)
                    timer = timer + 1
                listOfEntriesInTreeView = my_tree.get_children()
                if timer == 15:
                    my_tree.set(listOfEntriesInTreeView[x], 2, "error")
                    print("done")
                else:
                    print("data received")
                    print(messages)
                    print(messages[0].status)
                    my_tree.set(listOfEntriesInTreeView[x], 2, messages[0].status)
            else:
                pass
    # show_balance()
    print("final")


# Function to send messages at the click of send messages button
# sends message from numbers in csv file on each click
def send_messages():
    NOW = datetime.utcnow()
    file = entry_box.get("1.0", "end-1c")
    print(file)
    if file:
        if text_body.get("1.0", 'end-1c') != 'Enter text body...':
            # open csv file to get info to send text
            with open(file, 'r', encoding='utf-8-sig') as csv_file:
                csv_reader = csv.reader(csv_file)
                # skip first line of csv that contains headings and assign to first_row make all lowercase
                first_row = [x.lower() for x in next(csv_reader)]
                print(first_row)
                phone_column = first_row.index("phone1")
                fname_column = first_row.index("fname")
                lname_column = first_row.index("lname")
                caseno_column = first_row.index("caseno")
                # concatenate +1 before each phone # and send message
                for line in csv_reader:
                    phone_number = line[phone_column]
                    fname = line[fname_column]
                    lname = line[lname_column]
                    caseno = line[caseno_column]
                    # if the phone number cell is not empty check status else pass to next cell
                    if phone_number != "":
                        phone_number = ''.join(c for c in phone_number if c.isdigit())
                        phone_number = "+1" + phone_number
                        message_body = text_body.get("1.0", 'end-1c')
                        formatted = message_body.format(fname=fname, lname=lname, caseno=caseno)
                        try:
                            message = client.messages.create(
                                messaging_service_sid='MGdc55ba488c39e02ba46880998f678254',
                                body=f"{formatted}",
                                to=phone_number
                            )
                        except twilio.base.exceptions.TwilioRestException as e:
                            print(e)
            check_status(NOW, file)
        else:
            tkinter.messagebox.showerror(title=None, message="No message body")
    else:
        tkinter.messagebox.showerror(title=None, message="No file chosen")


def on_entry_click(event):
    """function that gets called whenever entry is clicked"""
    if text_body.get("1.0", 'end-1c') == 'Enter text body...':
        text_body.delete(1.0, "end")  # delete all the text in the entry
        text_body.insert(1.0, '')  # Insert blank for user input
        text_body.config(fg='black')


def on_focusout(event):
    if text_body.get("1.0", 'end-1c') == '':
        text_body.insert(1.0, 'Enter text body...')
        text_body.config(fg='grey')

def set_fname():
    if text_body.get("1.0", 'end-1c') == 'Enter text body...':
        text_body.delete(1.0, "end")  # delete all the text in the entry
        text_body.insert("end", '{fname}')  # Insert blank for user input
        text_body.config(fg='black')
        text_body.focus_set()
    else:
        text_body.insert("end", '{fname}')
        text_body.focus_set()

def set_lname():
    if text_body.get("1.0", 'end-1c') == 'Enter text body...':
        text_body.delete(1.0, "end")  # delete all the text in the entry
        text_body.insert("end", '{lname}')  # Insert blank for user input
        text_body.config(fg='black')
        text_body.focus_set()
    else:
        text_body.insert("end", '{lname}')
        text_body.focus_set()

def set_caseno():
    if text_body.get("1.0", 'end-1c') == 'Enter text body...':
        text_body.delete(1.0, "end")  # delete all the text in the entry
        text_body.insert("end", '{caseno}')  # Insert blank for user input
        text_body.config(fg='black')
        text_body.focus_set()
    else:
        text_body.insert("end", '{caseno}')
        text_body.focus_set()


sid, token = test_choice(TEST_MODE)
client = Client(sid, token)

# declare root and window size
root = Tk()
root.config(background="#A4A4A4")
root.title("Mass SMS Program")
root.geometry("700x650")
root.resizable(0, 0)

# change background colors of widgets to have better UI
style = ttk.Style()
style.theme_use("clam")

# file button declaration
file_button = ttk.Button(root, text="Choose File", command=browse_file)
file_button.place(relx=0.19, rely=0.07, anchor=CENTER)

# send button declaration
send_button = ttk.Button(root, text="Send SMS", command=send_messages)
send_button.place(relx=0.37, rely=0.85, anchor=CENTER)

# text box declaration(position and state)
entry_box = Text(root, width=63, height=2.49, relief=GROOVE, borderwidth=0)
entry_box.place(relx=.580, rely=.07, anchor=CENTER)
entry_box.config(background="#E8E9ED", highlightthickness=0)

# Frame for Treeview to add scroll bar
tree_frame = Frame(root)
tree_frame.place(relx=.18, rely=.12)

# add scroll bar to frame
tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side=RIGHT, fill=Y)

# declare Treeview
my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set)
my_tree.pack()

# Configure scroll bar
tree_scroll.config(command=my_tree.yview)

# format Treeview columns
my_tree['columns'] = ("Name", "Phone Number", "Status")
my_tree.column("#0", width=0, stretch=NO)
my_tree.column("Name", anchor=W, width=170)
my_tree.column("Phone Number", anchor=W, width=200)
my_tree.column("Status", anchor=W, width=80)

# Create Treeview Headings
my_tree.heading("#0", text="", anchor=W)
my_tree.heading("Name", text="Name", anchor=W)
my_tree.heading("Phone Number", text="Phone Number", anchor=W)
my_tree.heading("Status", text="Status", anchor=W)

# Entry widget for sms body
text_body = Text(root, width=65, height=15)
text_body.place(relx=.510, rely=.65, anchor=CENTER)
text_body.insert(1.0, "Enter text body...")
text_body.bind('<FocusIn>', on_entry_click)
text_body.bind('<FocusOut>', on_focusout)
text_body.config(fg='grey')

# buttons to insert field variables from csv (fname, lname, caseno)
fname_button = ttk.Button(root, text="{fname}", command=set_fname)
fname_button.place(relx=0.92, rely=0.55, anchor=CENTER, width=65)
lname_button = ttk.Button(root, text="{lname}", command=set_lname)
lname_button.place(relx=0.92, rely=0.65, anchor=CENTER, width=65)
caseno_button = ttk.Button(root, text="{caseno}", command=set_caseno)
caseno_button.place(relx=0.92, rely=0.75, anchor=CENTER, width=65)


root.mainloop()
