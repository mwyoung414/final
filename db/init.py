from db.UserDbContext import UserDb

async def init_databases(db_url: str):
    """
    Initialize the database connection and create the necessary tables.
    
    Args:
        db_url (str): The database URL for the connection.
    """
    # Create an instance of UserDbContext
    user_db_context = UserDb(db_url)
    
    # Initialize the database
    await user_db_context.init_db()
    
__all__ = ["init_databases", "UserDb"]