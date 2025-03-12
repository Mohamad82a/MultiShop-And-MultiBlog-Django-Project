from collections.abc import ItemsView

from product.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        self.post_price = 70000

        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}

        self.cart = cart

    def __iter__(self):
        cart = self.cart.copy()
        for item in cart.values():
            product = Product.objects.get(id=item['id'])
            item['product'] = product
            item['attributes'] = item.get('attributes', {})

            if product.discount > 0:
                item['discount_price'] = product.discount_price
                item['total'] = int(item['discount_price']) * int(item['quantity'])
            else:
                item['total'] = int(item['price']) * int(item['quantity'])


            item['unique_id'] = self.unique_id_generator(product.id, item.get('attributes', {}))
            yield item


    def unique_id_generator(self, id, attribute_name):
        result = f'{id}-{attribute_name}'
        return result


    def remove_cart(self):
        del self.session['cart']


    def add(self, product, selected_attributes, quantity):
        unique = self.unique_id_generator(product.id, selected_attributes)
        if unique not in self.cart:
            self.cart[unique] = {
                'quantity': 0,
                'price': str(product.price),
                'discount': int(product.discount),
                'attributes': selected_attributes,
                'id':str(product.id)
            }

        self.cart[unique]['quantity'] += int(quantity)
        self.save()


    def discount(self):
        cart = self.cart.values()
        discounts = sum(int(item['discount'])* int(item['quantity']) for item in cart)
        return discounts

    def subtotal(self):
        cart = self.cart.values()
        subtotal = sum(int(item['price']) * int(item['quantity']) for item in cart)
        return subtotal



    def product_quantity(self):
        cart = self.cart.values()
        quantities = sum(int(item['quantity']) for item in cart)
        return quantities

    def cart_grandtotal(self):
        discount = self.discount()
        grand_total = self.subtotal() - discount
        return grand_total

    def order_grandtotal(self):
        discount = self.discount()
        grand_total = self.subtotal() + self.post_price - discount
        return grand_total

    def delete(self, id):
        if id in self.cart:
            del self.cart[id]
            self.save()

    # def clear(self):
    #     self.session['cart'] = {}
    #     self.session.modified = True


    def save(self):
        self.session.modified = True


# https://rousek.name/articles/shopify-like-product-variants-in-django