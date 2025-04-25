from db.UserDbContext import UserDb
from db.CommonDataDbContext import *

async def init_databases(*db_urls): 
    """
    Initialize the database connection and create the necessary tables.
    
    Args:
        db_url (str): The database URL for the connection.
    """
    # Create an instance of UserDbContext
    user_db_context = UserDb(db_urls[0])
    common_db_context = CommonDataDb(db_urls[1])
    
    # Initialize the database
    await user_db_context.init_db()
    await common_db_context.init_db()
    
__all__ = ["init_databases", "UserDb", "CommonDataDb"]