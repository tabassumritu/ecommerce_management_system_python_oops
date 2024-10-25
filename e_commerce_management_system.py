from enum import Enum

class UserRole(Enum):
    CUSTOMER = "customer"
    ADMIN = "admin"
    VENDOR = "vendor"
    
class OrderStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    
class PaymentStatus(Enum):
    PENDING ="pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"
    
class PaymentMethod(Enum):
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    NET_BANKING = "net_banking"
    WALLET = "wallet"
    

import uuid
import hashlib
from typing import List, Optional, Dict

class Category:
    def __init__(self, name:str, description:str):
        self.id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.subcategories: List["Category"] = []
        self.parent: Optional["Category"] = None
        
    def add_subcategory(self, category:"Category"):
        category.parent = self
        self.subcategories.append(category)
        
    def get_full_path(self) -> str:
        if self.parent:
            return f'{self.parent.get_full_path()} > {self.name}'
        return self.name
    

class User:
    def __init__(self, username: str, email: str, password: str, role: UserRole = UserRole.CUSTOMER):
        self.id = str(uuid.uuid4())
        self.username = username
        self.email = email
        self._password_hash = self._hash_password(password) 
        self.role = role
        self.address: List[Address] = []
        self.cart: Cart = Cart(self)
        self.wishlit: List[Product] = []
        self.orders: List[Order] = []
        
    def _hash_password(self,password: str) ->str:
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password: str) -> bool:
        return self._password_hash == self._hash_password(password)
    
    def add_address(self,address: "Address"):
        self.address.append(address)
        
    def add_to_wishlist(self, product: "Product"):
        if product not in self.wishlist:
            self.wishlist.append(product)
            
    def remove_from_wishlist(self, product: "Product"):
        if product in self.wishlist:
            self.wishlist.remove(product)
            
            
            
class Address:
    def __init__(self, street: str, city: str, state: str, postal_code: str, country:str):
        self.id = str(uuid.uuid4())
        self.street = street
        self.city = city
        self.state = state
        self.postal_code = postal_code
        self.country = country
        
    def __str__(self) -> str:
        return f'{self.street}, {self.city}, {self.state}, {self.postal_code}, {self.country}'
    
class Product:
    def __init__(self, name: str, description:str, price:float, category: Category, vendor: User):
        self.id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self._price = price
        self.category= category
        self.vendor = vendor
        self.stock_quantity = 0
        self.reviews: List[Review] = []
        self.image: List[str] = []
        self.specification: Dict[str, str] = {}
        self.is_active = True
        
    @property
    def price(self)-> float:
        return self._price
    
    @price.setter
    def price(self, value : float):
        if value< 0:
            raise ValueError("Price cannot be negative")
        self._price = value
        
    def add_stock(self, quantity: int):
        if quantity < 0:
            raise ValueError("Quantity cannot be negative")
        self.stock_quantity += quantity
        
    def remove_stock(self, quantity: int) -> bool:
        if quantity <= self.stock_quantity:
            self.stock_quantity -= quantity
            return True
        return False
            
    
    
    def add_specification(self, key: str, value: str):
        self.specification[key] = value



    
    

import datetime
class Review:
    
    def __init__(self, user: User, product: Product, rating: int, comment:str):
        
        self.id = str(uuid.uuid4())
        self.user = user
        self. product = self.rating = min(max(rating, 1) , 5)
        self. comment = comment
        self.timestamp = datetime.now()
        
        
class  CartItem:
    def __init__(self, product: Product, quantity: int):
        self.product = product
        self._quantity = quantity
        
    @property 
    def quantity(self) -> int:
        return self._quantity
    
    @quantity.setter 
    def quantity(self, value : int):
        if value < 0:
            raise ValueError("Quantity cannot be negative")
        if value > self.product.stock_quantity:
            raise ValueError("Quantity cannot be exceed available stock")
            
        self._quantity = value
        
    @property 
    def subtotal(self)-> float:
        return self.product.price * self.quantity
        
    
    
        
    
class Cart:
    def __init__(self, user: User):
        self.user = user 
        self.items: List(CartItem)= []
        
    def add_item(self, product: Product, quantity: int = 1) -> bool:
        if product.stock_quantity < quantity:
            return False
        
        existing_item = next((item for item in self.items if item.product == product), None)
    
        if existing_item:
            existing_item.quantity += quantity
        else:
            self.items.append(CartItem(product, quantity))
        return True
    
    def remove_item(self, product: Product):
        self.items = [item for item in self.items if item.product != product]
        
        
    def update_quantity(self, product:Product, quantity : int)-> bool:
        item = next((item for item in self.items if item.product == product), None)
        
        if item:
            try:
                item.quantity = quantity
                return True
            except ValueError:
                return False
            return False
        
    
    def clear(self):
        self.items.clear()
        
        
    @property 
    def total(self)-> float:
        return sum(item.subtotal for item in self.items)
        


from abc import ABC, abstractmethod

class PaymentProcessor(ABC):

    @abstractmethod 
    def process_payment(self, amount: float, payment_info: Dict) -> bool:
        pass
    @abstractmethod 
    def refund_payment(self, amount: float, payment_info: Dict) -> bool:
        pass  
    


