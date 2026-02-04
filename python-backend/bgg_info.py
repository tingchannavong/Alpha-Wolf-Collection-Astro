# A program to request for public board game information from BGG
import requests
import xml.etree.ElementTree as ET
import os
import re
from dotenv import load_dotenv
# from bs4 import BeautifulSoup #Did not work

load_dotenv()

token = os.getenv("BOARDGAMEGEEK_API_TOKEN")
if not token:
    raise RuntimeError('BGG API is not set')

headers = {
    "Authorization" : f"Bearer {token}"
}

def get_board_game_info_by_id(board_game, bgg_game_id, image_folder='board_game_images'):
    """Fetch board game information from BoardGameGeek by knowing id.
    Ex: https://boardgamegeek.com/boardgame/226522/exit-the-game-dead-man-on-the-orient-express
    the game_ID is 226522"""
    
    game_id = bgg_game_id
    
    try:
        # Use the game ID to fetch detailed information
        detail_url = f'https://www.boardgamegeek.com/xmlapi/boardgame/{game_id}?stats=1'
        response = requests.get(detail_url, headers=headers)
        response.raise_for_status()
        
        # Parse the response XML
        root = ET.fromstring(response.content)

        # Extract the desired information
        description_elem = root.find('.//description')
        description = description_elem.text if description_elem is not None else "No description available"
        
        image_elem = root.find('.//image')
        image_url = image_elem.text if image_elem is not None else None
        
        playing_time_elem = root.find('.//playingtime')
        playing_time = playing_time_elem.text if playing_time_elem is not None else "Not specified"
        
        min_players_elem = root.find('.//minplayers')
        min_players = min_players_elem.text if min_players_elem is not None else "Not specified"
        
        max_players_elem = root.find('.//maxplayers')
        max_players = max_players_elem.text if max_players_elem is not None else "Not specified"
        
        categories_elems = root.findall('.//boardgamecategory')
        categories = ', '.join(category.text for category in categories_elems) if categories_elems else "Not specified"
        
        # Download and save the image to the specified folder
        if image_url:
            if not os.path.exists(image_folder):
                os.makedirs(image_folder)
            
            image_response = requests.get(image_url)
            image_filename = os.path.join(image_folder, f"{board_game.lower().replace(' ', '_')}.jpg")
            img_url = f"/{os.path.basename(image_filename)}"
            with open(image_filename, 'wb') as image_file:
                image_file.write(image_response.content)
            print(f"Image saved for {board_game} at {image_filename}")
            print(f"The image url to use in the markdown is {img_url}")
        else:
            print(f"No image found for {board_game}.")
        
        return {
            'Description': description,
            'Playing Time': playing_time,
            'Minimum Players': min_players,
            'Maximum Players': max_players,
            'Categories': categories,
            'Image URL': img_url #filepath saved locally in /public
        }
    except Exception as e:
        print(f"Error fetching information for {board_game}: {e}")
        return None
    
