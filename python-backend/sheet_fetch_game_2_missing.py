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
missing_games = {
        9: ('Ticket to Ride Map Collection 1: Asia', None), 
        15: ('Face Change Rubik Cube', None), 
        16: ('Pop-up Pirate', None), 
        21: ('Decrypto', 2018),  # Year specified
        33: ('Dead Man on the Orient Express', 2017), 
        49: ('Who Is It', 1979), 
        52: ('IQ Game', None), 
        62: ('Coup', 2012),  # Year specified
        63: ('Spot it Holidays', None), 
        83: ('The Empathy Box', None), 
        84: ('Evolution', 2014)  # Year specified
    }

# Loop through the description col G, check if blank then fetch information from value of B,
for i, game in enumerate(url, start=1): # Have to start at 1 for the logic to work  
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
            print(f"Details for {sheet[f'B{i}']} written to row {i}.")
        else:
            print(f"Failed to fetch details for {sheet[f'B{i}']}.")
            missing_games[i] = sheet[f'B{i}']

print(missing_games)
print("Finished writing all game details.")
