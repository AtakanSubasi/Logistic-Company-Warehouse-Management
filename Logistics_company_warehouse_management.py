
import datetime
import json
import sqlite3
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox

class Product:
    
    def __init__(self,product_id, name ,category, stock, price):
        
        self.product_id = product_id
        self.name = name
        self.category = category
        self.stock = stock
        self.price = price
        
    def __str__(self):
        
        return f"Product ID: {self.product_id}, Name: {self.name}, Category: {self.category}, Stock: {self.stock}, Price: {self.price} $ "
        

class User:

    def __init__(self, user_id, name, role):
        self.user_id = user_id
        self.name = name
        self.role = role  # "admin" or "customer"

    def __str__(self):
        return f"User ID: {self.user_id}, Name: {self.name}, Role: {self.role}"

    def is_admin(self):
        return self.role == "admin"  



class Warehouse:
    
    def __init__(self):
        
        self.products = []
        
        self.orders = []

        self.users = []

    def login(self, username):
    
        for user in self.users:  

            if user.name.lower() == username.lower():

                print(f" Login successful! Welcome, {user.name}. Role: {user.role.capitalize()}")

                return user 
        
        print(" Invalid username! Please try again.")
        
        return None 

    def register_user(self, user):
        
        self.users.append(user)

        print(f"{user.name} has been registered as {user.role}.")
        
    def add_product(self, user, product):

        if user.role != "admin":

            print("Access denied! Only admins can add products.")
            return

        self.products.append(product)

        print(f"{product.name} has been added to the warehouse.")

        self.log_action(f"Product added: {product.name} (ID: {product.product_id})")
        
    
    def list_products(self):
        
        if not self.products:
            print("No products available in the warehouse.")
            
        else:
            for product in self.products:
                print(product)
                
    def search_product(self, keyword):
        
        found_products = [] 

        
        for product in self.products:
           
            if keyword.lower() in product.name.lower() or keyword.lower() in product.category.lower():

                found_products.append(product)

        
        if found_products:

            print("\n Search Results:")

            for product in found_products:

                print(product)  
        else:
            print(f" No products found matching '{keyword}'.")



    def update_stock(self, product_id, new_stock):
        
        for product in self.products:
            
            if product.product_id == product_id:
                
                product.stock = new_stock
                
                print(f"Stock updated successfully: {product.name} now has {new_stock} units.")
                return
            
        print("Product not found.")
        
    def check_low_stock(self,threshold):
        
        low_stock_products = []
        
        for product in self.products:
            
            if product.stock < threshold:
                
                low_stock_products.append(product)
                
        if low_stock_products:

            print("Warning: The following products have low stock:")

            for product in low_stock_products:

                print(f"{product.name} - Stock: {product.stock}")
        else:
            print("All products have sufficient stock.")
        
    def remove_product(self, user, product_id):
        
        if user.role == "admin":

            for product in self.products:

                if product.product_id == product_id:

                    self.products.remove(product)
                    print(f"{product.name} has been removed from the warehouse.")
                    return
                
            print("Product not found.")

        else:
            print("Access denied! Only admins can remove products.")
            
    
    def update_price(self, user, product_id, new_price):
        
        if user.role != "admin":

            print("Access denied! Only admins can update product prices.")
            return

        for product in self.products:

            if product.product_id == product_id:

                product.price = new_price

                print(f"Price updated successfully: {product.name} now costs {new_price} $.")
                return
            
        print("Product not found.")

    def cancel_order(self, order_id):
    
        for order in self.orders:

            if order.order_id == order_id:

                
                order.product.stock += order.quantity

                self.orders.remove(order)

                print(f"Order {order_id} has been canceled. Stock restored.")
                return
            
        print(f"Order {order_id} not found.")
    
            
    def place_order(self, user, order_id, product_id, quantity):

        if user.role != "customer":

            print("Access denied! Only customers can place orders.")
            return

        for product in self.products:

            if product.product_id == product_id:

                if product.stock >= quantity:

                    product.stock -= quantity

                    total_price = product.price * quantity

                    order = Order(order_id, product, quantity, total_price) 

                    self.orders.append(order)

                    
                    print(f"Order placed successfully: {order_id} - {product.name}, Quantity: {quantity}, Total: {total_price} $")
                    
                    self.log_action(f"Order placed: {order_id}, Product: {product.name}, Quantity: {quantity}, Total: {total_price} $")
                    
                    return
                else:
                    print("Not enough stock!")
                    return
        print("Product not found.")
    
    
    def list_orders(self):
        
        if not self.orders:
            print("No orders have been placed.")
            
        else:
            print("Orders List:")
        
            for order in self.orders:
                print(order)  
    
    def generate_report(self):
    
        print("\n == WAREHOUSE REPORT == \n")

        total_products = len(self.products)
        total_orders = len(self.orders)
        total_stock = sum(product.stock for product in self.products)

        print(f"Total Products: {total_products}")
        print(f"Total Orders: {total_orders}")
        print(f"Total Stock: {total_stock}")

        if self.products:

            most_expensive = max(self.products, key=lambda p: p.price)
            cheapest = min(self.products, key=lambda p: p.price)
            print(f"Most Expensive Product: {most_expensive.name} => {most_expensive.price} $")
            print(f"Cheapest Product: {cheapest.name} => {cheapest.price} $")

        else:
            print("No products in warehouse.")

        if self.orders:

            product_order_count = {}

            for order in self.orders:

                product_order_count[order.product.name] = product_order_count.get(order.product.name, 0) + order.quantity
            most_ordered = max(product_order_count, key=product_order_count.get)
            print(f"Most Ordered Product: {most_ordered}")

        else:
            print("No orders placed yet.")

    def log_action(self, action):
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        log_message = f"[{timestamp}] {action}\n"

        with open("warehouse_log.txt", "a") as log_file:
            log_file.write(log_message)

    def get_order_history(self, user):
    
        if user.role == "customer":

            user_orders = [order for order in self.orders if order.product in [p for p in self.products]]

            if user_orders:

                print(f"\n Order History for {user.name}:")

                for order in user_orders:

                    print(f"Order ID: {order.order_id}, Product: {order.product.name}, Quantity: {order.quantity}, Total: {order.total_price} $")
            else:
                print(f"No orders found for {user.name}.")

        elif user.role == "admin":

            print("\n All Orders in Warehouse:")

            for order in self.orders:

                print(f"Order ID: {order.order_id}, Product: {order.product.name}, Quantity: {order.quantity}, Total: {order.total_price} $")
        else:
            print("Invalid user role!")

    def generate_sales_report(self):
    
        total_revenue = sum(order.total_price for order in self.orders)
        total_orders = len(self.orders)

        if self.orders:

            product_order_count = {}

            for order in self.orders:
                
                product_order_count[order.product.name] = product_order_count.get(order.product.name, 0) + order.quantity
            
            most_sold_product = max(product_order_count, key=product_order_count.get)

        else:

            most_sold_product = None

        print("\n SALES REPORT")
        print(f" Total Revenue: {total_revenue} $")
        print(f" Total Orders: {total_orders}")

        if most_sold_product:
            print(f" Most Sold Product: {most_sold_product}")

        else:

            print("No products have been sold yet.")

