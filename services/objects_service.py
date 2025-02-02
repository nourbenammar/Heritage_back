import os
import pandas as pd

class ObjectsService:
    
    def retrieve_all_fields_from_csv(self, file_path):
        all_data = []
        
        try:
            # Try reading the CSV file with auto-detecting the delimiter, handling encoding errors
            df = pd.read_csv(file_path, sep=None, engine="python", encoding='latin1', 
                 encoding_errors='replace', on_bad_lines='skip')
            
            # Print first few rows to check structure
            print(df.head())
            
            df.fillna('Unknown', inplace=True)
            
            all_data.extend(df.to_dict(orient='records'))
        except pd.errors.ParserError as e:
            print(f"Error reading {file_path}: {e}")
        except UnicodeDecodeError:
            print(f"Error reading {file_path} with utf-8 encoding. Retrying with latin1.")
            try:
                df = pd.read_csv(file_path, sep=None, engine="python", encoding='latin1', encoding_errors='replace', quotechar='"', na_values='')
                print(df.head())
                df.fillna('Unknown', inplace=True)
                all_data.extend(df.to_dict(orient='records'))
            except Exception as e:
                print(f"Failed to read {file_path} even with latin1 encoding: {e}")
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
        
        return all_data
