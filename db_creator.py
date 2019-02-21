#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###This program will fill an sql dataBase from The openFood API###

#imports module
import json

import MySQLdb
import requests as req

import db_lib as lib
import config as cfg

#Constants
CREATION_FILE = 'mySQL_DB_1.sql'
CATEGORIES_URL = 'https://fr.openfoodfacts.org/categories.json'
FOOD_URL = 'https://world.openfoodfacts.org/country/france/'

#DB Connection
DB = MySQLdb.connect(host=cfg.mysql['host'], user=cfg.mysql['user'], \
    passwd=cfg.mysql['passwd'], use_unicode=True, charset='utf8')
CURSOR = DB.cursor()

def get_data_from_api(url):
    data = req.get(url)
    return data.json()


######################################################################
###  fill the categories tables, with the categories from the API  ###
######################################################################
def fill_categories_table(url):   
    data_from_api = get_data_from_api(url)

    for data in data_from_api['tags']:
        
        if data['products'] > 300 and 'en:' in data['id']: #We won't take categories without some products
            try:
                category = lib.Categories(data)
                if 'en:' in category.name or 'fr:' in category.name:
                    pass
                else:
                    CURSOR.execute("INSERT INTO Categories (id, name)"\
                        "VALUES (%s, %s)", (category.id, category.name))
                    DB.commit()
            #We won't take non utf-8 data
            except DB.OperationalError:
                pass


######################################
###Function to fill the food tables###
######################################
def fill_food_table(url):   
    data_from_api = get_data_from_api(url)
    for data in data_from_api['products']:
        try:
            food = lib.Food(data)
            food_properties = (food.name, food.category_1, food.category_2, \
             food.category_3, food.category_4, food.category_5, food.nutri_score, food.stores, food.url)
            CURSOR.execute("INSERT INTO Food "\
                "(name, category_id_1, category_id_2, category_id_3, category_id_4, category_id_5, nutri_score, stores, url)"\
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", food_properties)
            DB.commit()
        except KeyError: 
            #We won't take lignes without : 'product_name'
            pass
        except AttributeError: 
            #We won't take products without categories
            pass
        except DB.OperationalError: 
            #We won't take products with an encoding error
            pass
        except DB.IntegrityError: 
            #We won't take products with a special category 
            pass
        except DB.DataError: 
            #We won't take products if the product name is too long
            pass

###################
###Main function###
###################
def main():
    #Creating the database
    file_sql = open(CREATION_FILE, 'r')
    query = " ".join(file_sql.readlines())
    CURSOR.execute(query)
    print("Database 'openfoodfacts' successfully created !")

    CURSOR.execute('use openfoodfacts;')
    fill_categories_table(CATEGORIES_URL)
    for i in range(1, 500): #Min pages --> Max pages
        url_food = FOOD_URL+str(i)+'.json'
        fill_food_table(url_food)
    print("Database 'openfoodfacts' successfully completed !")


if __name__ == "__main__":
    main()