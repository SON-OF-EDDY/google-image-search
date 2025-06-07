from dotenv import load_dotenv
import os
import requests

load_dotenv()

GOOGLE_KEY = os.getenv("GOOGLE_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")

url = "https://www.googleapis.com/customsearch/v1"

def delete_contents_of_image_folder():
    try:
        folder_path = os.path.join(os.getcwd(), 'images')
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
        print("Folder cleared")
    except Exception as e:
        print(f"An error occurred: {e}")

def get_image(query, counter):
    params = {
        "key": GOOGLE_KEY,
        "cx": SEARCH_ENGINE_ID,
        "q": query,
        "searchType": "image",  # Restricts results to images
        "num": 1  # Number of results to return
    }

    try:
        response = requests.get(url, params=params)

        if response.status_code == 200:
            results = response.json()

            # Extract the first image URL
            try:
                image_url = results['items'][0]['link']
            except (KeyError, IndexError):
                image_url = "https://via.placeholder.com/150"  # Placeholder if no image found

            # Save the image locally
            folder_path = os.path.join(os.getcwd(), 'images')
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            file_name = f"{str(counter)}.jpg"
            save_path = os.path.join(folder_path, file_name)

            img_response = requests.get(image_url, stream=True)
            if img_response.status_code == 200:
                with open(save_path, 'wb') as file:
                    for chunk in img_response.iter_content(1024):
                        file.write(chunk)
                print(f"Image successfully downloaded to {save_path}")
            else:
                print(f"Failed to download the image. Status code: {img_response.status_code}")

        else:
            print(f"Search failed with status code: {response.status_code}")
            print("Response Text:", response.text)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

# Prompt the user for a list of needed images
user_input = input("Enter a list of needed images, separated by commas: ")
list_of_needed_words = [word.strip() for word in user_input.split(sep=',')]
print(f"List of needed words: {list_of_needed_words}")

delete_contents_of_image_folder()

counter = 0
for word in list_of_needed_words:
    get_image(word, counter)
    counter += 1