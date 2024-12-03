import pandas as pd
from pandas import ExcelWriter
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Load existing orders from Excel to determine starting order number
try:
    # Load the Excel file
    existing_orders = pd.read_excel("finalized_orders.xlsx", sheet_name="Orders")
    
    # Check if "Order#" column exists and has data
    if not existing_orders.empty and "Order#" in existing_orders.columns:
        # Find the maximum order number in the existing orders
        last_order_number = existing_orders["Order#"].max()
        order_number = last_order_number + 1  # Start from the next order number
    else:
        order_number = 1  # Start from 1 if no data found
except FileNotFoundError:
    # If the file does not exist, start from order number 1
    order_number = 1

orders = pd.DataFrame(columns=["Order#", "Item", "Quantity", "Price"])
current_order = []
total_price = 0.0

window = Tk()
window.title("Order Management System BY JULS ADRIATICO CUH")
canvas = Canvas(
    window,
    bg = "#F6F7FB",
    height = 700,
    width = 1000,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge",
)

items = {
    "CFOC": {"price": 145, "stock": 0, "original_stock": 0, "quantity": 0},
    "SR": {"price": 60, "stock": 0, "original_stock": 0, "quantity": 0},
    "WTN": {"price": 70, "stock": 0, "original_stock": 0, "quantity": 0},
    "WTCO": {"price": 40, "stock": 0, "original_stock": 0, "quantity": 0},
    "S": {"price": 25, "stock": 0, "original_stock": 0, "quantity": 0},
    "TH": {"price": 30, "stock": 0, "original_stock": 0, "quantity": 0},
    "MT": {"price": 60, "stock": 0, "original_stock": 0, "quantity": 0},
    "LIT": {"price": 30, "stock": 0, "original_stock": 0, "quantity": 0},
}

item_display_names = {
    "CFOC": "Chaofan w/ Orange C",
    "SR": "Siomai Rice",
    "WTN": "Wonton Noodles",
    "WTCO": "Wonton w/ Chili Oil",
    "S": "Shut yo BITCH ass up",
    "TH": "Tanghulu",
    "MT": "Milk Tea",
    "LIT": "Lemon Iced Tea",
}

customer_name_entry = Entry(
    window,
    bd=0,
    bg="#FFFFFF",
    highlightthickness=0,
    font=("Poppins Regular", 12)
)
customer_name_entry.place(
    x=100,  # Adjust x and y as per your UI design
    y=650,
    width=200,
    height=30
)
canvas.create_text(
    100,
    630,
    anchor="nw",
    text="Customer Name:",
    fill="#000000",
    font=("Poppins Regular", 12)
)


# Functions
            
def load_stock_from_excel(file_path, sheet_name="StockData"):
    try:
        # Read the stock data from the specified sheet
        stock_data = pd.read_excel(file_path, sheet_name=sheet_name)
        
        # Check if necessary columns exist
        if "Item" in stock_data.columns and "Stock" in stock_data.columns:
            for _, row in stock_data.iterrows():
                item_name = row["Item"]
                stock_value = row["Stock"]
                
                # Update the stock in the items dictionary
                if item_name in items:
                    items[item_name]["stock"] = stock_value
                    items[item_name]["original_stock"] = stock_value
                    update_stock_quantity_display(item_name)
                    print(f"Updated {item_name} stock to {stock_value}.")
                else:
                    print(f"Item '{item_name}' in Excel not found in application.")
        else:
            print("Excel sheet does not have 'Item' or 'Stock' columns.")
    except FileNotFoundError:
        print(f"File {file_path} not found.")
    except Exception as e:
        print(f"Error loading stock from Excel: {e}")

# Store canvas text IDs for stock and quantity for easy updates
stock_text_ids = {}
quantity_text_ids = {}

