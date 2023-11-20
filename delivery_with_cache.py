from requests_html import HTMLSession
from bs4 import BeautifulSoup
import json

# URL to scrape
# url = "https://www.delivery.com/search/food/?address=3700%20Earhart%20Rd,%2048105&page=1&per_page=24&orderType=delivery&orderTime=2023-11-20T12:30:00Z&filter_categories=restaurant"
# url = "https://www.delivery.com/search/food/?address=3700%20Earhart%20Rd,%2048105&orderTime=ASAP&orderType=delivery&page=1"
url = "https://www.delivery.com/search/food/?address=3700%20Earhart%20Rd,%2048105&page=1&per_page=24&orderType=delivery&orderTime=2023-11-20T12:30:00Z&keyword=fast%20food&filter_categories=restaurant"
# url = "https://www.delivery.com/search/food?address=2228%20S%20Main%20St,%2048103&page=1&per_page=24&orderType=pickup&orderTime=ASAP&filter_categories=restaurant"

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
        "Delivery Fee": delivery_fee,
        "Minimum Order": minimum_order,
        "Delivery Time": delivery_time
    }
    restaurant_cache[restaurant_title] = restaurant_data

    print(f"Restaurant Name: {restaurant_title}")
    print(f"Rating: {rating}")
    print(f"Distance: {distance} Miles")
    print(f"Delivery Fee: {delivery_fee}")
    print(f"Minimum Order: {minimum_order}")
    print(f"Delivery Time: {delivery_time}")
    print('-' * 30)

with open('restaurant_cache.json', 'w') as file:
    json.dump(restaurant_cache, file)


class Node:
    def __init__(self, restaurant):
        self.restaurant = restaurant
        self.left = None
        self.right = None

def insert(root, restaurant):
    if root is None:
        return Node(restaurant)
    else:
        if float(restaurant["Distance"]) == float(root.restaurant["Distance"]):
            # If distances are the same, sort by rating (non-zero ratings first)
            if (int(restaurant["Rating"]) != 0 or int(root.restaurant["Rating"]) != 0) and int(restaurant["Rating"]) < int(root.restaurant["Rating"]):
                root.right = insert(root.right, restaurant)
            else:
                root.left = insert(root.left, restaurant)
        elif float(restaurant["Distance"]) < float(root.restaurant["Distance"]):
            root.left = insert(root.left, restaurant)
        else:
            root.right = insert(root.right, restaurant)
    return root

def inverse_traversal(root):
    if root:
        inverse_traversal(root.left)
        print(f"Restaurant: {root.restaurant['Restaurant Name']}, Distance: {root.restaurant['Distance']} miles, Rating: {root.restaurant['Rating']}, Delivery Fee: {root.restaurant['Delivery Fee']}, Minimum Order: {root.restaurant['Minimum Order']}, Delivery Time: {root.restaurant['Delivery Time']}")
        inverse_traversal(root.right)

def printTree(tree, prefix='', answer=''):
    if tree is not None:
        restaurant = tree.restaurant
        if restaurant["Restaurant Name"] is not None:
            print(f'{prefix}{answer}Restaurant: {restaurant["Restaurant Name"]}, Distance: {restaurant["Distance"]}, Rating: {restaurant["Rating"]}, Delivery Fee: {restaurant["Delivery Fee"]}, Minimum Order: {restaurant["Minimum Order"]}, Delivery Time: {restaurant["Delivery Time"]}')
            printTree(tree.left, prefix + '-', "Left: ")
            printTree(tree.right, prefix + '-', "Right: ")

with open('restaurant_cache.json', 'r') as file:
    restaurant_cache = json.load(file)

root = None

for restaurant_name, restaurant_details in restaurant_cache.items():
    root = insert(root, {"Restaurant Name": restaurant_name, **restaurant_details})

print("")
print("----------------------Printing the tree in sorted order using inverse traversal----------------------")
inverse_traversal(root)
print("")
print("----------------------Printing the entire tree----------------------")
printTree(root)




session.close()
