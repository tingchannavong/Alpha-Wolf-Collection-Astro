import ezsheets
import os

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

# Loop through the rows 3 to 88
for row in range(3, 4):
    # Get game data from the relevant columns
    title = sheet[f'B{row}']  # Title is in column B
    image_url = sheet[f'G{row}']  # Image URL in column G
    short_desc = sheet[f'I{row}'] or 'No description available'
    description = sheet[f'K{row}'] or 'No description available'
    category = sheet[f'M{row}'] or 'Not specified'
    playing_time = sheet[f'O{row}'] or 'Not specified'
    min_players = sheet[f'P{row}'] or 'Not specified'
    max_players = sheet[f'Q{row}'] or 'Not specified'

    # Format the markdown content
    markdown_content = f"""---
layout: ../../layouts/game-layout.astro
title: "{title}"
description: "{short_desc}"
image: "{image_url}"
category: "{category}"
---
# {title}

![{title} Image]({image_url})

{description}

### Category: {category}

### Playing Time: {playing_time} minutes

### Players: {min_players} - {max_players}

"""
    
    output_folder = r"C:\Users\Macbook pro\Desktop\AWsite\src\pages\game-details"
    
    # Save to a markdown file (one per game)
    file_name = f"{title.lower().replace(' ', '_')}.md"  # Create a markdown file name based on the game title
    file_path = os.path.join(output_folder, file_name)  # Combine folder path with file name

    with open(file_path, 'w') as file:
        file.write(markdown_content)

    print(f"Markdown file generated for {title}")