# Function to initialize stock and quantity display for all items
def initialize_stock_quantity_display():
    positions = {
        "CFOC": (100.0, 210.0, 116.0, 190.0),
        "SR": (100.0, 339.0, 116.0, 319.0),
        "WTN": (100.0, 468.0, 116.0, 448.0),
        "WTCO": (324.0, 210.0, 340.0, 190.0),
        "S": (324.0, 339.0, 340.0, 319.0),
        "TH": (324.0, 468.0, 340.0, 448.0),
        "MT": (543.0, 210.0, 559.0, 190.0),
        "LIT": (543.0, 339.0, 559.0, 319.0),
    }
    
    # Create text labels for each item
    for item_name, (stock_x, stock_y, qty_x, qty_y) in positions.items():
        stock_text_ids[item_name] = canvas.create_text(
            stock_x, stock_y, anchor="nw",
            text=f"Stock: {items[item_name]['stock']}",
            fill="#8E93A6", font=("Poppins Medium", 10 * -1)
        )
        quantity_text_ids[item_name] = canvas.create_text(
            qty_x, qty_y, anchor="nw",
            text=f"{items[item_name]['quantity']}",
            fill="#000000", font=("Kodchasan Regular", 10 * -1)
        )

        # Debug: Print to confirm the text was created
        print(f"Text for {item_name} created at ({stock_x}, {stock_y}) and ({qty_x}, {qty_y})")

# Function to update stock and quantity display for a specific item
def update_stock_quantity_display(item_name):
    # Update stock display
    canvas.itemconfig(
        stock_text_ids[item_name],
        text=f"Stock: {items[item_name]['stock']}"
    )
    # Update quantity display
    canvas.itemconfig(
        quantity_text_ids[item_name],
        text=f"{items[item_name]['quantity']}"
    )

    # Debug: Print to confirm the update
    print(f"Updated {item_name} stock to {items[item_name]['stock']} and quantity to {items[item_name]['quantity']}")

def update_order_display():
    canvas.itemconfig(
        order_number_label,
        text=f"Order # {order_number}"
    )

def update_total_price_display():
    total_price = sum(item['quantity'] * item['price'] for item in items.values())
    canvas.itemconfig(
        total_price_label,
        text=f"Total Price: ${total_price:.2f}"
    )
    print(f"Total Price updated: ${total_price:.2f}")

receipt_text_ids = {}  # Dictionary to store receipt text object IDs

def addItemInReceipt():
    ylevel = 120.0
    canvas.delete("receipt_text")  # Clear previous receipt entries

    for item_name, item_data in items.items():
        if item_data['quantity'] > 0:
            readable_name = item_display_names[item_name]  # Get readable name
            receipt_text = f"{item_data['quantity']}x {readable_name} : ₱{item_data['quantity'] * item_data['price']}\n"
            canvas.create_text(
                720.0,
                ylevel,
                anchor="nw",
                text=receipt_text,
                fill="#000000",
                font=("Poppins SemiBold", 14 * -1),
                tags="receipt_text"  # Use tags to group receipt entries
            )
            ylevel += 30.0

    # Add total price to the receipt
    total_price = sum(item['quantity'] * item['price'] for item in items.values())
    canvas.create_text(
        720.0,
        ylevel,
        anchor="nw",
        text=f"Total Price: ₱{total_price:.2f}\n",
        fill="#000000",
        font=("Poppins SemiBold", 16 * -1),
        tags="receipt_text"
    )

# Modify addEvent to update display dynamically
def addEvent(item_name):
    if item_name in items:
        available_stock = items[item_name]["stock"]
        
        # Check if there's enough stock to add 1 to the cart
        if available_stock > 0:
            # Increment the quantity by 1 and reduce the stock by 1
            items[item_name]["quantity"] += 1
            items[item_name]["stock"] -= 1
            print(f"Added 1 of {item_name}. New stock: {items[item_name]['stock']}, Quantity in cart: {items[item_name]['quantity']}")
            
            # Update the display
            update_stock_quantity_display(item_name)
            update_total_price_display()
            addItemInReceipt()  
        else:
            print(f"{item_name} is out of stock.")
    else:
        print("Item not found.")

