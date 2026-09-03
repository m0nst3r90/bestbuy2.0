class Product:
    """Product class"""
    def __init__(self, name, price, quantity):
        """Initialize the product"""
        self.name:str = name
        self.price:float = price
        self.quantity:int = quantity
        self.active:bool = self.quantity > 0

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

    def is_active(self):
        """Returns a bool indicating if the product is active"""
        return self.active

    def activate(self):
        """Activate the product"""
        self.active = True

    def deactivate(self):
        """Deactivate the product"""
        self.active = False

    def show(self):
        """Prints out the product"""
        print(f"Name: {self.name}, Price: {self.price}, Quantity: {self.quantity}")

    def buy(self, quantity) -> float:
        """
        Buy a quantity and return its price

        Raises:
            ValueError: If the quantity is too low or the product is not active
        """
        if not self.is_active():
            raise ValueError("Product is not active")

        if quantity > self.quantity:
            raise ValueError("Quantity is too high")

        self.quantity -= quantity
        if self.quantity <= 0:
            self.deactivate()
        return quantity * self.price
