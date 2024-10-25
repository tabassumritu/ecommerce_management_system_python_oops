# E-commerce System README

## Overview
This project simulates a basic E-commerce System using Python, object-oriented programming (OOP) concepts, and various modules. It provides functionality for managing users, products, categories, orders, and payments within an e-commerce context. This system supports different user roles (Customer, Admin, Vendor) and includes cart management, product searching, payment processing, and order management.

## Features
1. **User Management**
   - Support for multiple roles: `Customer`, `Admin`, and `Vendor`.
   - User registration with validation for unique usernames and emails.
   - Users can add addresses and manage wishlists.

2. **Product Management**
   - Categories and subcategories for products.
   - Products can have specifications, stock quantity, reviews, and images.
   - Vendors can add products, and customers can add products to their cart.

3. **Cart Management**
   - Add, remove, and update quantities for products in the shopping cart.
   - Cart calculates the total cost of all items.

4. **Order Management**
   - Orders are created from items in the customer’s cart.
   - Order status tracking from `Pending` to `Delivered`.
   - Orders include a tracking number and shipping cost.

5. **Payment Processing**
   - Multiple payment methods supported (currently Credit Card).
   - Secure payment processing with validation for card numbers.
   - Payment statuses: `Pending`, `Completed`, `Failed`, `Refunded`.

6. **Searching**
   - Products can be searched by name and description.
   - Results can be filtered by category.

## Installation and Requirements
This project only requires Python 3.x and standard Python libraries such as `uuid`, `hashlib`, `datetime`, `re`, and `abc`. No external libraries are required.

### Instructions:
1. Clone or download the project files.
2. Run the code with:
   ```bash
   python e_commerce_system.py
   ```

## Structure and Classes

### Enums
- `UserRole`, `OrderStatus`, `PaymentStatus`, `PaymentMethod`: Enumerations for role types, order status, payment status, and payment methods.

### Models
- **Category**: Manages product categories and subcategories.
- **User**: Stores user information, addresses, cart, and wishlists.
- **Address**: Represents a physical address.
- **Product**: Stores product details, stock, and specifications.
- **Review**: Represents a product review from a user.
- **CartItem**: Represents a product and quantity within a cart.
- **Cart**: Manages items, quantity, and total cost in the shopping cart.
- **Order**: Manages order items, status, and payment information.
- **PaymentProcessor**: Abstract class for payment processing. Implemented by `CreditCardProcessor`.

### System Classes
- **EcommerceSystem**: Manages user registration, order creation, and payment processing.

## Example Usage
The `main` function in `e_commerce_system.py` demonstrates a simple flow of using the system:
1. **Category Creation**: Adds "Electronics" and "Phone" categories.
2. **User Registration**: Registers an Admin, Vendor, and Customer.
3. **Product Addition**: Vendor adds "iPhone X" product with specifications and stock.
4. **Cart and Order Creation**: Customer adds the product to their cart and places an order.
5. **Payment Processing**: Customer completes payment using a credit card, with payment validation.

## Important Notes
- **Data Security**: Passwords are stored securely using SHA-256 hashing.
- **Data Persistence**: This code is designed for demonstration purposes; data persistence is not implemented.

## Potential Enhancements
- Integration with a database to store data.
- Implement additional payment processors.
- Add more search and filtering options for products.
- Improve error handling and validation across modules.

This project serves as a basic starting point for understanding e-commerce systems and applying OOP principles in Python.