#A program to request for public board game information from BGG
import ezsheets
import requests
import xml.etree.ElementTree as ET
import os

def get_board_game_info(board_game, image_folder='board_game_images'):
    """Fetch board game information from BoardGameGeek"""
    search_url = f'https://www.boardgamegeek.com/xmlapi/search?search={board_game}&exact=1'
    
    try:
        response = requests.get(search_url)
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
        response = requests.get(detail_url)
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
        
        min_age_elem = root.find('.//minage')
        min_age = min_age_elem.text if min_age_elem is not None else "Not specified"
        
        categories_elems = root.findall('.//boardgamecategory')
        categories = ', '.join(category.text for category in categories_elems) if categories_elems else "Not specified"
        
        # Download and save the image to the specified folder
        if image_url:
            if not os.path.exists(image_folder):
                os.makedirs(image_folder)
            
            image_response = requests.get(image_url)
            image_filename = os.path.join(image_folder, f"{board_game}.jpg")
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
            'Minimum Age': min_age,
            'Categories': categories,
            'Image URL': img_url #filepath saved locally in /public
        }
    except Exception as e:
        print(f"Error fetching information for {board_game}: {e}")
        return None

def main():
    # Access google sheet
    sheet_obj = ezsheets.Spreadsheet('1a-TIrVEULIaBvgeQDHj51CDNaIySzU27A-vkL05GQMw') 
    
    # Read the list of games from the first column
    sheet = sheet_obj['Game']

    #Set Image Folder
    image_folder = r"C:\Users\Macbook pro\Desktop\AWsite\python-backend\bgg_images"

if __name__ == "__main__":
    main()

