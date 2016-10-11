from faker import Factory
import random
import shopify


class Products(object):

    def __init__(self, settings=None):
        if not settings:
            from stdg import config
            self.settings = config.settings['shopify']
        else:
            self.settings = settings
            shop_url = "https://%s:%s@%s.myshopify.com/admin" % (self.settings['api_key'],
                                                                 self.settings['api_pass'],
                                                                 self.settings['store'])
            shopify.ShopifyResource.set_site(shop_url)

        return

    # class methods

    def generate_data(self, cls):
        variant_count = random.randint(1, 4)
        fake = Factory.create()

        product_data = {
                "title": fake.bs(),
                "body_html": fake.text(),
                "vendor": fake.company(),
                "product_type": fake.word(),
                "variants": [
                ]
            }

        for _ in range(variant_count):
            product_data['variants'].append(
                {
                    "option1": fake.word(),
                    "price": str(fake.pyint()),
                    "inventory_management": "shopify",
                    "inventory_quantity": 0,
                    "inventory_policy": "continue",
                    "sku": 123,
                }
            )

        return product_data

    def create(self, number_products):
        new_products = []

        for counter in range(number_products):
            print("Generating Product: {0}".format(str(counter + 1)))
            print("current site mang", shopify.Product()._site)

            new_product = shopify.Product().create(self.generate_data(self))

            if new_product.errors:
                # something went wrong!
                # TODO: we need to loop over our error messages and print them
                for message in new_product.errors.full_messages():
                    print("[ERROR] {0}".format(message))
                    break
            new_products.append(new_product)
        return new_products

    def delete(self, orders=None):

        if orders is None:
            # delete all orders
            with open('stdg-orders.csv') as order_file:
                orders_delete = order_file.read().splitlines()

            for order_number in orders_delete:

                try:
                    order = shopify.Order.find(int(order_number))
                    order.cancel()
                    order.destroy()
                    print("[DELETED] Order #{0}".format(order_number))
                except ResourceNotFound:
                    print("[WARNING] Order #{0} not found.".format(order_number))

        return
