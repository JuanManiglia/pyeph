import os
import pandas as pd

MODULE_PATH = os.getcwd()

class EPHLabels:

    FILES_DIR = "pyeph/.files"


    @classmethod
    def get_df(cls):
        pathfile = os.path.join(MODULE_PATH, cls.FILES_DIR, 'EPH_tot_urbano_estructura_bases.xlsx')
        df = pd.read_excel(pathfile, sheet_name = 'BASE PERSONAS', skiprows=6).dropna(axis=0, how='all')
        df = df.fillna(method='ffill')
        df['CAMPO'] = df['CAMPO'].str.strip()
        df['DESCRIPCIÓN'] = df['DESCRIPCIÓN'].str.replace(r'([0-9]\.)', '=', regex=True)
        df[['CODIGO', 'DESCRIPCIÓN']] = df['DESCRIPCIÓN'].str.split("=",expand=True,)
        return df

    @classmethod
    def vars_labels(cls):
        labels = cls.get_df()
        labels = labels[labels['DESCRIPCIÓN'].isna()][['CAMPO', 'CODIGO']].rename(columns = {'CODIGO': 'DESCRIPCION'})
        return labels

    @classmethod
    def map_labels(cls, df):
        #Obtenemos las columnas relevantes para etiquetar
        df = df.reset_index()
        cols = [c for c in df.columns]

        # Obtenemos dataframe de labels
        labels = cls.get_df()
        labels = labels[labels['DESCRIPCIÓN'].notna()]
        labels['DESCRIPCIÓN'] = labels['DESCRIPCIÓN'].astype(str)
        labels = labels[labels['CAMPO'].isin(cols)]
        
        
        variables = labels['CAMPO'].unique()

        for i in variables:            
            # Obtener la serie que mapea para cada variable
            df_i = labels[labels['CAMPO'] == i].rename(columns = {'CODIGO': f'{i}', 'DESCRIPCIÓN': f'DESCRIPCIÓN_{i}'}).reset_index()
            df_i[i] = df_i[i].str.strip()
            df_i = df_i.drop(columns = {'CAMPO', 'TIPO (longitud)', 'index'}).set_index(i).rename(columns = {f'DESCRIPCIÓN_{i}': i})
            dict_i = df_i.to_dict().get(i)

            df[i] = df[i].astype(str).str.strip()
            df[i] = df[i].map(dict_i)

        
        # Renombrar columnas con su etiqueta
        var_names = cls.vars_labels()
        var_names = var_names[var_names['CAMPO'].isin(cols)]
        var_names_dict = var_names.set_index('CAMPO').to_dict().get('DESCRIPCION')

        return df.rename(columns = var_names_dict)



vars_labels = EPHLabels.vars_labels
map_labels = EPHLabels.map_labels
# Traduccion
etiquetas_vars = vars_labels
etiquetar = map_labels