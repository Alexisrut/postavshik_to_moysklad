#CSV ПОЛНЫЙ КАТАЛОГ АВАНТМАРКЕТ
import base64
import xml.etree.ElementTree as ET
import csv
import requests
import datetime
import json
import time

username = 'ytesgr3705@vi64malishev'  # Замените на ваш логин
password = 'TUK4571vcz347'  # Замените на ваш пароль

    # Кодирование учетных данных в формат Base64
credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
headers = {
        "Authorization": f"Basic {credentials}",
        "Accept-Encoding": "gzip",
        "Content-Type": "application/json"
    }
#СКАЧИВАНИЕ ФАЙЛОВ
import os

#СОЗДАНИЕ ОПРИХОДОВАНИЙ
def add_ostat(product_url, quanity, code):
    store_href = "https://api.moysklad.ru/api/remap/1.2/entity/store/72b1fbcc-00b6-11ef-0a80-15390044905e"
    organization_href = "https://api.moysklad.ru/api/remap/1.2/entity/organization/72af2d26-00b6-11ef-0a80-15390044905b"
    url = "https://api.moysklad.ru/api/remap/1.2/entity/enter"
    data = {
        "name": f"enter{code}",
        "moment": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "code": f'{code}',
        "organization": {
                "meta": {
                    "href": organization_href,
                    "type": "organization",
                    "mediaType": "application/json"
                }
        }, 
        "store": {
                "meta": {
                    "href": store_href,
                    "type": "store",
                    "mediaType": "application/json"
                }
            },
        "positions": [{
                "quantity": int(quanity),
                "assortment": {
                  "meta": {
                    "href": product_url,
                    "metadataHref": "https://api.moysklad.ru/api/remap/1.2/entity/product/metadata",
                    "type": "product",
                    "mediaType": "application/json"
                  }
                },
                "overhead": 0
              }]
    }
    code += 2
    response = requests.post(url, headers=headers, json = data)
    print(response.json())
    return code

def remove_ostat(product_url, quanity, code):
  store_href = "https://api.moysklad.ru/api/remap/1.2/entity/store/72b1fbcc-00b6-11ef-0a80-15390044905e"
  organization_href = "https://api.moysklad.ru/api/remap/1.2/entity/organization/72af2d26-00b6-11ef-0a80-15390044905b"
  url = "https://api.moysklad.ru/api/remap/1.2/entity/loss"
  data = {
          "name": f"enter{code}",
          "moment": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
          "code": f'{code}',
          "organization": {
                  "meta": {
                      "href": organization_href,
                      "type": "organization",
                      "mediaType": "application/json"
                  }
          }, 
          "store": {
                  "meta": {
                      "href": store_href,
                      "type": "store",
                      "mediaType": "application/json"
                  }
              },
          "positions": [{
                  "quantity": int(quanity),
                  "assortment": {
                    "meta": {
                      "href": product_url,
                      "metadataHref": "https://api.moysklad.ru/api/remap/1.2/entity/product/metadata",
                      "type": "product",
                      "mediaType": "application/json"
                    }
                  },
                  "overhead": 0
                }]
      }
  code += 2
  response = requests.post(url, headers=headers, json = data)
  return code

def download_file(url, local_filename):
    # Скачиваем файл и сохраняем его локально
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename

def download_image(url, local_filename):
    # Скачиваем изображение и сохраняем его локально
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename

def delete_image(filename):
    os.remove(filename)

def images_folder_link(name, images_hrefs):
    import yadisk
    import os
    images = []
    y = yadisk.YaDisk(token="y0_AgAAAABntPPiAAvVuAAAAAEFmofoAADTHbNphWlBA4q--gkgCQ03uUAu6A")
    cnt = 1
    def split_image_links(input_string):
    # Используем метод split для разделения строки
        links = input_string.split(';')
        # Удаляем лишние пробелы в начале и конце каждой ссылки
        links = [link.strip() for link in links]
        return links

    # Пример использования
    input_string = images_hrefs
    images = split_image_links(input_string)
    def download_image(url, local_filename):
        # Скачиваем изображение и сохраняем его локально
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return local_filename
    def delete_image(filename):
        os.remove(filename)
    y.mkdir(f"/Avantmarket/{name}")
    for i in images:
        download_image(i, f"test-image-{cnt}.jpg")
        y.upload(f"test-image-{cnt}.jpg", f"/Avantmarket/{name}/test-image-{cnt}.jpg")
        delete_image(f"test-image-{cnt}.jpg")
        cnt += 1
    link = (y.get_download_link(f"/Avantmarket/{name}"))
    return link

