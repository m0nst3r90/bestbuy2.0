from products import Product


class Store:
    """Store class"""

    def __init__(self, products: list[Product]):
        """Initialize the store"""
        self.products: list[Product] = products

    def __contains__(self, item):
        return item in self.products

    def __add__(self, other):
        return Store(self.products + other.products)

    def add_product(self, product: Product):
        """Add a product to the store"""
        self.products.append(product)

    def remove_product(self, product: Product):
        """Remove a Product from the store"""
        self.products.remove(product)

    def get_total_quantity(self) -> int:
        """Get the total quantity from all products of the store"""
        total_quantity: int = 0
        for product in self.products:
            total_quantity += product.quantity
        return total_quantity

    def get_all_products(self) -> list[Product]:
        """Get all active products from the store"""
        return [product for product in self.products if product.is_active()]

    @staticmethod
    def order(shopping_list: list[tuple[Product, int]]) -> float:
        """Order the shopping list

        Returns: the total price of the shopping list"""

        order_total: float = 0
        for product, quantity in shopping_list:
            try:
                order_total += product.buy(quantity)
            except ValueError as error:
                print(error)
        return order_total
