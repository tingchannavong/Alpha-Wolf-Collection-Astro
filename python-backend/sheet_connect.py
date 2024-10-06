# A program to connect to google sheets and fetch game clean up new logic main check by image blank row

import ezsheets
from bgg_info import get_board_game_info

sheet_obj = ezsheets.Spreadsheet('1a-TIrVEULIaBvgeQDHj51CDNaIySzU27A-vkL05GQMw') # sheet ID between d/ and /edit
    
# Create game sheet object
sheet = sheet_obj['Game']

# Get array of image url list from column G
url = sheet.getColumn('G')

# Set Image Folder
image_folder = r"C:\Users\Macbook pro\Desktop\AWsite\python-backend\bgg_images"

# Dictionary to store missing games for future fetch
# key pair value is row:game_name
missing_games = {9: 'Ticket to Ride Map Collection 1: Asia + Legendary Asia', 15: 'Face Change Rubik Cube', 16: 'Jumping Pirates', 21: 'Decrypto (2018)', 33: 'Exit: The Game – Dead Man on the Orient Express', 49: 'Who Is It?', 52: 'IQ Game', 62: 'Coup (2012)', 63: 
'Spot it Holidays', 83: 'Empathy Box', 84: 'Evolution (2014)'}

# Loop through the description col K, check if blank then fetch information from value of B,
for i, game in enumerate(url, start=1):  
    print(f'We are in row {i}')
    if game != '':
        print(f"{sheet[f'B{i}']} info already exists...")
        print(f'The cell contains {game}')
        pass
    elif game == '':
        # Fetch game info using the BGG API
        game_info = get_board_game_info(sheet[f'B{i}'], image_folder)

        if game_info:
            # Specify the column letters (A to H) for each attribute
            sheet[f'G{i}'] = game_info.get('Image URL', '')  # Column G: Image URL local path, second arguement refers to what happens if not found
            sheet[f'K{i}'] = game_info.get('Description', 'No description available') 
            sheet[f'M{i}'] = game_info.get('Categories', 'Not specified') 
            sheet[f'O{i}'] = game_info.get('Playing Time', 'Not specified')  
            sheet[f'P{i}'] = game_info.get('Minimum Players', 'Not specified')  
            sheet[f'Q{i}'] = game_info.get('Maximum Players', 'Not specified') 
            sheet[f'R{i}'] = game_info.get('Minimum Age', 'Not specified')  
            print(f"Details for {sheet[f'B{i}']} written to row {i}.")
        else:
            print(f"Failed to fetch details for {sheet[f'B{i}']}.")
            missing_games[i] = sheet[f'B{i}']

print(missing_games)
print("Finished writing all game details.")
