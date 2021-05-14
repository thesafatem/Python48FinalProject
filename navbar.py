import tkinter as tk


class Navbar:
	def __init__(self, frame):
		self.restaurant_list_btn = tk.Button(
			master=frame,
			text='Restaurants',
			bg='green',
			command=show_restaurant_list,
			state='disabled'
		)
		self.order_list_btn = tk.Button(
			master=frame,
			text='Orders',
			bg='green',
			state='disabled',
			command=show_order_list
		)
		self.sign_up_btn = tk.Button(
			master=frame,
			text='Sign up',
			bg='green',
			command=show_registration
		)
		self.sign_in_btn = tk.Button(
			master=frame,
			text='Sign in',
			bg='green',
			command=show_authorization
		)
		self.log_out_btn = tk.Button(
			master=frame,
			text='Log out',
			bg='green',
			command=log_out,
			state='disabled'
		)

	def show(self):
		self.restaurant_list_btn.grid(row=0, column=0)
		self.order_list_btn.grid(row=0, column=1)
		self.sign_up_btn.grid(row=0, column=2)
		self.sign_in_btn.grid(row=0, column=3)
		self.log_out_btn.grid(row=0, column=4)