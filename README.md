# E-COMMERCE WEBSITE
An e-commerce website that contains all the basic functionalities you would expect, for example, browsing products, adding them to cart and a checking out amongst other features

## Table of Contents


## Built with
* Python
* MySQL
* Django

## Requirements
The website requires **python 3.11.*** or never version of python to run smoothly. The modules listed below are also mandatory to run the backend server:

* asgiref==3.7.2
* Authlib==1.3.0
* certifi==2023.11.17
* cffi==1.16.0
* charset-normalizer==3.3.2
* cryptography==41.0.7
* Django==5.0.1
* django-cors-headers==4.3.1
* django-filter==1.1.0
* django-haystack==3.2.1
* django-mysql==4.12.0
* djangorestframework==3.10.3
* drf-auto-endpoint==0.9.9
* idna==3.6
* Inflector==3.1.1
* jsonify==0.5
* mysqlclient==2.2.1
* pillow==10.2.0
* pycparser==2.21
* python-dotenv==1.0.0
* requests==2.31.0
* sqlparse==0.4.4
* urllib3==2.1.0


## Install

1. Clone the repository with the command below:

        `git clone https://github.com/Bot-on-Tapwater/django_apps_bot_on_tapwater.git`

2. Navigate to the root of the repo and install the requirements using the command below:

        `pip install -r requirements.txt`

3. Make sure MySQL is installed in your system, create the database **eridosolutions** and create a user, the user should be granted all privileges to the database you have created in the previous step. Create a .env file at the root of the repository. The .env file should be populated with content as shown below:

        `DATABASE='eridosolutions'`

        `DATABASE_USERNAME='enter username'`

        `PASSWORD='enter user password'`

        `HOST='enter host'`
        
        `PORT='5432'`

4. Execute database migrations by running the following two commands:

        `python manage.py makemigrations`

        `python manage.py migrate`

## Usage
To deploy the backend server use the following command while you are at the root of the repository:

        `python manage.py runserver`

### Authentication

- **Login**
 - Method: `GET`
 - Path: `/login/`
 - View: `views.login_view`
 - Description: Handles user login.

- **Logout**
 - Method: `GET`
 - Path: `/logout/`
 - View: `views.logout_view`
 - Description: Handles user logout.

- **Register**
 - Method: `GET`
 - Path: `/register/`
 - View: `views.register`
 - Description: Handles user registration.

- **User Status**
 - Method: `GET`
 - Path: `/user_status/`
 - View: `views.show_logged_in_user_id`
 - Description: Displays the logged-in user's ID.

### Product Management

- **List All Products**
 - Method: `GET`
 - Path: `/products/`
 - View: `views.list_all_products`
 - Description: Retrieves a list of all products.

- **Get Product Details**
 - Method: `GET`
 - Path: `/products/<int:id>/`
 - View: `views.get_product_with_product_id`
 - Description: Retrieves details of a specific product by ID.

- **Create New Product**
 - Method: `POST`
 - Path: `/products/create/`
 - View: `views.create_new_product`
 - Description: Creates a new product.

- **Update Product Details**
 - Method: `PUT`
 - Path: `/products/<int:id>/update/`
 - View: `views.update_product_with_product_id_details`
 - Description: Updates the details of a specific product by ID.

- **Delete Product**
 - Method: `DELETE`
 - Path: `/products/<int:id>/delete/`
 - View: `views.delete_product_with_product_id`
 - Description: Deletes a specific product by ID.

### User Profile

- **Get User Profile Details**
 - Method: `GET`
 - Path: `/users/<int:id>/`
 - View: `views.get_user_with_user_id_profile_details`
 - Description: Retrieves the profile details of a specific user by ID.

- **Update User Profile Details**
 - Method: `PUT`
 - Path: `/users/<int:id>/update/`
 - View: `views.update_user_with_user_id_profile_details`
 - Description: Updates the profile details of a specific user by ID.

- **List User Orders**
 - Method: `GET`
 - Path: `/users/<int:id>/orders/`
 - View: `views.list_orders_placed_by_user_with_user_id`
 - Description: Retrieves a list of orders placed by a specific user.

### Shopping Cart

- **Get Cart Contents**
 - Method: `GET`
 - Path: `/users/<int:id>/cart/`
 - View: `views.get_contents_of_shopping_cart_of_user`
 - Description: Retrieves the contents of a user's shopping cart.

- **Add Product to Cart**
 - Method: `POST`
 - Path: `/users/<int:id>/cart/add/<int:productId>/`
 - View: `views.add_product_to_user_cart`
 - Description: Adds a product to a user's shopping cart.

- **Remove Product from Cart**
 - Method: `DELETE`
 - Path: `/users/<int:id>/cart/remove/<int:productId>/`
 - View: `views.remove_product_from_user_cart`
 - Description: Removes a product from a user's shopping cart.

