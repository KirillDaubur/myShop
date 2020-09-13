from .models import Product, ProductInOrder, ParameterizedProduct, Order, ProductProperty

def get_parameterized_product_properties_string(properties):
	return ", ".join(": ".join((str(i.product_type_property.name), str(i.value))) for i in properties) if len(properties) > 0 else "default"

def get_products_in_cart(cart):
	parameterized_products_in_cart = list(ParameterizedProduct.objects.filter(id__in=cart.keys()))

	for prod in parameterized_products_in_cart:
		properties = prod.properties.all()
		prod.properties_string = get_parameterized_product_properties_string(properties)

	products_and_properties = [(i.product, i.id, i.properties_string, i.amount_in_stock) for i in parameterized_products_in_cart]

	products_in_cart = []
	for i in products_and_properties:
		i[0].id = i[1]
		i[0].properties_string = i[2]
		i[0].amount_ordered = cart[str(i[0].id)]
		i[0].amount_in_stock = i[3]
		products_in_cart.append(i[0])

	return products_in_cart