#!/usr/bin/env python

from yelpapi import YelpAPI
import argparse
import json

argparser = argparse.ArgumentParser()
argparser.add_argument('api_key', type=str, help='Yelp Fusion API Key')
args = argparser.parse_args()

class Node:
    def __init__(self, restaurant_info):
        self.restaurant_info = restaurant_info
        self.left = None
        self.right = None

def insert(root, restaurant_info):
    if root is None:
        return Node(restaurant_info)
    else:
        if float(restaurant_info['rating']) > float(root.restaurant_info['rating']):
            root.left = insert(root.left, restaurant_info)
        elif float(restaurant_info['rating']) < float(root.restaurant_info['rating']):
            root.right = insert(root.right, restaurant_info)
        else:
            if int(restaurant_info['review_count']) > int(root.restaurant_info['review_count']):
                root.left = insert(root.left, restaurant_info)
            else:
                root.right = insert(root.right, restaurant_info)
    return root

with YelpAPI(args.api_key) as yelp_api:
    response = yelp_api.search_query(term='pizza', location='1851 Lake Lila Ln', sort_by='rating', limit=50)
    import json
    
    restaurants = []
    for restaurant in response['businesses']:
        restaurant_info = {
            'name': restaurant['name'],
            'phone': restaurant['phone'],
            'price': restaurant.get('price', None),
            'rating': str(restaurant['rating']),  
            'review_count': str(restaurant['review_count'])  
        }
        restaurants.append(restaurant_info)
    
    root = None
    index = 1  
    for restaurant in restaurants:
        root = insert(root, restaurant)


    def display_in_order(root, index):
        if root:
            index = display_in_order(root.left, index)
            print(f"{index}. Restaurant Name: {root.restaurant_info['name']}, Rating: {root.restaurant_info['rating']}, Review Count: {root.restaurant_info['review_count']}, Price: {root.restaurant_info['price']}, Phone: {root.restaurant_info['phone']}")
            index += 1
            index = display_in_order(root.right, index)
        return index

    print("----------------------------------In order traversal----------------------------------")
    display_in_order(root, index)
    

    


