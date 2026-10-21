# A program to connect to google sheets and fetch game by 
# 1) game ID (if provided), more specific no room for mistake
# 2) name in a dictionary structure, more generic but less manual work

import ezsheets
from bgg_info import get_board_game_info_by_id, get_board_game_info, replace_spaces_in_filepath

# Dictionary to store missing games for future fetch
# key pair value is row: (game_name, game_id)
new_games = {
        85: ('Twice as Clever', 269210),
        86: ("That's pretty clever", 244522),
        }

def get_row_games_id(sheet, start, end):
    """Takes in start and end row of the sheet. Loop through a games sheet get the name and row and create games dictionary for search next step."""
    print("Creating the game dictionary...")
    len = end - start
    games_dict = {}
    for i in range(len+1):
        games_dict[start] = (sheet[f'B{start}'], sheet[f'C{start}'] if sheet[f'C{start}'] else None)
        start += 1
    print("Completed creating game dictionary below!")
    print(games_dict)
    return games_dict

def loop_sheet_find_game(sheet, img_folder, games_array):
    """Loop through a games dictionary with row number and name, fetch BGG API to find info and 
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

image_folder = r"C:\Users\Macbook pro\Desktop\AWsite\python-backend\bgg_images"
             
# EXAMPLE USAGE
# get_row_games_id(sheet, 93, 110)
# loop_sheet_find_game(sheet, image_folder, test)