from django.shortcuts import render, HttpResponse, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
# from django.contrib.auth.models import User
from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse
from urllib.parse import quote_plus, urlencode
import json
import requests
from django.http import JsonResponse, HttpResponse
from django.http import HttpResponseNotFound, HttpResponseServerError, Http404
from .models import Product, Category, User, Order, ShoppingCart, CartItem, Review, Address, OrderItem
from django.utils.datastructures import MultiValueDictKeyError
from django.core.exceptions import ValidationError, MultipleObjectsReturned, PermissionDenied
from django.http import QueryDict
from django.db.models import F, ExpressionWrapper, fields, Sum
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage
from django.core.serializers import serialize
from django.forms.models import model_to_dict

"""DECORATORS"""
def check_user_id(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.id:
            print(str(request))
            return JsonResponse({"error": "Unauthorized"}, status=401)
        return view_func(request, *args, **kwargs)
    return wrapper

"""LANDING PAGE"""
@require_http_methods(["GET"])
def index(request):
    return render(request, 'eridosolutions/index.html')

"""AUTHENTICATION"""
redirect_url_for_paths_that_fail_login_requirements = "http://localhost:3000/account/login"
@require_http_methods(["POST"])
@csrf_exempt # !!!SECURITY RISK!!! COMMENT OUT CODE
def register(request):
    try:
        data = request.POST

        username, password, email, first_name, last_name = [data['username'], data['password'], data['email'], data['first_name'], data['last_name']]

        user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)

        user.save()

        user_cart = ShoppingCart(user=user)

        user_cart.save()        

        return JsonResponse({
            "message": "user created successfully"
        }, status=200)
    
    except IntegrityError:
        return JsonResponse({
            "error": "Username or email already exists"
        }, status=409)

    except MultiValueDictKeyError as e:
        return JsonResponse({"error": f"The form value for attribute {str(e)} is missing"}, status=400)

@require_http_methods(["POST"])
@csrf_exempt # !!!SECURITY RISK!!! COMMENT OUT CODE
def login_view(request):
    try:
        data = request.POST
        username, password = [data['username'], data['password']]

    except MultiValueDictKeyError as e:
        return JsonResponse({"error":f"The form value for attribute {str(e)} is missing"
            }, status=400)
    
    try:
        user_email_passed_instead = User.objects.get(email=username)

        username = user_email_passed_instead.username

    except User.DoesNotExist:
        pass

    except MultipleObjectsReturned as e:
        return JsonResponse({
            "error":"You are using the same email for Django Admin Dashboard and your newly created user, change one of them."
            }, status=400)
    
    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        request.session.save()

        return JsonResponse({
            "message": "User logged in successfully",
        })
    
    else:
        return JsonResponse({"error":"Either the email/username or the password is incorrect"
                            }, status=401)
    
@csrf_exempt # !!!SECURITY RISK!!! COMMENT OUT CODE
def logout_view(request):
    logout(request)
    return JsonResponse({"message": "success"})

def show_logged_in_user_id(request):
    if request.user.id:
        return JsonResponse({"user": True})
    return JsonResponse({"user": False})

"""PAGINATION"""
def paginate_results(request, query_results, view_url, items_per_page=12):
    items_per_page = items_per_page

    page_number = request.GET.get('page', 1)

    paginator = Paginator(query_results, items_per_page)

    try:
        page_obj = paginator.get_page(page_number)
    
    except EmptyPage:
        return JsonResponse({"error": "Page not found"}, status=404)
    
    items_on_current_page = page_obj.object_list

    json_data = {
        'current_page': page_obj.number,
        'total_pages': paginator.num_pages,
        'query_results': [item.to_dict(request) for item in items_on_current_page],
    }
    
    if page_obj.has_previous():
        if "page=" in view_url:
            json_data['previous_page'] = f"{view_url[:view_url.rfind('page=')]}page={page_obj.previous_page_number()}"
        else:
            json_data['previous_page'] = f"{view_url}?page={page_obj.previous_page_number()}"

    if page_obj.has_next():
        if "page=" in view_url:
            json_data['next_page'] = f"{view_url[:view_url.rfind('page=')]}page={page_obj.next_page_number()}"
        else:
            json_data['next_page'] = f"{view_url}?page={page_obj.next_page_number()}"
    
    return json_data
    

