# use ttk.Frame as parent so we have a controller
import tkinter.messagebox
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from twilio.rest import Client
import csv
from datetime import datetime
import time
import twilio

# Declare constants
# Enter personal SID and Token here
ACCOUNT_SID = 0
TEST_SID =  0
ACCOUNT_TOKEN =  0
TEST_TOKEN =  0

class TreeView(ttk.Frame):
	'''Treeview class to display csv contents'''
	def __init__(self, master):
		# create frame for treeview to have scroll bar
		self.tree_frame = Frame(master)
		self.tree_frame.place(relx=.18, rely=.12)

		# add scroll bar to the frame
		self.tree_scroll = Scrollbar(self.tree_frame)
		self.tree_scroll.pack(side=RIGHT, fill=Y)

		# declare Treeview
		self.my_tree = ttk.Treeview(self.tree_frame, yscrollcommand=self.tree_scroll.set)
		self.my_tree.pack()

		# Configure scroll bar
		self.tree_scroll.config(command=self.my_tree.yview)

		# format Treeview columns
		self.my_tree['columns'] = ("Name", "Phone Number", "Status")
		self.my_tree.column("#0", width=0, stretch=NO)
		self.my_tree.column("Name", anchor=W, width=170)
		self.my_tree.column("Phone Number", anchor=W, width=200)
		self.my_tree.column("Status", anchor=W, width=80)

		# Create Treeview Headings
		self.my_tree.heading("#0", text="", anchor=W)
		self.my_tree.heading("Name", text="Name", anchor=W)
		self.my_tree.heading("Phone Number", text="Phone Number", anchor=W)
		self.my_tree.heading("Status", text="Status", anchor=W)

class TextBody(ttk.Frame):
	'''Text widget for text body'''
	def __init__(self, master):
		self.master = master
		self.text_body = Text(master, width=65, height=15)
		self.text_body.place(relx=.510, rely=.65, anchor=CENTER)
		self.text_body.insert(1.0, "Enter text body...")
		self.text_body.bind('<FocusIn>', self.on_entry_click)
		self.text_body.bind('<FocusOut>', self.on_focusout)
		self.text_body.config(fg='grey', bg='white', insertbackground='black')

		# buttons to insert field variables from csv (fname, lname, caseno)
		self.fname_button = ttk.Button(master, text="{fname}", command=self.set_fname)
		self.fname_button.place(relx=0.92, rely=0.55, anchor=CENTER, width=65)
		self.lname_button = ttk.Button(master, text="{lname}", command=self.set_lname)
		self.lname_button.place(relx=0.92, rely=0.65, anchor=CENTER, width=65)
		self.caseno_button = ttk.Button(master, text="{caseno}", command=self.set_caseno)
		self.caseno_button.place(relx=0.92, rely=0.75, anchor=CENTER, width=65)

	def on_entry_click(self, event):
		'''when the text box is clicked remove placeholder text'''
		if self.text_body.get("1.0", 'end-1c') == 'Enter text body...':
			self.text_body.delete(1.0, "end")  # delete all the text in the entry
			self.text_body.insert(1.0, '')  # Insert blank for user input
			self.text_body.config(fg='black')

	def on_focusout(self, event):
		'''if message box clicked out of with no text reset placeholder'''
		if self.text_body.get("1.0", 'end-1c') == '':
			self.text_body.insert(1.0, 'Enter text body...')
			self.text_body.config(fg='grey')

	def set_fname(self):
		'''when button clicked place f string variable'''
		if self.text_body.get("1.0", 'end-1c') == 'Enter text body...':
			self.text_body.delete(1.0, "end")  # delete all the text in the entry
			self.text_body.insert("end", '{fname}')  # Insert blank for user input
			self.text_body.config(fg='black')
			self.text_body.focus_set()
		else:
			self.text_body.insert("end", '{fname}')
			self.text_body.focus_set()

	def set_lname(self):
		if self.text_body.get("1.0", 'end-1c') == 'Enter text body...':
			self.text_body.delete(1.0, "end")  # delete all the text in the entry
			self.text_body.insert("end", '{lname}')  # Insert blank for user input
			self.text_body.config(fg='black')
			self.text_body.focus_set()
		else:
			self.text_body.insert("end", '{lname}')
			self.text_body.focus_set()

	def set_caseno(self):
		if self.text_body.get("1.0", 'end-1c') == 'Enter text body...':
			self.text_body.delete(1.0, "end")  # delete all the text in the entry
			self.text_body.insert("end", '{caseno}')  # Insert blank for user input
			self.text_body.config(fg='black')
			self.text_body.focus_set()
		else:
			self.text_body.insert("end", '{caseno}')
			self.text_body.focus_set()


