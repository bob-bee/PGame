To develop a supervisor agent that logs system health, model latency, and resource usage to an SQLite database, you can follow these steps:

1. **Understand Requirements**: Clearly define what information needs to be logged and how often.
2. **Set Up Environment**: Install necessary libraries for interacting with SQLite and retrieving system metrics.
3. **Write the Agent Code**:
   - Use a library like `psutil` to get system resource usage (CPU, memory, disk, network).
   - Use Python's `sqlite3` library to interact with an SQLite database.
4. **Schedule Logging**: Decide on how often you want to log the data (e.g., every minute, every 5 minutes).
5. **Error Handling and Testing**: Add error handling and test the agent thoroughly.

Below is a sample implementation of such a supervisor agent:

### Step-by-Step Implementation

1. **Install Necessary Libraries**:
   You need `psutil` for system metrics and `sqlite3` for interacting with SQLite.
   ```sh
   pip install psutil
   ```

2. **Create the SQLite Database and Table**:
   If you don't already have an SQLite database, create one and a table to store the logs.
   ```sql
   CREATE TABLE IF NOT EXISTS system_logs (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       log_time DATETIME DEFAULT CURRENT_TIMESTAMP,
       cpu_usage REAL,
       memory_usage REAL,
       disk_usage REAL,
       network_usage REAL
   );
   ```

3. **Write the Agent Code**:
   Create a Python script named `supervisor_agent.py`.
   ```python
   import sqlite3
   import psutil
   from datetime import datetime
   import time

   # Database configuration
   DB_PATH = 'system_logs.db'

   def log_system_health():
       # Get system metrics
       cpu_usage = psutil.cpu_percent(interval=1)
       memory_usage = psutil.virtual_memory().percent
       disk_usage = psutil.disk_usage('/').percent
       network_io_counters = psutil.net_io_counters()
       network_usage = (network_io_counters.bytes_sent + network_io_counters.bytes_recv) / 1024 / 1024

       # Connect to SQLite database
       conn = sqlite3.connect(DB_PATH)
       cursor = conn.cursor()

       # Insert data into the table
       query = '''
           INSERT INTO system_logs (cpu_usage, memory_usage, disk_usage, network_usage)
           VALUES (?, ?, ?, ?)
       '''
       cursor.execute(query, (cpu_usage, memory_usage, disk_usage, network_usage))
       conn.commit()
       conn.close()

   def main():
       while True:
           try:
               log_system_health()
           except Exception as e:
               print(f"Error logging system health: {e}")
           time.sleep(60)  # Log every minute

   if __name__ == "__main__":
       main()
   ```

4. **Run the Agent**:
   ```sh
   python supervisor_agent.py
   ```

### Explanation of the Code:

- **Database Connection**: The script connects to an SQLite database specified by `DB_PATH`.
- **Logging Function**: `log_system_health` function retrieves system metrics using `psutil`, formats them, and inserts them into the `system_logs` table.
- **Main Loop**: The `main` function runs in a loop, calling `log_system_health` every minute. It also includes basic error handling to catch and print any exceptions that occur during logging.

### Additional Features:

1. **Logging Model Latency**:
   If you need to log model latency, add a new column to the `system_logs` table for model latency and modify the `log_system_health` function accordingly.
   ```sql
   ALTER TABLE system_logs ADD COLUMN model_latency REAL;
   ```
   Then, update the `log_system_health` function to include the model latency:
   ```python
   def log_system_health():
       # ... (existing code)
       model_latency = fetch_model_latency()  # Add your logic here
       cursor.execute(query, (cpu_usage, memory_usage, disk_usage, network_usage, model_latency))
       conn.commit()
       conn.close()
   ```

2. **Error Handling**:
   Improve error handling by logging errors to a file or sending alerts if the database connection fails.

3. **Configuration Management**:
   Use environment variables or a configuration file to manage settings like the log interval and database path.

This is a basic implementation that you can extend based on your specific requirements.