"""PRODUCT MANAGEMENT"""
@require_http_methods(["GET"])
def list_all_products(request):
    view_url = request.build_absolute_uri()

    all_products = Product.objects.all()

    if all_products.exists():
        
        return JsonResponse(paginate_results(request, all_products, view_url), safe=False)
    else:
        return JsonResponse({"error": "No products found, add a product and try again."}, status=404)

@require_http_methods(["GET"])
def get_product_with_product_id(request, id):
    try:
        specific_product = Product.objects.get(product_id=id)
        return JsonResponse(specific_product.to_dict(request), safe=False)

    except Product.DoesNotExist:
        return JsonResponse({"error":f"Product with ID: {id} was not found."}, status=404)

@require_http_methods(["POST"])
@csrf_exempt # !!!SECURITY RISK!!! COMMENT OUT CODE
def create_new_product(request):
    try:
        name = request.POST['name']
        description = request.POST['description']
        price = request.POST['price']
        quantity_in_stock = request.POST['quantity_in_stock']
        category = request.POST['category']
        image = request.FILES['image']

    except MultiValueDictKeyError as e:
        return JsonResponse({"error": f"The form value for attribute {str(e)} is missing"
            }, status=400)

    try:
        new_product = Product(name=name, description=description, price=float(price), quantity_in_stock=quantity_in_stock, category=Category.objects.get(name=category), image=image)
        new_product.save()
    except (ValueError, ValidationError) as e:
        return JsonResponse({"error": f"{str(e)}"}, status=400)

    return JsonResponse({"success": True}, safe=False)

@require_http_methods(["PUT", "POST"])
@csrf_exempt # !!!SECURITY RISK!!! COMMENT OUT CODE
def update_product_with_product_id_details(request, id):
    try:
        product_to_update = Product.objects.get(product_id=id)

        if request.method == 'PUT':
            for field, value in QueryDict(request.body).items():
                if (hasattr(product_to_update, field) and field == "category"):              
                    try:
                        setattr(product_to_update, field, Category.objects.get(name=value))
                    except (ValueError, ValidationError, Category.DoesNotExist) as e:
                        return JsonResponse({"error": f"{str(e)}"}, status=400)
                
                elif (hasattr(product_to_update, field) and field == "image"):
                    return JsonResponse({"error": 'Use POST request to update image'}, status=405)
                
                elif (hasattr(product_to_update, field)):
                    setattr(product_to_update, field, value)
                
                else:
                    return JsonResponse({"error": f"There is no field named {field} in products table."}, status=400)
                
        if request.method == 'POST':
            data = request.POST
            image = request.FILES['image']
            
            for field, value in data.items():
                if (hasattr(product_to_update, field) and field == "category"):                
                    try:
                        setattr(product_to_update, field, Category.objects.get(name=value))
                    except (ValueError, ValidationError, Category.DoesNotExist) as e:
                        return JsonResponse({"error":f"{str(e)}"}, status=400)
                    
                elif (hasattr(product_to_update, 'image')):
                    product_to_update.image = image
                
                elif (hasattr(product_to_update, field)):
                    setattr(product_to_update, field, value)               
                
                else:
                    return JsonResponse({"error": f"There is no field named {field} in products table."}, status=400)

        product_to_update.save()
    
    except Product.DoesNotExist as e:
        return JsonResponse({"error": f"Product with ID: {id} was not found."}, status=404)

    return JsonResponse({"success": True}, safe=False)
        
