import sys
import csv
# 1. Declare two constant variables named COMBO_MEAL_PRICE and COLD_DRINK_PRICE

COMBO_MEAL_PRICE = 20.0
COLD_DRINK_PRICE = 3.0

# 2. Complete the function read_burger_from_file to read in burgers information from file named "burger_list.csv"
def read_burger_from_file():
    # Zero marks will be given if you assigned the burger data by this static variable

    list_dict_burgers = list()
    filename = "burger_list.csv"
    # your implemention starts here
    with open(filename, mode='r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            if row and not row[0].startswith('#'):
                list_dict_burgers.append({'Name': row[0], 'Price': float(row[1])})

    # This static variable is for your development in early stage
    # Comment out this static variable after you completed your implementation of read from file
    """list_dict_burgers = [
        {'Name': 'Queens\'s Signature', 'Price': 45.0},
        {'Name': 'Cheeseburger', 'Price': 25.0},
        {'Name': 'Chili Burger', 'Price': 32.0},
        {'Name': 'Olive Burger', 'Price': 36.0},
        {'Name': 'Beef Burger', 'Price': 40.0}
    ]
    """

    return list_dict_burgers



# Complete your compute_sales function here
def compute_sales(burger_price, combo_meal, cold_drink, quantity):
    sales = 0
    #Calculate package price
    sales = burger_price * quantity
    #add the combo_meal
    if combo_meal:
        sales += COMBO_MEAL_PRICE * quantity
    #add cold_drink
    if cold_drink:
        sales += COLD_DRINK_PRICE * quantity
    return sales

def display_menu(burgers):
    print("\nBurger Queen Menu:")
    print("{:<5} | {:<20} | {:<6}".format("No.", "Burger Type", "Price"))
    for index, burger in enumerate(burgers, start=1):
        print("{:<5} | {:<20} | ${:<6.1f}".format(index, burger['Name'], burger['Price']))

def get_user_selection(prompt, options):
    while True:
        user_input = input(prompt).strip()
        if user_input.upper() in options:
            #Returns all uppercase, yes, both uppercase and lowercase can be run
            return user_input.upper()
        else:
            print("Invalid input for choice")


def get_user_input(prompt, input_type=int):
    while True:
        user_input = input(prompt).strip()
        #return enter
        if user_input == "":
            return None
        try:
            #return integer
            return input_type(user_input)
        except ValueError:
            print(f"Invalid input for choice")


def main():

    # 3. Declare a list of dictionary named list_dict_burgers in main function
    #    to store all burgers information returned by the function read_burger_from_file()
    list_dict_burgers = read_burger_from_file()
  
    # 4. list of tuple to store all burger orders which are not yet completed by customer
    list_tuple_current_sales = list()

    # 5. dictionary to accumulate the quantity sold for each type of burger
    dict_no_of_burgers_sold = dict()

    # your implemention starts here
    # Display a welcome message and followed by the main menu of Burger Queen Food Ordering system
    dict_no_of_burgers_sold = {burger['Name']: 0 for burger in list_dict_burgers}
    print("Welcome to Burger Queen Food Ordering System.")
    # Used to calculate the price of each order and how many orders there are
    total_orders=list()
    order_count = 1
    burger_choice=0
    while True:
        display_menu(list_dict_burgers)
        while True:
            burger_choice = get_user_input("Please input your choice.Press \"Enter\" to confirm this order (1 - 5):", int)
            if burger_choice is None :
                #Return a space, but no order is generated
                if not list_tuple_current_sales:
                    print("Current sales order is empty.")
                    continue
                total_orders.append(current_sales)
                #calculate total_sales,lowest_sales,highest_sales,average_sales
                total_sales = sum(order for order in total_orders )
                lowest_sales = min(order for order in total_orders)
                highest_sales = max(order for order in total_orders)
                average_sales = total_sales / order_count
                #print data
                print("\nStatistics of Burger Queen:")
                print(f"Total number of orders = {order_count}")
                print(f"Lowest Sales Amount = ${lowest_sales:.1f}")
                print(f"Highest Sales Amount = ${highest_sales:.1f}")
                print(f"Total Sales Amount = ${total_sales:.1f}")
                print(f"Average Sales Amount = ${average_sales:.1f}")
                print("List of Total Number of Burgers Sold:")
                for burger, count in dict_no_of_burgers_sold.items():
                    if count != 0:
                        print(f"   {burger}: {count}")

                list_tuple_current_sales = []
                order_count += 1
                break

            burger_choice = burger_choice - 1
            if burger_choice < 0 or burger_choice >= len(list_dict_burgers):
                print("Invalid input for choice")
                continue



            combo_meal = get_user_selection("Combo meal required? Combo comes with fries and drinks. +$20.0 (Y/N): ", ['Y', 'N']) == 'Y'
            cold_drink = combo_meal and get_user_selection("Cold drink required? +$3.0 (Y/N): ", ['Y', 'N']) == 'Y'

            while True:
                quantity = get_user_input("please input quantity: ", int)
                if quantity is None or quantity <= 0:
                    print("Invalid input for choice")
                else:
                    break
            current_sales = compute_sales(
                list_dict_burgers[burger_choice]['Price'], combo_meal, cold_drink, quantity
            )
            current_order = [list_dict_burgers[burger_choice]['Name'], quantity, combo_meal, cold_drink, current_sales,order_count]
            #list_tuple_current_sales stores the contents of each order
            list_tuple_current_sales.append(current_order)
            dict_no_of_burgers_sold[list_dict_burgers[burger_choice]['Name']] += quantity
            print("\nCurrent Order Summary:")
            current_sales = sum(order[4] for order in list_tuple_current_sales)
            for order in list_tuple_current_sales:
                print(f"{order[1]}  {order[0]}{' with combo set and hot drink' if (order[2] == True and order[3] == False) else ''}{' with combo set and cold drink' if (order[2] == True and order[3]  == True) else ''}  ${order[4]:.1f}")
            print(f"Total amount of current order: ${current_sales:.1f}")
            if current_sales!=0:
                display_menu(list_dict_burgers)



if __name__ == "__main__":
    main()

