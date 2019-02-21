#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###Reading and Formating Json Files Library###

class Food():
    """For the 'Food' table in the DB"""
    
    ######################################
    ### take a dictionnary in argument ###
    ######################################
    def __init__(self, data, index=None):    
        
        #Use key when creating the database from OFF API
        try:
            #No id attribute because of the auto-increment
            self.name = data['product_name']
            #Take the first 4 categories of the product
            try:
                self.category_1 = data['categories_tags'][0]
            except IndexError:
                pass
            try:
                self.category_2 = data['categories_tags'][1]
            except IndexError:
                self.category_2 = "None"
            try:
                self.category_3 = data['categories_tags'][2]
            except IndexError:
                self.category_3 = "None"
            try:
                self.category_4 = data['categories_tags'][3]
            except IndexError:
                self.category_4 = "None"
            try:
                self.category_5 = data['categories_tags'][4]
            except IndexError:
                self.category_5 = "None"
            try:
                self.nutri_score = data['nutriments']['nutrition-score-fr_100g']
            except KeyError:
                self.nutri_score = ""
            try:
                self.stores = data['stores']
            except KeyError:
                self.stores = ""
            try:
                self.url = data['url']
            except KeyError:
                self.url = "no URL"
        except IndexError:
            pass

        #Use index when call the class from the programme
        except TypeError:
            self.id = data[0]
            self.name = data[1]
            self.category_1 = data[2]
            self.category_2 = data[3]
            self.category_3 = data[4]
            self.category_4 = data[5]
            self.category_5 = data[6]
            self.nutri_score = data[7]
            self.stores = ""
            try:
                self.stores = data[8]
            except IndexError:
                pass
            try:
                self.url = data[9]
            except IndexError:
                self.url = data[8]
            self.index = index

class Categories():
    """For the 'Categories' table in the DB"""

    ###########################################
    ### Init take a dictionnary in argument ###
    ###########################################
    
    def __init__(self, data, index=None):

        #Used when creating the database from the OpenFood API
        try:
            self.id = data['id']
            self.name = data['name']
        except TypeError:
            self.id = data[0]
            self.name = data[1]
            self.index = index

