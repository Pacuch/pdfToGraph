from mysql.connector import pooling, Error
from typing import Optional, Tuple, Any, List, Dict, Union


class MySQLDatabase:
    """
    Production-ready MySQL Database handler with connection pooling.

    Example usage:
    ----------------
    from mydb import MySQLDatabase

    # Initialize database connection pool
    db = MySQLDatabase(
        host="localhost",
        port=3306,
        user="root",
        password="my-pw",
        database="mydb"
    )

    # Create a table
    db.insert(
        \"\"\"
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(50),
            email VARCHAR(100) UNIQUE
        )
        \"\"\", ()
    )

    # Insert a record
    db.insert(
        "INSERT INTO users (name, email) VALUES (%s, %s)",
        ("Alice", "alice@example.com")
    )

    # Fetch all records
    users = db.fetch_all("SELECT * FROM users")
    print(users)

    # Fetch one record
    user = db.fetch_one("SELECT * FROM users WHERE email=%s", ("alice@example.com",))
    print(user)
    """

    def __init__(
        self,
        host: str = "localhost",
        port: int = 3306,
        user: str = "root",
        password: str = "",
        database: Optional[str] = None,
        pool_name: str = "pool",
        pool_size: int = 5
    ):
        """
        Initialize a MySQL connection pool.

        :param host: MySQL server hostname
        :param port: MySQL server port
        :param user: Database username
        :param password: Database user password
        :param database: Database name to connect to
        :param pool_name: Name for the connection pool
        :param pool_size: Number of connections in the pool
        """
        try:
            self.pool = pooling.MySQLConnectionPool(
                pool_name=pool_name,
                pool_size=pool_size,
                pool_reset_session=True,
                host=host,
                port=port,
                user=user,
                password=password,
                database=database,
            )
            print(f"[INFO] Connection pool '{pool_name}' created with size {pool_size}")
        except Error as e:
            raise RuntimeError(f"Error creating connection pool: {e}")

    def execute_query(
        self,
        query: str,
        params: Optional[Tuple[Any, ...]] = None,
        fetchone: bool = False,
        fetchall: bool = False,
        commit: bool = False
    ) -> Optional[Union[Dict[str, Any], List[Dict[str, Any]], int]]:
        """
        Execute a SQL query with automatic connection handling.

        :param query: SQL query string
        :param params: Optional tuple of parameters for the SQL query
        :param fetchone: If True, fetch only one result row
        :param fetchall: If True, fetch all result rows
        :param commit: If True, commit transaction (for INSERT/UPDATE/DELETE)
        :return: Query result(s), affected row count, or None
        """
        conn, cursor = None, None
        try:
            conn = self.pool.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params or ())

            if commit:
                conn.commit()
                return cursor.rowcount

            if fetchone:
                return cursor.fetchone()
            if fetchall:
                return cursor.fetchall()

        except Error as e:
            print(f"[ERROR] MySQL error: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def insert(self, query: str, params: Tuple[Any, ...]) -> int:
        """
        Execute an INSERT/UPDATE/DELETE query.

        :param query: SQL query string
        :param params: Tuple of parameters for the SQL query
        :return: Number of affected rows
        """
        return self.execute_query(query, params, commit=True)  # type: ignore

    def fetch_one(self, query: str, params: Optional[Tuple[Any, ...]] = None) -> Optional[Dict[str, Any]]:
        """
        Fetch a single row from the database.

        :param query: SQL SELECT query string
        :param params: Optional tuple of parameters
        :return: Dictionary representing a single row, or None
        """
        return self.execute_query(query, params, fetchone=True)  # type: ignore

    def fetch_all(self, query: str, params: Optional[Tuple[Any, ...]] = None) -> List[Dict[str, Any]]:
        """
        Fetch all rows from the database.

        :param query: SQL SELECT query string
        :param params: Optional tuple of parameters
        :return: List of dictionaries representing rows, or empty list
        """
        result = self.execute_query(query, params, fetchall=True)
        return result if isinstance(result, list) else []
