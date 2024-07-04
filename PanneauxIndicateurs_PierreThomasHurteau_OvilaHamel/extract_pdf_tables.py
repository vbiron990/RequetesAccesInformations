import os
import pdfplumber
import pandas as pd

def reverse_rows(df):
    """Reverse the order of characters in each cell of the DataFrame."""
    for col in df.columns:
        df[col] = df[col].apply(lambda x: x[::-1] if isinstance(x, str) else x)
    return df

def reverse_columns(df):
    """Reverse the order of columns in the DataFrame."""
    df = df.iloc[:, ::-1].reset_index(drop=True)
    return df

def extract_tables_from_pdf(pdf_path, output_dir, doc_number):
    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            try:
                # Extract tables from the page
                tables = page.extract_tables()
                for table_number, table in enumerate(tables, start=1):
                    # Convert the table to a DataFrame
                    df = pd.DataFrame(table)
                    
                    # Check if the DataFrame is not empty
                    if not df.empty:
                        # Reverse the order of characters in each cell
                        df = reverse_rows(df)
                        
                        # Handle the landscape format by transposing the table
                        df = df.T
                        
                        # Reverse the order of columns to match the correct order
                        df = reverse_columns(df)
                        
                        # Set the first row as the header
                        df.columns = df.iloc[0]
                        df = df[1:]
                        
                        # Save the DataFrame to a CSV file
                        csv_path = os.path.join(output_dir, f'document_{doc_number}_page_{page_number}_table_{table_number}.csv')
                        df.to_csv(csv_path, index=False)
                        print(f"Table {table_number} from Page {page_number} of Document {doc_number} saved to {csv_path}")
            except Exception as e:
                print(f"Error processing page {page_number} of document {doc_number}: {e}")

if __name__ == "__main__":
    # Paths to the PDF documents
    pdf_paths = [
        (r'documents\reponse\Document 1 - AI-2024-0763 - Rue Ovila-Hamel, direction Cousineau.pdf', 1),
        (r'documents\reponse\Document 2 - AI-2024-0763 - Rue Ovila-Hamel, direction PTH.pdf', 2)
    ]
    
    # Output directory
    output_dir = r'raw'
    
    # Create output directory if it does not exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Extract tables from each PDF
    for pdf_path, doc_number in pdf_paths:
        extract_tables_from_pdf(pdf_path, output_dir, doc_number)