def removeEvent(item_name):
    if item_name in items:
        available_quantity = items[item_name]["quantity"]
        
        # Check if item quantity is greater than 0
        if available_quantity > 0:
            # Increment the quantity by 1 and reduce the stock by 1
            items[item_name]["quantity"] -= 1
            items[item_name]["stock"] += 1
            print(f"Removed 1 of {item_name}. New stock: {items[item_name]['stock']}, Quantity in cart: {items[item_name]['quantity']}")
            
            # Update the display
            update_stock_quantity_display(item_name)
            update_total_price_display()
            addItemInReceipt()  
        else:
            print(f"You cannot remove {item_name}'s quantity below 0.")
    else:
        print("Item not found.")

def addOrder():
    global order_number, orders

    customer_name = customer_name_entry.get().strip()  # Get customer name
    if not customer_name:
        print("Customer name is required.")
        return

    if sum(item['quantity'] for item in items.values()) == 0:
        print("No items in cart. Cannot add order.")
        return

    total_order_price = 0.0
    rows_to_add = []

    for item_name, item_data in items.items():
        if item_data['quantity'] > 0:
            item_total = item_data['quantity'] * item_data['price']
            total_order_price += item_total
            rows_to_add.append({
                "Order#": order_number,
                "Item": item_name,
                "Quantity": item_data['quantity'],
                "Price": item_total,
                "Total Cost": "",
                "Customer Name": ""  # Add customer name
            })

            # Deduct stock
            item_data['original_stock'] -= item_data['quantity']

    # Set "Total Cost" only in the last item of the order
    if rows_to_add:
        rows_to_add[-1]["Total Cost"] = total_order_price
        rows_to_add[-1]["Customer Name"] = customer_name

    # Append rows to the DataFrame
    orders = pd.concat([orders, pd.DataFrame(rows_to_add)], ignore_index=True)

    # Save the updated orders DataFrame to Excel
    try:
        with pd.ExcelWriter("finalized_orders.xlsx", engine="openpyxl", mode="a", if_sheet_exists="overlay") as writer:
            orders.to_excel(writer, sheet_name="Orders", index=False, header=False, startrow=writer.sheets["Orders"].max_row)
    except Exception as e:
        print(f"Error saving orders to Excel: {e}")

    # Update stock in Excel
    try:
        stock_data = pd.DataFrame(
            {"Item": [item_name for item_name in items],
             "Stock": [items[item_name]["original_stock"] for item_name in items]}
        )
        with pd.ExcelWriter("finalized_orders.xlsx", engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
            stock_data.to_excel(writer, sheet_name="StockData", index=False)
        print("Stock updated in Excel.")
    except Exception as e:
        print(f"Error updating stock in Excel: {e}")

    # Increment the order number for the next order
    order_number += 1
    for item_name in items:
        items[item_name]['quantity'] = 0
        update_stock_quantity_display(item_name)

    update_total_price_display()
    update_order_display()
    canvas.delete("receipt_text")
    customer_name_entry.delete(0, 'end')  # Clear the name entry field


def clear_total_price_display():
    canvas.itemconfig(
        total_price_label,
        text=f"Total Price: ${total_price:.2f}"
    )

def clearSelection():
    global total_price
    for item_name, item_data in items.items():
        # Reset stock to original stock
        item_data["stock"] = item_data["original_stock"]
        # Reset quantity to 0
        item_data["quantity"] = 0
        # Update the display
        update_stock_quantity_display(item_name)
    print("All selections cleared and stocks reset to original values.")
    total_price = 0.0
    clear_total_price_display()
    print("All selections cleared, stocks reset, and total price updated.")


window.geometry("1000x700")
window.configure(bg = "#F6F7FB")

canvas.place(x = 0, y = 0)
canvas.create_text(
    39.0,
    20.0,
    anchor="nw",
    text="Order Management System",
    fill="#000000",
    font=("Poppins SemiBold", 16 * -1)
)

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    118.0,
    91.0,
    image=image_image_1
)

