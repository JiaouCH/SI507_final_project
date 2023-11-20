# SI507_final_project
Readme for checkpoint
### At the checkpoint, I obtain the sample data from the Internet.
#### In the first part, I used the Yelp fusion API.
I get the information of restaurants with Yelp API with sample search term "pizza" and sample location "1851 Lake Lila Ln" so users can get the information of pizza restaurant nearby the location, this part is for users who have time to eat in the restaurant. 
1. The result is stored in cache and stored as a tree.
2. There are several fields for a restaurant: name, home, price, rating and review count.
3. The key for inserting node is restaurant rating.
4. In the display part, I used in order traversal, so readers can have the data sorted by ratings. Also, the restaurant with same rating but higher review count will be displayed first.
#### In the second part, I scarpped the food delivery website. 
The url I am scrapping is "https://www.delivery.com/search/food/address=3700%20Earhart%20Rd,%2048105&page=1&per_page=24&orderType=delivery&orderTime=2023-11-20T12:30:00Z&keyword=fast%20food&filter_categories=restaurant". Users can visit this website and access delivery and pickup information about restaurants nearby. This part is for users who are hurrying for their business and have no time sit in the restaurant to eat.
1. I used session to visit the website because it uses javascript to dynamically load the data. 
2. I used binary search tree to store my data, The key for inserting node is distance.
3. For one restaurant, there are several fields: name, rating, distance, delivery fee, minimum order and delivery time.
4. In the display part, I used in order traversal, so readers can have the data sorted by ratings. The restaurant with same rating but higher review count will be displayed first.
