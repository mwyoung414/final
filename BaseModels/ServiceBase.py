import asyncmy
from asyncmy.cursors import DictCursor

class ServiceBase:
    def __init__(self, host: str, port: int, user: str, password: str, database: str):
        self._db_config = {
            "host": host,
            "port": port,
            "user": user,
            "password": password,
            "database": database,
        }
        self._connection = None

    async def connect(self):
        """Establish a connection to the MySQL database."""
        if not self._connection:
            self._connection = await asyncmy.connect(**self._db_config)

    async def disconnect(self):
        """Close the connection to the MySQL database."""
        if self._connection:
            await self._connection.close()
            self._connection = None

    async def execute_query(self, query: str, params: tuple = None):
        """Execute a query and return the result."""
        if not self._connection:
            raise RuntimeError("Database connection is not established.")
        async with self._connection.cursor(DictCursor) as cursor:
            await cursor.execute(query, params or ())
            return await cursor.fetchall()

    async def execute_non_query(self, query: str, params: tuple = None):
        """Execute a query that does not return results (e.g., INSERT, UPDATE, DELETE)."""
        if not self._connection:
            raise RuntimeError("Database connection is not established.")
        async with self._connection.cursor() as cursor:
            await cursor.execute(query, params or ())
            await self._connection.commit()