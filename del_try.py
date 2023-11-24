# from pymilvus import connections

# try:
#     connections.connect(host='localhost', port=19530, timeout=10)
#     # Rest of your code
# except Exception as e:
#     print(f"Error: {e}")

import re
name = "TBS00012KHAKI_1.jpj"
try:
    product_id = re.sub(r'[._]','||',name)
    product_id = product_id.split('||')[0]
except:
    pass
print(product_id)
