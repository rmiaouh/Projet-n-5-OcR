#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Main script of the P5 programm"""

#imports
import MySQLdb

import db_lib as lib
import config as cfg

#DB Connection
DB = MySQLdb.connect(host=cfg.mysql['host'], user=cfg.mysql['user'], \
    passwd=cfg.mysql['passwd'], use_unicode=True, charset='utf8')
CURSOR = DB.cursor()


###Show XX categories###
def select_categories(dict_categories):
    #Ask the user for enter a category
    #SQL request for categories
    CURSOR.execute('USE openfoodfacts;')
    CURSOR.execute("""SELECT id, name \
        FROM Categories ORDER BY name
        """)
    categories = CURSOR.fetchall()
    #Fill dict_categories with the result of the request
    index = 1
    for i in categories:
        categories_display = lib.Categories(i, index)
        dict_categories[categories_display.index] = (categories_display.name, categories_display.id)
        print(index, " : ", categories_display.name)
        index += 1
    return dict_categories

###Select 10 products in the database###
def select_products(category):
    category = '%' + category + '%'
    CURSOR.execute('USE openfoodfacts;')
    CURSOR.execute("""SELECT id, name, category_id_1, category_id_2, category_id_3, \
        category_id_4, category_id_5, nutri_score, stores, url \
        FROM Food \
        WHERE category_id_1 LIKE %s OR category_id_2 LIKE %s OR category_id_3 LIKE %s \
        OR category_id_4 LIKE %s OR category_id_5 LIKE %s
        LIMIT 10""", (category, category, category, category, category))
    products = CURSOR.fetchall()
    return products


###Add the chosen product and his substitute to the TABLE User in the database###
def add_favorite(product, substitute):
    print('\n Do you want to save this match as favorite ?')
    print('1. Yes')
    print('2. No')
    choice = try_user_input(2)
    if choice == 1:
        CURSOR.execute('USE openfoodfacts;')
        CURSOR.execute("""INSERT INTO Favorites (product_id, substitute_id) \
            VALUES (%s,%s)""", (product.id, substitute.id))
        DB.commit()
        print('Your favorite product has been saved')
    elif choice == 2:
        print("The product wasn't saved")

###Seach a correct substitute of the product in the database###
def search_substitute(product):
    CURSOR.execute('USE openfoodfacts;')
    #Make a string with the categories, used in the query
    search = (product.category_1, product.category_2, product.category_3, \
        product.category_4, product.category_5)
    #Other variables of the request
    product_name = product.name
    product_score = product.nutri_score
    CURSOR.execute("""SELECT Food.id, Food.name, C1.name as category_1, C2.name as category_2, \
        C3.name as category_3, C4.name as category_4, C5.name as category_5, nutri_score, stores, url \
    FROM Food \
    INNER JOIN Categories C1 ON C1.id = Food.category_id_1 \
    INNER JOIN Categories C2 ON C2.id = Food.category_id_2 \
    INNER JOIN Categories C3 ON C3.id = Food.category_id_3 \
    INNER JOIN Categories C4 ON C4.id = Food.category_id_4 \
    INNER JOIN Categories C5 ON C5.id = Food.category_id_5 \
    WHERE (C1.name IN %s OR C2.name IN %s OR C3.name IN %s OR C4.name IN %s OR C5.name IN %s) \
    AND Food.name NOT LIKE %s
    AND Food.nutri_score = %s""", (search, search, search, search, search, product_name, product_score))
    substitute = CURSOR.fetchone()
    try:
        return lib.Food(substitute)
    except TypeError :
        print("We didn't find a substitute for your product")

###Use the result of the products selection function and display it###
def display_products_list(products):
    print('\n Select a product : ')
    dict_product = {}
    index = 1
    for i in products:
        products_display = lib.Food(i, index)
        dict_product[products_display.index] = products_display.name
        print(index, " : ", products_display.name)
        index += 1
    return dict_product

###Test the input value###
def try_user_input(number_of_choice):
    test_input = True
    while test_input is True:
        input_user = input('Please choose a list number : ')
        try:
            int(input_user)
            if int(input_user) <= 0 or int(input_user) > number_of_choice:
                print('Please select a number in the list :')
            else:
                test_input = False
                return int(input_user)
        except ValueError:
            print('Invalid answer, please choose a number')


