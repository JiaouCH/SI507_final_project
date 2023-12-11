from requests_html import HTMLSession
from bs4 import BeautifulSoup
import json
from address_encoding import construct_delivery_url
from flask import Flask, render_template
import webbrowser
from print_tree_delivery import inverse_traversal, print_tree, load_tree_from_json

def create_flask_app():
    '''
    Creates a Flask app that displays the restaurants in the restaurant_cache.json file.
    
    Parameters
    ----------
    None
    
    Returns
    -------
    Flask
    '''
    app = Flask(__name__)

    @app.route('/')
    def show_restaurants():
        with app.app_context():
            with open("restaurant_cache.json", 'r') as file:
                restaurant_cache = json.load(file)
            return render_template('restaurants.html', restaurants=restaurant_cache)
    show_restaurants()
    return app

def save_cache(restaurant_cache):
    '''
    Saves the restaurant_cache to a JSON file.

    Parameters
    ----------
    restaurant_cache : dict
        A dictionary of restaurant information.

    Returns
    -------
    None
    '''
    with open('restaurant_cache.json', 'w') as file:
        json.dump(restaurant_cache, file, indent=2)

def delivery():
    '''
    Scrapes the delivery.com website for restaurants and their information.

    Parameters
    ----------
    None

    Returns
    -------
    None
    '''

    class Node:
        '''
    A class used to represent a node in a binary tree.
    
    Attributes
    ----------
    restaurant : dict
        A dictionary of restaurant information.
    left : Node
        The left child of the node.
    right : Node
        The right child of the node.
    
    Methods
    -------
    __init__(self, restaurant)
        Initializes the node with the restaurant information.
        '''
        def __init__(self, restaurant):
            self.restaurant = restaurant
            self.left = None
            self.right = None

    def insert(root, restaurant):
        '''
        Inserts a node into a binary tree.

        Parameters
        ----------
        root : Node
            The root node of the binary tree.
        
        restaurant : dict
            A dictionary of restaurant information.
        
        Returns
        -------
        Node
            The root node of the binary tree.
        '''
        if root is None:
            return Node(restaurant)
        else:
            if float(restaurant["Distance"]) == float(root.restaurant["Distance"]):
                if (int(restaurant["Rating"]) != 0 or int(root.restaurant["Rating"]) != 0) and int(restaurant["Rating"]) < int(root.restaurant["Rating"]):
                    root.right = insert(root.right, restaurant)
                else:
                    root.left = insert(root.left, restaurant)
            elif float(restaurant["Distance"]) < float(root.restaurant["Distance"]):
                root.left = insert(root.left, restaurant)
            else:
                root.right = insert(root.right, restaurant)
        return root

    def build_tree_structure(node):
        '''
        Builds a tree structure from a binary tree.
        
        Parameters
        ----------
        node : Node
            The root node of the binary tree.
        
        Returns
        -------
        dict
            A dictionary representing the tree structure.
        '''
        if node is None:
            return None
        else:
            return {
                "restaurant": node.restaurant,
                "left": build_tree_structure(node.left),
                "right": build_tree_structure(node.right)
            }

    def save_tree_to_json(root):
        '''
        Saves the tree structure to a JSON file.

        Parameters
        ----------
        root : Node
            The root node of the binary tree.
        
        Returns
        -------
        None
        '''
        tree_structure = build_tree_structure(root)
        with open("restaurant_delivery_tree.json", 'w') as file:
            json.dump(tree_structure, file, indent=2)    
    
    def open_browser():
        '''
        Opens the flask app page in a web browser.

        Parameters
        ----------
        None
        
        Returns
        -------
        None
        '''
        print("Opening restaurant's Yelp page in a web browser...")
        webbrowser.open_new("http://127.0.0.1:5000/")
    

    url = construct_delivery_url()
    session = HTMLSession()
    response = session.get(url)
    response.close()
    response.html.render(timeout=1000)
    
    soup = BeautifulSoup(response.html.html, 'html.parser')
    restaurants = soup.find_all('li', class_='SearchResults__List__Item')
    restaurant_cache = {}

    for restaurant in restaurants:
        restaurant_title = restaurant.find(class_='SearchResult__TitleWrap__Title__Name').text.strip()
        rating_stars = restaurant.select('.StarRating__base')
        filled_stars = len([star for star in rating_stars if 'StarRating__filled' in star.get('class')])
        total_stars = len(rating_stars)
        rating = f'{filled_stars}/{total_stars}'
        distance = restaurant.find(class_='SearchResultDistance__Distance').text.strip()
        if restaurant.find(class_="SearchResultFee__Amount"):
            delivery_fee = restaurant.find(class_="SearchResultFee__Amount").text.strip()
        else:
            delivery_fee = None
        if restaurant.find(class_="SearchResultMinimum__Amount"):
            minimum_order = restaurant.find(class_="SearchResultMinimum__Amount").text.strip()
        else:
            minimum_order = None
        if restaurant.find(class_='SearchResultTimeEstimate__Time'):
            delivery_time = restaurant.find(class_='SearchResultTimeEstimate__Time').text.strip()
        else:
            delivery_time = None

        restaurant_data = {
            "Rating": filled_stars,
            "Distance": distance,
            "Delivery_Fee": delivery_fee,
            "Minimum_Order": minimum_order,
            "Delivery_Time": delivery_time
        }
        restaurant_cache[restaurant_title] = restaurant_data

        print(f"Restaurant Name: {restaurant_title}")
        print(f"Rating: {rating}")
        print(f"Distance: {distance} Miles")
        print(f"Delivery Fee: {delivery_fee}")
        print(f"Minimum Order: {minimum_order}")
        print(f"Delivery Time: {delivery_time}")
        print('-' * 30)

    save_cache(restaurant_cache)

    root = None

    for restaurant_name, restaurant_details in restaurant_cache.items():
        root = insert(root, {"Restaurant Name": restaurant_name, **restaurant_details})
    
    build_tree_structure(root)
    save_tree_to_json(root)
    


    print("")
    print("----------------------Printing the tree in sorted order using in order traversal----------------------")
    tree_data = load_tree_from_json('restaurant_delivery_tree.json')
    inverse_traversal(tree_data)

    print("")
    print("----------------------Printing the entire tree----------------------")
    print_tree(tree_data)

    session.close()
    open_browser()

    

if __name__ == "__main__":
    delivery()
