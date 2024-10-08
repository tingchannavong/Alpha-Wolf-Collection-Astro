# A program to connect to google sheets and fetch game by 
# 1) game ID (if provided), more specific no room for mistake
# 2) name in a dictionary structure, more generic but less manual work

import ezsheets
from bgg_info import get_board_game_info_by_id, get_board_game_info

# Dictionary to store missing games for future fetch
# key pair value is row: (game_name, game_id)
missing_games = {
        9: ('Ticket to Ride: Asia Map', 106637), 
        16: ('Pop-up Pirate', 9004), 
        19: ('The Resistance: Avalon', 128882),
        21: ('Decrypto', 225694),  
        33: ('Dead Man on the Orient Express', 226522), 
        49: ('Who Is It', 4143), 
        62: ('Coup', 131357), 
        84: ('Evolution', 155703),
        34: ('Carcassonne', None),
        36: ('Cashflow 101', None),  
    }

year_search = {
        21: ('Decrypto', 2018),  
        33: ('Dead Man on the Orient Express', 2017), 
        49: ('Who Is It', 1979), 
        62: ('Coup', 2012),  
        84: ('Evolution', 2014)  
    }

manual_search = {
        15: ('Face Change Rubik Cube', None),
        52: ('IQ Game', None),
        63: ('Spot it Holidays', None), 
        83: ('The Empathy Box', None), 
}

new_game = {
        89: ('Forbidden Island', None),
        }

def loop_sheet_find_game(sheet, img_folder, games_array):
    """Loop through a games array with row number and name, fetch BGG API to find info and 
    write to googlesheet Game sheet page."""
    image_folder = img_folder
    # Loop through the missing games and fetch information with ID (if provided)
    for row, (game, id) in games_array.items():
        print(f"Fetching info for {game} (ID: {id})...")
        
        # Fetch game info
        if id:
            game_info = get_board_game_info_by_id(game, id, image_folder)
        elif id is None:
            game_info = get_board_game_info(game, image_folder)
        
        if game_info:
            # Write the information to the respective columns in the Google Sheet
            sheet[f'G{row}'] = game_info.get('Image URL', '')  # Column G: Image URL local path, second arguement refers to what happens if not found
            sheet[f'K{row}'] = game_info.get('Description', 'No description available') 
            sheet[f'M{row}'] = game_info.get('Categories', 'Not specified') 
            sheet[f'O{row}'] = game_info.get('Playing Time', 'Not specified')  
            sheet[f'P{row}'] = game_info.get('Minimum Players', 'Not specified')  
            sheet[f'Q{row}'] = game_info.get('Maximum Players', 'Not specified') 
            print(f"Details for {sheet[f'B{row}']} written to row {row}.")
        else:
            print(f"Failed to fetch details for {game}.")

    print("Finished writing all missing game details.")

sheet_obj = ezsheets.Spreadsheet('1a-TIrVEULIaBvgeQDHj51CDNaIySzU27A-vkL05GQMw') # sheet ID between d/ and /edit
    
# Create game sheet object
sheet = sheet_obj['Game']

# Set Image Folder
image_folder = r"C:\Users\Macbook pro\Desktop\AWsite\python-backend\bgg_images"

# EXAMPLE USAGE
loop_sheet_find_game(sheet, image_folder, new_game)