def csv_avant_all():
    url = 'https://avantmarket.ru/price1/xml/avantmarket-all12.xml?1613570927'
    xml_file = download_file(url, "avantmarket-all12.xml")
    # Загрузка и парсинг XML файла
    tree = ET.parse('avantmarket-all12.xml')
    root = tree.getroot()

    # Поиск всех уникальных имен параметров
    param_names = set()
    for offer in root.findall('.//offer'):
        for param in offer.findall('param'):
            param_names.add(param.get('name'))

    # Сортировка имен параметров для упорядоченного вывода
    param_names = sorted(param_names)

    # Открытие CSV файла для записи
    with open('output.csv', 'w', newline='', encoding='utf-8') as csvfile:
        # Создание объекта writer
        csvwriter = csv.writer(csvfile)
        
        # Запись заголовков
        header = ['id', 'available', 'url', 'price', 'oldprice', 'currencyId', 'categoryId', 
                'picture', 'vendor', 'name', 'barcode', 'model', 'weight', 'description'] + param_names
        csvwriter.writerow(header)
        
        # Поиск всех элементов offer и запись их в CSV
        for offer in root.findall('.//offer'):
            # Сбор данных из каждого offer
            offer_data = [
                offer.get('id'),
                offer.get('available'),
                offer.find('url').text if offer.find('url') is not None else '',
                offer.find('price').text if offer.find('price') is not None else '',
                offer.find('oldprice').text if offer.find('oldprice') is not None else '',
                offer.find('currencyId').text if offer.find('currencyId') is not None else '',
                offer.find('categoryId').text if offer.find('categoryId') is not None else '',
                ';'.join([pic.text for pic in offer.findall('picture')]),
                offer.find('vendor').text if offer.find('vendor') is not None else '',
                offer.find('name').text if offer.find('name') is not None else '',
                offer.find('barcode').text if offer.find('barcode') is not None else '',
                offer.find('model').text if offer.find('model') is not None else '',
                offer.find('weight').text if offer.find('weight') is not None else '',
                offer.find('description').text if offer.find('description') is not None else ''
            ]
            
            # Словарь для параметров текущего offer
            params_dict = {name: '' for name in param_names}
            for param in offer.findall('param'):
                param_name = param.get('name')
                param_value = param.text
                if param_name in params_dict:
                    params_dict[param_name] = param_value
            
            # Добавление параметров к данным offer
            offer_data.extend([params_dict[name] for name in param_names])
            
            # Запись данных в CSV
            csvwriter.writerow(offer_data)

def csv_avant_category():
    import xml.etree.ElementTree as ET
    import csv
    # Загрузка и парсинг XML файла
    tree = ET.parse('avantmarket-all12.xml')
    root = tree.getroot()

    # Открытие CSV файла для записи
    with open('categories.csv', 'w', newline='', encoding='utf-8') as csvfile:
        # Создание объекта writer
        csvwriter = csv.writer(csvfile)
        cnt = 0
        # Запись заголовков
        header = ['category', 'code-category', 'parent-category', 'code-parent-category']
        csvwriter.writerow(header)
        # Поиск всех элементов offer и запись их в CSV
        

        for offer in root.findall('.//category'):
            if (cnt <= 7):
                cnt += 1
                continue
            # Сбор данных из каждого offer
            if (offer.get('id') == 1716):
                offer_data = [
                    offer.text,
                    offer.get('id'),
                    'Другое',
                    0
                ]
            if (offer.get('parentId') == '1241'):
                offer_data = [
                    offer.text,
                    offer.get('id'),
                    'Фонари',
                    offer.get('parentId')
                ]
            elif (offer.get('parentId') == '1250'):
                offer_data = [
                    offer.text,
                    offer.get('id'),
                    'Туристическое снаряжение',
                    offer.get('parentId')
                ]
            elif (offer.get('parentId') == '1276'):
                offer_data = [
                    offer.text,
                    offer.get('id'),
                    'Мультитулы',
                    offer.get('parentId')
                ]
            elif (offer.get('parentId') == '1283'):
                offer_data = [
                    offer.text,
                    offer.get('id'),
                    'Ножи',
                    offer.get('parentId')
                ]
            elif (offer.get('parentId') == '1292'):
                offer_data = [
                    offer.text,
                    offer.get('id'),
                    'Точилки для ножей',
                    offer.get('parentId')
                ]
            elif (offer.get('parentId') == '1506'):
                offer_data = [
                    offer.text,
                    offer.get('id'),
                    'Туристическая одежда',
                    offer.get('parentId')
                ]
            elif (offer.get('parentId') == '1688'):
                offer_data = [
                    offer.text,
                    offer.get('id'),
                    'Инструменты',
                    offer.get('parentId')
                ]
            elif (offer.get('parentId') == '1700'):
                offer_data = [
                    offer.text,
                    offer.get('id'),
                    'Термобелье',
                    offer.get('parentId')
                ]
            elif (offer.get('parentId') == '1716'):
                offer_data = [
                    offer.text,
                    offer.get('id'),
                    'Маркетинговая продукция',
                    offer.get('parentId')
                ]
            else:
                offer_data = [
                    offer.text,
                    offer.get('id'),
                    'Другое',
                    0
                ]
            
            # Запись данных в CSV
            csvwriter.writerow(offer_data)

