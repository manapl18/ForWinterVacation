db = {
        'user' : 'root',
        'password' : 'dyeksdf12',
        'host' : 'localhost',
        'port' : 3306,
        'database' : 'miniter'
}
DB_URL = f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8"
DB = create_engine(DB_URL,encoding='utf-8',max_overflow=0)


