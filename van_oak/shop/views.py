from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from .forms import OrderForm, ProductForCartModel
from .models import Product, ProductInOrder, ParameterizedProduct, Order, ProductProperty
from .services import get_products_in_cart, get_parameterized_product_properties_string


def product_list(request):
	products = list(set(Product.objects.filter(parametrized_products__amount_in_stock__gt=0)))

	return render(
        request,
        'product_list.html',
        context={'products':products},
    )

def product(request, id):
	try:
		product = Product.objects.get(id=id)
	except ObjectDoesNotExist:
		return HttpResponse("Product not found.")

	prameterized_products = product.parametrized_products.filter(amount_in_stock__gt=0)

	if not prameterized_products:
		return HttpResponse("Sorry, but current product is out of stock.")
	parameters_dict = {}

	for prod in prameterized_products:
		properties = prod.properties.all()
		parameters_dict[str(prod.id)] = get_parameterized_product_properties_string(properties)

	if request.method == 'POST':
		form = ProductForCartModel(parameters_dict, request.POST)
		if(form.is_valid()):
			form.save(request)
			return redirect("product_list")

	form = ProductForCartModel(properties=parameters_dict)
	blanks = product.blanks.all()
	compounds = product.compounds.all()
	return render(request, 'product.html', context = { 'product': product, 'blanks': blanks, 'compounds': compounds, 'form': form })
		

def cart(request):
	errors = ""
	order_form = OrderForm()	
	cart = request.session.get('cart', {})
	
	products_in_cart = get_products_in_cart(cart)

	for product in products_in_cart:
		if product.amount_ordered > product.amount_in_stock:
			errors += "Not enough items in the stock. Order may be shipped a week later.\n"
			break

	order_total = sum(i.price * i.amount_ordered for i in products_in_cart)

	if request.method == 'POST':
		if not cart:
			errors += "No items to purchase. Please, add items to cart first.\n"
		else:
			order_form = OrderForm(request.POST)
			if order_form.is_valid():
				order = order_form.save(request)
				return redirect("thanks")

	return render(request, 'cart.html', context = { 'products_in_cart': products_in_cart, "order_form": order_form, "order_total": order_total, "errors": errors })

def remove_from_cart(request, product_id):
	cart = request.session.get('cart', {})
	del cart[str(product_id)]
	request.session['cart'] = cart
	return redirect("cart")

def increase_item_count_in_order(request, product_id):
	cart = request.session.get('cart', {})
	cart[str(product_id)] = cart.get(str(product_id), 0) + 1
	request.session['cart'] = cart
	return redirect("cart")

def decrease_item_count_in_order(request, product_id):
	cart = request.session.get('cart', {})
	count = cart.get(str(product_id), 0)
	if count > 1:
		cart[str(product_id)] = count - 1
	else:
		del cart[str(product_id)]

	request.session['cart'] = cart
	return redirect("cart")


def thanks_for_order(request):
	return render(request, 'thanks_for_order.html')
