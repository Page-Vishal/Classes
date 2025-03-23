# SQLConnection

## Overview
`SQLConnection` is a Python class that simplifies database connectivity and querying using PostgreSQL. It utilizes `configparser`, `sqlalchemy`, and `tabulate` to handle database connections, execute SQL queries, and display results in a readable format.

## Features
- Establishes a connection to a PostgreSQL database using configurations from a `.ini` file.
- Executes SQL queries and fetches results.
- Displays query results in tabular or formatted output.
- Uses `tabulate` for enhanced readability of tabular results.

## Installation
Ensure you have the required dependencies installed:
```sh
pip install sqlalchemy tabulate psycopg2 configparser
```

## Configuration
The database connection details should be stored in a `config.ini` file:

```ini
[pgsql]
hostname = localhost
database = db_phone
username = postgres
password = yourpassword
port = 5432
```

## Usage
### 1. Initialize the Connection
```python
from sql_connection import SQLConnection

conn = SQLConnection()
```

### 2. Running Queries
```python
query = "SELECT brand, model FROM tbl_phones WHERE price < 500 LIMIT 5;"
results = conn.run_query(query)
```

### 3. Displaying Results
#### Formatted Output:
```python
conn.display_results(results)
```
#### Tabular Output:
```python
conn.display_table(query)
```

## Class Methods
### `__init__(config_file='config.ini')`
- Initializes the SQL connection and loads database configurations.

### `config`
- Property that loads and caches database configuration from the provided `.ini` file.

### `_load_config()`
- Reads and parses the database configuration file.

### `_connect()`
- Establishes a connection to the PostgreSQL database using SQLAlchemy.

### `run_query(query)`
- Executes the provided SQL query and returns results as a list of dictionaries.

### `display_results(results)`
- Prints query results in a formatted key-value format.

### `display_table(query)`
- Displays the query results in a table format using `tabulate`.

### `row_format(rows)`
- Prints the raw output type and structure for debugging.

## Error Handling
- If the configuration file is missing or incorrect, an appropriate exception is raised.
- If the database connection fails, an error message is displayed.
- If the SQL query fails, an exception message is shown.

## License
This project is open-source and available under the MIT License.

