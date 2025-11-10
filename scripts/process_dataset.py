"""
Process the Gen_AI Dataset.xlsx file to extract training and test data.
Expected columns: 'Query' and 'Assessment_url' (or similar variations)
"""
import argparse
import pandas as pd
import json
import os
from collections import defaultdict


def normalize_column_names(df):
    """Normalize column names to handle variations."""
    col_mapping = {}
    for col in df.columns:
        col_lower = col.lower().strip()
        if 'query' in col_lower:
            col_mapping[col] = 'Query'
        elif 'assessment' in col_lower and 'url' in col_lower:
            col_mapping[col] = 'Assessment_url'
        elif 'url' in col_lower and col_mapping.get(col) is None:
            col_mapping[col] = 'Assessment_url'
    
    if col_mapping:
        df = df.rename(columns=col_mapping)
    return df


def extract_catalog_from_data(df_dict):
    """Extract unique assessments to create a catalog."""
    all_urls = set()
    url_data = {}
    
    for sheet_name, df in df_dict.items():
        if 'Assessment_url' in df.columns:
            for _, row in df.iterrows():
                url = row.get('Assessment_url')
                if pd.notna(url) and url:
                    all_urls.add(url)
                    if url not in url_data:
                        # Extract assessment name from URL or use as-is
                        name = url.split('/')[-1].replace('-', ' ').title()
                        url_data[url] = {
                            'name': name,
                            'url': url,
                            'description': f"Assessment from {sheet_name}",
                            'type': None,
                            'duration': None,
                            'skills': []
                        }
    
    return list(url_data.values())


def process_dataset(input_path: str, output_dir: str = "data"):
    """Process Excel dataset and save as CSV and JSON."""
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Read all sheets
        print(f"📂 Reading {input_path}...")
        df_dict = pd.read_excel(input_path, sheet_name=None)
        
        print(f"\n📊 Found {len(df_dict)} sheet(s): {list(df_dict.keys())}")
        
        # Process each sheet
        processed_sheets = {}
        for sheet_name, df in df_dict.items():
            print(f"\n{'='*60}")
            print(f"Processing: {sheet_name}")
            print(f"{'='*60}")
            print(f"Original shape: {df.shape}")
            print(f"Original columns: {list(df.columns)}")
            
            # Normalize column names
            df = normalize_column_names(df)
            print(f"Normalized columns: {list(df.columns)}")
            
            # Remove rows with missing critical data
            if 'Query' in df.columns and 'Assessment_url' in df.columns:
                original_len = len(df)
                df = df.dropna(subset=['Query', 'Assessment_url'])
                if len(df) < original_len:
                    print(f"⚠️  Removed {original_len - len(df)} rows with missing data")
                print(f"Final shape: {df.shape}")
                
                # Show sample
                if len(df) > 0:
                    print(f"\n📋 Sample data:")
                    print(df.head(2).to_string(index=False, max_colwidth=50))
            
            # Save as CSV
            csv_filename = sheet_name.lower().replace(' ', '_')
            csv_path = f"{output_dir}/{csv_filename}.csv"
            df.to_csv(csv_path, index=False)
            print(f"\n✓ Saved CSV: {csv_path}")
            
            processed_sheets[sheet_name] = df
        
        # Extract catalog from all sheets
        print(f"\n{'='*60}")
        print("Creating Assessment Catalog")
        print(f"{'='*60}")
        catalog = extract_catalog_from_data(processed_sheets)
        
        if catalog:
            # Save catalog as JSON
            catalog_path = f"{output_dir}/catalog.json"
            with open(catalog_path, 'w') as f:
                json.dump(catalog, f, indent=2)
            print(f"✓ Created catalog with {len(catalog)} unique assessments")
            print(f"✓ Saved to: {catalog_path}")
            
            # Also save as CSV for easy viewing
            catalog_df = pd.DataFrame(catalog)
            catalog_csv_path = f"{output_dir}/catalog.csv"
            catalog_df.to_csv(catalog_csv_path, index=False)
            print(f"✓ Saved to: {catalog_csv_path}")
        
        # Print summary
        print(f"\n{'='*60}")
        print("📊 SUMMARY")
        print(f"{'='*60}")
        for sheet_name, df in processed_sheets.items():
            if 'Query' in df.columns:
                unique_queries = df['Query'].nunique()
                total_rows = len(df)
                print(f"{sheet_name}:")
                print(f"  - Total rows: {total_rows}")
                print(f"  - Unique queries: {unique_queries}")
                if 'Assessment_url' in df.columns:
                    unique_assessments = df['Assessment_url'].nunique()
                    print(f"  - Unique assessments: {unique_assessments}")
        
        if catalog:
            print(f"\nCatalog: {len(catalog)} unique assessments")
        
        print(f"\n✅ Dataset processing complete!")
        print(f"📁 All files saved to: {output_dir}/")
        
        return processed_sheets, catalog
        
    except Exception as e:
        print(f"\n❌ Error processing dataset: {e}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process Gen_AI Dataset.xlsx")
    parser.add_argument("--input", default="Gen_AI Dataset.xlsx", help="Input Excel file")
    parser.add_argument("--output", default="data", help="Output directory")
    args = parser.parse_args()
    
    process_dataset(args.input, args.output)
