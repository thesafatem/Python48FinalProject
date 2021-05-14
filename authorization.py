import tkinter as tk
from database import DB

cursor = DB.cursor()


class Authorization:
	def __init__(self, frame):
		self.user = None
		self.frame = frame
		self.email_label = tk.Label(master=frame, text = 'Email', width = 10)
		self.password_label = tk.Label(master=frame, text = 'Password', width = 10)
		self.email_entry = tk.Entry(master=frame, width = 30)
		self.password_entry = tk.Entry(master=frame, width = 30)
		self.sign_up_button = tk.Button(master=frame, text = 'Sign in', command = self.authorize)
		self.authorization_failed_label = tk.Label(master=frame, text = 'Authorization failed', \
													 fg = 'red', width = 20)

	def clear(self):
		elements = self.frame.grid_slaves()
		for el in elements:
			el.grid_forget()

	def show(self):
		self.clear()
		self.email_label.grid(row=0, column=0)
		self.email_entry.grid(row=1, column=0)
		self.password_label.grid(row=2, column=0)
		self.password_entry.grid(row=3, column=0)
		self.sign_up_button.grid(row=4, column=0)

	def authorize(self, navbar):
		email = self.email_entry.get()
		password = self.password_entry.get()
		email = f"""'{email}'"""
		password = f"""'{password}'"""
		sql = f'SELECT id FROM users WHERE email = {email} and \
				password = {password}'
		cursor.execute(sql)
		res = cursor.fetchall()
		print(res)
		if len(res) == 0:
			self.authorization_failed_label.grid(row=5, column=0)
		else:
			self.user = res[0][0]
			navbar.restaurant_list_btn['state'] = 'normal'
			navbar.order_list_btn['state'] = 'normal'
			navbar.log_out_btn['state'] = 'normal'
			show_restaurant_list()