@require_http_methods(["DELETE"])
def delete_product_with_product_id(request, id):
    try:
        product_to_delete = Product.objects.get(product_id=id)

        product_to_delete_details = product_to_delete.to_dict(request)

        product_to_delete.delete()

    except Product.DoesNotExist as e:
        return JsonResponse({"error": f"Product with ID: {id} was not found."}, status=404)
    
    return JsonResponse({"success": True}, safe=False)

"""USER PROFILE"""
@check_user_id
@require_http_methods(["GET"])
def get_user_with_user_id_profile_details(request):
    try:
        id = request.user.id
        specific_user = User.objects.get(id=id)
        return JsonResponse({'id': specific_user.id, 'username': specific_user.username, 'email': specific_user.email, 'first_name': specific_user.first_name, 'last_name': specific_user.last_name}, safe=False)
    except User.DoesNotExist:
        return JsonResponse({"error": f"User does not exist."}, status=404)

@check_user_id
@require_http_methods(["PUT"])
def update_user_with_user_id_profile_details(request):
    try:
        id = request.user.id

        user_to_update = User.objects.get(id=id)

        for field, value in QueryDict(request.body).items():
            if (hasattr(user_to_update, field) and field == "password"):                
                try:
                    user_to_update.set_password(value)
                except (ValueError, ValidationError, Category.DoesNotExist) as e:
                    return JsonResponse(f"{str(e)}", safe=False)
            
            elif (hasattr(user_to_update, field)):
                setattr(user_to_update, field, value)

            else:
                return JsonResponse({"error": f"There is no field named {field} in users table."}, status=404)

        user_to_update.save()      
    
    except User.DoesNotExist as e:
        return JsonResponse({"error": f"user with ID: {id} was not found."}, status=404)

    return JsonResponse({"success": True}, safe=False)

"""LIST OF USER'S ORDERS"""
@check_user_id
@require_http_methods(["GET"])
def list_orders_placed_by_user_with_user_id(request):
    view_url = request.build_absolute_uri()

    try:
        id = request.user.id
        orders_placed_by_user = Order.objects.filter(user=id)
        return JsonResponse(paginate_results(request, orders_placed_by_user, view_url), safe=False)
    except Order.DoesNotExist:
        return JsonResponse(None, safe=False)

"""SHOPPING CART"""
@check_user_id
@require_http_methods(["GET"])
def get_contents_of_shopping_cart_of_user(request):
    view_url = request.build_absolute_uri()
    
    id = request.user.id

    try:
        cart_contents_of_user = ShoppingCart.objects.get(user=id)

        return JsonResponse(paginate_results(request, [item for item in CartItem.objects.filter(cart=cart_contents_of_user.cart_id)], view_url), safe=False)

    except ShoppingCart.DoesNotExist:
        return JsonResponse(None, safe=False)
    
    except TypeError:
        return JsonResponse(None, safe=False)

@require_http_methods(["POST"])
@csrf_exempt # !!!SECURITY RISK!!! COMMENT OUT CODE
@check_user_id
def add_product_to_user_cart(request, productId):
    try:
        id = request.user.id

        if not id: # user not authenticated
            return HttpResponse("unauthorized", status=401)

        quantity = request.POST['quantity']

        if (int(quantity) > Product.objects.get(product_id=productId).quantity_in_stock):
            return JsonResponse(f"Quantity in stock is {Product.objects.get(product_id=productId).quantity_in_stock}, reduce your current quantity of ({quantity}) items.", safe=False)

        try:
            try:
                existing_cart_item = CartItem.objects.get(cart=ShoppingCart.objects.get(user=id), product=Product.objects.get(product_id=productId))
                
                existing_cart_item.quantity += int(quantity)

                existing_cart_item.save()

                return JsonResponse(existing_cart_item.to_dict(), safe=False)
            except CartItem.DoesNotExist:
                new_cart_item = CartItem(cart=ShoppingCart.objects.get(user=id), product=Product.objects.get(product_id=productId), quantity=quantity)
            

        except ShoppingCart.DoesNotExist:
            try:
                new_shopping_cart = ShoppingCart(user=User.objects.get(id=id))

                new_shopping_cart.save()

                new_cart_item = CartItem(cart=ShoppingCart.objects.get(user=id), product=Product.objects.get(product_id=productId), quantity=quantity)
            except User.DoesNotExist:
                return JsonResponse({"error": f"User with ID: {id} does not exist."}, status=404)
        
        except Product.DoesNotExist:
            return JsonResponse({"error": f"Product with ID: {productId} not found."
            }, status=404)
    
    except MultiValueDictKeyError as e:
        return JsonResponse({"error": f"The form value for attribute {str(e)} is missing"
            }, status=400)
    
    new_cart_item.save()    

    return JsonResponse({"success": True}, safe=False)

