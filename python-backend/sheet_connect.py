# A program to connect to google sheets and operate on different tasks

import ezsheets
from bgg_info import replace_spaces_in_filepath, replace_many, find_first_sentence

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
    """Loop through column and perform find & replace certain parts of text on the cell."""

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

# sample replacements dictionary
replacements_dict = {
    "&quot;": " ",
    "&mdash;": " ",
    "&ldquo;": " ",
    "&hellip;": " ",
    "&rdquo;": " ",
    "&lsquo;": " ",
    "&rsquo;": " "
}

# EXAMPLE USAGE
# replace_spaces_in_filepath(sheet, 'G', 3, 90)
