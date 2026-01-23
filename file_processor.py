import pandas as pd
import numpy as np

class DfConfigMixin:
        # INDEX : [SAP Export, DataFrame]

    settings_columns = [{'export_name': 'Customer Package No', 'column_name': 'Package No', 
                   'column_type': 'str', 'group_by': True, 'sum_columns': False, 'col_width': 30}, 

                  {'export_name': 'Handling Unit', 'column_name': 'Handling Unit', 
                   'column_type': 'str', 'group_by': True, 'sum_columns': False, 'col_width': 30},

                  {'export_name': 'Length', 'column_name': 'Length', 
                   'column_type': 'float64', 'group_by': True, 'sum_columns': False, 'col_width': 20},
                   
                  {'export_name': 'Pieces', 'column_name': 'Pieces', 
                   'column_type': 'int32', 'group_by': False, 'sum_columns': True, 'col_width': 35},

                  {'export_name': 'Confirmation Net Weight', 'column_name': 'Net, kg', 
                   'column_type': 'float64', 'group_by': False, 'sum_columns': True, 'col_width': 80},

                  {'export_name': 'Gross Weight', 'column_name': 'Gross, kg', 
                   'column_type': 'float64', 'group_by': False, 'sum_columns': True, 'col_width': 25},

                  {'export_name': 'Material.1', 'column_name': 'Material', 
                   'column_type': 'str', 'group_by': True, 'sum_columns': False, 'col_width': 25},

                  {'export_name': 'Material Description', 'column_name': 'Component-Material Description', 
                   'column_type': 'str', 'group_by': True, 'sum_columns': False, 'col_width': 25},]
    
    settings_company = {'city': 'Company City',
                        'company_name': 'Company Name',
                        'address': 'Company Addres'}

    @property
    def _groupby_columns(self):
        return [c['column_name'] for c in self.settings_columns if c['group_by']]


    @property
    def _sum_columns(self):
        return [c['column_name'] for c in self.settings_columns if c['sum_columns']]

    @property
    def sap_columns(self) -> list[str]:
        return [c['export_name'] for c in self.settings_columns]

    @property
    def df_columns(self) -> list[str]:
        return [c['column_name'] for c in self.settings_columns]

    @property
    def _column_widths(self):
        return [c['col_width'] for c in self.settings_columns]



class FileProccessor(DfConfigMixin):
    def __init__(self):
        self._df = None #pd.DataFrame({column: [None] for column in self.columns.values().keys()})
        self._totals = dict()


    @property
    def df(self) -> pd.DataFrame:
        if self._df is None:
            raise ValueError('Невалидна таблица!')
        return self._df

    @property
    def totals(self) -> dict[str, float|int]:
        if self._df is None:
            raise ValueError('Невалидна таблица!')

        for column_name in self._sum_columns:
            total = self._df[column_name].sum()

            if isinstance(total, (np.floating, float)):
                self._totals[column_name] = round(float(total), 3)    
            elif isinstance(total, (np.integer, int)):
                self._totals[column_name] = int(total)
            else:
                self._totals[column_name] = total

        return self._totals
     


    def process_file(self) -> None:
        current_columns = set(self._df.columns)
        required_columns = set(self.sap_columns)

        if not required_columns.issubset(current_columns):
            missing = required_columns - current_columns
            raise ValueError(f"Липсващи колони: {', '.join(missing)}")

        df = self._df[self.sap_columns].copy()
        df.dropna(inplace=True)

        for c in self.settings_columns:
            df[c['export_name']] = df[c['export_name']].astype(c['column_type'])

    
        renamed_columns = dict(zip(self.sap_columns, self.df_columns))
        df.rename(columns=renamed_columns, inplace=True)


        df = df.groupby(self._groupby_columns)[self._sum_columns].sum().round(3).reset_index()
        self._df = df.copy()

        return self

        


    def load_file(self, file_path: str) -> None:
        self._df = pd.read_excel(file_path)
    
