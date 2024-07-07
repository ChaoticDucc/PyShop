
import time

class Operation:
    
    def __init__(self) -> None:
        pass

    @classmethod
    def Debug(cls):
        print("---------------------- DEBUG ----------------------") 
        print(Products.categories_dict)
        print("-------------------- DEBUG END --------------------") 

    # Sets a blank line 100 times
    def ClearTerminal():
        for loop in range(0, 100):
            print("")

    def Pause(pause_for):
        if pause_for == 0:
            input("Press enter to continue")
        else:
            print(f"Wait {pause_for} seconds")
            time.sleep(pause_for)

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
    id_dict = {}
    categories_dict = {}

    def __init__(self, name, price, category) -> None:
        # Tracks the number of products added
        Products.number_of_products += 1
        # Uses number_of_products to assign an ID (self.id) to instance.
        self.id = int(Products.number_of_products)
        # Adds ID (self.id) as key and instance (self) as value to product dictionary (id_dict).
        Products.id_dict[self.id] = self
        # Collects additional information
        self.name = name
        self.price = price
        self.category = category
        # Adds category (self.category) as key and instance (self) as value to product dictionary (categories_dict).
        # Checks if self.category is in categories_dict.
        if self.category in Products.categories_dict:
            # Adds the instance (self) to the list associated with the existing key (self.category).
            Products.categories_dict[self.category].append(self)
        else:
            # Creates new key (self.category) and a list as its value, containing the instance (self).
            Products.categories_dict[self.category] = [self]

    @classmethod
    # Displays a list of all products.
    def DisplayFullList(cls): 
        print("List of Products:")
        print("")
        for category in Products.categories_dict:
            print(category.capitalize())
            print("")
            for item in Products.categories_dict[category]:
                print(f"[{item.id}] {item.name.capitalize()}")
                print(f"${item.price:.2f}")
                print("")
    
    @classmethod
    def AddProduct(cls):
        while True:
            new_name = input("Enter Name: ")
            while True:
                new_price = input("Enter Price: $")
                if Operation.TypeCheck(new_price, "float") == True:
                    break
                else:
                    print("Invalid")
            new_category = input("Enter Category: ")
            try:
                Products(new_name, float(new_price), new_category)
                break
            except:
                print("oh oh")


class User:

    user_dict = {}
    logged_in_user = None

    def __init__(self, username, admin_rights) -> None:
        if username.islower() == False:
            raise ValueError("Only lowercase permitted")
        self.username = username
        # Adds username (self.username) as key and instance (self) as value to user dictionary (user_dict).
        User.user_dict[self.username] = self
        self.admin_rights = admin_rights
        self.cart = {}
        self.cart_total = 0

    @classmethod
    def Login(cls):
        print("Select a User")
        for item in User.user_dict.values():
            print(item.username)
        while True:
            username_to_login = input("Enter username: ")
            if username_to_login not in User.user_dict:
                print("User not found")
            else: 
                User.logged_in_user = User.user_dict[username_to_login]
                print(f"Logged in as {User.logged_in_user.username}")
                Operation.ClearTerminal()
                break

    @classmethod
    def LoggedInNow(cls):
        return(f"Logged in as {User.logged_in_user.username}")


class Purchasing(User):

    def __init__(self) -> None:
        pass
    
    # Receives and validates the input. 
    def Selection(self): 
        Products.DisplayFullList()
        print("Select your product(s) by entering the ID (eg: 1).")
        print("Use 0 to finish.")
        while True:
            print("")
            user_input_id = input("Product ID: ")
            # If user enters 0, displays cart and breaks loop.
            if user_input_id == "0":
                print("Displaying Cart")
                Purchasing.DisplayCart(self)
                break
            if user_input_id == "admin" and self.admin_rights == True:
                print("epic")
            # Checks if entered value is an integer.
            elif Operation.TypeCheck(user_input_id, "int") == False:
                print("Invalid Input")
            # Checks if entered value is a key in product dictionary (Products.id_dict).
            elif int(user_input_id) not in Products.id_dict:
                print("Not Found")
            # If none of the above tests have discovered any issues, asks user for quantity. 
            else:
                # Looks up the instance value (output_instance) in dictionary (Products.id_dict) using key (user_input_id).
                output_instance = Products.id_dict[int(user_input_id)]
                print(f"{output_instance.name.capitalize()} selected")
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
                        output_qty = int(user_input_qty)
                        Purchasing.AddToCart(self, output_instance, output_qty)
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
        print(User.LoggedInNow())
        print("")
        print("Cart:") 
        print("")
        # Checks if the cart is empty. An empty list is false. 
        if not user.cart:  
            print("Cart is Empty")
        else:
            for item in user.cart:
                item_quantity = user.cart[item]
                print(f"{item.name.capitalize()}")
                print(f"{item_quantity}x ${item.price:.2f}")
                print(f"                ${(item.price*item_quantity):.2f}")
            print("_____________________")
            print(f"Total: $ {user.cart_total:.2f}")
        Operation.Pause(0)

class Admin():

    def __init__(self) -> None:
        pass
    
    def PasswordCheck(self):
        print("Admin Console")
        entered_password = input("Enter Password: ")

# Class Instances

Products("apple", 0.50, "fruit")
Products("banana", 0.70, "fruit")
Products("pretzel", 0.80, "snack")
Products("muffin", 2.00, "snack")
Products("chips", 1.50, "snack")
Products("cola", 2.70, "drink")
Products("orange juice", 2.50, "drink")
Products("water", 1.20, "drink")

User("chaoticducc",True)
User("steve",False)


# Operating Code

User.Login()
print(f'''
---------------------------------
Welcome to the School Store!
{User.LoggedInNow()}
---------------------------------''')
Products.AddProduct()
Purchasing.Selection(User.logged_in_user)