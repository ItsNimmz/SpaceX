# SpaceX Data Pipeline and API

This project is a data pipeline and API for processing and serving SpaceX-related data. It consists of two main components: an ETL (Extract, Transform, Load) pipeline and a Flask-based REST API.

---

## ETL Pipeline

The ETL pipeline is responsible for fetching, cleaning, transforming, and loading SpaceX data into a PostgreSQL database. Below is a detailed explanation of the ETL process:

### Data Source
- The data is fetched from the **SpaceX GraphQL API** available at:  
  [https://api.spacex.land/graphql/](https://api.spacex.land/graphql/)

### ETL Approach

1. **Extract**:
   - Data is retrieved from the SpaceX GraphQL API using the `fetch_graphql_data` function in [`data_processing/extract.py`](data_processing/extract.py).
   - The extraction process uses batched queries to handle large datasets efficiently.
   - Example data fetched includes information about rockets, launches, and payloads.

2. **Transform**:
   - Data is cleaned and transformed using functions in [`data_processing/data_transformer.py`](data_processing/data_transformer.py).
   - Key transformations include:
     - **Normalization**: Rocket and launch data are normalized into separate entities to reduce redundancy.
     - **Flattening**: Nested fields (e.g., payload details within launches) are flattened for easier database storage.
     - **Data Cleaning**: Missing or inconsistent fields are handled to ensure data integrity.

3. **Load**:
   - Transformed data is inserted into a PostgreSQL database using functions in [`data_processing/database.py`](data_processing/database.py).
   - The database schema is designed to efficiently store and query SpaceX data.

### Database Schema

The database schema consists of the following tables:

- **Rockets**: Stores information about rockets, such as name, type, and active status.
- **Launches**: Stores details about launches, including date, success status, and associated rocket.
- **Payloads**: Stores payload details, such as type, weight, and orbit.

Below is a diagram of the database schema:

```plaintext
+------------------+       +------------------+       +------------------+
|     Rockets      |       |     Launches     |       |     Payloads     |
+------------------+       +------------------+       +------------------+
| rocket_id (PK)   |<----->| launch_id (PK)   |<----->| payload_id (PK)  |
| name             |       | rocket_id (FK)   |       | launch_id (FK)   |
| type             |       | date             |       | type             |
| active           |       | success          |       | weight           |
+------------------+       +------------------+       | orbit            |
                                                    +------------------+



# How to Run the ETL Pipeline

The ETL pipeline is executed via the `main.py` script. It performs the following:

1. Creates database tables if they don't exist.
2. Fetches data from the SpaceX API.
3. Cleans and transforms the data.
4. Loads the data into the database.



## To run the pipeline:

```bash
python [main.py](http://_vscodecontentref_/0)


# Flask API

The Flask API provides endpoints to query and retrieve processed SpaceX data from the database. It is implemented in `api/app.py` and exposes the following endpoints:

## Endpoints

### `GET /api/launches/stats`

Returns yearly launch statistics and rocket statistics.  
Data is fetched using the `fetch_yearly_stats` and `fetch_rocket_stats` functions in `api/database.py`.

### `GET /api/metrix`

Returns payload contribution by rocket, launch frequencies, and total launches.  
Data is fetched using the `fetch_payload_contribution_by_rocket` and `fetch_launch_frequencies` functions in `api/database.py`.

### `GET /api/test`

A test endpoint to verify that the API is running successfully.


# How to Run the Flask API

1. Install the required dependencies from `requirements.txt`:

   ```bash
   pip install -r requirements.txt

2. Start the Flask server:

   ```bash
   python api/app.py

The API will be available at [http://localhost:5000](http://localhost:5000).

Use [http://localhost:5000/api/test](http://localhost:5000/api/test) for testing the API setup.


