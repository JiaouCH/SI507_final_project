from delivery_warp import delivery, create_flask_app

from yelp_fusion_api_wrap import yelp
api_key="RfPfwBElXyOSmjBD2DwJELekhVB85ixOoJjjsTqeUUmaYv08V4a2pc_Qs_zkqfL5mfSndoOmE7tntJnq9u80mM0oETsBTyb1xPuPWnAbNtEU6Oj-5V5MBLQP2sFaZXYx"

# Assuming you have a restaurant_cache defined somewhere
app = create_flask_app()

def main():
    print("Welcome to the restaurant finder!")
    while True:
        user_choice = input("Enter 'delivery' for delivery.com or 'yelp' for Yelp: ")
        if user_choice.lower() == 'delivery':
            delivery()
            app.run(debug=False)
            if input("Do you want to try another option? (yes/no): ").lower() != 'yes':
                break
        elif user_choice.lower() == 'yelp':
            yelp(api_key)
            if input("Do you want to try another option? (yes/no): ").lower() != 'yes':
                break
        else:
            print("Invalid choice. Please enter 'delivery' or 'yelp'.")


    

if __name__ == "__main__":
    main()
