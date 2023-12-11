import json

def load_tree_from_json(file_path):
    '''
    Loads the tree structure from a JSON file.

    Parameters
    ----------
    file_path : str
        The path to the JSON file.

    Returns
    -------
    dict
        A dictionary representing the tree structure.
    '''
    with open(file_path, 'r') as file:
        return json.load(file)

def inverse_traversal(root):
    '''
    Traverses the tree in inverse order.

    Parameters
    ----------
    root : dict
        The root node of the binary tree.
    
    Returns
    -------
    None
    '''
    if root:
        inverse_traversal(root.get('left'))  
        restaurant = root.get('restaurant')
        if restaurant:
            print(f"Restaurant: {restaurant['Restaurant Name']}, Distance: {restaurant['Distance']} miles, Rating: {restaurant['Rating']}, Delivery Fee: {restaurant['Delivery_Fee']}, Minimum Order: {restaurant['Minimum_Order']}, Delivery Time: {restaurant['Delivery_Time']}")
        inverse_traversal(root.get('right'))  

def print_tree(tree_data, prefix='', answer=''):
    '''
    Prints the tree structure.

    Parameters
    ----------
    tree_data : dict
        A dictionary representing the tree structure.
    prefix : str
        The prefix to be printed before the node.
    answer : str
        The answer to be printed before the node.
    
    Returns
    -------
    None
    '''
    if tree_data is not None:
        restaurant = tree_data['restaurant']
        if restaurant["Restaurant Name"] is not None:
            print(f'{prefix}{answer}Restaurant: {restaurant["Restaurant Name"]}, Distance: {restaurant["Distance"]}, Rating: {restaurant["Rating"]}, Delivery Fee: {restaurant["Delivery_Fee"]}, Minimum Order: {restaurant["Minimum_Order"]}, Delivery Time: {restaurant["Delivery_Time"]}')
            print_tree(tree_data['left'], prefix + '-', "Left: ")
            print_tree(tree_data['right'], prefix + '-', "Right: ")

# The functions have been directly used in the delivery function, if you want to test them separately, you can use the following code:
# if __name__ == "__main__":
    #tree_data = load_tree_from_json('restaurant_delivery_tree.json')
    #inverse_traversal(tree_data)

    #print("")
    #print("----------------------Printing the entire tree----------------------")
    #print_tree(tree_data)
