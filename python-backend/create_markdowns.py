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

def bulk_create_mds(sheet, from_row, to_row, output_folder):
    """Function to create markdown files in bulk taking information from google spreadsheet."""
    # Loop through the google sheet rows 3 to 89, have to plus 1
    for row in range(from_row, to_row):
        # Get game data from the relevant columns
        title = sheet[f'B{row}']  or 'Untitled Game'
        image_url = sheet[f'G{row}']  or 'No image url available'
        short_desc = sheet[f'I{row}'] or 'No description available'
        description = sheet[f'K{row}'] or 'No description available'
        category = sheet[f'M{row}'] or 'Not specified'
        playing_time = sheet[f'O{row}'] or 'Not specified'
        min_players = sheet[f'P{row}'] or 'Not specified'
        max_players = sheet[f'Q{row}'] or 'Not specified'
        location = sheet[f'R{row}'] or 'Not specified' 

        # Format the markdown content
        markdown_content = f"""---
layout: ../../layouts/game-layout.astro
title: "{title}"
description: "{short_desc}"
image: "{image_url}"
category: "{category}"
location: "{location}"
playing_time: "{playing_time}"
min_players: "{min_players}"
max_players: "{max_players}"
---
# {title}

{description}

### Category: {category}

### Playing Time: {playing_time} minutes

### Players: {min_players} - {max_players}

### Location: {location}

<img src="{image_url}" alt="{title} Image" width="500" style="display: block; margin: 0 auto">

    """
        print(f'We are in row {row}')
        
        # Save to a markdown file (one per game)
        file_name = f"{title.lower().replace(' ', '_')}.md"  # Create a markdown file name based on the game title
        file_path = os.path.join(output_folder, file_name)  # Combine folder path with file name

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(markdown_content)

        sheet[f'S{row}'] = file_path
        print(f"Markdown file generated for {title} and file path saved to sheets.")

    print('Bulk markdown creations completed.')

def update_markdown_from_sheet(sheet, from_row, to_row):
    """Function to bulk update markdown short description in the front matter, given the markdown paths in column S, and new short desc content in column I."""
    # Loop through each row where markdown paths and new descriptions are located
    for row in range(from_row, to_row):  # Modify row range as needed
        markdown_path = sheet[f'S{row}']  # Column S: markdown file path
        short_description = sheet[f'I{row}']  # Column I: new short description

        if markdown_path and short_description:
            try:
                # Read the content of the markdown file
                with open(markdown_path, 'r', encoding='utf-8') as file:
                    content = file.readlines()

                # Find and replace the short description in the file
                updated_content = []
                in_frontmatter = False
                for line in content:
                    if line.strip() == '---':
                        in_frontmatter = not in_frontmatter
                    if 'description:' in line and in_frontmatter:
                        updated_content.append(f'description: "{short_description}"\n')
                    else:
                        updated_content.append(line)

                # Write the updated content back to the markdown file
                with open(markdown_path, 'w', encoding='utf-8') as file:
                    file.writelines(updated_content)

                print(f"Updated description in {markdown_path}")

            except FileNotFoundError:
                print(f"File not found: {markdown_path}")
            except Exception as e:
                print(f"Error updating {markdown_path}: {e}")

def validate_length(text, max_length):
    if len(text) > max_length:
        return True
    else:
        return False

# Example usage
# update_markdown_from_sheet(sheet, 3, 90)

output_folder = r"C:\Users\Macbook pro\Desktop\AWsite\src\pages\boardgames"