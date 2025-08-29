#!/usr/bin/python3

import json
import sys
import html

def node_to_html(node):
    """
    Recursively convert a JSON node to HTML bookmark format.
    """
    if node.get('type') == 'folder':
        folder_name_escaped = html.escape(node['name'])
        html_str = f'<DT><H3>{folder_name_escaped}</H3>\n<DL><p>\n'
        children = node.get('children', [])
        for child in children:
            html_str += node_to_html(child)
        html_str += '</DL><p>\n'
        return html_str
    elif node.get('type') == 'url':
        name_escaped = html.escape(node['name'])
        url_escaped = html.escape(node['url'], quote=True)
        return f'<DT><A HREF="{url_escaped}">{name_escaped}</A>\n'
    else:
        return ''  # Ignore any other types or invalid nodes

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python bookmark_converter.py input.json output.html")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Extract root name and escape it for HTML
        root_name = html.escape(data.get('name', 'Bookmarks'))
        
        # Build the HTML content
        html_content = """<!DOCTYPE NETSCAPE-Bookmark-file-1>
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<TITLE>Bookmarks from JSON</TITLE>
<H1>{}</H1>
<DL><p>
""".format(root_name)
        
        # Add the recursive HTML for the root node
        html_content += node_to_html(data)
        
        # Close the main DL tag
        html_content += '</DL><p>\n'
        
        # Write the output to the specified file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"Bookmarks successfully written to {output_file}. You can import this HTML file into your browser.")
    
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)
    
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in input file '{input_file}'.")
        sys.exit(1)
    
    except KeyError as e:
        print(f"Error: Missing key in JSON structure: {e}. Ensure all nodes have 'type', 'name', and for URLs, 'url'.")
        sys.exit(1)
    
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)
