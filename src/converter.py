import json
import os
import base64
import sys
from pathlib import Path

def create_book_structure(json_file, output_dir, book_name):
    # Create the base directory structure
    book_dir = Path(output_dir) / 'static' / book_name
    book_dir.mkdir(parents=True, exist_ok=True)

    # Load the JSON data
    with open(json_file, 'r') as f:
        data = json.load(f)

    # Create pages
    for index, page_data in enumerate(data, start=1):
        # Create page directory
        page_dir = book_dir / str(index)
        page_dir.mkdir(exist_ok=True)

        # Write text file
        text_file = page_dir / 'text.txt'
        with open(text_file, 'w', encoding='utf-8') as f:
            f.write(page_data['paragraph'])

        # Write image file
        image_file = page_dir / 'image.jpg'
        image_data = base64.b64decode(page_data['b64'])
        with open(image_file, 'wb') as f:
            f.write(image_data)

    print(f"Created book '{book_name}' with {len(data)} pages in {output_dir}/static")

def main():
    if len(sys.argv) != 3:
        print("Usage: python convert_json.py <json_file> <book_name>")
        sys.exit(1)

    json_file = sys.argv[1]
    book_name = sys.argv[2]
    output_dir = '.'

    create_book_structure(json_file, output_dir, book_name)

if __name__ == "__main__":
    main()