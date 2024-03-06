from JPyDB import pyDatabase, Tables, Columns

pyd = pyDatabase('data/database','pydata')
db = pyd.db()

def CreateTables():
    db.create_table('config',[('data',dict)])
    db.create_table('saves',[('data',dict)])
    db.save()

if __name__ == '__main__':
    # Code for test
    pass