order_number_label = canvas.create_text(
    48.0,
    70.0,
    anchor="nw",
    text=f"Order # {order_number}",
    fill="#000000",
    font=("Kodchasan Regular", 14 * -1)
)

total_price_label = canvas.create_text(
    48.0,
    91.0,
    anchor="nw",
    text="Total Price: $0.00",                                                                                                                                                                                      
    fill="#000000",
    font=("Kodchasan Regular", 14 * -1)
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    818.0,
    290.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    817.0,
    109.0,
    image=image_image_3
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    127.0,
    192.0,
    image=image_image_4
)

image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(
    127.0,
    321.0,
    image=image_image_5
)

image_image_6 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(
    127.0,
    450.0,
    image=image_image_6
)

image_image_7 = PhotoImage(
    file=relative_to_assets("image_7.png"))
image_7 = canvas.create_image(
    351.0,
    192.0,
    image=image_image_7
)

image_image_8 = PhotoImage(
    file=relative_to_assets("image_8.png"))
image_8 = canvas.create_image(
    351.0,
    321.0,
    image=image_image_8
)

image_image_9 = PhotoImage(
    file=relative_to_assets("image_9.png"))
image_9 = canvas.create_image(
    351.0,
    450.0,
    image=image_image_9
)

image_image_10 = PhotoImage(
    file=relative_to_assets("image_10.png"))
image_10 = canvas.create_image(
    570.0,
    192.0,
    image=image_image_10
)

image_image_11 = PhotoImage(
    file=relative_to_assets("image_11.png"))
image_11 = canvas.create_image(
    570.0,
    321.0,
    image=image_image_11
)

### FOOD

canvas.create_text(
    40.0,
    158.0,
    anchor="nw",
    text="Chaofan w/ Orange Chicken",
    fill="#000000",
    font=("Kodchasan Regular", 13 * -1)
) 

canvas.create_text(
    83.0,
    287.0,
    anchor="nw",
    text="Siomai Rice",
    fill="#000000",
    font=("Kodchasan Regular", 14 * -1)
)

canvas.create_text(
    70.0,
    416.0,
    anchor="nw",
    text="Wonton Noodles",
    fill="#000000",
    font=("Kodchasan Regular", 14 * -1)
)

canvas.create_text(
    285.0,
    158.0,
    anchor="nw",
    text="Wonton w/ Chili Oil",
    fill="#000000",
    font=("Kodchasan Regular", 14 * -1)
)

canvas.create_text(
    324.0,
    287.0,
    anchor="nw",
    text="IGNOR",
    fill="#000000",
    font=("Kodchasan Regular", 14 * -1)
)

canvas.create_text(
    315.0,
    416.0,
    anchor="nw",
    text="Tanghulu",
    fill="#000000",
    font=("Kodchasan Regular", 14 * -1)
)

canvas.create_text(
    537.0,
    158.0,
    anchor="nw",
    text="Milk Tea",
    fill="#000000",
    font=("Kodchasan Regular", 14 * -1)
)

canvas.create_text(
    512.0,
    287.0,
    anchor="nw",
    text="Lemon Iced Tea",
    fill="#000000",
    font=("Kodchasan Regular", 14 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: addEvent("CFOC"),
    relief="flat"
)
button_1.place(
    x=159.0,
    y=186.0,
    width=24.0,
    height=24.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: addEvent("SR"),
    relief="flat"
)
button_2.place(
    x=159.0,
    y=315.0,
    width=24.0,
    height=24.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: addEvent("WTN"),
    relief="flat"
)
button_3.place(
    x=159.0,
    y=444.0,
    width=24.0,
    height=24.0
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: addEvent("WTCO"),
    relief="flat"
)
button_4.place(
    x=383.0,
    y=186.0,
    width=24.0,
    height=24.0
)

button_image_6 = PhotoImage(
    file=relative_to_assets("button_6.png"))
button_6 = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: addEvent("TH"),
    relief="flat"
)
button_6.place(
    x=383.0,
    y=444.0,
    width=24.0,
    height=24.0
)

