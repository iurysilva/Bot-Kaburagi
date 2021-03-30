import pymongo

def pega_conexao() -> pymongo.MongoClient :

    return pymongo.MongoClient("mongodb://localhost:27017/")