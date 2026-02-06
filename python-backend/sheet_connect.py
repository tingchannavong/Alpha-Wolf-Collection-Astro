# A program to connect to google sheets and operate on different tasks
import ezsheets
from bgg_info import replace_spaces_in_filepath, replace_many, find_first_sentence, get_board_game_info_by_id, get_board_game_info
from fetch_gameids import loop_sheet_find_game, get_row_games_id
from create_markdowns import bulk_create_mds

def loop_col_find_replace(column, replacements):
    """Loop through all column and perform find & replace certain parts of text on the cell."""

    # Make data array/list from specified column
    data_array = sheet.getColumn(column, replacements)

    # Loop through the description array 
    for row, each in enumerate(data_array, start=1): #Start at 1 because google sheet start counting from row 1 
        print(f'We are in row {row}')

        # Perform find and replace
        new_text = replace_many(each, replacements) 

        # Write new text to the cell
        sheet[f'{column}{row}'] = new_text
        print(f'Text found and replaced for {row}')

        # Different operations to perform
        short_desc = find_first_sentence(each)
        print(short_desc)

        # Write first sentence to cell in column I 
        sheet[f'I{row}'] = short_desc
        print(f'Short description for {sheet[f'B{row}']} written to {row}')
        
    print("All operations completed.")

def loop_range_fnr_1s(sheet, row_from, row_to):
    """Loop a given range in the google sheet to perform operations such as find and replace syntax in long description (col K) and find first sentence and write to short desc (col I)"""
    # Loop through the K on specific row
    for row in range(row_from, row_to): 
        print(f'We are in row {row}')

        # Perform find and replace
        new_text = replace_many(sheet[f'K{row}'], replacements_dict) 

        # Write new text to the cell
        sheet[f'K{row}'] = new_text
        print(f'Text found and replaced for {row}')

        # Different operations to perform
        short_desc = find_first_sentence(sheet[f'K{row}'])
        print(short_desc)

        # Write first sentence to cell in column I 
        sheet[f'I{row}'] = short_desc
        print(f'Short description for {sheet[f'B{row}']} written to {row}')
        
    print("All operations completed.")

# sample replacements dictionary
replacements_dict = {
    "<br/>": " ",
    "&quot;": " ",
    "&mdash;": " ",
    "&ldquo;": " ",
    "&hellip;": " ",
    "&rdquo;": " ",
    "&lsquo;": " ",
    "&rsquo;": " "
}

# Connect to sheet
sheet_obj = ezsheets.Spreadsheet('1a-TIrVEULIaBvgeQDHj51CDNaIySzU27A-vkL05GQMw') # sheet ID between d/ and /edit
    
# Create game sheet object
sheet = sheet_obj['Game']

# 1. Set Image Folder
# image_folder = r"C:\Users\Macbook pro\Desktop\AWsite\public"
image_folder = r"/Users/macbook/Desktop/Alpha-Wolf-Collection-Astro/python-backend/bgg-images"

# 2. Set markdown save folder
output_folder = r"/Users/macbook/Desktop/Alpha-Wolf-Collection-Astro/src/pages/boardgames"

# search_sample = {109: ('Mr. Jack New York', None), 110: ('Die Fiesen 7', None)}
# Games to fetch info and create markdowns
manual_search = {
        'row-number': ("Game name", '6-digit-id'), 
}

# 3. EXAMPLE USAGE
# get_row_games_id(sheet, 93, 110)

# loop_sheet_find_game(sheet, image_folder, search)

# loop_range_fnr_1s(sheet, 93, 108)

# replace_spaces_in_filepath(sheet, "G", 93, 110)

# bulk_create_mds(sheet, 109, 110, output_folder)