@require_http_methods(["DELETE"])
@csrf_exempt # !!!SECURITY RISK!!! COMMENT OUT CODE
@check_user_id
def remove_product_from_user_cart(request, productId):
    try:
        id = request.user.id

        cart_item_to_delete = CartItem.objects.get(cart=ShoppingCart.objects.get(user=id), product=Product.objects.get(product_id=productId))

        cart_item_to_delete_details = cart_item_to_delete.to_dict()

        cart_item_to_delete.delete()
    
    except ShoppingCart.DoesNotExist:
        return JsonResponse({"error": f"User with ID: {id} does not have an active cart."}, status=404)

    except Product.DoesNotExist:
        return JsonResponse({"error": f"Product with ID: {productId} not found in cart."}, status=404)

    except CartItem.DoesNotExist:
        return JsonResponse({"error": f"CartItem does not exist."}, status=404)
    
    return JsonResponse({"message": "item deleted"})

@require_http_methods(["DELETE", "POST"])
@csrf_exempt # !!!SECURITY RISK!!! COMMENT OUT CODE
@check_user_id
def clear_entire_shopping_cart(request):
    try:
        id = request.user.id

        cart_to_clear = ShoppingCart.objects.get(user=id)

        cart_to_clear_items = CartItem.objects.filter(cart=cart_to_clear)

        _ = list(map(lambda x: x.delete(), cart_to_clear_items))

    except ShoppingCart.DoesNotExist:
        return JsonResponse({"error": f"User with ID: {id} does not have a cart."}, status=404)

    return JsonResponse({"message": "cart cleared"})

"""ORDER MANAGEMENT"""
@require_http_methods(["GET"])
def get_list_of_all_orders(request):
    view_url = request.build_absolute_uri()

    all_orders = Order.objects.all()

    if all_orders.exists():
        return JsonResponse(paginate_results(request, [order for order in all_orders], view_url), safe=False)
    else:
        return JsonResponse({"error": f"No orders found, add an order and try again."}, status=404)

@require_http_methods(["GET"])
def get_details_of_order_with_order_id(request, id):
    try:
        specific_order_details = Order.objects.get(order_id=id)

    except Order.DoesNotExist:
        return JsonResponse({"error": f"Order with ID: {id} does not exist."}, status=404)
    
    return JsonResponse(specific_order_details.to_dict(), safe=False)

@require_http_methods(["POST"])
@csrf_exempt # !!!SECURITY RISK!!! COMMENT OUT CODE
@check_user_id
def create_new_order(request):
    try:
        userId = request.user.id

        user_cart = ShoppingCart.objects.get(user=userId)

        cartitems = CartItem.objects.filter(cart=user_cart).all()

        if not cartitems:
            return JsonResponse({"error": f"User has no items in cart."}, status=404)
        
        else:
            total_cost_of_cart_items = CartItem.objects.filter(cart=user_cart).aggregate(total_cost=Sum(ExpressionWrapper(F('quantity') * F('product__price'), output_field=fields.FloatField())))
            total_cost = total_cost_of_cart_items.get('total_cost', 0) or 0

            new_order = Order(user=User.objects.get(id=userId), total_amount=total_cost, order_status='ACTIVE')

            new_order.save()

            new_order_items = list(map(lambda item: OrderItem(order=new_order, product=item.product, quantity=item.quantity, unit_price=item.product.price), [item for item in CartItem.objects.filter(cart=user_cart)]))

            for item in CartItem.objects.filter(cart=user_cart):
                product_to_update_quantity = Product.objects.get(product_id=item.product.product_id)

                product_to_update_quantity.quantity_in_stock -= item.quantity

                product_to_update_quantity.save()

            OrderItem.objects.bulk_create(new_order_items)

            clear_entire_shopping_cart(request)

    except ShoppingCart.DoesNotExist:
        return JsonResponse({"error": f"User with ID: {userId} has no items in cart."}, status=404)

    return JsonResponse({"success": True}, safe=False)

