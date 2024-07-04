import pdfplumber
import pandas as pd

def extract_tables_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        all_tables = []
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                all_tables.append(table)

    for idx, table in enumerate(all_tables):
        df = pd.DataFrame(table[1:], columns=table[0])
        csv_path = f'table_{idx+1}.csv'
        df.to_csv(csv_path, index=False)
        print(f"Table {idx+1} saved to {csv_path}")

if __name__ == "__main__":
    pdf_path = 'path_to_your_pdf.pdf'  :: Change this to the path of your PDF file
    extract_tables_from_pdf(pdf_path)
