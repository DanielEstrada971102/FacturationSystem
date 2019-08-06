class Bill(object):
	def __init__(self, customer = ""):
		self.customer = customer
		self.products = dict()

	def addField(self, amount, productName, price):
		self.products[productName] = amount, price, amount * price

	def deleteField(self, productName):
		self.products.pop(productName)

	def getTotal(self):
		total = 0

		for _, (_, _, subtotal) in self.products.items():
			total += subtotal

		return total

	def show(self):
		pass

	def renderProduct(self, product):
		amount, price, subtotal = self.products[product]

		text = '%.2f %s %f %f\n' % (amount, product, price, subtotal)

		return text

	def save(self, filename):
		with open(filename, 'w') as file:
			for productName in self.products:
				file.write(self.renderProduct(productName))

