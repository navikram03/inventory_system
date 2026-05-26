import os
import json
import subprocess


inventory = {
    "laundry soap": {"qty":10, "price":12.00},
    "cigarettes": {"qty":30, "price":17.00},
    "candy": {"qty":20, "price":34.00},
    "instant noodles": {"qty":15, "price":23.00},
    "softdrinks": {"qty":25, "price":51.00},
}
restock_list = {
    "laundry soap": 20,
    "cigarettes": 30,
    "candy": 40,
    "instant noodles": 20,
    "softdrinks": 25,
}

begin_inventory = False

def inventory_checker():
    while True:
        condition = input(">>>What do you want to do? 'create', 'load', 'delete'" \
        " inventory? ")
        subprocess.run("cls", shell=True)
        
        if condition.lower() == "exit":
            break
        elif condition.lower() == "create":
            what = input(">>>What do you want to do? display, add, sell, " \
            "check, total, sort, restock, save: ")
            try:
                globals()[f"{what.lower()}_item"]()
            except:
                print("Invalid Input")
        elif condition.lower() == "load":
            load_save()
        elif condition.lower() == "delete":
            delete_save()
        else:
            print("Invalid Input")
        
def display_item():
    what = input("inventory or restock? ")
    if what == "inventory":
        for item, info in inventory.items():
            print(f"{item}: {info["qty"]} out of {restock_list[item]}")
    else:
        for item in restock_list.items():
            print(f"{item}: {info}")

def add_item():
    new_item = input("Add item: ")  
    add_quantity = int(input("How many quantity? "))
    add_price = int(input("How much? "))
    inventory[new_item] = {"qty":add_quantity, "price":add_price}
    print(inventory)

def sell_item():
    sell_item = input("What item do you want to sell? ")
    sell_quantity = int(input("How many items do you want to sell? "))
    inventory[sell_item]["qty"] -= sell_quantity
    print(f"You now only have {inventory[sell_item]["qty"]} for the item '{sell_item}'")

def check_item():
    check_item = input("What item do you want to check? ")
    print(f"{check_item} has {inventory[check_item]["qty"]} qty, {inventory[check_item]["qty"]} price")

def total_item():
    arr = []
    for each in inventory:
        arr.append((inventory[each]["qty"]) *(inventory[each]["price"]))
    print(f"There is a total of ${sum(arr)} for all items")

def sort_item():
    for i, i2 in inventory.items():
        sorted_arr = dict(sorted(i2.items(), key=lambda item:item[1]))
        print(f"{i}: {sorted_arr}")

def restock_item():
    what = input("all or specific? ")
    if what == "all":
        for i,i2 in inventory.items():
            inventory[i]["qty"] += int(restock_list[i] - inventory[i]["qty"])
    else:
        item = input("What item? ")
        inventory[item]["qty"] += (restock_list[item] - inventory[item]["qty"])
    for item, info in inventory.items():
        print(f"{item}: {info["qty"]}")

def save_item():
    file_name = input("What is the file name? ")
    with open(f"{file_name}.json","w") as file:
        json.dump(inventory,file,indent=2)
        print(f"Saved successfully with file name '{file_name}'")

def load_save():
    file_name = input("What is the file name? ")
    try:
        with open(f"{file_name}.json","r") as file:
            inventory = json.load(file)
            print(json.dumps(inventory, indent=2))
    except FileNotFoundError:
        print("File does not exist")

def delete_save():
    file_name = input("What is the file name? ")
    script_dir = os.path.dirname(os.path.abspath(file_name))
    file_path = os.path.join(script_dir,f"{file_name}.json")
    try: 
        os.remove(file_path)
        print(f"Successfully deleted: {file_path}")
    except:
        print(f"File does not exist at: {file_path}")

inventory_checker()