import re
class CreditCardProcessor(PaymentProcessor):
    def process_payment(self, amount: float, payment_info:Dict) -> bool:
        
        card_number = payment_info.get('card_number')
        if not card_number or not self._validate_card_number(card_number):
            return False
        return True
    
    def refund_payment(self, amount: float, payment_info:Dict) -> bool:
        return True
    
    def _validate_card_number(self, card_number: str) -> bool:
        return bool(re.match(r'^\d{16}$', card_number))
        
    

class Order:
    
    def __init__(self, user:User, shipping_address: Address):
        self.id = str(uuid.uuid4())
        self.user = user
        self.items: List[CartItem] = []
        self.shipping_address = shipping_address
        self.order_date = datetime.datetime.now()
        self.status = OrderStatus.PENDING
        self.payment_method: Optional[PaymentMethod] = None
        self.shipping_cost = 0.0
        self.tracking_number: Optional[str] = None
        
        
    @property 
    def subtotal(self) -> float:
        return sum(item.subtotal for item in self.items)
    
    @property 
    def total(self) -> float:
        return self.subtotal + self.shipping_cost
    
    
    def add_tracking_number(self, tracking_number: str):
        self.tracking_number = tracking_number
        self.status = OrderStatus().SHIPPED
        
    
    def cancel_order(self) -> bool:
        if self.status in [OrderStatus.PENDING, OrderStatus.CONFIRMED]:
            self.status = OrderStatus.CANCELLED
            
            
            for item in self.items:
                item.product.add_stock(item.quantity)
            return True
        return False
    
    


class EcommerceSystem:
    def __init__(self):
        self.users: List[User] = []
        self.products: List[Product] = [] 
        self.categories: List[Category] = []
        self.orders: List[Order] = []
        self.payment_processors: Dict[PaymentMethod, PaymentProcessor] = {
            PaymentMethod. CREDIT_CARD: CreditCardProcessor()
            }
    
    def register_user(self, username: str, email: str, password: str, role: UserRole) -> User:
        
        
        if any(user.email == email for user in self.users): 
            raise ValueError( "Email already registered")
            
        if any(user.username == username for user in self.users):
            raise ValueError(" Username already taken")
            
        user = User(username, email, password, role)
        self.users.append(user)
        
        
        return user
    def create_order(self, user: User, shipping_address: Address) -> Optional[Order]:
        if not user.cart.items:
            return None
        
        for cart_item in user.cart.items:
            if cart_item.quantity > cart_item.product.stock_quantity:
                return None
            
        order = Order(user, shipping_address)
        order.items = user.cart.items.copy()
        
        for item in order.items:
            item.product.remove_stock(item.quantity)
            
        
        #claer cart
        user.cart.clear()
        
        #add ord4ers to system and user
        
        self.orders.append(order)
        user.orders.append(order)
        
        return order 
    
    
    def process_payment(self, order: Order, payment_method: PaymentMethod, payment_info: Dict) -> bool:
        process = self.payment_processors.get(payment_method)
        
        if not process:
            return False
        
        if process.process_payment(order.total, payment_info):
            order.payment_status = PaymentStatus.COMPLETED
            order.status = OrderStatus.CONFIRMED
            order.payment_method = payment_method
            
            return True
    
        order.payment_method = PaymentStatus.FAILED
        return False
    
    def search_products(self, query: str, category: Optional[Category] = None) -> List[Product]:
        results = []
        for product in self.products:
            if(query.lower() in product.name.lower() or query.lower() in product.description.lower()):
                results.append(product)
                
                
        return results
    
def main():
    system= EcommerceSystem()
    
    #create categories
    electronics = Category("Electronics", "Electronics Device and accessories")
    phones = Category("Phone", "Mobile phones and accessories")
    electronics.add_subcategory(phones)
    system.categories.extend([electronics, phones])
    
    #register users
    admin = system.register_user('John', 'John@example.com', '123456', UserRole.ADMIN)
    vendor = system.register_user('Doe', 'Doe@example.com', '123456', UserRole.VENDOR)
    customer = system.register_user('Doe2', 'Doe2@example.com', '123456', UserRole.CUSTOMER)
    
    
    print(f'Users: {admin.username}, {vendor.username}, {customer.username}' )
    
    for category in system.categories:
        print(f'{category.name}')
        
        
    
    #add products
    print("==================adding product===================")
    Iphone_x = Product("Iphone X", "Latest Iphone Model", 999.99, phones, vendor)
    Iphone_x.add_stock(10)
    Iphone_x.add_specification("screen size", "6 inch")
    Iphone_x.add_specification("storage size", "128gb")
    system.products.append(Iphone_x)
    
    #add address
    print("==================adding address===================")
    customer.add_address(Address("123 street", 'ctg', 'state', '4212', 'Bangladesh'))
    
    #adding product to customer cart
    print("==================adding product to cart===================")
    customer.cart.add_item(Iphone_x)
        
    order = system.create_order(customer, customer.address[0])
    
    if order:
        
        payment_info = {
            'card_number': '1234567890123456',
            'expiry':'12/25',
            'cvv': '000',
            
            }
        if system.process_payment(order, PaymentMethod.CREDIT_CARD, payment_info):
            print(f'order {order.id}, process successfully')
            print(f'Total amount ${order.total}')
            
        else:
            print("Payment process failed")
            
    else:
        print("Order creation failed")
        
if __name__ == "__main__":
    main()