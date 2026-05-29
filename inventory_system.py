from datetime import datetime
import os
import json
import subprocess

INVENTORY_FILE = "store_inventory.json"
SALES_FILE = "sales_history.json"

def main():
    inventory,sales = load_data()
    while True:
        subprocess.run("cls",shell=True)
        print("What do you want to do?")
        print("")
        print("1. View Inventory")
        print("2. Add or restock items")
        print("3. Sell items and update stock")
        print("4. Check stocks")
        print("5. Save and load inventory data")
        print("6. Delete save file")
        print("7. Exit")
        print("")
        condition = input("Choose 1-7: ")

        if condition.lower() == "7":
            break
        elif condition.lower() == "1":
            display_item(inventory)
        elif condition.lower() == "2":
            add_item(inventory)
        elif condition.lower() == "3":
            sell_item(inventory,sales)
        elif condition.lower() == "4":
            check_stocks(inventory)
        elif condition.lower() == "5":
            save_data(inventory,sales)
        elif condition.lower() == "6":
            delete_save()
        else:
            print("Invalid Input")

def continue_indicator():
    i = input("Press any key to continue...")

def display_item(inventory):
    subprocess.run("cls",shell=True)
    if inventory:
        for item, info in inventory.items():
            print(f"{item}: 'qty' = {info["qty"]}, 'price' = {info["price"]},'stocks' = {info["stocks"]}, 'max_restock' = {info["max_restock"]}")
    else:
        print("File does not exist")
        print("Please create an inventory first")
    continue_indicator()
    subprocess.run("cls",shell=True)
    
def add_item(inventory):
    subprocess.run("cls",shell=True)
    print("What do you want to do?")
    print("")
    print("1. Add an item")
    print("2. Restock")
    what = input("Choose 1-2: ")
    if what.lower() == "1":
        item = input("What item? ")
        if item not in inventory:
            add_quantity = int(input("How many quantity? "))
            add_price = int(input("How much? "))
            max_restock = int(input("How many for max restocking? "))
            stocks = add_quantity * add_price
            inventory[item] = {"qty":add_quantity, "price":add_price, 
                                    "stocks":stocks, "max_restock":max_restock}
            print(f"'{item}' was succesfully added.")
        else:
            print(f"'{item}' is already on the inventory")
        continue_indicator()
    elif what.lower() == "2":
        print("What do you want to do?")
        print("")
        print("1. Restock all")
        print("2. Restock an item")
        restock = input("What item? ")
        if inventory:
            if restock == "1":
                for item, info in inventory.items():
                    inventory[item]["qty"] += int(inventory[item]["max_restock"] - inventory[item]["qty"])
                    print(f"'{item}' was succesfully added.")
            elif restock == "2":
                item = input("What item? ")
                inventory[item]["qty"] += int(inventory[item]["max_restock"] - inventory[item]["qty"])
                print(f"'{item}' was succesfully added.")
            else:
                print("Invalid Input")
            
        else:
            print("File does not exist")
            print("Please create an inventory first")
        continue_indicator()
    else:
        print("Invalid Input")

    for item, info in inventory.items():
        print(f"{item}: {info["qty"]}")
    subprocess.run("cls",shell=True)

def sell_item(inventory,sales):
    subprocess.run("cls",shell=True)
    name = input("What item do you want to sell? ")
    if name not in inventory:
        print("Item not found.")
        continue_indicator()
        return
    qty = int(input("How many items do you want to sell? "))
    item = inventory[name]
    item = inventory[name]
    if item["qty"] < qty:
        print(f"Not enough stocks available: {item['qty']}")
        continue_indicator()
        return
    total = f"$ {item["price"] * qty}"
    item["qty"] -= qty
    sale = {
        "date": datetime.now().isoformat(),
        "item": item,
        "qty": qty,
        "total": total,
    }
    sales.append(sale)

def check_stocks(inventory):
    for name, data in inventory.items():
        if data["qty"] <= 5:
            print(f"⚠️  {name}: low stock (Available Items: {data['qty']})")
        else:
            print(f"✅ {name}: okay (Available Items: {data['qty']})")
    continue_indicator()

def save_json(filename, data):
    with open(filename,"w") as file:
        json.dump(data,file,indent=2)

def save_data(inventory,sales):
    subprocess.run("cls",shell=True)
    save_json(INVENTORY_FILE, inventory)
    save_json(SALES_FILE, sales)
    print("Saved successfully")
    continue_indicator()

def load_json(filename, default):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            return json.load(file)
    return default

def load_data():
    subprocess.run("cls",shell=True)
    inventory = load_json(INVENTORY_FILE, {})
    sales = load_json(SALES_FILE, [])
    return inventory,sales

def delete_save():
    subprocess.run("cls",shell=True)
    print("What do you want to do delete?")
    print("")
    print("1. Delete Inventory")
    print("2. Delete Sales History")
    file_dict = {
        "1" : INVENTORY_FILE,
        "2" : SALES_FILE
    }
    file_name = input("Choose 1-2: ")
    script_dir = os.path.dirname(os.path.abspath(file_dict[file_name]))
    file_path = os.path.join(script_dir,file_dict[file_name])
    subprocess.run("cls",shell=True)
    try: 
        os.remove(file_path)
        print(f"Successfully deleted: {file_path}")
    except:
        print(f"File does not exist at: {file_path}")
    continue_indicator()

main()