from promotions import Promotion


class Product:
    """Product class"""

    def __init__(self, name, price, quantity):
        """Initialize the product"""
        self.name: str = name
        self.price: float = price
        self.quantity: int = quantity
        self.active: bool = self.quantity > 0
        self._promotion: list[Promotion] = []

    @property
    def name(self):
        """Get the name of the product"""
        return self._name

    @name.setter
    def name(self, name):
        """
        Set the name of the product

        Raises:
            ValueError: If the name is not at least 1 character
        """
        if len(name.strip()) < 1:
            raise ValueError("Product name must be at least 1 characters")
        self._name = name

    @property
    def quantity(self):
        """Return the quantity of the product"""
        return self._quantity

    @quantity.setter
    def quantity(self, quantity):
        """Set the quantity of the product"""
        self._quantity = quantity

        if self._quantity <= 0:
            self.deactivate()

    @property
    def price(self):
        """Return the price of the product"""
        return self._price

    @price.setter
    def price(self, price):
        """
        Set the price of the product

        Raises:
            ValueError: If the price is too low
        """
        if price >= 0:
            self._price = price
        else:
            raise ValueError("Price is too low")

    def get_promotion(self) -> list[Promotion]:
        """Return the promotion of the product"""
        return self._promotion

    def set_promotion(self, promotion: Promotion | list[Promotion]):
        """Set the promotion of the product"""
        if not isinstance(promotion, list):
            promotion = [promotion]

        self._promotion = promotion

    def is_active(self):
        """Returns a bool indicating if the product is active"""
        return self.active

    def activate(self):
        """Activate the product"""
        self.active = True

    def deactivate(self):
        """Deactivate the product"""
        self.active = False

    def __str__(self):
        """Prints out the product"""
        promo_print = ""
        if self._promotion:
            promo_print = promo_print.join(f", {self._promotion}")
        return f"Physical Product -> Name: {self.name}, Price: {self.price}, Quantity: {self.quantity}{promo_print}"

    def __gt__(self, other):
        return self.price > other.price

    def __lt__(self, other):
        return self.price < other.price


    def buy(self, quantity) -> float:
        """
        Buy a quantity and return its price

        Raises:
            ValueError: If the quantity is too low or the product is not active
        """
        if not self.is_active():
            raise ValueError("Product is not active")

        if quantity > self._quantity:
            raise ValueError("Quantity is too high")
        total_price = 0
        if self._promotion:
            for promotion in self._promotion:
                total_price = promotion.apply_promotion(self, quantity)
        else:
            total_price = quantity * self.price

        self._quantity -= quantity
        if self._quantity <= 0:
            self.deactivate()
        return total_price


class LimitedProduct(Product):
    """Product class for limited products"""

    def __init__(self, name, price, quantity, maximum):
        """Initialize the product"""
        super().__init__(name, price, quantity)
        self.maximum = maximum

    @property
    def maximum(self):
        """Return the limit of the product"""
        return self._maximum

    @maximum.setter
    def maximum(self, maximum):
        """Set the limit of the product"""
        self._maximum = maximum

    def __str__(self):
        """Prints out the product"""
        print(f"Limited Product -> Name: {self.name}, Price: {self.price}, Quantity: {self.quantity}, Maximum: {self._maximum}")
        if self._promotion:
            print(f"Promotion: {self._promotion}")

    def buy(self, quantity) -> float:
        """
        Buy a quantity and return its price

        Raises:
            ValueError: If the Limit is reached
        """
        if quantity > self._maximum:
            raise ValueError("Limit is reached")

        return super().buy(quantity)


class NonStockedProduct(Product):
    """Product class for digital products"""

    def __init__(self, name, price):
        """Initialize the product"""
        super().__init__(name, price, 0)
        self.activate()

    def __str__(self):
        """Prints out the product"""
        print(f"Non stocked Product -> Name: {self.name}, Price: {self.price}, Quantity: Unlimited")
        if self._promotion:
            print(f"Promotion: {self._promotion}")

    def buy(self, quantity) -> float:
        """
        Buy a quantity and return its price

        Raises:
            ValueError: If the product is not active
        """
        if not self.is_active():
            raise ValueError("Product is not active")

        total_price = 0
        if self._promotion:
            for promotion in self._promotion:
                total_price = promotion.apply_promotion(self, quantity)
        else:
            total_price = quantity * self.price

        return total_price