def get_board_game_info(board_game, image_folder='board_game_images'):

    """Fetch board game information from BoardGameGeek"""
    search_url = f'https://www.boardgamegeek.com/xmlapi/search?search={board_game}&exact=1'
    
    try:
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()
        
        # Parse the response XML
        root = ET.fromstring(response.content)
        
        # Get the first search result (assuming it's the most relevant)
        boardgame = root.find('.//boardgame')
        if boardgame is None:
            print(f"No information found for {board_game}.")
            return None
        
        game_id = boardgame.attrib.get('objectid')
        if not game_id:
            print(f"No game ID found for {board_game}.")
            return None
        
        # Use the game ID to fetch detailed information
        detail_url = f'https://www.boardgamegeek.com/xmlapi/boardgame/{game_id}?stats=1'
        response = requests.get(detail_url, headers=headers)
        response.raise_for_status()
        
        # Parse the response XML
        root = ET.fromstring(response.content)
        
        # Extract the desired information
        description_elem = root.find('.//description')
        description = description_elem.text if description_elem is not None else "No description available"
        
        image_elem = root.find('.//image')
        image_url = image_elem.text if image_elem is not None else None
        
        playing_time_elem = root.find('.//playingtime')
        playing_time = playing_time_elem.text if playing_time_elem is not None else "Not specified"
        
        min_players_elem = root.find('.//minplayers')
        min_players = min_players_elem.text if min_players_elem is not None else "Not specified"
        
        max_players_elem = root.find('.//maxplayers')
        max_players = max_players_elem.text if max_players_elem is not None else "Not specified"
        
        categories_elems = root.findall('.//boardgamecategory')
        categories = ', '.join(category.text for category in categories_elems) if categories_elems else "Not specified"
        
        # Download and save the image to the specified folder
        if image_url:
            if not os.path.exists(image_folder):
                os.makedirs(image_folder)
            
            image_response = requests.get(image_url)
            image_filename = os.path.join(image_folder, f"{board_game.lower().replace(' ', '_')}.jpg")
            img_url = f"/{os.path.basename(image_filename)}"
            with open(image_filename, 'wb') as image_file:
                image_file.write(image_response.content)
            print(f"Image saved for {board_game} at {image_filename}")
            print(f"The image url to use in the markdown is {img_url}")
        else:
            print(f"No image found for {board_game}.")
        
        return {
            'Description': description,
            'Playing Time': playing_time,
            'Minimum Players': min_players,
            'Maximum Players': max_players,
            'Categories': categories,
            'Image URL': img_url #filepath saved locally in /public
        }
    except Exception as e:
        print(f"Error fetching information for {board_game}: {e}")

def find_first_sentence(text):
    """A function that finds and returns only the first sentence in a given text."""
    match = re.search(r"^[^.]*\.", text)
    if match:
        return match.group()
    else:
        return None  # No sentence found
    
def replace_one(text, find, replace):
    """Replaces all occurrences of old_string with new_string in text.

    Args:
        text: The input text.
        find: The old_string to be replaced.
        replace: The replacement new_string.

    Returns:
        The modified text with all occurrences of old_string replaced.
    """

    return re.sub(re.escape(find), replace, text)

def replace_many(text, replacements):
    """Replaces multiple occurrences of strings in text.

    Args:
        text: The input text.
        replacements: A dictionary where keys are the strings to be replaced and values are their replacements.
                {find: replace,
                find: replace}
    Returns:
        The modified text with all occurrences of the strings replaced.
    """

    for old_string, new_string in replacements.items():
        text = re.sub(re.escape(old_string), new_string, text)
    return text

def replace_spaces_in_filenames(folder_path):
    """This function takes a folder path, goes through the folder and rename all the files by replacing spaces with _."""
    # Ensure the folder path exists
    if not os.path.exists(folder_path):
        print(f"The folder '{folder_path}' does not exist.")
        return

    # Iterate through all files in the specified folder
    for filename in os.listdir(folder_path):
        # Check if the file name contains spaces
        if ' ' in filename:
            # Create the new file name by replacing spaces with underscores
            new_filename = filename.replace(' ', '_')
            
            # Construct full file paths
            old_file = os.path.join(folder_path, filename)
            new_file = os.path.join(folder_path, new_filename)
            
            # Rename the file
            os.rename(old_file, new_file)
            print(f"Renamed: '{filename}' to '{new_filename}'")

def replace_spaces_in_filepath(sheet, col, from_row, to_row):
    """This function takes a sheet object, column alphabet, row number from and row number to, goes through the rows and rename all the files by replacing spaces with _."""
    # Loop through each row where image URLs are located (modify row range as needed)
    for row in range(from_row, to_row):  # Update for your actual range
        image_url = sheet[f'{col}{row}']

        if image_url:
            # Get the filename from the URL
            image_name = os.path.basename(image_url)
            new_image_name = image_name.replace(' ', '_')  # Replace spaces with underscores

            # If the name changed, update the Google Sheet entry
            if image_name != new_image_name:
                # Update the URL in the Google Sheet
                new_image_url = image_url.replace(image_name, new_image_name)
                sheet[f'G{row}'] = new_image_url
                print(f"Updated Google Sheet URL for row {row}: {new_image_url}")

            else:
                print(f"No spaces in filename for row {row}, no change needed.")

# Example usage
# folder_path = r"C:\Users\Macbook pro\Desktop\AWsite\public"
# replace_spaces_in_filenames(folder_path)
