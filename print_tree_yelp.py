import json

def display_in_order():
    '''
    Displays the restaurant data in order of ratings, review count, or price. The data is read from restaurant_yelp_tree.json.
    The data are already sorted when saved with the save_tree function with in order traversal in the yelp_fusion_api_wrap.py, so this function just prints the data in the tree in order.
    '''
    with open("restaurant_yelp_tree.json", 'r') as file:
        data = json.load(file)
    restaurants = data['restaurants']
    for restaurant in restaurants:
        print(f"{restaurant['index']}. Restaurant Name: {restaurant['name']}, Rating: {restaurant['rating']}, Review Count: {restaurant['review_count']}, Price: {restaurant['price']}, Phone: {restaurant['phone']}")