button_image_7 = PhotoImage(
    file=relative_to_assets("button_7.png"))
button_7 = Button(
    image=button_image_7,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: addEvent("MT"),
    relief="flat"
)
button_7.place(
    x=600.0,
    y=186.0,
    width=24.0,
    height=24.0
)

button_image_8 = PhotoImage(
    file=relative_to_assets("button_8.png"))
button_8 = Button(
    image=button_image_8,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: addEvent("LIT"),
    relief="flat"
)
button_8.place(
    x=600.0,
    y=315.0,
    width=24.0,
    height=24.0
)

button_image_10 = PhotoImage(
    file=relative_to_assets("button_10.png"))
button_10 = Button(
    image=button_image_10,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: removeEvent("CFOC"),
    relief="flat"
)
button_10.place(
    x=59.0,
    y=186.0,
    width=24.0,
    height=24.0
)

button_image_11 = PhotoImage(
    file=relative_to_assets("button_11.png"))
button_11 = Button(
    image=button_image_11,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: removeEvent("SR"),
    relief="flat"
)
button_11.place(
    x=59.0,
    y=315.0,
    width=24.0,
    height=24.0
)

button_image_12 = PhotoImage(
    file=relative_to_assets("button_12.png"))
button_12 = Button(
    image=button_image_12,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: removeEvent("WTN"),
    relief="flat"
)
button_12.place(
    x=59.0,
    y=444.0,
    width=24.0,
    height=24.0
)

button_image_13 = PhotoImage(
    file=relative_to_assets("button_13.png"))
button_13 = Button(
    image=button_image_13,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: removeEvent("WTCO"),
    relief="flat"
)
button_13.place(
    x=283.0,
    y=186.0,
    width=24.0,
    height=24.0
)

button_image_15 = PhotoImage(
    file=relative_to_assets("button_15.png"))
button_15 = Button(
    image=button_image_15,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: removeEvent("TH"),
    relief="flat"
)
button_15.place(
    x=283.0,
    y=444.0,
    width=24.0,
    height=24.0
)

button_image_16 = PhotoImage(
    file=relative_to_assets("button_16.png"))
button_16 = Button(
    image=button_image_16,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: removeEvent("MT"),
    relief="flat"
)
button_16.place(
    x=502.0,
    y=186.0,
    width=24.0,
    height=24.0
)

button_image_17 = PhotoImage(
    file=relative_to_assets("button_17.png"))
button_17 = Button(
    image=button_image_17,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: removeEvent("LIT"),
    relief="flat"
)
button_17.place(
    x=502.0,
    y=315.0,
    width=24.0,
    height=24.0
)

button_image_19 = PhotoImage(
    file=relative_to_assets("button_19.png"))
button_19 = Button(
    image=button_image_19,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: addOrder(),
    relief="flat"
)
button_19.place(
    x=376.0,
    y=515.0,
    width=57.0,
    height=36.0
)

button_image_20 = PhotoImage(
    file=relative_to_assets("button_20.png"))
button_20 = Button(
    image=button_image_20,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: clearSelection(),
    relief="flat"
)
button_20.place(
    x=270.0,
    y=515.0,
    width=79.0,
    height=36.0
)

canvas.create_text(
    758.0,
    76.0,
    anchor="nw",
    text="Order Receipt",
    fill="#000000",
    font=("Poppins SemiBold", 16 * -1)
)

# Call initialize_stock_quantity_display after setting up the canvas
def period_update_stock():
    load_stock_from_excel("finalized_orders.xlsx", sheet_name="StockData")
    canvas.after(500, period_update_stock)

period_update_stock()
initialize_stock_quantity_display()
update_total_price_display()
update_order_display()

window.resizable(False, False)
window.mainloop()
