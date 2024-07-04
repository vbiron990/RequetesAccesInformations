# PDF Table Extraction

This project extracts tables from PDF documents and saves them as CSV files. It uses `pdfplumber` to read the PDF and `pandas` to handle the data and save it to CSV.

## Setup and Installation

### Prerequisites

- Anaconda (https://www.anaconda.com/products/distribution)
- Python 3.9

### Create and Activate Anaconda Environment

1. Open your terminal (Anaconda Prompt on Windows).

2. Create a new environment:
    ```sh
    conda create -n pdf_extraction python=3.9
    ```

3. Activate the environment:
    ```sh
    conda activate pdf_extraction
    ```

### Install Required Libraries

1. Install `pandas` using conda:
    ```sh
    conda install pandas
    ```

2. Install `pdfplumber` using pip:
    ```sh
    pip install pdfplumber
    ```

## Usage

1. Clone this repository or download the `extract_pdf_tables.py` script and place it in your working directory.

2. Place the PDF file you want to extract tables from in the same directory as the script.

3. Open `extract_pdf_tables.py` in a text editor and change the `pdf_path` variable to the path of your PDF file.

4. Run the script:
    ```sh
    python extract_pdf_tables.py
    ```

5. The tables will be extracted and saved as CSV files in the same directory.

## Example

For a PDF file named `example.pdf` in the same directory as the script, set the `pdf_path` variable:
```python
pdf_path = 'example.pdf'
```

Then run the script:
```sh
python extract_pdf_tables.py
```

The output CSV files will be named `table_1.csv`, `table_2.csv`, etc.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [pdfplumber](https://github.com/jsvine/pdfplumber)
- [pandas](https://pandas.pydata.org/)