@require_http_methods(["PUT"])
def cancel_order_with_order_id(request, id):
    try:
        order_to_cancel = Order.objects.get(order_id=id)

        order_to_cancel.order_status = "CANCELED"

        order_to_cancel.save()

        return JsonResponse({"success": True}, safe=False)
    
    except Order.DoesNotExist:
        return JsonResponse({"error": f"Order with ID: {id} does not exist."}, status=404)
    

"""PAYMENT INTEGRATION"""
@require_http_methods(["POST"])
@csrf_exempt # !!!SECURITY RISK!!! COMMENT OUT CODE
def process_payment(request, orderId):
    try:
        order_to_pay_for = Order.objects.get(order_id=orderId)

        return JsonResponse({"success": True}, safe=False) if (order_to_pay_for.order_status == "ACTIVE") else JsonResponse(f"Can't process payment for a CANCELLED/COMPLETED order.", safe=False)
    
    except Order.DoesNotExist:
        return JsonResponse({"error": f"Order with ID: {orderId} does not exist."}, status=404)

# @login_required(login_url=redirect_url_for_paths_that_fail_login_requirements)
@require_http_methods(["POST"])
@csrf_exempt # !!!SECURITY RISK!!! COMMENT OUT CODE
def refund_payment(request, orderId):
    try:
        order_to_refund = Order.objects.get(order_id=orderId)
        return JsonResponse(order_to_refund.to_dict(), safe=False)
    
    except Order.DoesNotExist:
        return JsonResponse({"error": f"Order with ID: {orderId} does not exist."}, status=404)


"""CATEGORY MANAGEMENT"""
@require_http_methods(["GET"])
def get_list_of_all_product_categories(request):
    view_url = request.build_absolute_uri()

    list_of_all_categories = Category.objects.all()

    if list_of_all_categories.exists():
        return JsonResponse(paginate_results(request, [category for category in list_of_all_categories], view_url), safe=False)
    else:
        return JsonResponse(None, safe=False)
    
@require_http_methods(["GET"])
def get_list_of_all_products_in_category(request, id):
    view_url = request.build_absolute_uri()

    return JsonResponse(paginate_results(request, [product for product in Product.objects.filter(category=id)], view_url), safe=False)

@require_http_methods(["POST"])
@csrf_exempt # !!!SECURITY RISK!!! COMMENT OUT CODE
def create_new_product_category(request):
    try:
        name = request.POST["name"]

        new_category = Category(name=name)

    except MultiValueDictKeyError as e:
        return JsonResponse({"error": f"The form value fo attribute {e} is missing."}, status=400)
    
    new_category.save()

    return JsonResponse({"success": True}, safe=False)

@require_http_methods(["PUT"])
def update_details_of_category_with_category_id(request, id):
    try:
        category_to_update = Category.objects.get(category_id=id)

        name = QueryDict(request.body)['name']

        category_to_update.name = name
    
    except Category.DoesNotExist:
        return JsonResponse({"error": f"Category with ID: {id} does not exist."}, status=404)

    except MultiValueDictKeyError as e:
        return JsonResponse({"error": f"The form value for attribute {str(e)} is missing."}, status=400)
    
    category_to_update.save()

    return JsonResponse({"success": True}, safe=False)

