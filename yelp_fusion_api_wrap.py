from yelpapi import YelpAPI
import json
import webbrowser
import folium
from folium.plugins import HeatMap
import json
from print_tree_yelp import display_in_order

def yelp(api_key):

    class Node:
        def __init__(self, restaurant_info):
            self.restaurant_info = restaurant_info
            self.left = None
            self.right = None

    def save_to_json(restaurants):
        '''
        Saves the restaurant data to cache in JSON format.

        Parameters
        ----------
        restaurants : list
            A list of restaurant information.
        
        Returns
        -------
        None
        '''
        with open('restaurant_yelp_cache.json', 'w') as file:
            json.dump(restaurants, file, indent=2)

    def read_from_json():
        '''
        Reads the restaurant data from cache in JSON format.

        Parameters
        ----------
        None

        Returns
        -------
        list
        '''
        with open('restaurant_yelp_cache.json', 'r') as file:
            return json.load(file)

    def save_to_tree(root):
        '''
        Saves the restaurant tree with in order traversal in JSON format.

        Parameters
        ----------
        root : Node
            The root of the restaurant tree.
        
        Returns
        -------
        None
        '''
        cache_data = {"restaurants": []}

        def traverse_and_save(node):
            if node:
                traverse_and_save(node.left)
                cache_data["restaurants"].append(node.restaurant_info)
                traverse_and_save(node.right)

        traverse_and_save(root)

        with open('restaurant_yelp_tree.json', 'w') as cache_file:
            json.dump(cache_data, cache_file, indent=2)
    
    def get_coordinates_from_cache():
        '''
        Gets the coordinates of the restaurants from the cache.

        Parameters
        ----------
        None
        
        Returns
        -------
        list
        '''
        with open("restaurant_yelp_tree.json", 'r') as file:
            data = json.load(file)
        restaurants = data.get('restaurants', [])
        coordinates = [(float(restaurant.get('coordinates', {}).get('latitude')),
                        float(restaurant.get('coordinates', {}).get('longitude')))
                       for restaurant in restaurants]
        return coordinates

    def insert(root, restaurant_info):
        '''
        Inserts a restaurant into the restaurant tree.

        Parameters
        ----------
        root : Node
            The root of the restaurant tree.
        restaurant_info : dict
            The restaurant information to be inserted into the tree.
        sort_key : str
            The sort key to be used for inserting the restaurant into the tree.
        
        Returns
        -------
        Node
        '''
        if root is None:
            return Node(restaurant_info)
        else:
            if float(restaurant_info['rating']) > float(root.restaurant_info['rating']):
                root.left = insert(root.left, restaurant_info)
            else:
                root.right = insert(root.right, restaurant_info)
            return root

    def get_restaurant_url_at_index(index_to_find):
        '''
        Gets the restaurant URL at the given index.

        Parameters
        ----------
        index_to_find : int
            The index of the restaurant to find.

        Returns
        -------
        str
        '''
        with open('restaurant_yelp_tree.json', 'r') as file:
            data = json.load(file)
        restaurants = data.get('restaurants', [])
        for restaurant in restaurants:
            if restaurant.get('index') == index_to_find:
                print(restaurant.get('name'))
                return restaurant.get('url')
        return None

    def open_browser(index):
        '''
        Opens the restaurant's Yelp page in a web browser.

        Parameters
        ----------
        index : int
            The index of the restaurant to open in a web browser.
        
        Returns
        -------
        None
        '''
        print("Opening restaurant's Yelp page in a web browser...")
        webbrowser.open_new(get_restaurant_url_at_index(index))

    with YelpAPI(api_key) as yelp_api:
        '''
        The main function of the program. It prompts the user for a search term, location, and sort key, and then displays the restaurants in order of the sort key. It also saves the restaurant data to cache and saves the restaurant tree to cache.

        Parameters
        ----------
        api_key : str
            The API key for the Yelp Fusion API.

        Returns
        -------
        None
        '''
        search_term = input("Enter search term: ")
        search_location = input("Enter location: ")
        response = yelp_api.search_query(term=search_term, location=search_location, sort_by='rating', limit=50)
        
        restaurants = []
        for restaurant in response['businesses']:
            restaurant_info = {
                'name': restaurant['name'],
                'phone': restaurant['phone'],
                'price': restaurant.get('price', None),
                'rating': str(restaurant['rating']),  
                'review_count': str(restaurant['review_count']),
                'url': restaurant['url'],
                'coordinates': restaurant['coordinates'],
                'index': 0
            }
            restaurants.append(restaurant_info)

        # The Data obtained through the yelp fusion api is saved to cache
        save_to_json(restaurants)

        # The Data is read from cache to form the tree
        restaurant_data = read_from_json()
        root = None
        index = 1  

        for restaurant in restaurant_data:
            root = insert(root, restaurant)

        def set_index(root, index):
            if root:
                index = set_index(root.left, index)
                root.restaurant_info['index'] = index
                index += 1
                index = set_index(root.right, index)
            return index
        
        set_index(root, index)

        # The tree is saved to cache
        save_to_tree(root)

        # The restaurants are displayed in order
        display_in_order()

        # A heatmap of the restaurants is created and saved as restaurant_heatmap.html
        restaurant_coordinates = get_coordinates_from_cache()
        m = folium.Map(location=[42.2808, -83.7430], zoom_start=13)
        heat_map = HeatMap(restaurant_coordinates, radius=15)
        m.add_child(heat_map)
        m.save("restaurant_heatmap.html")
        print("A heatmap of the restaurants has been saved as restaurant_heatmap.html. Opening the file in a web browser to view the heatmap.")
        webbrowser.open_new("restaurant_heatmap.html")

        # The user is prompted to open a restaurant's Yelp page in a web browser
        open_browser_option = input("Would you like to open a restaurant's Yelp page in a web browser? (y/n): ").lower()
        while open_browser_option == 'y':
            restaurant_index = int(input("Enter the index of the restaurant you would like to open: "))
            open_browser(restaurant_index)
            open_browser_option = input("Would you like to open another restaurant's Yelp page in a web browser? (y/n): ").lower()
        print("Thank you for using the Yelp Fusion API Wrapper!")
