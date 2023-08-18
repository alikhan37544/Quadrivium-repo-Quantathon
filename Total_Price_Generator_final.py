import pandas as pd


df = pd.read_csv('file.csv')


item_data = {}
for index, row in df.iterrows():
    item_name = row['Name'].lower() 
    item_data[item_name] = {'price': row['Cost per Unit'], 'unit': 'unit'}  


selected_items = {}


try:
    saved_data = pd.read_csv('selected_items.csv')
    for index, row in saved_data.iterrows():
        selected_items[row['Item']] = row['Quantity']
except FileNotFoundError:
    pass


def display_and_select_items():
    print("Available items:")
    for item in item_data:
        print(f"{item.capitalize()} - ${item_data[item]['price']} per {item_data[item]['unit']}")

    while True:
        selected_item = input("Enter the name of the item you want to add (or 'done' to finish): ").lower()
        
        if selected_item == 'done':
            break
        
        if selected_item in item_data:
            while True:
                quantity = input(f"How many {item_data[selected_item]['unit']} of {selected_item.capitalize()} do you want? ")
                try:
                    quantity = int(quantity)
                    if quantity >= 0:
                        break
                    else:
                        print("Please enter a non-negative quantity.")
                except ValueError:
                    print("Invalid input. Please enter a valid quantity.")

            if selected_item in selected_items:
                selected_items[selected_item] += quantity
            else:
                selected_items[selected_item] = quantity
            print(f"{quantity} {item_data[selected_item]['unit']} of {selected_item.capitalize()} added to the list.")
        else:
            print("Invalid item name. Please enter a valid item.")


display_and_select_items()


total_value = sum(item_data[item]['price'] * quantity for item, quantity in selected_items.items())


print("\nYour Shopping List:")
for item, quantity in selected_items.items():
    print(f"{item.capitalize()}: {quantity} {item_data[item]['unit']}")

print(f"\nTotal estimated value of selected items: ${total_value}")


selected_items_df = pd.DataFrame(selected_items.items(), columns=['Item', 'Quantity'])
selected_items_df.to_csv('selected_items.csv', index=False)