@require_http_methods(["DELETE"])
def remove_product_category_with_category_id(request, id):
    try:
        category_to_delete = Category.objects.get(category_id=id)

        category_to_delete_details = category_to_delete.to_dict()

        category_to_delete.delete()

    except Category.DoesNotExist:
        return JsonResponse({"error": f"Category with ID: {id} does not exist."}, status=404)
    
    return JsonResponse({"success": True}, safe=False)

"""REVIEWS AND RATINGS"""
@require_http_methods(["GET"])
def get_reviews_for_product_with_product_id(request, id):
    view_url = request.build_absolute_uri()

    reviews = Review.objects.filter(product=id)

    if reviews.exists():
        return JsonResponse(paginate_results(request, [review for review in reviews], view_url), safe=False)
    else:
        return JsonResponse({"current_page": 0, "total_pages": 0, "query_results": []})

@check_user_id
@require_http_methods(["GET"])
def list_reviews_created_by_user_with_user_id(request):
    view_url = request.build_absolute_uri()

    try:
        user_id = request.user.id
        reviews_by_user = Review.objects.filter(user=user_id)  # Assuming you have a 'user' field in your Review model

        if reviews_by_user.exists():
            return JsonResponse(paginate_results(request, [review for review in reviews_by_user], view_url), safe=False)
        else:
            return JsonResponse(None, safe=False)
            # return JsonResponse({"current_page": 0, "total_pages": 0, "query_results": []})
    except Review.DoesNotExist:
        return JsonResponse(None, safe=False)


@require_http_methods(["POST"])
@csrf_exempt # !!!SECURITY RISK!!! COMMENT OUT CODE
@check_user_id
def creat_review_for_product_with_product_id(request, id):
    try:
        userId = request.user.id
        user_leaving_review = User.objects.get(id=userId)
        product_to_review = Product.objects.get(product_id=id)

        # Check if the user has already submitted a review for this product
        existing_review = Review.objects.filter(product=product_to_review, user=user_leaving_review).first()

        if existing_review:
            # User has already submitted a review for this product
            return JsonResponse({"error": "You can only submit one review per product.Check your profile for more actions."}, status=400)



        rating = request.POST['rating']
        comment = request.POST['comment']

        new_review = Review(product=product_to_review, user=user_leaving_review, rating=rating, comment=comment)

        new_review.full_clean()
        new_review.save()

        return JsonResponse({"success": True})  # Added this
    
    except ValidationError as e:
        return JsonResponse(str(e), safe=False)

    except User.DoesNotExist:
        return JsonResponse({"error": f"User with ID: {userId} does not exist."}, status=404)
    
    except Product.DoesNotExist:
        return JsonResponse({"error": f"Product with ID: {id} does not exist."}, status=404)

    except MultiValueDictKeyError as e:
        return JsonResponse({"error": f"The form value for attribute {str(e)} is missing."}, status=400)

@csrf_exempt # !!!SECURITY RISK!!! COMMENT OUT CODE
@require_http_methods(["DELETE"])
@check_user_id
def user_delete_review(request, id):
    try:
        userId = request.user.id

        review_to_delete = Review.objects.get(review_id=id, user=userId)

        review_to_delete.delete()

        return JsonResponse({"success": True}, safe=False)
    
    except Review.DoesNotExist:
            return JsonResponse({"error": f"Review with ID: {id} does not exist."}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)



"""SEARCH AND FILTERS"""
@require_http_methods(["POST", "GET"])
@csrf_exempt # !!!SECURITY RISK!!! COMMENT OUT CODE
def search_products(request):
    view_url = request.build_absolute_uri()

    try:
        search = request.POST['search']

        search_results = Product.objects.raw("SELECT * FROM eridosolutions_product WHERE MATCH (name, description) AGAINST (%s IN NATURAL LANGUAGE MODE)", [search])

        request.session['search_results'] = serialize('python', search_results)

        return JsonResponse(paginate_results(request, search_results, view_url), safe=False)
    
    except MultiValueDictKeyError as e:
        return JsonResponse({"error": f"The form value for attribute {str(e)} is missing."}, status=400)


