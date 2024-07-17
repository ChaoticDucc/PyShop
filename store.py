
import time

products_file = "products.txt"
users_file = "users.txt"

banner = '''---------------------------------
Welcome to the School Store!
---------------------------------'''

class Operation:

    # Sets a blank line 100 times
    def ClearTerminal():
        for loop in range(0, 100):
            print("")

    def Pause(pause_for = 0):
        if pause_for == 0:
            input("Press enter to continue")
        else:
            print(f"Wait {pause_for} seconds")
            time.sleep(pause_for)

    # TypeCheck is used because it can verify if a given string can be converted to another type. 
    def TypeCheck (input_value, check_for_type): 
        # Checks if integer check has been requested.
        if check_for_type == "int":
            # Attempts to convert value (input_value) to an integer. 
            try:
                input_value=int(input_value)
                return(True)
            except:
                return(False)
    	# Checks if integer check has been requested.
        elif check_for_type == "float":
            # Attempts to convert value (input_value) to an integer. 
            try:
                input_value=float(input_value)
                return(True)
            except:
                return(False)
        else:
            raise TypeError("Invalid/unsupported type")


class Products:

    number_of_products = 0
    product_id_dict = {}
    product_name_dict = {}
    product_categories_dict = {}

    def ReadFile():
        print (f"Adding products from '{products_file}'")
        print("")
        with open(products_file) as file:
            file_content = file.readlines()
        for content in file_content:
            content_line = content.strip()
            content_items = content_line.split(", ")
            try:
                Products(content_items[0],content_items[1],content_items[2])
            except IndexError:
                print(f"⚠ FAILURE: '{content_items[0]}' failed. Missing arguments. Currently: '{content_line}'.")
            print("")

    def __init__(self, name, price, category) -> None:
        ## TESTS
        # checks if product name has already been added
        if name in Products.product_name_dict:
            existing = Products.product_name_dict[name]
            print(f"⚠ FAILURE: '{name}' failed. '{existing.name}' already exists with price '{existing.price}' in category '{existing.category}'.")
        # checks if price is float
        elif Operation.TypeCheck(price, "float") == False:
            print(f"⚠ FAILURE: '{name}' failed. Price is not a number. Currently: '{price}'")
        ## IF TESTS PASSED
        else:
            ## INSTANCE VARIABLES
            self.name = name
            self.price = float(price)
            self.category = category
            # Tracks the number of products added
            Products.number_of_products += 1
            # Uses number_of_products to assign an ID (self.id) to instance.
            self.id = int(Products.number_of_products)
            ## DICTIONARIES
            # Adds ID (self.id) as key and instance (self) as value to product id dictionary (product_id_dict).
            Products.product_id_dict[self.id] = self
            # Adds name (self.name) as key and instance (self) as value to name dictionary (product_name_dict).
            Products.product_name_dict[self.name] = self
            # Adds category (self.category) as key and instance (self) as value to category dictionary (product_categories_dict).
            # - Checks if self.category is in product_categories_dict.
            if self.category in Products.product_categories_dict:
                # Adds the instance (self) to the list associated with the existing key (self.category).
                Products.product_categories_dict[self.category].append(self)
            else:
                # Creates new key (self.category) and a list as its value, containing the instance (self).
                Products.product_categories_dict[self.category] = [self]
            print(f"SUCCESS: '{self.name}' added with price '{self.price}' in category '{self.category}'.")
            # Asks user if price should be negative
            if float(price) < 0:
                print(f"🛈 Price is negative. Is this correct?")

    # Displays a list of all products.
    def DisplayFullList(): 
        print("List of Products:")
        print("")
        for category in Products.product_categories_dict:
            print(category.capitalize())
            print("")
            for item in Products.product_categories_dict[category]:
                print(f"[{item.id}] {item.name}")
                print(f"${item.price:.2f}")
                print("")


