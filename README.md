# BIK-JSON-to-HTML-converter
for bik.pl

USAGE: 
-   **From the Command Line** with a URL:
  
    `python script_name.py -u https://example.com/data.json` 
    
    -   This fetches the JSON data from the URL and generates an HTML file named `output.html`.
-   **From the Command Line** with a File:
    
    `python script_name.py -f /path/to/your/file.json` 
    
    -   This uses the specified JSON file to generate an HTML output.
-   **Without Arguments**:
    
    `python script_name.py` 
    
    -   The script will prompt you to select a JSON file via a file dialog.
