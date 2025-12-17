import pandas as pd

class stage2(): 
    def __init__(self):
        pass 
    
    def find_more_details(self, df, persons): 
        #Search for spacific person details in database 
        data = pd.read_csv(persons)
        full_details = data.merge(df, on = 'name', how = 'left', suffixes = ("", "_drop")) 
        found_data = full_details[full_details['name'].notna()] 
        not_found_data = full_details[full_details['name'].isna()]['name'].tolist() 
        return found_data, not_found_data