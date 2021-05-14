import tkinter as tk
from database import DB

cursor = DB.cursor()


class Registration:
	def __init__(self, frame):
		self.frame = frame
		self.email_label = tk.Label(master=frame, text = 'Email', width = 10)
		self.password_label = tk.Label(master=frame, text = 'Password',width = 10)
		self.repeat_password_label = tk.Label(master=frame, text = 'Repeat your password')
		self.firstname_label = tk.Label(master=frame, text = 'Firstname')
		self.lastname_label = tk.Label(master=frame, text = 'Lastname')
		self.email_entry = tk.Entry(master=frame, width = 30)
		self.password_entry = tk.Entry(master=frame, width = 30)
		self.repeat_password_entry = tk.Entry(master=frame, width = 30)
		self.firstname_entry = tk.Entry(master=frame, width = 30)
		self.lastname_entry = tk.Entry(master=frame, width = 30)
		self.sign_up_button = tk.Button(master=frame, text = 'Sign up',command = self.register)
		self.user_already_exists = tk.Label(
			master=frame,
			text = 'User with such email is already registered',
			fg = 'red',
			width = 50
		)
		self.password_error = tk.Label(
			master=frame,
			text = 'Passwords do not coincide',
			fg = 'red',
			width = 50
		)

	def clear(self):
		elements = self.frame.grid_slaves()
		for el in elements:
			el.grid_forget()

	def show(self):
		self.clear()
		self.email_label.grid(row=0, column=0)
		self.email_entry.grid(row=1, column=0)
		self.firstname_label.grid(row=2, column=0)
		self.firstname_entry.grid(row=3, column=0)
		self.lastname_label.grid(row=4, column=0)
		self.lastname_entry.grid(row=5, column=0)
		self.password_label.grid(row=6, column=0)
		self.password_entry.grid(row=7, column=0)
		self.repeat_password_label.grid(row=8, column=0)
		self.repeat_password_entry.grid(row=9, column=0)
		self.sign_up_button.grid(row=10, column=0)

	def register(self):
		email = self.email_entry.get()
		firstname = self.firstname_entry.get()
		lastname = self.lastname_entry.get()
		password = self.password_entry.get()
		repeat_password = self.repeat_password_entry.get()
		check_email = f"""'{email}'"""
		sql = f'SELECT id FROM users WHERE email = {check_email}'
		cursor.execute(sql)
		res = cursor.fetchall()
		print(res)
		if len(res) > 0:
			self.user_already_exists.grid(row=11, column=0)
		elif password != repeat_password:
			self.password_error.grid(row=11, column=0)
		else:
			sql = "INSERT INTO users (email, password, firstname, lastname) \
								VALUES (%s, %s, %s, %s)"
			val = (email, password, firstname, lastname)
			cursor.execute(sql, val)
			DB.commit()