- **Clear Cart**
 - Method: `DELETE`
 - Path: `/users/<int:id>/cart/clear/`
 - View: `views.clear_entire_shopping_cart`
 - Description: Clears the entire shopping cart.

### Order Management

- **List All Orders**
 - Method: `GET`
 - Path: `/orders/`
 - View: `views.get_list_of_all_orders`
 - Description: Retrieves a list of all orders.

- **Get Order Details**
 - Method: `GET`
 - Path: `/orders/<int:id>/`
 - View: `views.get_details_of_order_with_order_id`
 - Description: Retrieves the details of a specific order by ID.

- **Create New Order**
 - Method: `POST`
 - Path: `/users/<int:userId>/orders/create/`
 - View: `views.create_new_order`
 - Description: Creates a new order for a specific user.

- **Cancel Order**
 - Method: `DELETE`
 - Path: `/orders/<int:id>/cancel/`
 - View: `views.cancel_order_with_order_id`
 - Description: Cancels a specific order by ID.

### Payment Integration

- **Process Payment**
 - Method: `POST`
 - Path: `/payment/charge/<int:orderId>/`
 - View: `views.process_payment`
 - Description: Processes payment for a specific order by ID.

- **Refund Payment**
 - Method: `POST`
 - Path: `/payment/refund/<int:orderId>/`
 - View: `views.refund_payment`
 - Description: Refunds payment for a specific order by ID.

### Category Management

- **List All Categories**
 - Method: `GET`
 - Path: `/categories/`
 - View: `views.get_list_of_all_product_categories`
 - Description: Retrieves a list of all product categories.

- **Get Products in Category**
 - Method: `GET`
 - Path: `/categories/<int:id>/`
 - View: `views.get_list_of_all_products_in_category`
 - Description: Retrieves a list of all products in a specific category by ID.

- **Create New Category**
 - Method: `POST`
 - Path: `/categories/create/`
 - View: `views.create_new_product_category`
 - Description: Creates a new product category.

- **Update Category Details**
 - Method: `PUT`
 - Path: `/categories/<int:id>/update/`
 - View: `views.update_details_of_category_with_category_id`
 - Description: Updates the details of a specific category by ID.

- **Delete Category**
 - Method: `DELETE`
 - Path: `/categories/<int:id>/delete/`
 - View: `views.remove_product_category_with_category_id`
 - Description: Deletes a specific category by ID.

### Reviews and Ratings

- **Get Product Reviews**
 - Method: `GET`
 - Path: `/products/<int:id>/reviews/`
 - View: `views.get_reviews_for_product_with_product_id`
 - Description: Retrieves reviews for a specific product by ID.

- **Create Product Review**
 - Method: `POST`
 - Path: `/users/<int:userId>/products/<int:id>/reviews/create/`
 - View: `views.creat_review_for_product_with_product_id`
 - Description: Creates a review for a specific product by ID.

### Search and Filters

- **Search Products**
 - Method: `GET`
 - Path: `/search/`
 - View: `views.search_products`
 - Description: Searches for products based on a query.

- **Turn On Filters**
 - Method: `GET`
 - Path: `/filters/`
 - View: `views.turn_on_filters`
 - Description: Activates filters for product search.

### Shipping and Address

- **Get Available Shipping Options**
 - Method: `GET`
 - Path: `/shipping-options/`
 - View: `views.get_available_shipping_options`
 - Description: Retrieves available shipping options.

- **Get User Saved Addresses**
 - Method: `GET`
 - Path: `/users/<str:userId>/addresses/`
 - View: `views.get_user_saved_addresses`
 - Description: Retrieves a list of addresses saved by a specific user.

- **Add Address to User Profile**
 - Method: `POST`
 - Path: `/users/<str:userId>/addresses/create/`
 - View: `views.add_address_to_user_profile`
 - Description: Adds a new address to a user's profile.

- **Update Address Details**
 - Method: `PUT`
 - Path: `/users/<str:userId>/addresses/<int:id>/update/`
 - View: `views.update_details_of_address_with_address_id`
 - Description: Updates the details of a specific address by ID.

- **Delete Address**
 - Method: `DELETE`
 - Path: `/users/<str:userId>/addresses/<int:id>/delete/`
 - View: `views.delete_address_with_address_id`
 - Description: Deletes a specific address by ID.

## Contributing
Contributions are welcome! Please follow these guidelines:

1. Fork the repository and create your branch: git checkout -b feature.
2. Commit your changes: git commit -am 'Add new feature'.
3. Push to the branch: git push origin feature.
4. Submit a pull request.

## License
For permission to use, modify, or distribute this project, please contact the author.

## API Documentation
The application is currently set to use **PORT 8000** and it hosts on **127.0.0.1**, the django application name is **eridosolutions**, thus any API routes should be added to the end of:

        `http://127.0.0.1:8000/eridosolutions`


