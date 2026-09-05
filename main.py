import os
import time

import promotions
import store
import products

# Colors for console output
YELLOW = '\033[33m'
GREEN = '\033[32m'
RED = '\033[31m'
BLUE = '\033[34m'
CYAN = '\033[36m'
RESET = '\033[0m'

# setup initial stock of inventory
product_list = [products.Product("MacBook Air M2", price=1450, quantity=100),
                products.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
                products.Product("Google Pixel 7", price=500, quantity=250)
                ]

product_list[0].set_promotion(promotions.PercentDiscount("20% OFF", 20))
product_list[0].set_promotion(promotions.ThirdOneFree("Third one free"))
product_list[0].set_promotion(promotions.SecondHalfPrice("Second 50% OFF", True))



best_buy = store.Store(product_list)


def main_menu():
    """Handles the main menu"""

    os.system("cls" if os.name == "nt" else "clear")
    print(f"{YELLOW}{'Store Menu':^30}\n{'----------':^30}{RESET}")
    print(f"{GREEN}1.{RESET} List all products in store")
    print(f"{GREEN}2.{RESET} Show total amount in store")
    print(f"{GREEN}3.{RESET} Make an order")
    print(f"{GREEN}4.{RESET} {RED}Quit{RESET}")

    return input(f"Please choose a {GREEN}number{RESET}: ")


def list_all_products_menu(menu_store):
    """Handles the list all products menu"""

    os.system("cls" if os.name == "nt" else "clear")
    print(f"{YELLOW}{'All Products':^30}\n{'------------':^30}{RESET}")
    handle_product_listing(menu_store, None, None)
    input(f"\nPress enter to go {GREEN}back{RESET}")


def show_total_amount_menu(menu_store):
    """Handles the total amount menu"""

    os.system("cls" if os.name == "nt" else "clear")
    print(f"{YELLOW}{'Total Amount in Store':^30}\n{'---------------------':^30}{RESET}")
    print(f"Total of {CYAN}{menu_store.get_total_quantity()}{RESET} items in store")

    input(f"\nPress enter to go {GREEN}back{RESET}")


def order_main_menu(menu_store, order, total_order_cost):
    """Handles the order main menu"""

    os.system("cls" if os.name == "nt" else "clear")
    print(f"{YELLOW}{'Order Menu':^30}\n{'----------':^30}{RESET}")
    handle_product_listing(menu_store, order, total_order_cost)

    print(f"\nWhen you want to finish order or leave, press {GREEN}enter{RESET}")
    print(f"Current cart: {BLUE}${calculate_total_order(order)}{RESET}")
    return input(f"\nWich product {GREEN}#{RESET} do you want? ")


def handle_product_listing(menu_store, order, choosen_product):
    """handles product listing printing"""
    for i, product in enumerate(menu_store.get_all_products()):
        cart_product_amount = 0
        is_product_chosen = product == choosen_product
        if order:
            for order_product, amount in order:
                if order_product == product:
                    cart_product_amount += amount
        print(
            f"{i + 1}. {YELLOW if is_product_chosen else ''}"
            f"{product.name:<26}{RESET if is_product_chosen else ''} "
            f"{BLUE}{'$':>2}{product.price:>6}{RESET}"
            f"{CYAN}{product.quantity:>10}{RESET} "
            f"{RED}{('- ' + str(cart_product_amount)) if cart_product_amount > 0 else ''}{RESET}"
            f"{YELLOW}\t{", ".join(str(promotion) for promotion in product.get_active_promotions())}{RESET}")


def calculate_total_order(order) -> float:
    """calculates and returns the total price in the order"""
    order_sum = 0
    for product, amount in order:
        if product.get_active_promotions():
            for promotion in product.get_active_promotions():
                order_sum += promotion.apply_promotion(product, amount)
        else:
            order_sum += (product.price * amount)
    return order_sum


def handle_cart(order, chosen_product, amount_input):
    """handles the cart loop"""
    total_order_amount = get_order_amount(order, chosen_product) + amount_input
    if 0 <= total_order_amount <= chosen_product.quantity:
        for i, (product, amount) in enumerate(order):
            if product == chosen_product:
                order[i] = (product, total_order_amount)
                break
        else:
            order.append((chosen_product, amount_input))
        print("Product added to list")
        time.sleep(1)
    else:
        print(f"{RED}Amount not available{RESET}")
        time.sleep(1)


def get_order_amount(order, product) -> int:
    """returns the amount of one specific product in the order"""
    return sum(amount for order_product, amount in order if order_product == product)


def handle_payment(active_store, order):
    """handles the payment"""
    print(f"Order made! Total payment: {BLUE}${active_store.order(order)}{RESET}")
    input(f"\nPress enter to go {GREEN}back{RESET}")
    order.clear()


def order_menu(menu_store):
    """Handles the order loop"""

    order: list[tuple[products.Product, int]] = []
    total_order_cost = 0

    while True:
        userinput = order_main_menu(menu_store, order, total_order_cost)
        try:
            userinput = int(userinput)
            if 0 < userinput < len(menu_store.get_all_products()) + 1:
                chosen_product = menu_store.get_all_products()[userinput - 1]
                os.system("cls" if os.name == "nt" else "clear")
                print(f"{YELLOW}{'Order Menu':^30}\n{'----------':^30}{RESET}")

                handle_product_listing(menu_store, order, chosen_product)

                print(f"\nChoosen Product: {YELLOW}{chosen_product.name}{RESET}")
                amount_input = int(input(f"\nWhat {CYAN}amount{RESET} do you want? "))

                if isinstance(amount_input, int):
                    handle_cart(order, chosen_product, amount_input)
                    print(order)

        except ValueError:
            if userinput == "":
                if len(order) < 1:
                    break
                handle_payment(menu_store, order)
                break


def start(start_store: store.Store):
    """Main application loop"""

    while True:
        should_exit = False
        while True:
            userinput = main_menu()
            if userinput == "1":
                list_all_products_menu(start_store)
                break
            if userinput == "2":
                show_total_amount_menu(start_store)
                break
            if userinput == "3":
                order_menu(start_store)
                break
            if userinput == "4":
                should_exit = True
                break
        if should_exit:
            break


start(best_buy)