def add_category(df_avant_all, df_avant_category):
    categories = []
    parent_categories = []
    cnt = 1
    for category in df_avant_all["categoryId"]:
        try:
            selected = df_avant_category[df_avant_category['code-category'] == int(category)]
            categories.append(selected.values.flatten().tolist()[0])
            parent_categories.append(selected.values.flatten().tolist()[3])
            cnt += 1
        except:
            try:
                selected = df_avant_category[df_avant_category['code-parent-category'] == int(category)]
                categories.append(selected.values.flatten().tolist()[3])
                parent_categories.append('Другое')
                cnt += 1
            except:
                categories.append('Другое')
                parent_categories.append('Другое')
    df_avant_all["category"] = categories
    df_avant_all["parent-category"] = parent_categories

def edit_description(df_avant_all):
    import pandas as pd
    from bs4 import BeautifulSoup

    # Предположим, ваш DataFrame называется df и имеет колонку 'description'
    def clean_html(text):
        # Убираем CDATA
        text = text.replace('<![CDATA[', '').replace(']]>', '')
        # Парсим текст с BeautifulSoup
        soup = BeautifulSoup(text, 'html.parser')
        # Возвращаем текст без HTML тегов
        return soup.get_text(separator=' ', strip=True)
    
    for i in df_avant_all["description"]:
        i = clean_html(str(i))

def create_groups(df_avant_all, df_avant_category):
    url = 'https://api.moysklad.ru/api/remap/1.2/entity/productfolder'  # Замените на URL вашего API
    username = 'ytesgr3705@vi64malishev'  # Замените на ваш логин
    password = 'TUK4571vcz347'  # Замените на ваш пароль

    # Кодирование учетных данных в формат Base64
    credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
    df_groups = pd.DataFrame(columns = ["name", "href"])
    df_parent_groups = pd.DataFrame(columns = ["name", "href"])
    headers = {
        "Authorization": f"Basic {credentials}",
        "Accept-Encoding": "gzip",
        "Content-Type": "application/json"
    }
    for i in df_avant_category["parent-category"].unique():
        data = {
            'name' : str(i)
        }
        response = requests.post(url, headers=headers, json=data)
        token = response.json()
        df_parent_groups.loc[len(df_parent_groups.index)] = [i, token["meta"]["href"]]
    for i in df_avant_all["category"].unique():
        try:
            value = df_avant_category.loc[df_avant_category['category'] == i, 'parent-category'].iloc[0]
            res_value = df_parent_groups.loc[df_parent_groups['name'] == value, 'href'].iloc[0]
            data = {
                'name' : i,
                'productFolder': {
                    "meta": {
                            "href": res_value,
                            "metadataHref": "https://api.moysklad.ru/api/remap/1.2/entity/productfolder/metadata",
                            "type": "productfolder",
                            "mediaType": "application/json"
                        }
                    }
                }
            response = requests.post(url, headers=headers, json=data)
            token = response.json()
            df_groups.loc[len(df_groups.index)] = [i, token["meta"]["href"]]
            #print(i, token["meta"]["href"])
        except:
            if (i == 'Другое'):
                res_value = df_parent_groups.loc[df_parent_groups['name'] == i, 'href'].iloc[0]
                data = {
                'name' : i,
                'productFolder': {
                    "meta": {
                            "href": res_value,
                            "metadataHref": "https://api.moysklad.ru/api/remap/1.2/entity/productfolder/metadata",
                            "type": "productfolder",
                            "mediaType": "application/json"
                        }
                    }
                }
                response = requests.post(url, headers=headers, json=data)
                token = response.json()
                df_groups.loc[len(df_groups.index)] = [i, token["group"]["meta"]["href"]]
            else:
                value = df_avant_category.loc[df_avant_category['code-parent-category'] == i, 'parent-category'].iloc[0]
                res_value = df_parent_groups.loc[df_parent_groups['name'] == value, 'href'].iloc[0]
                df_groups.loc[len(df_groups.index)] = [i, res_value]
    return df_groups

