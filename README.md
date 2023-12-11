# SI507_final_project
Readme for final submission </br>
### Prerequisite
To run this program, make sure you have the following python package installed, if not please use the following commands in your console to install packages:
1. yelpapi: `pip install yelpapi`
2. webbrowser: `pip install webbrowser` 
3. folium: `pip install folium`
4. flask: `pip install flask`
5. Beautifulsoup4:  `pip install Beautifulsoup4`
6. Request_html: `pip install requests_html` </br>
### How to run this program?
1. This program consists of two main parts: yelp fusion api and delivery. The yelp fusion api allows you to find information about restaurants nearby and the delivery program allows you to find restaurants providing food delivery service.
2. To run this function please type `python find_restaurants.py`: It will give you options to choose from, by poping up the message "Enter 'delivery' for delivery.com or 'yelp' for Yelp: ". </br>
You can either choose to interact with the yelp by typing "yelp" or interact with the delivery app by typing "delivery". </br>
3. The API key for yelp has been included in the yelp_fusion_api_wrap file. You donot need to generate an api key on your own. However, there are possibilities that the api key access the use limit. In this case, you need to generate an api key on your own and replace the old one with your own api key. The website for API key generation is "https://www.yelp.com/developers/v3/manage_app"
### Guidelines for using yelp fusion api app:
1. The yelp fusion api prompts you to enter the search key words, search address
2. It returns with you a list of restaurants nearby with the restaurant information: 'name', 'phone', 'price', 'rating','review_count'.
3. It then generates a heatmap using folium. The program automatically opens the html for the heatmap. You can find the places with most restaurants with warmest color.
4. Then return to your console, the yelp app will allow you to choose whether you want the detail page of a certain restaurant.
5. If you choose yes, please enter the restaurant index you are interested in the restaurant list previously shown in your console.
6. It will then open the yelp page for this restaurant in a web browser.
7. If you choose no, you would exit this app, and the main program will ask you to choose whether you want to use the delivery app.
### Guidelines for using delivery app:
1. The delivery app prompts you to enter the search address, type:delivery or pickup and your preferred time. <strong>*****Please type only street address in the Ann Arbor*****</strong>.  If your address does not work, please try with sample address: <br>
Sample address: `1851 Lake Lila Lane`
Sample zipcode: `48105`
2. It then opens a webpage and allows you to view the information of the restaurants: Name, Rating, Distance, Delivery Fee, Minimum Order and Delivery Time in an HTML table form. <br>
3. It also prints a restaurant list sorted by the distance in the console and a structure representing the restaurant tree.
### Data Structure:
All resturant data are stored as a binary tree structure. with a left node and a right node.
1. The yelp fusion app first reads data from the yelp app, then it inserts node into a tree with key being the ratings of each restaurant. For simpler use, the tree data are using a traverse store into a json file called [restaurant_yelp_tree.json](restaurant_yelp_tree.json), the restaurant with highest ratings are listed first in the json dictionary.
2. The delivery app first scrap data from the https://www.delivery.com/search/food/ website, then it stores the restaurant data into a tree structure. The key for inserting node is the distance attribute. The hierachal tree structure is then stored in a json file. In order traverse is used to access the data in the json file called [restaurant_delivery_tree.json](restaurant_delivery_tree.json)



