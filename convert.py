import json
import argparse
import requests
from yattag import Doc, indent
from tkinter import Tk, filedialog

def json_to_html(json_data, output_html):
    # Initialize HTML document
    doc, tag, text = Doc().tagtext()

    def recursive_json_to_html(data, tag, text, parent_id=""):
        if isinstance(data, dict):
            element_id = f"collapse-{parent_id}"
            with tag("div", klass="card"):
                with tag("div", klass="card-header"):
                    with tag("a", href=f"#{element_id}", **{'data-toggle': "collapse", 'aria-expanded': "true", 'aria-controls': element_id}):
                        with tag("i", klass="fas fa-key"): pass
                        text(f" Object with {len(data)} elements")
                with tag("div", id=element_id, klass="collapse show"):
                    with tag("table", klass="table table-striped table-bordered"):
                        for key, value in data.items():
                            sub_element_id = f"{element_id}-{key}"
                            with tag("tr"):
                                with tag("th", klass="json-key"):
                                    text(key)
                                with tag("td", klass="json-value"):
                                    recursive_json_to_html(value, tag, text, sub_element_id)
        elif isinstance(data, list):
            element_id = f"collapse-{parent_id}"
            with tag("div", klass="card"):
                with tag("div", klass="card-header"):
                    with tag("a", href=f"#{element_id}", **{'data-toggle': "collapse", 'aria-expanded': "true", 'aria-controls': element_id}):
                        with tag("i", klass="fas fa-list-ul"): pass
                        text(f" List with {len(data)} items")
                with tag("div", id=element_id, klass="collapse show"):
                    with tag("table", klass="table table-bordered table-hover"):
                        for index, item in enumerate(data):
                            sub_element_id = f"{element_id}-item-{index}"
                            with tag("tr"):
                                with tag("th", scope="row"):
                                    text(f"Item {index + 1}")
                                with tag("td"):
                                    recursive_json_to_html(item, tag, text, sub_element_id)
        else:
            with tag("span"):
                if isinstance(data, bool):
                    with tag("i", klass="fas fa-toggle-on" if data else "fas fa-toggle-off"): pass
                    text(f" {str(data)}")
                elif isinstance(data, (int, float)):
                    with tag("i", klass="fas fa-hashtag"): pass
                    text(f" {str(data)}")
                else:
                    with tag("i", klass="fas fa-font"): pass
                    text(f" {str(data)}")

    with tag("html"):
        with tag("head"):
            with tag("title"):
                text("JSON Data Visualization")
            with tag("link", rel="stylesheet", href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"):
                pass
            with tag("link", rel="stylesheet", href="https://cdn.datatables.net/1.10.24/css/dataTables.bootstrap4.min.css"):
                pass
            with tag("link", rel="stylesheet", href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css"):
                pass
            with tag("script", src="https://code.jquery.com/jquery-3.5.1.js"):
                pass
            with tag("script", src="https://cdn.datatables.net/1.10.24/js/jquery.dataTables.min.js"):
                pass
            with tag("script", src="https://cdn.datatables.net/1.10.24/js/dataTables.bootstrap4.min.js"):
                pass
            with tag("script", src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"):
                pass
            with tag("style"):
                text("""
                    body {
                        font-family: Arial, sans-serif;
                        margin: 20px;
                    }
                    h1 {
                        text-align: center;
                        color: #333;
                        margin-bottom: 20px;
                    }
                    .json-key {
                        font-weight: bold;
                    }
                    .json-value {
                        width: 100%;
                    }
                    .card-header a {
                        text-decoration: none;
                        display: block;
                        width: 100%;
                    }
                """)
            with tag("script"):
                text("""
                    $(document).ready(function() {
                        $('.table').DataTable({
                            "paging": true,
                            "searching": true,
                            "ordering": true,
                            "responsive": true
                        });
                    });
                """)

        with tag("body", klass="container-fluid"):
            with tag("h1", klass="my-4"):
                text("JSON Data Visualization")
            recursive_json_to_html(json_data, tag, text, "root")

    # Write the HTML to file with indentation for readability
    with open(output_html, 'w', encoding='utf-8') as file:
        file.write(indent(doc.getvalue(), indentation='    ', newline='\r\n'))

def choose_file():
    # Create a root window and hide it
    root = Tk()
    root.withdraw()
    # Open a file dialog to choose the JSON file
    file_path = filedialog.askopenfilename(
        title="Select JSON File",
        filetypes=(("JSON files", "*.json"), ("All files", "*.*"))
    )
    return file_path

def fetch_json_from_url(url):
    response = requests.get(url)
    response.raise_for_status()  # Raise an error if the request was unsuccessful
    return response.json()

# Main function to run the script
def main():
    parser = argparse.ArgumentParser(description="Convert JSON file to an HTML visualization.")
    parser.add_argument('-f', '--file', type=str, help="Path to the JSON file.")
    parser.add_argument('-u', '--url', type=str, help="URL to fetch the JSON file from.")
    
    args = parser.parse_args()
    
    if args.url:
        print(f"Fetching JSON data from {args.url}...")
        json_data = fetch_json_from_url(args.url)
        json_file_path = "downloaded_json"
    elif args.file:
        json_file_path = args.file
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            json_data = json.load(json_file)
    else:
        json_file_path = choose_file()
        if not json_file_path:
            print("No file selected. Exiting.")
            return
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            json_data = json.load(json_file)

    # Set the output HTML file path
    output_html = json_file_path.replace(".json", ".html") if json_file_path != "downloaded_json" else "output.html"
    
    # Convert JSON data to HTML
    json_to_html(json_data, output_html)
    
    print(f"HTML file generated: {output_html}")

if __name__ == "__main__":
    main()
    
