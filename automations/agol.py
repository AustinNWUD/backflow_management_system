import pandas as pd
import os
from dotenv import load_dotenv
from arcgis.gis import GIS
import datetime
from datetime import timedelta

class agol:
    def __init__(self) -> None:
        import os
        from dotenv import load_dotenv
        from arcgis.gis import GIS
        
        #used to navigate to location of .env
        load_dotenv('automations/.env')
        
        #storing connection for agol in self.gis variable
        #for later reference in class functions

        url = os.getenv('_url')
        un = os.getenv('_un')
        pw = os.getenv('_pw')
        self.gis = GIS(url, un, pw)
        
    def gather_data(self, 
                    feature_service_id: str, 
                    table_pos: dict, 
                    most_recent_layer_id: str) -> None:
        
        '''
        ### Parameters
        1. feature_service_id: str
            - Should be a string of the ID for the feature service taken from AGOL
        2. table_pos: dict
            - Provice a dictionary indicating the index of the specific tables
            - Expected format:
            {'facilities' : 0, 'letters' : 0}
            - Note that Layer indexes begin at 0, and table indexes begin at 0
        3. most_recent_layer_id: str
            - Should be a string of the ID for the Joined Table View containing
            the most recent device and test information
        
        ### Return
        Funtion returns nothing, instead stores all relevant information in
        class variables for access by other class functions
        
        ### Raises
        1. TypeError
            - Most likely the result of an improper argument provided
        2. IndexError
            - The integers provided in the table dictionary are not valid
        3. Other Misc Errors:
            - The ArcGIS API may return an error in the event the provided id
            is incorrect
        '''
        import pandas as pd
        
        gis = self.gis
        
        #define major endpoints used as class attribute
        main_target = gis.content.get(feature_service_id)
        self.facility_target = main_target.layers[table_pos['facilities']]
        self.letter_target = main_target.tables[table_pos['letters']]
        self.recent_target = gis.content.get(most_recent_layer_id)
        
        #queries data into pandas dataframes for 
        #later query operations in memory
        #this reduces the number of API queries 
        #and thus improves overall performance
        self.facilities_data = self.facility_target.query(where="1=1").sdf
        self.letter_data = self.letter_target.query(where="1=1").sdf
        self.recent_data = self.recent_target.query(where='device_status=1').sdf
        
    def query_past_due(self, 
                       date_column:str = 'next_test') -> dict:
        '''
        Returns data for all past due devices
        
        ### Parameters
        1. date_column: str
            - The name of the column containing the due date for each devices next test
        
        ### Return
        1. data packaged into dictionary for comprehension in other functions/classes
        
             - Keys:
                'data' - paired with data frame
                'interest' - discriptive pair to identify dataframe
                'validated' - bool to determine whether dataframe has been checked
                against previous notices
                
        ### Raises
        1. KeyError
            - the provided column name doesn't exist in the queried dataset
        '''
        
        import datetime as dt
        from datetime import timedelta
        
        df = self.recent_data
        
        #defines date of interest to use in df.loc query
        q_date = dt.date.today()
        
        df = df.loc[df[date_column].dt.date < q_date]
        
        result = {
            'data' : df,
            'interest' : 'past due',
            'validated' : False
        }
        
        return result
        
    def query_30_day(self, date_column:str = 'next_test') -> dict:
        '''
        Returns data for all devices with tests due in exactly 30 days
        
        ### Parameters
        1. date_column: str
            - The name of the column containing the due date for each devices next test
        
        ### Return
        1. data packaged into dictionary for comprehension in other functions/classes
        
             - Keys:
                'data' - paired with data frame
                'interest' - discriptive pair to identify dataframe
                'validated' - bool to determine whether dataframe has been checked
                against previous notices
                
        ### Raises
        1. KeyError
            - the provided column name doesn't exist in the queried dataset
        '''
        
        import datetime as dt
        from datetime import timedelta
        
        df = self.recent_data
        
        #defines date of interest to use in df.loc query
        q_date = dt.date.today() + timedelta(30)
        
        df = df.loc[df[date_column].dt.date == q_date]
        
        result = {
            'data' : df,
            'interest' : 'due in 30 days',
            'validated' : False
        }
        
        return result
        
    def query_60_day(self, date_column:str = 'next_test') -> dict:
        '''
        Returns data for all devices with tests due in exactly 60 days
        
        ### Parameters
        1. date_column: str
            - The name of the column containing the due date for each devices next test
        
        ### Return
        1. data packaged into dictionary for comprehension in other functions/classes
        
             - Keys:
                'data' - paired with data frame
                'interest' - discriptive pair to identify dataframe
                'validated' - bool to determine whether dataframe has been checked
                against previous notices
                
        ### Raises
        1. KeyError
            - The provided column name doesn't exist in the queried dataset
        '''
        
        import datetime as dt
        from datetime import timedelta
        
        df = self.recent_data
        
        #defines date of interest to use in df.loc query
        q_date = dt.date.today() + timedelta(60)
        
        df = df.loc[df[date_column].dt.date == q_date]
        
        result = {
            'data' : df,
            'interest' : 'due in 60 days',
            'validated' : False
        }
        
        return result
    
    def query_90_day(self, date_column:str = 'next_test') -> dict:
        '''
        Returns data for all devices with tests due in exactly 90 days
        
        ### Parameters
        1. date_column: str
            - The name of the column containing the due date for each devices next test
        
        ### Return
        1. data packaged into dictionary for comprehension in other functions/classes
        
             - Keys:
                'data' - paired with data frame
                'interest' - discriptive pair to identify dataframe
                'validated' - bool to determine whether dataframe has been checked
                against previous notices
                
        ### Raises
        1. KeyError
            - the provided column name doesn't exist in the queried dataset
        '''        
        
        import datetime as dt
        from datetime import timedelta
        
        df = self.recent_data
        
        #defines date of interest to use in df.loc query
        q_date = dt.date.today() + timedelta(90)
        
        df = df.loc[df[date_column].dt.date == q_date]
        
        result = {
            'data' : df,
            'interest' : 'due in 90 days',
            'validated' : False
        }
        
        return result
    
    def query_new_facilities(self, facility_status_column: str = 'fac_status') -> dict:
        #placeholder to refactor new facility queries
        return 'Hell, World!'