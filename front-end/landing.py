from nicegui import ui
import os
import re,requests


image_path = "images/"
BASE_URL = 'http://127.0.0.1:8000/'
dummy_description = '''
     pair of fashion pants can vary depending on the style, material, and design. Here's a generic description that you can modify based on the specific characteristics of the pants you have in mind
'''

  
@ui.page('/item/{name}')
async def get_similarity_popup(name:str):
    product_id = re.sub(r'[._]','||',name)
    product_id = product_id.split('||')[0]
    
    try:
        similar_product = requests.post(
            url=BASE_URL+'recommendation/similar-products',
            json={'product_id':product_id}
            )
        similar_products = similar_product.json()
        similar_products = similar_products['similar_products']
    except Exception as exp:
        ui.notify(exp)
        similar_products = []
    
    with ui.splitter() as splitter:
        with splitter.before:
            with ui.card().classes('w-full'):
                ui.image(image_path+name)
                with ui.card_section():
                    ui.label(name)
                    ui.label(dummy_description)
        with splitter.after:
            with ui.row():
                for image in similar_products:
                    with ui.card().classes('w-1/2.5 p-4'):
                        ui.image(image['image_url'])
                        with ui.card_section():
                            ui.link(image['variant_code'])
                            ui.label(image['description'])



def image_cards(images_with_name):
    pagination = ui.pagination(1, len(images_with_name)%9, direction_links=True)

    with ui.row():
        for image,name in images_with_name:
            with ui.card().classes('w-1/4 p-4'):
                ui.image(image)
                with ui.card_section():
                    ui.link(name,'/item/'+name)

images = os.listdir(image_path)[1:20]
images = [(image_path+image,image) for image in images]
image_cards(images)
ui.run()

