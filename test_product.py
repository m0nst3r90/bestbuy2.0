import pytest

from products import Product


def test_create_product():
    """Test creating a product"""
    test_product = Product("Name", 100,0)

    assert test_product.name == "Name"
    assert test_product.price == 100
    assert test_product.quantity == 0
    assert test_product.is_active() == False

def test_create_invalid_product():
    """Test creating a product with invalid name and price"""
    with pytest.raises(ValueError):
        Product("", -1,0)

def test_product_gets_inactive():
    """Test getting inactive product after reaching 0 quantity"""
    test_product = Product("Name", 100,1)
    assert test_product.is_active() == True
    test_product.quantity = 0
    assert test_product.is_active() == False

def test_buy_product():
    """Test buying product and checking correct return of price"""
    test_product = Product("Name", 100,10)
    test_return = test_product.buy(5)
    print(test_return)
    assert test_return == 500
    assert test_product.quantity == 5

def test_buy_to_many_products():
    """Test buying more than the available quantity"""
    test_product = Product("Name", 100,10)
    with pytest.raises(ValueError):
        test_product.buy(20)

