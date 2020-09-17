from django import forms
from .models import Order, Product, ParameterizedProduct, ProductInOrder

class OrderItemForm(forms.Form):
	parameterized_product_id = forms.IntegerField(widget=forms.HiddenInput)
	count = forms.IntegerField(min_value=1)

	def __init__(self, porduct, properties, *args, **kwargs):
		super(forms.Form, self).__init__(*args, **kwargs)
		self.product = product
		self.properties = properties

class ProductForCartModel(forms.Form):
	desirable_parameters = forms.ChoiceField(widget=forms.Select(), label="")

	def __init__(self, properties, *args, **kwargs):
		super(forms.Form, self).__init__(*args, **kwargs)
		print(properties)
		if properties is not None:
			self.fields['desirable_parameters'].choices = [(k, v) for k, v in properties.items()] 

	def save(self, request):
		product_id = self.data['desirable_parameters']
		cart = request.session.get('cart', {})
		cart[product_id] = cart.get(product_id, 0) + 1
		request.session['cart'] = cart

class OrderForm(forms.ModelForm):
	class Meta:
		model = Order
		exclude = ['products', 'total_cost']

	def __init__(self, *args, **kwargs):	
		super(forms.ModelForm, self).__init__(*args, **kwargs)
		self.fields['name'].widget = forms.TextInput(attrs={
			'class': 'form-control' })
		self.fields['surname'].widget = forms.TextInput(attrs={
			'class': 'form-control' })
		self.fields['email'].widget = forms.EmailInput(attrs={
			'class': 'form-control' })
		self.fields['phone_number'].widget = forms.TextInput(attrs={
			'class': 'form-control' })
		self.fields['shipping_address'].widget = forms.Textarea(attrs={
			'class': 'form-control' })

	def save(self, request):
		cart = request.session.get('cart', {})
		if not cart:
			return

		order = self.instance
		order.total_cost = sum(i.product.price * j[1] for i in list(ParameterizedProduct.objects.filter(id__in=cart.keys())) for j in cart.items() if str(i.id) == j[0])
		order.save()

		for product_id, amount in cart.items():
			product_in_order = ProductInOrder(order=order, product=ParameterizedProduct.objects.get(id=int(product_id)), amount_ordered=amount)
			product_in_order.save()

		request.session["cart"] = {}

