import tkinter as tk
from database import DB
from PIL import ImageTk
from image import *
from registration import Registration
from navbar import Navbar 

cursor = DB.cursor()

window = tk.Tk()

user = None

navbar_frame = tk.Frame(master=window)
main_frame = tk.Frame(master=window)
navbar_frame.grid(row=0, column=0)
main_frame.grid(row=1, column=0)

def clear():
	elements = main_frame.grid_slaves()
	for el in elements:
		el.grid_forget()

def show_registration():
	clear()
	registration.show()

def show_authorization():
	clear()
	authorization.show()

def log_out():
	user = None
	navbar.restaurant_list_btn['state'] = 'disabled'
	navbar.order_list_btn['state'] = 'disabled'
	navbar.log_out_btn['state'] = 'disabled'
	show_authorization()

def show_restaurant_list():
	clear()
	sql = 'SELECT *, open_time <= current_time() AND current_time() <= close_time \
		AS status  FROM restaurants ORDER BY STATUS desc'
	cursor.execute(sql)
	res = cursor.fetchall()
	for i in range(len(res)):
		restaurantDetail = RestaurantDetail(res[i], main_frame)
		restaurantDetail.show(i)

def show_order_list():
	clear()
	sql = f'SELECT order_id, order_date, restaurant_name, SUM(my_order.total) as total FROM \
		(SELECT orders_dishes.order_id as order_id, \
		(orders_dishes.amount * dishes.price) as total, \
		orders.order_date, restaurants.name as restaurant_name\
		FROM orders_dishes\
		INNER JOIN dishes ON orders_dishes.dish_id = dishes.id\
		INNER JOIN orders ON orders_dishes.order_id = orders.id \
		INNER JOIN restaurants ON orders.restaurant_id = restaurants.id WHERE orders.user_id = {user}) as my_order \
		group by my_order.order_id'

	cursor.execute(sql)
	res = cursor.fetchall()

	for i in range(len(res)):
		orderDetail = OrderDetail(res[i], main_frame)
		orderDetail.show(i)


def make_order(restaurant_id, menuDishDetailList):
	empty_order = True
	for menuDishDetail in menuDishDetailList:
		if int(menuDishDetail.amount.cget('text')) > 0:
			empty_order = False

	if empty_order:
		return

	sql = 'INSERT INTO orders (restaurant_id, user_id) VALUES (%s, %s)'
	val = (restaurant_id, user)
	cursor.execute(sql, val)
	DB.commit()
	order_id = cursor.lastrowid
	sql = 'INSERT INTO orders_dishes (amount, order_id, dish_id) VALUES (%s, %s, %s)'
	for menuDishDetail in menuDishDetailList:
		if int(menuDishDetail.amount.cget('text')) > 0:
			val = (int(menuDishDetail.amount.cget('text')), order_id, menuDishDetail.id)
			cursor.execute(sql, val)
			DB.commit()

	show_order_list()


def show_menu(restaurant_id):
	clear()
	sql = f'SELECT * FROM dishes WHERE restaurant_id = {restaurant_id}'
	cursor.execute(sql)
	res = cursor.fetchall()
	menuDishDetailList = []
	for i in range(len(res)):
		menuDishDetail = MenuDishDetail(res[i], main_frame)
		menuDishDetail.show(i)
		menuDishDetailList.append(menuDishDetail)

	make_order_btn = tk.Button(
		master=main_frame,
		text='Make order',
		bg='green',
		command=lambda: make_order(restaurant_id, menuDishDetailList)
	)

	make_order_btn.grid(row=len(res), column=0)

def show_detailed_order(order_id):
	clear()
	sql = f'SELECT dishes.id, dishes.name, dishes.category, dishes.price, \
			dishes.image, dishes.restaurant_id, orders_dishes.amount, \
			(orders_dishes.amount * dishes.price) as total FROM orders_dishes \
			INNER JOIN dishes ON orders_dishes.dish_id = dishes.id \
			WHERE orders_dishes.order_id = {order_id}'
	cursor.execute(sql)
	res = cursor.fetchall()
	for i in range(len(res)):
		orderDishDetail = OrderDishDetail(res[i], main_frame)
		orderDishDetail.show(i)



class DishDetail:
	def __init__(self, dish, frame):
		img = Image.open(f'media/dishes/{dish[4]}')
		img = get_square_image(img)
		img = image_resize(img, 50)
		img = get_circle_image(img)
		render = ImageTk.PhotoImage(img)
		self.image = tk.Label(master=frame, image=render)
		self.image.image = render
		self.name = tk.Label(master=frame, text=dish[1])
		self.price = tk.Label(master=frame, text=dish[3])
		self.id = dish[0]

	def show(self, row):
		self.image.grid(row=row, column=0)
		self.name.grid(row=row, column=1)
		self.price.grid(row=row, column=2)


