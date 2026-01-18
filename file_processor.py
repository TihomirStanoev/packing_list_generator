import pandas as pd
import numpy as np

class DfConfigMixin:
        # INDEX : [SAP Export, DataFrame]
    columns_settings: dict[int, list[str]]= {
        0: ['Customer Package No', 'Package No'],
        1: ['Handling Unit', 'Handling Unit'],
        2: ['Length', 'Length'],
        3: ['Pieces', 'Pieces'],
        4: ['Confirmation Net Weight', 'Net Weight'],
        5: ['Gross Weight', 'Gross Weight'],
        6: ['Material.1', 'Material'],
        7: ['Material Description', 'Material Description']
    }
    
    # Convert columns 
    settings: dict[str, set[int]]= {
        'columns_types': {
                'float64': {2,4,5},
                'int32': {3},
                'object': {0,1,6,7}},
        'group_by': {0,2,6,7,1},
        'sum_columns': {3,4,5},
        }


    def _df_columns_name_by_index(self, index_list: set[int]|list[int]) -> list[str]:
        return [self.df_columns[i] for i in index_list]


    @property
    def sap_columns(self) -> list[str]:
        return [k[0] for k in self.columns_settings.values()]

    @property
    def df_columns(self) -> list[str]:
        return [k[1] for k in self.columns_settings.values()]



class FileProccessor(DfConfigMixin):
    def __init__(self):
        self.df = None #pd.DataFrame({column: [None] for column in self.columns.values().keys()})


    @property
    def totals(self) -> dict[str, float|int]:
        if self.df is None:
            raise ValueError('Невалидна таблица!')
        
        totals = dict() 

        for index in self.settings['sum_columns']:
            column_name = self._df_columns_name_by_index([index])[0]

            total = self.df[column_name].sum()
            if isinstance(total, (np.floating, float)):
                totals[column_name] = round(float(total), 3)
            elif isinstance(total, (np.integer, int)):
                totals[column_name] = int(total)
            else:
                totals[column_name] = total

        return totals   


    def load_file(self, file_path: str) -> None:
        self.df = pd.read_excel(file_path)


    def process_file(self):
        current_columns = set(self.df.columns)
        required_columns = set(self.sap_columns)

        if not required_columns.issubset(current_columns):
            missing = required_columns - current_columns
            raise ValueError(f"Липсващи колони: {', '.join(missing)}")

        df = self.df[self.sap_columns].copy()
        df.dropna(inplace=True)

        for new_type, cols in self.settings['columns_types'].items():
            for col in cols:
                    df[self.sap_columns[col]] = df[self.sap_columns[col]].astype(new_type)

                
        renamed_columns = dict(zip(self.sap_columns, self.df_columns))
        df.rename(columns=renamed_columns, inplace=True)

        group_by_columns = self._df_columns_name_by_index(self.settings['group_by'])
        sum_columns = self._df_columns_name_by_index(self.settings['sum_columns'])

        df = df.groupby(group_by_columns)[sum_columns].sum().round(3).reset_index()
        self.df = df.copy()

        return self
    