@login_required(login_url=redirect_url_for_paths_that_fail_login_requirements)
@require_http_methods(["GET", "POST"])
@csrf_exempt # !!!SECURITY RISK!!! COMMENT OUT CODE
def turn_on_filters(request):
    view_url = request.build_absolute_uri()

    search_results = request.session.get('search_results')

    search_results = [Product.objects.get(product_id=product['pk']) for product in search_results]

    min_price = int(request.POST.get('min_price', 0))

    max_price = int(request.POST.get('max_price', 1_000_000_000))

    category = request.POST.get('category', None)

    if category:
        search_results = [product for product in search_results if (category == product.category.name and product.price > min_price and product.price < max_price)]
    
    else:
        search_results = [product for product in search_results if (product.price > min_price and product.price < max_price)]

    return JsonResponse(paginate_results(request, search_results, view_url), safe=False)

"""SHIPPING AND ADDRESS"""
@require_http_methods(["GET"])
def get_available_shipping_options(request):
    view_url = request.build_absolute_uri()

    return JsonResponse(dict(request.session), safe=False)

@require_http_methods(["GET"])
@check_user_id
def get_user_saved_addresses(request):
    userId = request.user.id

    view_url = request.build_absolute_uri()

    user_saved_addresses = Address.objects.filter(user=userId)

    if user_saved_addresses.exists():
        return JsonResponse(paginate_results(request, [address for address in user_saved_addresses], view_url), safe=False)
    else:  # we don't need to return an error here
        return JsonResponse(None, safe=False)

@require_http_methods(["POST"])
@csrf_exempt # !!!SECURITY RISK!!! COMMENT OUT CODE
@check_user_id
def add_address_to_user_profile(request):
    try:
        userId = request.user.id

        data = request.POST

        street_address, town, zipcode, county, phone_number_1, phone_number_2, additional_details = [data['street_address'], data['town'], data['zipcode'], data['county'], data['phone_number_1'], data['phone_number_2'], data['additional_details']]

        user = User.objects.get(id=userId)

        new_address = Address(street_address=street_address, town=town,  zipcode=zipcode, county=county, phone_number_1=phone_number_1, phone_number_2=phone_number_2, additional_details=additional_details, user=user)

        new_address.save()

        return JsonResponse({"message": "address created successfully"})
    
    except User.DoesNotExist:
        return JsonResponse({"error": f"User with ID: {userId} does not exist."}, status=404)
    
    except MultiValueDictKeyError as e:
        return JsonResponse({"error": f"The form value for attribute {str(e)} is missing."}, status=400)

@require_http_methods(["PUT"])
@check_user_id
def update_details_of_address_with_address_id(request, id):
    try:
        userId = request.user.id

        address_to_update = Address.objects.get(address_id=id)

        user = User.objects.get(id=userId)

        data = QueryDict(request.body)

        for field, value in data.items():
            
            if (hasattr(address_to_update, field)):
                setattr(address_to_update, field, value)
            
            else:
                return JsonResponse(f"There is no field named {field} in address table.", safe=False)

        address_to_update.save()

        return JsonResponse({"success": True}, safe=False)

    except Address.DoesNotExist:
        return JsonResponse({"error": f"Address with ID: {id} does not exist."}, status=404)
    
    except User.DoesNotExist:
        return JsonResponse({"error": f"User with ID: {userId} does not exist."}, status=404)

@require_http_methods(["DELETE"])
@check_user_id
@csrf_exempt # !!!SECURITY RISK!!! COMMENT OUT CODE
def delete_address_with_address_id(request, id):
    try:
        userId = request.user.id

        address_to_delete = Address.objects.get(address_id=id, user=userId)

        address_to_delete.delete()

        return JsonResponse({"success": True}, safe=False)
    
    except Address.DoesNotExist:
        return JsonResponse({"error": f"Address with ID: {id} does not exist."}, status=404)
