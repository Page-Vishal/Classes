import configparser
from sqlalchemy import create_engine, text
from tabulate import tabulate

class SQLConnection:
    """Handles SQL connection and querying.
        Needs configparser, sqlalchemy and tabulate \n
    Example:
        query = "select brand,model from tbl_phones where price < 500 Limit 5;" \n
        conn = SQLConnection() \n
        result = conn.run_query(query) \n
        conn.display_results(result) \n
    
    If you want the result in a tabular format: `pip install tabulate` and run: \n
        conn.display_table(query)

    The database connection is handled by the config property. While loading the
    database, the configurations is to be inside config.ini file or specify the config file in the format: \n
        [pgsql] \n
        hostname = localhost \n
        database = db_phone \n
        username = postgres \n
        password = sigdel \n
        port = 8080 \n
    
    Check how the results are being returned with row_format(rows) \n
        conn.row_format(result)
    """

    def __init__(self, config_file='config.ini'):
        """initailize with a config file, configuration storing variable, and a database variable."""
        self.config_file = config_file
        self._config = None
        _ = self.config
        self.db = self._connect()

    @property
    def config(self):
        """Loads and caches database configuration."""
        if self._config is None:
            self._config = self._load_config()
        return self._config
    
    def _load_config(self):
        """Reads database configuration from the config file."""
        config = configparser.ConfigParser()
        
        if not config.read(self.config_file):  # Check if file exists
            raise FileNotFoundError(f"Config file '{self.config_file}' not found.")

        try:
            db_config = {
                'hostname': config['pgsql']['hostname'],
                'database': config['pgsql']['database'],
                'username': config['pgsql']['username'],
                'password': config['pgsql']['password'],
                'port': int(config['pgsql']['port'])  # Ensure port is an integer
            }
            return db_config
        except KeyError as e:
            raise KeyError(f"Missing required database config key: {e}")
        
    def _connect(self):
        """Connects to the database as config provided in config.ini file"""
        try:
            cfg = self._config
            url= f"postgresql://{cfg['username']}:{cfg['password']}@{cfg['hostname']}:{cfg['port']}/{cfg['database']}"
            engine = create_engine(url)
            return engine.connect()
            # return SQLDatabase.from_uri(url)
        except Exception as e:
            print(f"Error loading config: {e}")

    def run_query(self,query):
        """Executes an SQL query and returns results."""
        if not self.db :
            print("Database not connected...")
            return None
        try:
            print(f"Executing query: {query}")
            result =  self.db.execute(text(query))
            rows = [dict(zip(result.keys(), row)) for row in result]

            if not rows:
                print("Query returned no results.")  # Debugging: no results found

            return rows
        except Exception as e:
            print(f"Query Execution Failed: {e}")
            return None

    def display_results(self, results):
        """Display results in a readable format."""
        # results = self.run_query(query)
        if not results:
            print("No results found.")
            return

        # Print results in a more readable format (as dictionaries)
        print("\n")
        print("Query Results:")
        for row in results:
            formatted_row = ",  ".join([f"{key}: {value}" for key, value in row.items()])
            print(formatted_row)

    def display_table(self,query):
        """Display the result in tabular form after passing in query"""
        if not query:
            print("No queries found.")
            return
        result =  self.db.execute(text(query))
        # Get the column headers from the first row of the dictionary
        headers = result.keys()

        table = tabulate(result, headers=headers, tablefmt="grid")
        print(table)
    
    def row_format(self,rows):
        """Shows teh format at which the data is being printed out."""
        if not rows:
            print("No results found.")
            return
        print(type(rows))
        print("\n")
        print("Result: ",rows)
        print("\n")
        print("Each row: ")
        for row in rows:
            print(row)