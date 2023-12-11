from urllib.parse import quote

def construct_delivery_url():
    # Get user inputs
    address = input("Enter the address: ")
    zip_code = input("Enter the zip code: ")
    order_type = input("Enter the order type (e.g., delivery, pickup): ")
    order_time = input("Enter the order time (YYYY-MM-DDTHH:MM:SSZ): ")

    # Construct the full address string including the zip code


    # URL-encode the full address
    encoded_address = quote(address)
    zip_code = quote(zip_code)

    # Construct the URL including the address and zip code in the desired format
    delivery_url = f"https://www.delivery.com/search/food/?address={encoded_address},%20{zip_code}"

    # Append other query parameters
    delivery_url += f"&filter_categories=restaurant&orderTime={order_time}&orderType={order_type}"

    return delivery_url

