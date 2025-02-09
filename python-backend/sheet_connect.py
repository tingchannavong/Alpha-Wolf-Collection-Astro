# A program to connect to google sheets and operate on different tasks

import ezsheets
from bgg_info import replace_spaces_in_filepath, replace_many, find_first_sentence, get_board_game_info_by_id, get_board_game_info
from create_markdowns import bulk_create_mds
from sheet_fetch_game3_id import loop_sheet_find_game

def connect_to_sheet(sheet_id, sheet_title):
    """Connect to your specific google sheet and select the sheet title you want to work with." 
      Args:
        sheet_id: The sheet ID is between d/ and /edit in the url.
        sheet_title: The literal string title of your sheet.
        Returns sheet object for you to work with."""
    # Make a request to google sheet API provided your ID
    sheet_obj = ezsheets.Spreadsheet(sheet_id) 
    
    # Create game sheet object
    sheet = sheet_obj[sheet_title]
    return sheet

sheet_id = '1a-TIrVEULIaBvgeQDHj51CDNaIySzU27A-vkL05GQMw'
sheet_title = 'Game'
sheet = connect_to_sheet(sheet_id, sheet_title)

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

# Games to fetch info and create markdowns
new_game = {
        85: ('Twice as Clever', 269210),
        86: ("That's pretty clever", 244522),
        }

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

# Set Image Folder
image_folder = r"C:\Users\Macbook pro\Desktop\AWsite\public"

# Set markdown save folder
output_folder = r"C:\Users\Macbook pro\Desktop\AWsite\src\pages\boardgames"

# EXAMPLE USAGE
# loop_sheet_find_game(sheet, image_folder, new_game)

# loop_range_fnr_1s(sheet, 85, 87)

bulk_create_mds(sheet, 3, 89, output_folder)
