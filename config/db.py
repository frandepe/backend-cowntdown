#C:\Users\jeroa\Desktop\JeroAlderete\3 - CowntDown Project\backend-cowntdown-main\config\db.py

from supabase import create_client, Client
import os
from dotenv import load_dotenv

# load enviroment variables from .env file
load_dotenv()

SUPABASE_URL= os.getenv('SUPABASE_URL')
SUPABASE_KEY= os.getenv('SUPABASE_KEY')
SUPABASE_BUCKET= os.getenv('SUPABASE_BUCKET')

if not all([SUPABASE_URL,SUPABASE_URL,SUPABASE_BUCKET]):
    raise EnvironmentError("una o mas Variables de Supabase estan faltando")

# Initialize Supabase Client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# import bcrypt

# -----  CRUD OPERATIONS ------ #

# insert a new row into table
# new_row= {'username': 'asd'}
# supabase.table('users').insert(new_row).execute()

# #update row in a table
# new_row= {'username': 'asd updated'}
# supabase.table('users').update(new_row).eq('id',2).execute()

# plain_password = "asdasd123"
# hashed = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt())
# hashed_password = hashed.decode('utf-8')  # Esto es un string legible para guardar
# print(hashed_password)

# data = {
#     "email": "asd@asd.com",
#     "username": "asd",
#     "password": hashed_password
# }

# response = supabase.table("users").insert(data).execute()
# print(response)

# delete a record
# supabase.table('users').delete().eq('id',6).execute()


# -----  SUPABASE STORAGE BUCKET------ #

# response = supabase.storage.from_('demo-bucket').get_public_url('farmer.png')
# print(response) # ejecutamos con python config/db.py y nos devuelve la url


# -----  FETCH ALL RECORDS ------ # 

# results = supabase.table('demo-table').select('*').execute()
# print(results)

