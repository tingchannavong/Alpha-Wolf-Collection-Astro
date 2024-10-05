# A program to connect to google sheets and fetch game clean up new logic main check by image blank row

import ezsheets
from bgg_info import get_board_game_info

sheet_obj = ezsheets.Spreadsheet('1a-TIrVEULIaBvgeQDHj51CDNaIySzU27A-vkL05GQMw') # sheet ID between d/ and /edit
    
# Create game sheet object
sheet = sheet_obj['Game']

# Get array of image url list from column K 
description = sheet.getColumn('K')

#Set Image Folder
image_folder = r"C:\Users\Macbook pro\Desktop\AWsite\python-backend\bgg_images"

# Loop through the description col K, check if blank then fetch information from value of B,
for i, game in enumerate(games, start=3):  # Start from row 3 (to skip the header and data type rows)
    print(f"Fetching info for {game}...")

    # Fetch game info using the BGG API
    game_info = get_board_game_info(game, image_folder)

    if game_info:
        # Specify the column letters (A to H) for each attribute
        sheet[f'G{i}'] = game_info.get('Image URL', '')  # Column G: Image URL local path, second arguement refers to what happens if not found
        sheet[f'K{i}'] = game_info.get('Description', 'No description available') 
        sheet[f'M{i}'] = game_info.get('Categories', 'Not specified') 
        sheet[f'O{i}'] = game_info.get('Playing Time', 'Not specified')  
        sheet[f'P{i}'] = game_info.get('Minimum Players', 'Not specified')  
        sheet[f'Q{i}'] = game_info.get('Maximum Players', 'Not specified') 
        sheet[f'R{i}'] = game_info.get('Minimum Age', 'Not specified')  
        print(f"Details for {game} written to row {i}.")
    else:
        print(f"Failed to fetch details for {game}.")

print("Finished writing all game details.")
