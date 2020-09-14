from django.db import models
from django.core.validators import RegexValidator

class ProductTypeProperty(models.Model):
	"""
	Class representing the special property for appropriate Product type (e.g. size for the Ring or Plug Earings or Height, Width for the table, Length for the Bracelet etc.).
	"""

	name = models.CharField(max_length=20, help_text="Input product type name")
	product_type = models.ForeignKey("ProductType", on_delete=models.CASCADE, null=True, to_field="id")

	def __str__(self):
		return "{}: {}".format(self.product_type, self.name)

class ProductType(models.Model):
	"""
	Class representing the type of product, produced by my manufacture: rings, earings, necklets, phone cases, etc.
	"""

	name = models.CharField(max_length=20, help_text="Input product type name")

	def __str__(self):
		return self.name

class Blank(models.Model):
	"""
	Class representing a handmade blank, produced by manufacture, which will become a part of the final product
	after customization, post-processing (according to the order), combining with other Compounds.
	"""

	name = models.CharField(max_length=20, help_text="Input blank name")
	type = models.ForeignKey("ProductType", on_delete=models.SET_NULL, null=True, to_field="id")
	amount_in_stock = models.PositiveSmallIntegerField(null=False)

	def __str__(self):
		return "{} ({})".format(self.name, str(self.amount_in_stock))

	class Meta:
		ordering = ["type", "amount_in_stock", "name"]

class BlankTrafaret(models.Model):
	"""
	Class representing the trafaret for the Blank, the way it should be post-processed 
	to become a part of the final product (e.g. cut for jewelry, trafaret for appropriate phone model phone case)
	"""

	type = models.ForeignKey("ProductType", 
		on_delete=models.SET_NULL, 
		null=True, 
		to_field="id")
	name = models.CharField(max_length=40, help_text="Input trafaret name")

	#ToDo: add links to .png transparent trafaret pictures for website

	def __str__(self):
		return "{}: {}".format(self.type, self.name)	#maybe should be refactored in future

	class Meta:
		ordering = ["type", "name"]


class Compound(models.Model):
	"""
	Class representing the part of the final product, which is NOT produced by manufacture, but bought in the "ready-to-use" 
	state, which can be combined with Blank(s) to create a fincal product. E.g. fittings, silicone phone case, rope for bracelets, etc. 
	"""

	type = models.ForeignKey("ProductType", 
		on_delete=models.SET_NULL, 
		null=True, 
		to_field="id")
	name = models.CharField(max_length=40, help_text="Input compound name") 
	amount_in_stock = models.PositiveSmallIntegerField(null=False)
	color_rgb = models.CharField(max_length=7, help_text="Input Color RGB code")
	particular_matches = models.ManyToManyField(BlankTrafaret)

	def __str__(self):
		return "{} ({})".format(self.name, str(self.amount_in_stock))


class ProductProperty(models.Model):
	"""
	Class representing an instance of a ProductTypeProperty for a particular Product 
	"""

	relying_product = models.ForeignKey("ParameterizedProduct", 
		on_delete=models.CASCADE, 
		to_field="id", 
		related_name="properties", 
		related_query_name="properties")
	product_type_property = models.ForeignKey("ProductTypeProperty", 
		on_delete=models.SET_NULL, null=True, to_field="id")
	value = models.DecimalField(max_digits=10, decimal_places=2, null=False)

	def __str__(self):
		return "{}:{}".format(self.product_type_property, self.value)


class Product(models.Model):
	"""
	Class representing a complete product
	"""

	name = models.CharField(max_length=40, help_text="Input product name")
	price = models.DecimalField(max_digits=7, decimal_places=2, help_text="Input price")
	type = models.ForeignKey("ProductType", on_delete=models.SET_NULL, null=True, to_field="id")
	blanks = models.ManyToManyField(Blank)
	trafaret = models.ForeignKey("BlankTrafaret", on_delete=models.SET_NULL, null=True)
	compounds = models.ManyToManyField(Compound, blank=True)

	image = models.ImageField(upload_to="Images/Products/", null=True)

	def __str__(self):
		return self.name


class ParameterizedProduct(models.Model):
	"""
	Class representing a stack of particular product instances with a set of parameters (product property values) (e.g. 25 Diamond shaped rings of the size 16,5cm) 
	"""

	product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="parametrized_products", to_field="id")
	amount_in_stock = models.PositiveSmallIntegerField(null=False, default=0)

	def __str__(self):
		return str(self.product)


class ProductInOrder(models.Model):
	"""
	The intermediate entity between Parameterized Product and Order, representing Product in Order
	"""

	order = models.ForeignKey("Order", on_delete=models.CASCADE)
	product = models.ForeignKey("ParameterizedProduct", on_delete=models.CASCADE)
	amount_ordered = models.PositiveSmallIntegerField(null=False)

	def __str__(self):
		return "{} ordered {} {}(s)".format(str(self.order), str(self.amount_ordered), str(self.product))

class Order(models.Model):
	"""
	Class representing the User order in the shop
	"""

	name = models.CharField(max_length=25, help_text="Input your name")
	surname = models.CharField(max_length=25, help_text="Input your surname")
	email = models.EmailField()
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
	phone_number = models.CharField(validators=[phone_regex], max_length=17)
	shipping_address = models.TextField(help_text="Input the address of shipping (post office etc.)")

	products = models.ManyToManyField("ParameterizedProduct", through='ProductInOrder')
	total_cost = models.DecimalField(max_digits=7, decimal_places=2)

	def __str__(self):
		return "{}".format(self.email)
