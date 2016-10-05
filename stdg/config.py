import shopify
import csv

try:
    import configparser
except:
    from ConfigParser import configparser

zip_csv = 'zip-codes-100.csv'

settings = configparser.SafeConfigParser()
settings.read('stgd.ini')

store_settings = settings._sections['shopify']
shop_url = "https://%s:%s@%s.myshopify.com/admin" % (
    store_settings['api_key'], store_settings['api_pass'], store_settings['store'])
shopify.ShopifyResource.set_site(shop_url)

with open(zip_csv, 'rb') as cvsfile:
    postal_data = csv.reader(cvsfile)
    postal_data = list(postal_data)
