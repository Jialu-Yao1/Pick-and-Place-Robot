import xmlrpc.client
from PIL import Image
import base64

url = 'https://edu-ff219.odoo.com'
db = 'edu-ff219'

username = 'tanya.raja@ubc.ca'
password = 'EDUFF219!!' 
#API Key = 'd0e2e79d0fccd90702f9c490a2063d2fe0eb9d89'

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
print ("version info",common.version())

uid = common.authenticate(db, username, password, {})  

print("UID", uid)

## Don't run - this test only works with Tanya's local laptop
with open(r"C:\Users\tanya\Documents\Test2.png", "rb") as file:
    image_base64string = base64.b64encode(file.read()).decode('ascii')
    
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
create_id = models.execute_kw(db, uid, password, 'product.template', 'create', [{'name': "Specimen_1", 'image_1920': image_base64string}])
print("Created Product. Product ID:", create_id)


    
    

