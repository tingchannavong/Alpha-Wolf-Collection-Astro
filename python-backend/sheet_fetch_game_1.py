# A program to connect to google sheets and fetch game info version 1

import ezsheets
from bgg_info import get_board_game_info

sheet_obj = ezsheets.Spreadsheet('1a-TIrVEULIaBvgeQDHj51CDNaIySzU27A-vkL05GQMw') # sheet ID between d/ and /edit
    
# print(sheet_obj.title)
# print(sheet_obj.sheetTitles)

# Create game sheet object
sheet = sheet_obj['Game']

# Get array of game list from column B 
# games = sheet.getColumn('B')
# print(games)

# Array copied from terminal
games = ['Catan', 'Mahjong Cards Red Box', 'Ticket to Ride ', 'Sequece', 'Spot it! Animals', 'Patchwork ', 'Ticket to Ride Asia', 'Sushi Go Party Pack', 'Codenames Original ', '7 Wonders', 'Azul ', 'Root', 'Face Change Rubik Cube', "Werewolves of Miller's Hollow ", 'Jumping Pirates', 'Dix It Square ', 'The Mind', 'Avalon', 'Dix It', 'Decrypto', 'Magic Maze', 'Ultimate Werewolf ', 'Cockroach poker', 'Saboteur ', 'Salem', 'Sheriff of Nottingham ', 'Chinatown', 'Bang the Dice Game', 'Taboo Purple Edition', 'Chess Magnetic 25x25 cm', 'In Front of the Elevator', 'Exit: Dead Man on Orient Express', 
'Carcassone', 'Taco Goat Cheese Pizza: On The Flip Side ', 'Coup', 'Splendor ', 'Taco Goat Cheese Pizza', 'Ghost Blitz: 5 to 12', 'Spot it! On the road', 'Camel Up', 'Uno Flip ', 'Codenames Pictures ', 'Cluedo ', 'Hickory Dickory', 'Monopoly Deal', 'Hanabi', 'Exploding Kittens', 'Who is it?', 'Halli Gali', 'Chess Wood 29*29 cm', "I'm the Boss", 'IQ Game', 'Apples to Apples', 'Exploding Kittens 18+', 'Werewolves Chinese Version ', 'Organ Attack', 'Risk Fight for Global Domination', 'One Night Ultimate Vampire', 'One Night Ultimate Werewolves', 'Pandemic', 'Contagion', 'Tichu', 'Coup', 'Empathy Box Lao Version', 
'Spot it Holidays', 'Monopoly Cantabria Version', 'Cards Against Humanity (Red)', 'Fuse', 'Cluedo Suspect', 'Timeline Classic', 'The Coding', 'Timeline Invention', 'Truth or Drink', 'Timeline Events', 'Team 3 (Green Version)', 'Team 3 (Pink Version)', 'Tiny Towns', 'For Sale', 'I should have known that', 'Jungle Speed', 'Misty', 'Power Grid', 'Uno Wild', 'If You Had To', 'Empathy Box', 'Evolution', "It's pretty clever", 'Twice as clever', 'Secret Hitler']

#Set Image Folder
image_folder = r"C:\Users\Macbook pro\Desktop\AWsite\python-backend\bgg_images"

# Loop through the games and fetch information
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