def create_all_prod_with_ost(df_avant_all, df_groups, credentials, code):
    cnt = 1
    for i in df_avant_all["name"]:
        try:
            buy_price = df_avant_all.loc[df_avant_all['name'] == i, 'Opt'].iloc[0]
            price = df_avant_all.loc[df_avant_all['name'] == i, 'rrc'].iloc[0]
            category_name = df_avant_all.loc[df_avant_all['name'] == i, 'category'].iloc[0]
            category_href = df_groups.loc[df_groups['name'] == category_name, 'href'].iloc[0]
            picture_name = df_avant_all.loc[df_avant_all['name'] == i, 'picture'].iloc[0]
            url = df_avant_all.loc[df_avant_all['name'] == i, 'url'].iloc[0]
            quanity = df_avant_all.loc[df_avant_all['name'] == i, 'Остаток'].iloc[0]
            model = df_avant_all.loc[df_avant_all['name'] == i, 'model'].iloc[0]
            weight = df_avant_all.loc[df_avant_all['name'] == i, 'weight'].iloc[0]
            description = df_avant_all.loc[df_avant_all['name'] == i, 'description'].iloc[0]
            volume = ""
            params = ""
            try:
                if (picture_name != ""):
                    images_href = images_folder_link(i, str(picture_name))
                    params += "Ссылка на фото:" + str(images_href) + '\n'
                else:
                    params += "Ссылка на фото:-"
                params += "Описание:" + str(description) + '\n'
                barcode = df_avant_all.loc[df_avant_all['name'] == i, 'barcode'].iloc[0]
                #print(price, category_name, category_href, picture_name, url, quanity, model, weight)
                for j in df_avant_all.columns:
                    if (cnt > 15):
                        if (str(df_avant_all.loc[df_avant_all['name'] == i, j].iloc[0]) != 'nan' and j != 'Краткое описание' and j != 'Остаток' and j != 'category' and j != 'parent-category' and j != 'Объём'):
                            params = params + j + ':' + str(df_avant_all.loc[df_avant_all['name'] == i, j].iloc[0]) + '\n'
                        elif (j == 'Объём'):
                            volume = str(df_avant_all.loc[df_avant_all['name'] == i, j])
                    else:
                        cnt += 1
                cnt = 0
                #params = params + "Ссылка на загрузку папки яндекс диск:" + df_image.loc[df_image['name'] == i, 'link'].iloc[0]
                barcodes = []
                barcodes.append({
                    "ean13": str(barcode)
                    })
                request_url = "https://api.moysklad.ru/api/remap/1.2/entity/product"
                headers = {
                "Authorization": f"Basic {credentials}",
                "Accept-Encoding": "gzip",
                "Content-Type": "application/json"
                }
                print(model)
                if volume != '':
                    data = {
                        'name' : i,
                        "description": params,
                        "salePrices": [{
                            "value": int(price) * 100,
                            "currency": {
                            "meta": {
                                'href': 'https://api.moysklad.ru/api/remap/1.2/entity/currency/72b26f85-00b6-11ef-0a80-153900449063', 
                                'metadataHref': 'https://api.moysklad.ru/api/remap/1.2/entity/currency/metadata', 
                                'type': 'currency', 
                                'mediaType': 'application/json'
                            }
                            },
                            "priceType": {
                                    'meta': {
                                        'href': 'https://api.moysklad.ru/api/remap/1.2/context/companysettings/pricetype/ee676643-0148-11ef-0a80-0d680009531f', 
                                        'type': 'pricetype', 
                                        'mediaType': 'application/json'
                                        }, 
                                    'id': 'ee676643-0148-11ef-0a80-0d680009531f', 
                                    'name': 'Цена продажи', 
                                    'externalCode': 'be069eaa-2a59-48b8-bc0b-5c54a4c393fe'
                                }
                        }],
                        'productFolder': {
                            "meta": {
                            "href": category_href,
                            "metadataHref": "https://api.moysklad.ru/api/remap/1.2/entity/productfolder/metadata",
                            "type": "productfolder",
                            "mediaType": "application/json"
                            }
                        },
                        'weight': int(weight),
                        'volume': int(volume),
                        'barcode': barcodes,
                        'article': model
                    }
                else:
                    data = {
                    'name' : i,
                    "description": params,
                    "salePrices": [{
                        "value": int(price) * 100,
                        "currency": {
                        "meta": {
                            'href': 'https://api.moysklad.ru/api/remap/1.2/entity/currency/72b26f85-00b6-11ef-0a80-153900449063', 
                            'metadataHref': 'https://api.moysklad.ru/api/remap/1.2/entity/currency/metadata', 
                            'type': 'currency', 
                            'mediaType': 'application/json'
                        }
                        },
                        "priceType": {
                                'meta': {
                                    'href': 'https://api.moysklad.ru/api/remap/1.2/context/companysettings/pricetype/ee676643-0148-11ef-0a80-0d680009531f', 
                                    'type': 'pricetype', 
                                    'mediaType': 'application/json'
                                    }, 
                                'id': 'ee676643-0148-11ef-0a80-0d680009531f', 
                                'name': 'Цена продажи', 
                                'externalCode': 'be069eaa-2a59-48b8-bc0b-5c54a4c393fe'
                            }
                    }],
                    'productFolder': {
                        "meta": {
                        "href": category_href,
                        "metadataHref": "https://api.moysklad.ru/api/remap/1.2/entity/productfolder/metadata",
                        "type": "productfolder",
                        "mediaType": "application/json"
                        }
                    },
                    'weight': int(weight),
                    'barcodes': barcodes,
                    'article': model
                    }
                response = requests.post(request_url, headers=headers, json=data)
                token = response.json()
                #ДОБАВЛЕНИЕ ОСТАТКОВ
                store_href = "https://api.moysklad.ru/api/remap/1.2/entity/store/72b1fbcc-00b6-11ef-0a80-15390044905e"
                organization_href = "https://api.moysklad.ru/api/remap/1.2/entity/organization/72af2d26-00b6-11ef-0a80-15390044905b"
                url = "https://api.moysklad.ru/api/remap/1.2/entity/enter"
                data = {
                    "name": f"enter{code}",
                    "moment": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "code": f'{code}',
                    "organization": {
                            "meta": {
                                "href": organization_href,
                                "type": "organization",
                                "mediaType": "application/json"
                            }
                    }, 
                    "store": {
                            "meta": {
                                "href": store_href,
                                "type": "store",
                                "mediaType": "application/json"
                            }
                        },
                    "positions": [{
                            "quantity": int(quanity),
                            "assortment": {
                            "meta": {
                                "href": token["meta"]["href"],
                                "metadataHref": "https://api.moysklad.ru/api/remap/1.2/entity/product/metadata",
                                "type": "product",
                                "mediaType": "application/json"
                            }
                            },
                            "overhead": 0
                        }]
                }
                code += 2
                response = requests.post(url, headers=headers, json = data)
            except:
                params += "Описание:" + str(description) + '\n'
                barcode = df_avant_all.loc[df_avant_all['name'] == i, 'barcode'].iloc[0]
                #print(price, category_name, category_href, picture_name, url, quanity, model, weight)
                for j in df_avant_all.columns:
                    if (cnt > 15):
                        if (str(df_avant_all.loc[df_avant_all['name'] == i, j].iloc[0]) != 'nan' and j != 'Краткое описание' and j != 'Остаток' and j != 'category' and j != 'parent-category' and j != 'Объём'):
                            params = params + j + ':' + str(df_avant_all.loc[df_avant_all['name'] == i, j].iloc[0]) + '\n'
                        elif (j == 'Объём'):
                            volume = str(df_avant_all.loc[df_avant_all['name'] == i, j])
                    else:
                        cnt += 1
                cnt = 0
                #params = params + "Ссылка на загрузку папки яндекс диск:" + df_image.loc[df_image['name'] == i, 'link'].iloc[0]
                barcodes = []
                barcodes.append({
                    "ean13": str(barcode)
                    })
                request_url = "https://api.moysklad.ru/api/remap/1.2/entity/product"
                headers = {
                "Authorization": f"Basic {credentials}",
                "Accept-Encoding": "gzip",
                "Content-Type": "application/json"
                }
                print(model)
                if volume != '':
                    data = {
                        'name' : i,
                        "description": params,
                        "salePrices": [{
                            "value": int(price) * 100,
                            "currency": {
                            "meta": {
                                'href': 'https://api.moysklad.ru/api/remap/1.2/entity/currency/72b26f85-00b6-11ef-0a80-153900449063', 
                                'metadataHref': 'https://api.moysklad.ru/api/remap/1.2/entity/currency/metadata', 
                                'type': 'currency', 
                                'mediaType': 'application/json'
                            }
                            },
                            "priceType": {
                                    'meta': {
                                        'href': 'https://api.moysklad.ru/api/remap/1.2/context/companysettings/pricetype/ee676643-0148-11ef-0a80-0d680009531f', 
                                        'type': 'pricetype', 
                                        'mediaType': 'application/json'
                                        }, 
                                    'id': 'ee676643-0148-11ef-0a80-0d680009531f', 
                                    'name': 'Цена продажи', 
                                    'externalCode': 'be069eaa-2a59-48b8-bc0b-5c54a4c393fe'
                                }
                        }],
                        'productFolder': {
                            "meta": {
                            "href": category_href,
                            "metadataHref": "https://api.moysklad.ru/api/remap/1.2/entity/productfolder/metadata",
                            "type": "productfolder",
                            "mediaType": "application/json"
                            }
                        },
                        'weight': int(weight),
                        'volume': int(volume),
                        'barcode': barcodes,
                        'article': model
                    }
                else:
                    data = {
                    'name' : i,
                    "description": params,
                    "salePrices": [{
                        "value": int(price) * 100,
                        "currency": {
                        "meta": {
                            'href': 'https://api.moysklad.ru/api/remap/1.2/entity/currency/72b26f85-00b6-11ef-0a80-153900449063', 
                            'metadataHref': 'https://api.moysklad.ru/api/remap/1.2/entity/currency/metadata', 
                            'type': 'currency', 
                            'mediaType': 'application/json'
                        }
                        },
                        "priceType": {
                                'meta': {
                                    'href': 'https://api.moysklad.ru/api/remap/1.2/context/companysettings/pricetype/ee676643-0148-11ef-0a80-0d680009531f', 
                                    'type': 'pricetype', 
                                    'mediaType': 'application/json'
                                    }, 
                                'id': 'ee676643-0148-11ef-0a80-0d680009531f', 
                                'name': 'Цена продажи', 
                                'externalCode': 'be069eaa-2a59-48b8-bc0b-5c54a4c393fe'
                            }
                    }],
                    'productFolder': {
                        "meta": {
                        "href": category_href,
                        "metadataHref": "https://api.moysklad.ru/api/remap/1.2/entity/productfolder/metadata",
                        "type": "productfolder",
                        "mediaType": "application/json"
                        }
                    },
                    'weight': int(weight),
                    'barcodes': barcodes,
                    'article': model
                    }
                response = requests.post(request_url, headers=headers, json=data)
                token = response.json()
                #ДОБАВЛЕНИЕ ОСТАТКОВ
                store_href = "https://api.moysklad.ru/api/remap/1.2/entity/store/72b1fbcc-00b6-11ef-0a80-15390044905e"
                organization_href = "https://api.moysklad.ru/api/remap/1.2/entity/organization/72af2d26-00b6-11ef-0a80-15390044905b"
                url = "https://api.moysklad.ru/api/remap/1.2/entity/enter"
                data = {
                    "name": f"enter{code}",
                    "moment": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "code": f'{code}',
                    "organization": {
                            "meta": {
                                "href": organization_href,
                                "type": "organization",
                                "mediaType": "application/json"
                            }
                    }, 
                    "store": {
                            "meta": {
                                "href": store_href,
                                "type": "store",
                                "mediaType": "application/json"
                            }
                        },
                    "positions": [{
                            "quantity": int(quanity),
                            "assortment": {
                            "meta": {
                                "href": token["meta"]["href"],
                                "metadataHref": "https://api.moysklad.ru/api/remap/1.2/entity/product/metadata",
                                "type": "product",
                                "mediaType": "application/json"
                            }
                            },
                            "overhead": 0
                        }]
                }
                code += 2
                response = requests.post(url, headers=headers, json = data)
        except:
            continue
    return code

        

