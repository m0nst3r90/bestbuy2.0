from abc import ABC, abstractmethod

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from products import Product


class Promotion(ABC):
    """Promotion class"""

    def __init__(self, name: str):
        """Initialize the promotion"""
        self.name = name

    @abstractmethod
    def apply_promotion(self, product: Product, quantity: int) -> float:
        """Calculates the promotion for a product"""
        pass


class PercentDiscount(Promotion):
    """PercentDiscount class"""

    def __init__(self, name: str, percent: float):
        """Initialize the promotion with percent"""
        super().__init__(name)
        self.percent = percent

    @property
    def percent(self) -> float:
        """return percent"""
        return self._percent

    @percent.setter
    def percent(self, percent: float):
        """set percent"""
        self._percent = percent

    def apply_promotion(self, product, quantity) -> float:
        """Calculates the promotion for a product"""

        return (quantity * product.price) * (1 - self.percent / 100)


class SecondHalfPrice(Promotion):
    """SecondHalfPrice class"""

    def apply_promotion(self, product, quantity) -> float:
        """Calculates the promotion for a product"""
        price = product.price
        discounted = quantity // 2
        full_priced = quantity - discounted

        return full_priced * price + discounted * (price / 2)


class ThirdOneFree(Promotion):
    """ThirdOneFree class"""

    def apply_promotion(self, product, quantity) -> float:
        """Calculates the promotion for a product"""
        price = product.price
        discounted = quantity // 3
        full_priced = quantity - discounted

        return full_priced * price
