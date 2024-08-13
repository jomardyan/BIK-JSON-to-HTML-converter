import json
import argparse
import requests
from yattag import Doc, indent
from tkinter import Tk, filedialog

def json_to_html(json_data, output_html):
    # Initialize HTML document
    doc, tag, text = Doc().tagtext()

    def recursive_json_to_html(data, tag, text):
        if isinstance(data, dict):
            with tag("table", klass="table table-striped table-bordered"):
                for key, value in data.items():
                    with tag("tr"):
                        with tag("th", klass="json-key"):
                            text(key)
                        with tag("td", klass="json-value"):
                            recursive_json_to_html(value, tag, text)
        elif isinstance(data, list):
            with tag("table", klass="table table-bordered table-hover"):
                for index, item in enumerate(data):
                    with tag("tr"):
                        with tag("th", scope="row"):
                            text(f"Item {index + 1}")
                        with tag("td"):
                            recursive_json_to_html(item, tag, text)
        else:
            text(data)

    with tag("html"):
        with tag("head"):
            with tag("title"):
                text("JSON to HTML Visualization")
            with tag("link", rel="stylesheet", href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"):
                pass
            with tag("link", rel="stylesheet", href="https://cdn.datatables.net/1.10.24/css/dataTables.bootstrap4.min.css"):
                pass
            with tag("script", src="https://code.jquery.com/jquery-3.5.1.js"):
                pass
            with tag("script", src="https://cdn.datatables.net/1.10.24/js/jquery.dataTables.min.js"):
                pass
            with tag("script", src="https://cdn.datatables.net/1.10.24/js/dataTables.bootstrap4.min.js"):
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
                    table.json-table {
                        width: 100%;
                        border-collapse: collapse;
                        margin: 20px 0;
                    }
                    table.json-table th, table.json-table td {
                        padding: 10px;
                        text-align: left;
                        vertical-align: top;
                    }
                    .json-key {
                        font-weight: bold;
                    }
                    .json-value {
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
            recursive_json_to_html(json_data, tag, text)

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
