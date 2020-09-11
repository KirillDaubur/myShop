from django.db import models

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

	type = models.ForeignKey("ProductType", on_delete=models.SET_NULL, null=True, to_field="id")
	name = models.CharField(max_length=20, help_text="Input trafaret name")

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

	type = models.ForeignKey("ProductType", on_delete=models.SET_NULL, null=True, to_field="id")
	name = models.CharField(max_length=30, help_text="Input compound name") 
	amount_in_stock = models.PositiveSmallIntegerField(null=False)
	color_rgb = models.CharField(max_length=7, help_text="Input Color RGB code")
	particular_matches = models.ManyToManyField(BlankTrafaret)

	def __str__(self):
		return "{} ({})".format(self.name, str(self.amount_in_stock))


class Product(models.Model):
	"""
	Class representing a ready for purchase final product
	"""

	name = models.CharField(max_length=20, help_text="Input product name")
	price = models.DecimalField(max_digits=7, decimal_places=2, help_text="Input price")
	type = models.ForeignKey("ProductType", on_delete=models.SET_NULL, null=True, to_field="id")
	blanks = models.ManyToManyField(Blank)
	trafaret = models.ForeignKey("BlankTrafaret", on_delete=models.SET_NULL, null=True)
	compounds = models.ManyToManyField(Compound)

	def __str__(self):
		return self.name