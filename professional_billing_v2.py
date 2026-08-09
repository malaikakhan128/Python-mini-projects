# Professional Restaurant Billing System v2
# Features: Dynamic menu, customer invoices, + Total Sales Report

from datetime import datetime
import os

menu = {
    "1": {"name": "Burger", "price": 300},
    "2": {"name": "Pizza", "price": 800},
    "3": {"name": "Pasta", "price": 500},
    "4": {"name": "Coke", "price": 100},
    "5": {"name": "Fries", "price": 200}
}

TAX_RATE = 0.1
DISCOUNT_THRESHOLD = 1000
DISCOUNT_RATE = 0.05
SALES_FILE = "all_sales.txt"  # This will store total of all bills


def show_menu():
    print("\n" + "=" * 40)
    print(" FOODIE RESTAURANT MENU")
    print("=" * 40)
    for key, item in menu.items():
        print(f"{key}. {item['name']:<15} Rs.{item['price']}")
    print("A. Add New Item to Menu")
    print("S. Search Item")
    print("R. View Total Sales Report")  # NEW
    print("C. Checkout & Generate Bill")


def add_new_item():
    name = input("Enter new item name: ").title()
    try:
        price = float(input("Enter price: Rs."))
        new_id = str(len(menu) + 1)
        menu[new_id] = {"name": name, "price": price}
        print(f"{name} added successfully!")
    except ValueError:
        print("Invalid price entered.")


def search_item():
    keyword = input("Enter item name to search: ").lower()
    found = False
    for key, item in menu.items():
        if keyword in item["name"].lower():
            print(f"{key}. {item['name']} - Rs.{item['price']}")
            found = True
    if not found:
        print("Item not found.")


def calculate_total(order):
    subtotal = sum(menu[item]["price"] * qty for item, qty in order.items())
    discount = subtotal * DISCOUNT_RATE if subtotal >= DISCOUNT_THRESHOLD else 0
    after_discount = subtotal - discount
    tax = after_discount * TAX_RATE
    total = after_discount + tax
    return subtotal, discount, tax, total


def save_receipt(customer, table, order, subtotal, discount, tax, total):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = f"receipt_{customer.replace(' ', '_')}_{table}.txt"

    # 1. Save individual receipt
    with open(filename, "w") as f:
        f.write("=" * 45 + "\n")
        f.write(" FOODIE RESTAURANT - INVOICE\n")
        f.write("=" * 45 + "\n")
        f.write(f"Customer: {customer}\nTable No: {table}\nDate & Time: {timestamp}\n")
        f.write("-" * 45 + "\n")
        for item, qty in order.items():
            name = menu[item]["name"]
            price = menu[item]["price"]
            f.write(f"{name} x {qty} = Rs.{price * qty}\n")
        f.write("-" * 45 + "\n")
        f.write(
            f"Subtotal: Rs.{subtotal:.2f}\nDiscount: -Rs.{discount:.2f}\nTax: +Rs.{tax:.2f}\nTOTAL: Rs.{total:.2f}\n")
        f.write("=" * 45 + "\n")

    # 2. NEW: Append to master sales file
    with open(SALES_FILE, "a") as f:
        f.write(f"{timestamp} | Customer: {customer} | Table: {table} | Total: Rs.{total:.2f}\n")

    print(f"\nReceipt saved as '{filename}'")
    print(f"Sale added to total report.")


def view_total_sales():  # NEW FUNCTION
    print("\n" + "=" * 50)
    print(" TOTAL SALES REPORT")
    print("=" * 50)
    if not os.path.exists(SALES_FILE):
        print("No sales recorded yet.")
        return

    grand_total = 0
    with open(SALES_FILE, "r") as f:
        lines = f.readlines()
        for line in lines:
            print(line.strip())
            if "Total: Rs." in line:
                grand_total += float(line.split("Rs.")[1])

    print("-" * 50)
    print(f"GRAND TOTAL OF ALL BILLS: Rs.{grand_total:.2f}")
    print(f"TOTAL ORDERS: {len(lines)}")
    print("=" * 50)


def take_order():
    customer = input("Enter Customer Name: ")
    table = input("Enter Table No: ")
    order = {}

    while True:
        show_menu()
        choice = input("\nEnter choice: ").upper()

        if choice == "C":
            break
        elif choice == "A":
            add_new_item()
        elif choice == "S":
            search_item()
        elif choice == "R":  # NEW
            view_total_sales()
        elif choice in menu:
            try:
                qty = int(input(f"Enter quantity for {menu[choice]['name']}: "))
                if qty > 0:
                    order[choice] = order.get(choice, 0) + qty
            except ValueError:
                print("Please enter a valid number")
        else:
            print("Invalid choice. Try again.")

    if order:
        subtotal, discount, tax, total = calculate_total(order)
        print("\n" + "=" * 30)
        print(f"TOTAL: Rs.{total:.2f}")
        print("=" * 30)
        save_receipt(customer, table, order, subtotal, discount, tax, total)


def main():
    while True:
        take_order()
        again = input("\nTake another order? y/n: ").lower()
        if again != "y":
            print("Shutting down system. Goodbye!")
            break


if __name__ == "__main__":
    main()