def find_substitute():
    #dict with the Categories instances
    dict_categories = {}
    dict_product = {}
    #Display a list of 10 categories in which the user has to chose one
    #Search product until one product is ok with the chosen category
    while len(dict_product) == 0:
        while dict_categories == {}:
            select_categories(dict_categories)
            if dict_categories == {}:
                print('Sorry, there is no category for this search...')
                print('Try another.')
        choice = try_user_input(len(dict_categories))
        #Display a list of 10 (maximum) products contained in the chosen category
        #User has to chose one product
        dict_product = display_products_list(select_products(dict_categories[choice][1]))
        if len(dict_product) == 0:
            print('\n There is no product for this category, choose another one. \n')
            dict_categories = {}

    choice = try_user_input(len(dict_product))
    product_chosen = extract_product(dict_product[choice])
    #Display the description of the chosen product
    print('\n You chosed this product : \n')
    print_product(product_chosen)

    #Search a substitute and display it
    print('\n You can substitute this product by : \n')
    substitute = search_substitute(product_chosen)
    try : 
        print_product(substitute)
        add_favorite(product_chosen, substitute)
    except AttributeError:
        pass

###Display all the favorites of the user###
def display_favorites():
    #List of favorites used for the function "select_favorite"
    favorites_dict = {}
    # for products in Count(requete nb product in the database)
    CURSOR.execute('USE openfoodfacts;')
    # CURSOR.execute('SELECT COUNT(*) FROM Favorites;')
    # nb_favorites = CURSOR.fetchone()
    CURSOR.execute("""SELECT F1.name as Product, F2.name as Substitute \
        FROM Favorites \
        INNER JOIN Food F1 ON Favorites.product_id = F1.id
        INNER JOIN Food F2 ON Favorites.substitute_id = F2.id""")
    favorites = CURSOR.fetchall()
    index = 1
    for i in favorites:
        favorite_tuple = (i[0], i[1])
        print("\n {}. {}, can be substitute by {}.".format(index, \
            favorite_tuple[0], favorite_tuple[1]))
        favorites_dict[index] = favorite_tuple
        index += 1
    print('Select a number for more details.')
    select_favorite(favorites_dict)

###Display all the favorites of the user###
def select_favorite(favorites_dict):
    choice = try_user_input(len(favorites_dict))
    #Extract the specifitions of the product to display it
    product = extract_product(favorites_dict[choice][0])
    #Extract the specifitions of the substitute to display it
    substitute = extract_product(favorites_dict[choice][1])
    print_product(product)
    print('\n You can substitute this product by : \n')
    print_product(substitute)

###Take the name of a product and return an object containing the specifications of this product###
def extract_product(product):
    CURSOR.execute("USE openfoodfacts;")
    CURSOR.execute("""SELECT Food.id, Food.name, C1.name AS Category_1, C2.name AS Category_2, \
        C3.name AS Category_3, C4.name AS Category_4, C5.name AS Category_5, nutri_score, stores, url
        FROM Food
        INNER JOIN Categories C1 ON C1.id = Food.category_id_1
        INNER JOIN Categories C2 ON C2.id = Food.category_id_2
        INNER JOIN Categories C3 ON C3.id = Food.category_id_3
        INNER JOIN Categories C4 ON C4.id = Food.category_id_4
        INNER JOIN Categories C5 ON C5.id = Food.category_id_5
        WHERE Food.name LIKE %s;""", (product,))
    product = CURSOR.fetchone()
    product_class = lib.Food(product)
    return product_class

###Take a product (object) and print his specifications###
def print_product(product):
    print('\n \
Name : {} \n \
Categories : {}, {}, {}, {}, {} \n \
Store : {} \n \
URL : {}'.format(product.name, product.category_1, product.category_2, \
    product.category_3, product.category_4, product.category_5, product.stores, product.url))

###Main function of the program###
def main():
    running = True
    while running is True:
        print('\n''-------------MAIN MENU-------------')
        print('1. Find a substitute')
        print('2. Show favorites')
        print('3. Exit')
        print('-----------------------------------')
        choice = try_user_input(3)
        if choice == 1:
            find_substitute()
        elif choice == 2:
            display_favorites()
        elif choice == 3:
            running = False

if __name__ == "__main__":
    main()