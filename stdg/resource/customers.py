import shopify
import random
from faker import Factory
from pyactiveresource.connection import ResourceNotFound

from stdg import config


class Customers(object):
    settings = config.settings['customers']

    def __init__(self, locale="en_US"):

        self.locale = locale

        return

    def generate_data(self):

        # We're forcing US locale since it contains the most complete providers for the Faker package.
        fake = Factory.create(self.settings['locale'])

        first_name = fake.first_name()
        last_name = fake.last_name()

        # get the state info from the postal data we loaded eariler, [[zip, st]]
        state_info = random.sample(config.postal_data, 1)[0]

        customer = {
            'first_name': first_name,
            'last_name': last_name,
            'addresses': [
                {
                    'address1': fake.street_address(),
                    'city': fake.city(),
                    'province_code': str(state_info[1]),
                    'phone': fake.phone_number(),
                    'zip': str(state_info[0]),
                    'last_name': first_name,
                    'first_name': last_name,
                    'country': 'US'
                }
            ],
        }

        return customer

    # instance methods

    def create(self, number_customers):

        customers_created = []

        for counter in range(number_customers):

            print("Generating Customer: {0}".format(str(counter + 1)))

            new_customer = shopify.Customer().create(self.generate_data())

            if new_customer.errors:
                # something went wrong!
                for message in new_customer.errors.full_messages():
                    print(message)
                return

            customers_created.append(str(new_customer.id))

        with open('stdg-customers.csv', mode='a') as customers_file:
            customers_file.write('\n'.join(customers_created) + '\n')

        return

    def delete(self, customers=None):

        if customers is None:
            # delete all orders
            with open('stdg-customers.csv') as customer_file:
                customers_delete = customer_file.read().splitlines()

            for customer_id in customers_delete:

                try:
                    customer = shopify.Customer.find(int(customer_id))
                    customer.destroy()
                    print("[DELETED] Customer #{0}".format(customer_id))
                except ResourceNotFound:
                    print("[WARNING]: Customer #{0} not found.".format(customer_id))

        return
