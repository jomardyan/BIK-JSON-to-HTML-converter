import json
from yattag import Doc, indent
from tkinter import Tk, filedialog

def json_to_html(json_data, output_html):
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
                text("BIK report to HTML Visualization")
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

        with tag("body", klass="container"):
            with tag("h1", klass="my-4"):
                text("JSON Data Visualization")
            recursive_json_to_html(json_data, tag, text)

    with open(output_html, 'w', encoding='utf-8') as file:
        file.write(indent(doc.getvalue(), indentation='    ', newline='\r\n'))

def choose_file():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select JSON File",
        filetypes=(("JSON files", "*.json"), ("All files", "*.*"))
    )
    return file_path

def main():
    json_file_path = choose_file()
    if not json_file_path:
        print("No file selected. Exiting.")
        return
    
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)
# REPLACE THE LOCATION TO THE FILSERVER LOCATION
    output_html = json_file_path.replace(".json", ".html")
    
    json_to_html(json_data, output_html)
    
    print(f"HTML file generated: {output_html}")

if __name__ == "__main__":
    main()