def update_ostat(ostat_df, code):
    url = 'https://api.moysklad.ru/api/remap/1.2/entity/product'
    response = requests.get(url, headers=headers)
    products = response.json()
    url = 'https://api.moysklad.ru/api/remap/1.2/report/stock/all'
    response = requests.get(url, headers=headers)
    ostat = response.json()
    for i in products["rows"]:
        for j in ostat["rows"]:
            if i["meta"]["href"]+"?expand=supplier" == j["meta"]["href"]:
                if (ostat_df.loc[ostat_df['Артикул'] == i['article'], 'В наличии'].iloc[0] > j["stock"]):
                    code = add_ostat(i["meta"]["href"], ostat_df.loc[ostat_df['Артикул'] == i['article'], 'В наличии'].iloc[0]-j["stock"], code)
                else:
                    code = remove_ostat(i["meta"]["href"], j["stock"]-ostat_df.loc[ostat_df['Артикул'] == i['article'], 'В наличии'].iloc[0], code)
    return code

#СОЗДАНИЕ ВСЕХ DATAFRAME
csv_avant_all()
csv_avant_category()
code = 200100
import pandas as pd
df_avant_category = pd.read_csv('categories.csv')
df_avant_all = pd.read_csv('output.csv')

df_avant_stock = pd.read_csv('avantmarket-price (1).csv', sep=';', header=None)
df_avant_stock = df_avant_stock.rename(columns=df_avant_stock.iloc[0])
df_avant_stock = df_avant_stock.drop(df_avant_stock.index[0])

