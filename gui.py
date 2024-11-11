import pandas as pd
from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"L:\Louis\Documents\tkinter\build\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

orders = pd.DataFrame(columns=["Order#", "Item", "Quantity", "Price"])
current_order = []
order_number = 1

window = Tk()
canvas = Canvas(
    window,
    bg = "#F6F7FB",
    height = 700,
    width = 1000,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

items = {
    "Sisig": {"price": 5.0, "stock": 5, "quantity": 0},
    "Bulalo": {"price": 10.0, "stock": 10, "quantity": 0},
    "Chicken": {"price": 7.0, "stock": 15, "quantity": 0},
    "Pork": {"price": 70.0, "stock": 20, "quantity": 0},
    "Beef": {"price": 100.0, "stock": 25, "quantity": 0},
    "Cookies": {"price": 20.0, "stock": 30, "quantity": 0},
    "Wonton": {"price": 85.0, "stock": 35, "quantity": 0},
    "Chowfan": {"price": 80.0, "stock": 40, "quantity": 0},
    "Fried Rice": {"price": 75.0, "stock": 45, "quantity": 0},
}


##### TODO: make functions

# Store canvas text IDs for stock and quantity for easy updates
stock_text_ids = {}
quantity_text_ids = {}

# Function to initialize stock and quantity display for all items
def initialize_stock_quantity_display():
    positions = {
        "Sisig": (100.0, 210.0, 116.0, 190.0),
        "Bulalo": (100.0, 339.0, 116.0, 319.0),
        "Chicken": (100.0, 468.0, 116.0, 448.0),
        "Pork": (324.0, 210.0, 340.0, 190.0),
        "Beef": (324.0, 339.0, 340.0, 319.0),
        "Cookies": (324.0, 468.0, 340.0, 448.0),
        "Wonton": (543.0, 210.0, 559.0, 190.0),
        "Chowfan": (543.0, 339.0, 559.0, 319.0),
        "Fried Rice": (543.0, 468.0, 559.0, 448.0),
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
        else:
            print(f"{item_name} is out of stock.")
    else:
        print("Item not found.")


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

canvas.create_text(
    48.0,
    70.0,
    anchor="nw",
    text="Order # 5",
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

# Call initialize_stock_quantity_display after setting up the canvas
initialize_stock_quantity_display()

canvas.create_text(
    758.0,
    76.0,
    anchor="nw",
    text="Pending Orders",
    fill="#000000",
    font=("Poppins SemiBold", 16 * -1)
)

canvas.create_text(
    783.0,
    129.0,
    anchor="nw",
    text="Order # 5",
    fill="#000000",
    font=("Kodchasan Regular", 14 * -1)
)

canvas.create_text(
    783.0,
    166.0,
    anchor="nw",
    text="Order # 69",
    fill="#000000",
    font=("Kodchasan Regular", 14 * -1)
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

image_image_12 = PhotoImage(
    file=relative_to_assets("image_12.png"))
image_12 = canvas.create_image(
    570.0,
    450.0,
    image=image_image_12
)


### FOOD

canvas.create_text(
    104.0,
    158.0,
    anchor="nw",
    text="Sisig",
    fill="#000000",
    font=("Kodchasan Regular", 14 * -1)
) 

canvas.create_text(
    104.0,
    287.0,
    anchor="nw",
    text="Sisig",
    fill="#000000",
    font=("Kodchasan Regular", 14 * -1)
)

canvas.create_text(
    104.0,
    416.0,
    anchor="nw",
    text="Sisig",
    fill="#000000",
    font=("Kodchasan Regular", 14 * -1)
)

canvas.create_text(
    328.0,
    158.0,
    anchor="nw",
    text="Sisig",
    fill="#000000",
    font=("Kodchasan Regular", 14 * -1)
)

canvas.create_text(
    328.0,
    287.0,
    anchor="nw",
    text="Sisig",
    fill="#000000",
    font=("Kodchasan Regular", 14 * -1)
)

canvas.create_text(
    328.0,
    416.0,
    anchor="nw",
    text="Sisig",
    fill="#000000",
    font=("Kodchasan Regular", 14 * -1)
)

canvas.create_text(
    547.0,
    158.0,
    anchor="nw",
    text="Sisig",
    fill="#000000",
    font=("Kodchasan Regular", 14 * -1)
)

canvas.create_text(
    547.0,
    287.0,
    anchor="nw",
    text="Sisig",
    fill="#000000",
    font=("Kodchasan Regular", 14 * -1)
)

canvas.create_text(
    547.0,
    416.0,
    anchor="nw",
    text="Sisig",
    fill="#000000",
    font=("Kodchasan Regular", 14 * -1)
)


button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: addEvent("Sisig"),
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
    command=lambda: addEvent("Bulalo"),
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
    command=lambda: addEvent("Chicken"),
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
    command=lambda: addEvent("Pork"),
    relief="flat"
)
button_4.place(
    x=383.0,
    y=186.0,
    width=24.0,
    height=24.0
)

button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: addEvent("Beef"),
    relief="flat"
)
button_5.place(
    x=383.0,
    y=315.0,
    width=24.0,
    height=24.0
)

button_image_6 = PhotoImage(
    file=relative_to_assets("button_6.png"))
button_6 = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: addEvent("Cookies"),
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
    command=lambda: addEvent("Wonton"),
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
    command=lambda: addEvent("Chowfan"),
    relief="flat"
)
button_8.place(
    x=600.0,
    y=315.0,
    width=24.0,
    height=24.0
)

button_image_9 = PhotoImage(
    file=relative_to_assets("button_9.png"))
button_9 = Button(
    image=button_image_9,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: addEvent("Fried Rice"),
    relief="flat"
)
button_9.place(
    x=600.0,
    y=444.0,
    width=24.0,
    height=24.0
)

button_image_10 = PhotoImage(
    file=relative_to_assets("button_10.png"))
button_10 = Button(
    image=button_image_10,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_10 clicked"),
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
    command=lambda: print("button_11 clicked"),
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
    command=lambda: print("button_12 clicked"),
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
    command=lambda: print("button_13 clicked"),
    relief="flat"
)
button_13.place(
    x=283.0,
    y=186.0,
    width=24.0,
    height=24.0
)

button_image_14 = PhotoImage(
    file=relative_to_assets("button_14.png"))
button_14 = Button(
    image=button_image_14,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_14 clicked"),
    relief="flat"
)
button_14.place(
    x=283.0,
    y=315.0,
    width=24.0,
    height=24.0
)

button_image_15 = PhotoImage(
    file=relative_to_assets("button_15.png"))
button_15 = Button(
    image=button_image_15,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_15 clicked"),
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
    command=lambda: print("button_16 clicked"),
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
    command=lambda: print("button_17 clicked"),
    relief="flat"
)
button_17.place(
    x=502.0,
    y=315.0,
    width=24.0,
    height=24.0
)

button_image_18 = PhotoImage(
    file=relative_to_assets("button_18.png"))
button_18 = Button(
    image=button_image_18,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_18 clicked"),
    relief="flat"
)
button_18.place(
    x=502.0,
    y=444.0,
    width=24.0,
    height=24.0
)

button_image_19 = PhotoImage(
    file=relative_to_assets("button_19.png"))
button_19 = Button(
    image=button_image_19,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_19 clicked"),
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
    command=lambda: print("button_20 clicked"),
    relief="flat"
)
button_20.place(
    x=270.0,
    y=515.0,
    width=79.0,
    height=36.0
)

button_image_21 = PhotoImage(
    file=relative_to_assets("button_21.png"))
button_21 = Button(
    image=button_image_21,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_21 clicked"),
    relief="flat"
)
button_21.place(
    x=876.0,
    y=128.0,
    width=24.0,
    height=24.0
)

button_image_22 = PhotoImage(
    file=relative_to_assets("button_22.png"))
button_22 = Button(
    image=button_image_22,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_22 clicked"),
    relief="flat"
)
button_22.place(
    x=876.0,
    y=165.0,
    width=24.0,
    height=24.0
)

button_image_23 = PhotoImage(
    file=relative_to_assets("button_23.png"))
button_23 = Button(
    image=button_image_23,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_23 clicked"),
    relief="flat"
)
button_23.place(
    x=723.0,
    y=126.0,
    width=49.0,
    height=27.0
)

button_image_24 = PhotoImage(
    file=relative_to_assets("button_24.png"))
button_24 = Button(
    image=button_image_24,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_24 clicked"),
    relief="flat"
)
button_24.place(
    x=723.0,
    y=163.0,
    width=49.0,
    height=27.0
)

image_image_13 = PhotoImage(
    file=relative_to_assets("image_13.png"))
image_13 = canvas.create_image(
    287.0,
    626.0,
    image=image_image_13
)

canvas.create_text(
    57.0,
    577.0,
    anchor="nw",
    text="Completed Order # 10",
    fill="#000000",
    font=("Kodchasan Regular", 14 * -1)
)

canvas.create_text(
    57.0,
    604.0,
    anchor="nw",
    text="Completed Order # 69",
    fill="#000000",
    font=("Kodchasan Regular", 14 * -1)
)
window.resizable(False, False)
window.mainloop()