class Order:

    def __init__(self, order_id, product, quantity, total_price):
        self.order_id = order_id
        self.product = product
        self.quantity = quantity
        self.total_price = total_price
        
    def __str__(self):
        
        return f"Order ID: {self.order_id}, Product: {self.product.name}, Quantity: {self.quantity}, Total Price: {self.total_price} $"

# Tkinter part 

class WarehouseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Warehouse Management System")
        self.user = None
        self.root.withdraw()
        self.setup_database()
        self.login_screen()

    def setup_database(self):
        self.conn = sqlite3.connect("warehouse.db")
        self.cursor = self.conn.cursor()
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                username TEXT UNIQUE,
                                password TEXT,
                                role TEXT)''')
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                                id INTEGER PRIMARY KEY,
                                name TEXT,
                                category TEXT,
                                stock INTEGER,
                                price REAL)''')
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
                                id INTEGER PRIMARY KEY,
                                product_id INTEGER,
                                quantity INTEGER,
                                FOREIGN KEY (product_id) REFERENCES products(id))''')
        
        self.conn.commit()

    def login_screen(self):
        self.root.withdraw()
        self.login_window = tk.Toplevel(self.root)
        self.login_window.title("User Login")

        tk.Label(self.login_window, text="Username:").grid(row=0, column=0)
        self.entry_username = tk.Entry(self.login_window)
        self.entry_username.grid(row=0, column=1)

        tk.Label(self.login_window, text="Password:").grid(row=1, column=0)
        self.entry_password = tk.Entry(self.login_window, show="*")
        self.entry_password.grid(row=1, column=1)

        self.login_button = tk.Button(self.login_window, text="Login", command=self.login)
        self.login_button.grid(row=2, column=0)
        
        self.signup_button = tk.Button(self.login_window, text="Sign Up", command=self.signup_screen)
        self.signup_button.grid(row=2, column=1)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        conn = sqlite3.connect("warehouse.db")
        cursor = conn.cursor()
        cursor.execute("SELECT role FROM users WHERE username=? AND password=?", (username, password))
        result = cursor.fetchone()
        conn.close()

        if result:
            role = result[0]
            self.user = {"username": username, "role": role}  

            self.login_window.destroy()
            self.root.deiconify()
            self.root.geometry("600x400")  
            
            print(dir(self))  
            
            self.create_widgets()  
            messagebox.showinfo("Success", f"Login successful! Welcome, {username} ({role}).")
        else:
            messagebox.showerror("Error", "Invalid username or password")
    
    
    def create_widgets(self):

        print("Creating UI components...")

        try:
            
            if self.user["role"] == "admin":  

                frame_products = ttk.LabelFrame(self.root, text="Product Management")
                frame_products.grid(row=0, column=0, padx=10, pady=10)

                ttk.Label(frame_products, text="Product Name:").grid(row=0, column=0)
                self.entry_product_name = ttk.Entry(frame_products)
                self.entry_product_name.grid(row=0, column=1)

                ttk.Label(frame_products, text="Category:").grid(row=1, column=0)
                self.entry_category = ttk.Entry(frame_products)
                self.entry_category.grid(row=1, column=1)

                ttk.Label(frame_products, text="Stock:").grid(row=2, column=0)
                self.entry_stock = ttk.Entry(frame_products)
                self.entry_stock.grid(row=2, column=1)

                ttk.Label(frame_products, text="Price:").grid(row=3, column=0)
                self.entry_price = ttk.Entry(frame_products)
                self.entry_price.grid(row=3, column=1)

                self.add_button = ttk.Button(frame_products, text="Add Product", command=self.add_product)
                self.add_button.grid(row=4, columnspan=2)

            # Products Display Button (Everyone should be able to see it)
            self.view_products_button = ttk.Button(self.root, text="View Products", command=self.list_products)
            self.view_products_button.grid(row=2, column=0, pady=5)

            # Order Management (Everyone Should Be Able to See)
            frame_orders = ttk.LabelFrame(self.root, text="Order Management")
            frame_orders.grid(row=1, column=0, padx=10, pady=10)

            ttk.Label(frame_orders, text="Order ID:").grid(row=0, column=0)
            self.entry_order_id = ttk.Entry(frame_orders)
            self.entry_order_id.grid(row=0, column=1)

            ttk.Label(frame_orders, text="Product ID:").grid(row=1, column=0)
            self.entry_order_product_id = ttk.Entry(frame_orders)
            self.entry_order_product_id.grid(row=1, column=1)

            ttk.Label(frame_orders, text="Quantity:").grid(row=2, column=0)
            self.entry_order_quantity = ttk.Entry(frame_orders)
            self.entry_order_quantity.grid(row=2, column=1)

            self.place_order_button = ttk.Button(frame_orders, text="Place Order", command=self.place_order)
            self.place_order_button.grid(row=3, columnspan=2)

            # Order Cancellation (Only Admin Should See)
            if self.user["role"] == "admin":

                ttk.Label(frame_orders, text="Cancel Order ID:").grid(row=4, column=0)
                self.entry_cancel_order_id = ttk.Entry(frame_orders)
                self.entry_cancel_order_id.grid(row=4, column=1)

                self.cancel_order_button = ttk.Button(frame_orders, text="Cancel Order", command=self.cancel_order)
                self.cancel_order_button.grid(row=5, columnspan=2)

            print("UI components created successfully!")

        except Exception as e:

            print(f"UI creation failed: {e}")
    


    def signup_screen(self):
        self.signup_window = tk.Toplevel(self.root)
        self.signup_window.title("Sign Up")

        tk.Label(self.signup_window, text="Username:").grid(row=0, column=0)
        self.signup_username = tk.Entry(self.signup_window)
        self.signup_username.grid(row=0, column=1)

        tk.Label(self.signup_window, text="Password:").grid(row=1, column=0)
        self.signup_password = tk.Entry(self.signup_window, show="*")
        self.signup_password.grid(row=1, column=1)

        tk.Label(self.signup_window, text="Role (admin/customer):").grid(row=2, column=0)
        self.signup_role = tk.Entry(self.signup_window)
        self.signup_role.grid(row=2, column=1)

        self.register_button = tk.Button(self.signup_window, text="Register", command=self.register_user)
        self.register_button.grid(row=3, columnspan=2)

    def register_user(self):
        username = self.signup_username.get()
        password = self.signup_password.get()
        role = self.signup_role.get().strip().lower()
        
        if role not in ["admin", "customer"]:
            messagebox.showerror("Error", "Invalid role! Use 'admin' or 'customer'.")
            return
        
        conn = sqlite3.connect("warehouse.db")
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
            conn.commit()
            messagebox.showinfo("Success", "User registered successfully!")
            self.signup_window.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists!")
        finally:
            conn.close()

    def add_product(self):

            if self.user["role"] != "admin":

                messagebox.showwarning("Permission Denied", "Only admins can add products.")
                return
            
            name = self.entry_product_name.get()
            category = self.entry_category.get()
            stock = self.entry_stock.get()
            price = self.entry_price.get()
            
            if name and category and stock and price:

                self.cursor.execute("INSERT INTO products (name, category, stock, price) VALUES (?, ?, ?, ?)", 
                                    (name, category, int(stock), float(price)))
                self.conn.commit()


                messagebox.showinfo("Success", f"{name} has been added to the warehouse.")
                
            else:

                messagebox.showwarning("Input Error", "Please fill all fields.")

    def place_order(self):
        product_id = self.entry_order_product_id.get()
        quantity = self.entry_order_quantity.get()

        if not product_id or not quantity:
            messagebox.showwarning("Input Error", "Please enter product ID and quantity.")
            return

        try:
            product_id = int(product_id)
            quantity = int(quantity)
        except ValueError:
            messagebox.showerror("Error", "Product ID and quantity must be integers.")
            return

        self.cursor.execute("SELECT stock FROM products WHERE id=?", (product_id,))
        result = self.cursor.fetchone()

        if result is None:
            messagebox.showerror("Error", "Product not found.")
            return

        available_stock = result[0]

        if quantity > available_stock:
            messagebox.showwarning("Stock Error", "Not enough stock available.")
            return

        
        new_stock = available_stock - quantity
        self.cursor.execute("UPDATE products SET stock=? WHERE id=?", (new_stock, product_id))
        self.cursor.execute("INSERT INTO orders (product_id, quantity) VALUES (?, ?)", (product_id, quantity))
        self.conn.commit()

        messagebox.showinfo("Success", "Order placed successfully!")


    def list_products(self):

        self.cursor.execute("SELECT * FROM products")
        products = self.cursor.fetchall()
        product_list = "\n".join([f"ID: {p[0]}, Name: {p[1]}, Stock: {p[3]}, Price: {p[4]}" for p in products])
        messagebox.showinfo("Products", product_list if product_list else "No products available.")
    
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    app = WarehouseApp(root)
    root.mainloop()