add_category(df_avant_all, df_avant_category)
edit_description(df_avant_all)
df_groups = create_groups(df_avant_all, df_avant_category)
code = create_all_prod_with_ost(df_avant_all, df_groups, credentials, code)

download_file("https://avantmarket.ru/price1/csv/avantmarket-price.csv", "avant_ostat.csv")
ostat_df = pd.read_csv("avant_ostat.csv", delimiter=";")

code = update_ostat(ostat_df, code)

while(True):
    time.sleep(432000)
    url = 'https://api.moysklad.ru/api/remap/1.2/entity/enter'
    response = requests.get(url, headers=headers)
    for i in response.json()["rows"]:
        response = requests.delete(i["meta"]["href"], headers=headers)
    url = 'https://api.moysklad.ru/api/remap/1.2/entity/loss'
    response = requests.get(url, headers=headers)
    for i in response.json()["rows"]:
        response = requests.delete(i["meta"]["href"], headers=headers)
    url = 'https://api.moysklad.ru/api/remap/1.2/entity/product'
    response = requests.get(url, headers=headers)
    for i in response.json()["rows"]:
        response = requests.delete(i["meta"]["href"], headers=headers)
    url = 'https://api.moysklad.ru/api/remap/1.2/entity/productfolder/delete'
    url_get = 'https://api.moysklad.ru/api/remap/1.2/entity/productfolder' 
    response = requests.get(url_get, headers=headers)
    result = response.json()
    for i in result["rows"]:
        response = requests.post(url, headers=headers, json=i)
        token = response.json()

    csv_avant_all()
    csv_avant_category()
    import pandas as pd
    df_avant_category = pd.read_csv('categories.csv')
    df_avant_all = pd.read_csv('output.csv')

    df_avant_stock = pd.read_csv('avantmarket-price (1).csv', sep=';', header=None)
    df_avant_stock = df_avant_stock.rename(columns=df_avant_stock.iloc[0])
    df_avant_stock = df_avant_stock.drop(df_avant_stock.index[0])

    add_category(df_avant_all, df_avant_category)
    edit_description(df_avant_all)
    df_groups = create_groups(df_avant_all, df_avant_category)
    code = create_all_prod_with_ost(df_avant_all, df_groups, credentials, code)

    download_file("https://avantmarket.ru/price1/csv/avantmarket-price.csv", "avant_ostat.csv")
    ostat_df = pd.read_csv("avant_ostat.csv", delimiter=";")

    code = update_ostat(ostat_df, code)