class MenuDishDetail(DishDetail):
	def __init__(self, dish, frame):
		super().__init__(dish, frame)
		self.amount = tk.Label(master=frame, text='0', bg='skyblue')
		self.add_dish_btn = tk.Button(master=frame, text='+', bg='green', command=self.add_dish)
		self.remove_dish_btn = tk.Button(master=frame, text='-', bg='green', command=self.remove_dish, state='disabled')

	def show(self, row):
		super().show(row)
		self.remove_dish_btn.grid(row=row, column=3)
		self.amount.grid(row=row, column=4)
		self.add_dish_btn.grid(row=row, column=5)

	def add_dish(self):
		amount = self.amount.cget('text')
		amount = int(amount) + 1
		self.remove_dish_btn['state'] = 'normal'
		self.amount.configure(text=amount)

	def remove_dish(self):
		amount = self.amount.cget('text')
		amount = int(amount) - 1
		if amount == 0:
			self.remove_dish_btn['state'] = 'disabled'
		self.amount.configure(text=amount)


class OrderDishDetail(DishDetail):
	def __init__(self, dish, frame):
		super().__init__(dish, frame)
		self.amount = tk.Label(master=frame, text=dish[6])
		self.total = tk.Label(master=frame, text=dish[7])

	def show(self, row):
		super().show(row)
		self.amount.grid(row=row, column=3)
		self.total.grid(row=row, column=4)


class RestaurantDetail:
	def __init__(self, restaurant, frame):
		state = ['disabled', 'normal']
		color = ['gray', 'green']
		img = Image.open(f'media/logos/{restaurant[3]}')
		img = get_square_image(img)
		img = image_resize(img, 50)
		img = get_circle_image(img)
		render = ImageTk.PhotoImage(img)
		self.logo = tk.Label(master=frame, image=render)
		self.logo.image = render
		self.name = tk.Label(master=frame, text=restaurant[1])
		self.address = tk.Label(master=frame, text=restaurant[2])
		self.go = tk.Button(
			master=frame, 
			text='Go!', 
			bg=color[restaurant[6]], 
			state=state[restaurant[6]],
			command=lambda: show_menu(restaurant[0])
		)

	def show(self, row):
		self.logo.grid(row=row, column=0)
		self.name.grid(row=row, column=1)
		self.address.grid(row=row, column=2)
		self.go.grid(row=row, column=3)


class OrderDetail:
	def __init__(self, order, frame):
		self.order_date = tk.Label(master=frame, text=order[1].strftime("%d, %B, %Y, %X"))
		self.restaurant = tk.Label(master=frame, text=order[2])
		self.total = tk.Label(master=frame, text=order[3], bg='crimson')
		self.detailed = tk.Button(master=frame, text='See', bg='green', command=lambda: show_detailed_order(order[0]))

	def show(self, row):
		self.order_date.grid(row=row, column=0)
		self.restaurant.grid(row=row, column=1)
		self.total.grid(row=row, column=2)
		self.detailed.grid(row=row, column=3)


class Authorization:
	def __init__(self):
		self.email_label = tk.Label(
			master=main_frame,
			text = 'Email',
			width = 10
		)
		self.password_label = tk.Label(
			master=main_frame,
			text = 'Password',
			width = 10
		)
		self.email_entry = tk.Entry(
			master=main_frame,
			width = 30
		)
		self.password_entry = tk.Entry(
			master=main_frame,
			width = 30
		)
		self.sign_up_button = tk.Button(
			master=main_frame,
			text = 'Sign in',
			command = self.authorize
		)
		self.authorization_failed_label = tk.Label(
			master=main_frame,
			text = 'Authorization failed',
			fg = 'red',
			width = 20
		)

	def show(self):
		clear()
		self.email_label.grid(row=0, column=0)
		self.email_entry.grid(row=1, column=0)
		self.password_label.grid(row=2, column=0)
		self.password_entry.grid(row=3, column=0)
		self.sign_up_button.grid(row=4, column=0)

	def authorize(self):
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
			global user
			user = res[0][0]
			navbar.restaurant_list_btn['state'] = 'normal'
			navbar.order_list_btn['state'] = 'normal'
			navbar.log_out_btn['state'] = 'normal'
			show_restaurant_list()


registration = Registration(main_frame)
authorization = Authorization()

navbar = Navbar(navbar_frame)
navbar.show()

window.mainloop()