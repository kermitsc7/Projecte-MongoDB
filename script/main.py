import pandas as pd
from pymongo import MongoClient

csv_path = 'Dades.xlsx'
db_name = 'Lliurament'

# Leer el archivo XLSX
xl_file = pd.read_excel( 'Dades.xlsx', sheet_name=None)

# Conectarse a la base de datos MongoDB

client = MongoClient('mongodb://dcccluster.uab.cat:8227/')

# Creamos Base de Datos
db = client[db_name]

# Crear una colección por cada pestaña
for sheet_name, df in xl_file.items():

    if sheet_name == 'Colleccions-Publicacions':
    
        collectionC = db['Colleccions']
        collectionP = db['Publicacions']
        collectionE = db['Editorial']
        df = xl_file[sheet_name]
        
        dfC = df[['NomColleccio', 'total_exemplars','genere','idioma','any_inici','any_fi','tancada','NomEditorial']]
        dfC.genere = dfC.genere.apply(lambda x: x[1:-1].split(', '))
        dataC = dfC.to_dict('records')
        
        dfP = df[['ISBN','titol','stock','autor','preu','num_pagines','guionistes','dibuixants','NomColleccio']]
        dfP.guionistes = dfP.guionistes.apply(lambda x: x[1:-1].split(', '))
        dfP.dibuixants = dfP.dibuixants.apply(lambda x: x[1:-1].split(', '))
        dataP = dfP.to_dict('records')
        
        dataE = df[['NomEditorial','resposable','adreca','pais']].to_dict('records')
        collectionC.insert_many(dataC)
        collectionP.insert_many(dataP)
        collectionE.insert_many(dataE)
    else:
        # Obtener el nombre de la colección
        collection_name = sheet_name
        # Insertar los datos en la colección
        collection = db[collection_name]
        data = df.to_dict('records')
        collection.insert_many(data)


 # Contar el número de colecciones creadas
num_collections = len(db.list_collection_names())

# Imprimir el número de colecciones creadas
print(f'Se crearon {num_collections} colecciones en la base de datos.')

