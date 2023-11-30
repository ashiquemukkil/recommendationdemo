from nicegui import ui
import requests
# import pandas as pd


image_path = "images/"
HOST = 'host.docker.internal'
BASE_URL = 'http://'+HOST #'http://127.0.0.1'
dummy_description = '''
     pair of fashion pants can vary depending on the style, material, and design. Here's a generic description that you can modify based on the specific characteristics of the pants you have in mind
'''


@ui.page('/item/{name}')
async def get_similarity_popup(name:str):
    image  = requests.get(
            url=BASE_URL+':8000/recommendation/items',
            params={"index":name,"unique":1}
            ).json()
    try:
        similar_product = requests.post(
            url=BASE_URL+':8000/recommendation/similar-products',
            json={'product_id':name}
            )
        similar_products = similar_product.json()
        similar_products = similar_products['similar_products']
    except Exception as exp:
        print(exp)
        ui.notify(exp)
        similar_products = []
    
    with ui.splitter() as splitter:
        with splitter.before:
            with ui.card().classes('w-full'):
                ui.image(image)
                with ui.card_section():
                    ui.label(name)
                    ui.label(dummy_description)
        with splitter.after:
            with ui.row():
                for image in similar_products:
                    with ui.card().classes('w-1/4 p-4'):
                        ui.image(image['image_url'])
                        with ui.card_section():
                            ui.link(image['variant_code'])
                            ui.label(image['description'])



def image_cards():
    pagination = ui.pagination(1, 10, direction_links=True)
    images_with_name = requests.get(
            url=BASE_URL+':8000/recommendation/items/',
            params={"index":pagination.value,"unique":0}
            ).json()
    with ui.row():
        for image,name in images_with_name:
            with ui.card().classes('w-1/4 p-4'):
                ui.image(image)
                with ui.card_section():
                    ui.link(name,'/item/'+str(name))


# PROJECT_ROOT = '.'
# data = pd.read_excel(f"{PROJECT_ROOT}/cleaned_data.xlsx").head(25)

# images =[(j["images"],j["variant_code"]) for _,j in data.iterrows()]
image_cards()
ui.run()