class MainApplication(ttk.Frame):
	'''Main class that will display the entire GUI'''
	def __init__(self, master):
		self.master = master
		self.__style()

		sid, token = ACCOUNT_SID, ACCOUNT_TOKEN
		print(sid)
		print(token)
		self.client = Client(sid, token)

		# button to allow us to open file dialog box
		self.file_button = ttk.Button(self.master, text="Choose File", command=self.browse_file)
		self.file_button.place(relx=0.19, rely=0.07, anchor=CENTER)

		# text widget that displays file path
		self.entry_box = Text(self.master, width=63, height=2.49, relief=GROOVE, borderwidth=0)
		self.entry_box.place(relx=.580, rely=.07, anchor=CENTER)
		self.entry_box.config(background="#E8E9ED", highlightthickness=0, fg='black', insertbackground='black')

		# treeview instance (bc same parents we can pass self.master)
		self.treeview = TreeView(self.master)
		print(self.treeview.my_tree)

		# text widget to customize sms body
		self.text_box = TextBody(self.master)
		print(f' text box {self.text_box.text_body}')

		# send button
		send_button = ttk.Button(master, text="Send SMS", command=self.send_messages)
		send_button.place(relx=0.37, rely=0.85, anchor=CENTER)


	def __style(self):
		'''Styles the main window'''
		self.master.config(background="#A4A4A4")
		self.master.title("Mass SMS Program")
		self.master.geometry("700x650")
		self.master.resizable(0, 0)
		style = ttk.Style()
		style.theme_use("clam")

	def browse_file(self):
		'''method opens directory and fills in treeview and file path text box'''
		self.filename = filedialog.askopenfilename(initialdir="/", title="Select a file",
										filetypes=(("csv files", "*.csv"),))
		self.entry_box.delete("1.0", END)
		self.entry_box.insert(INSERT, self.filename)
		self.treeview.my_tree.delete(*self.treeview.my_tree.get_children())
		try:
			with open(self.filename, encoding='utf-8-sig') as csv_file:
				csv_reader = csv.reader(csv_file)
				# skip first line of csv that contains headings and assign to first_row make all lowercase
				first_row = [x.lower() for x in next(csv_reader)]
				fname_column = first_row.index("fname")
				phone_column = first_row.index("phone1")
				for line in csv_reader:
					firstname = line[fname_column]
					phone_number = line[phone_column]
					if phone_number != "":
						phone_number = ''.join(c for c in phone_number if c.isdigit())
						phone_number = "+1" + phone_number
						status = "Pending"
						self.treeview.my_tree.insert("", "end", values=(firstname, phone_number, status))
				else:
					pass
		except OSError as e:
			pass

	def send_messages(self):
		'''method to send message with corresponding # from csv and text from text box'''
		NOW = datetime.utcnow()
		file = self.entry_box.get("1.0", "end-1c")
		if file:
			if self.text_box.text_body.get("1.0", 'end-1c') != 'Enter text body...':
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
							message_body = self.text_box.text_body.get("1.0", 'end-1c')
							formatted = message_body.format(fname=fname, lname=lname, caseno=caseno)
							try:
								message = self.client.messages.create(
									messaging_service_sid='MGdc55ba488c39e02ba46880998f678254',
									body=f"{formatted}",
									to=phone_number
								)
							except twilio.base.exceptions.TwilioRestException as e:
								print(e)
				self.check_status(NOW, file)
			else:
				tkinter.messagebox.showerror(title=None, message="No message body")
		else:
			tkinter.messagebox.showerror(title=None, message="No file chosen")

	def check_status(self, now, file):
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
					messages = self.client.messages \
						.list(
						date_sent_after=datetime(now.year, now.month, now.day, now.hour, now.minute, now.second),
						to=phone_number
					)
					timer = 0
					while (not messages) and timer != 15:
						print("waiting for data")
						messages = self.client.messages.list(
							date_sent_after=datetime(now.year, now.month, now.day, now.hour, now.minute, now.second),
							to=phone_number
						)
						time.sleep(.25)
						timer = timer + 1
					listOfEntriesInTreeView = self.treeview.my_tree.get_children()
					if timer == 15:
						self.treeview.my_tree.set(listOfEntriesInTreeView[x], 2, "error")
						print("done")
					else:
						print("data received")
						print(messages)
						print(messages[0].status)
						self.treeview.my_tree.set(listOfEntriesInTreeView[x], 2, messages[0].status)
				else:
					pass
		# show_balance()
		print("final")


def main():
	root = Tk()
	app = MainApplication(root)
	root.mainloop()

if __name__ == '__main__':
	main()