class User:

    available_permission_levels = ("user","admin")
    user_dict = {}
    logged_in_user = None

    def ReadFile():
        print (f"Adding users from '{users_file}'")
        print("")
        with open(users_file) as file:
            file_content = file.readlines()
        for content in file_content:
            content_line = content.strip()
            content_items = content_line.split(", ")
            try:
                User(content_items[0], content_items[1])
            except IndexError:
                print(f"⚠ FAILURE: '{content_items[0]}' failed. Missing arguments. Currently: '{content_line}'.")
            print("")

    def __init__(self, name, permission_level) -> None:
        # Checks if entered name is lowercase. Makes it so if not. 
        if name.islower() == False:
            print(f"🛈 Changed '{name}' to '{name.lower()}'.")
            name = name.lower()
        ## TESTS
        # checks if user name has already been added
        if name in User.user_dict: 
            existing = User.user_dict[name]
            print(f"⚠ FAILURE: '{name}' failed. '{existing.name}' already exists with permission level '{existing.permission_level}'.")
        # check if given permissions level matches available levels
        elif permission_level not in User.available_permission_levels: 
            print(f"⚠ FAILURE: '{name}' failed. Admin rights must be one of the following: {User.available_permission_levels}. Currently: '{permission_level}'")
        ## IF TESTS PASSED
        else:
            self.name = name.lower()
            self.permission_level = permission_level
            # Adds name (self.name) as key and instance (self) as value to user dictionary (user_dict).
            User.user_dict[self.name] = self
            self.cart = {}
            self.cart_total = 0
            print(f"SUCCESS: '{self.name}' added with  permission level '{self.permission_level}'.")
            
    def Login():
        Operation.ClearTerminal()
        while True:
            user_to_login = input("Enter username: ")
            if user_to_login not in User.user_dict:
                print("User not found")
            else: 
                User.logged_in_user = User.user_dict[user_to_login]
                print(f"Logged in as {User.logged_in_user.name}")
                Operation.ClearTerminal()
                break


class Purchasing(User):
    
    # Receives and validates the input. 
    def Menu(user): 
        print(banner)
        Products.DisplayFullList()
        print("Select your product(s) by entering the ID (eg: 1).")
        print("Use 0 to finish.")
        while True:
            print("")
            user_input = input("Product ID: ")
            # If user enters 0, displays cart and breaks loop.
            if user_input == "0":
                print("Displaying Cart")
                Purchasing.DisplayCart(user)
                break
            elif user_input == "exit" and user.permission_level == "admin":
                break
            else:
                Purchasing.ProductSelection(user, user_input)


    def ProductSelection(user, requested_id): 
        # Checks if entered value is an integer.
        if Operation.TypeCheck(requested_id, "int") == False:
            print("Invalid Input")
        # Checks if entered value is a key in product dictionary (Products.product_id_dict).
        elif int(requested_id) not in Products.product_id_dict:
            print("Not Found")
        # If none of the above tests have discovered any issues, asks user for quantity. 
        else:
            # Looks up the instance value (output_instance) in dictionary (Products.product_id_dict) using key (user_input_id).
            product = Products.product_id_dict[int(requested_id)]
            print(f"{product.name.capitalize()} selected")
            print("Use 0 to cancel")
            while True:
                user_input_qty = input("Quantity: ")
                # If user enters 0, breaks loop and resets, allowing user to select new item, .
                if user_input_qty == "0":
                    print("Cancelled")
                    break
                # Checks if entered value is an integer
                if Operation.TypeCheck(user_input_qty, "int") == False:
                    print("Invalid Input")
                else:
                    qty = int(user_input_qty)
                    Purchasing.AddToCart(user, product, qty)
                    break
    
    # Adds a given number (qty_to_add) of given items (item_to_add) to cart.
    def AddToCart(self, item_to_add, qty_to_add):
        # Checks if item_to_add is already in cart dictionary (self.cart).
        if item_to_add in self.cart:
            # Looks up the current quantity (current_qty) in (self.cart).
            current_qty = self.cart [item_to_add]
            # Changes the current quantity in self.cart, adding qty_to_add. 
            self.cart[item_to_add] = qty_to_add + current_qty
        else:
            # Adds the item_to_add as the key and the qty_to_add as the value to the cart dictionary (self.cart).
            self.cart[item_to_add] = qty_to_add
        # Adds up the new total
        self.cart_total = self.cart_total + (item_to_add.price * qty_to_add)
        print(f"Added {qty_to_add} {item_to_add.name}(s) to Cart")
 
    def DisplayCart(user):
        Operation.ClearTerminal()
        print("Cart:") 
        print("")
        # Checks if the cart is empty. An empty list is false. 
        if not user.cart:  
            print("Cart is Empty")
        else:
            for item in user.cart:
                item_quantity = user.cart[item]
                print(f"{item.name.capitalize()}")
                print(f"{item_quantity}x $ {item.price:.2f}")
                print(f"                $ {(item.price*item_quantity):.2f}")
            print("_____________________")
            print(f"Total: $ {user.cart_total:.2f}")
        Operation.Pause()
        user.cart = {}
        user.cart_total = 0
        Navigator()

def Navigator():
    User.Login()
    Purchasing.Menu(User.logged_in_user)

def StartUp():
    Products.ReadFile()
    User.ReadFile()
    Operation.Pause()

# Operating Code
StartUp()
Navigator()