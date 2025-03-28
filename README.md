# SpaceX Data Pipeline and API 🚀

This project is a data pipeline and API for processing and serving SpaceX-related data. It consists of two main components: an ETL (Extract, Transform, Load) pipeline and a Flask-based REST API.

---

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [ETL Pipeline](#etl-pipeline)
  - [Data Source](#data-source)
  - [ETL Approach](#etl-approach)
  - [Database Schema](#database-schema)
  - [How to Run the ETL Pipeline](#how-to-run-the-etl-pipeline)
- [Flask API](#flask-api)
  - [Endpoints](#endpoints)
  - [How to Run the Flask API](#how-to-run-the-flask-api)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
- [License](#license)

---

## Overview

This project automates the process of fetching, cleaning, transforming, and storing SpaceX data into a PostgreSQL database. It also provides a REST API to query and retrieve processed data.

---

## Features

- **ETL Pipeline**: Fetches data from the SpaceX GraphQL API, cleans and transforms it, and loads it into a database.
- **REST API**: Exposes endpoints to query launch statistics, rocket data, and payload contributions.
- **Database Integration**: Uses PostgreSQL for efficient data storage and querying.
- **Modular Design**: Cleanly separated ETL and API components for maintainability.

---

## ETL Pipeline

The ETL pipeline is responsible for fetching, cleaning, transforming, and loading SpaceX data into a PostgreSQL database.

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

```plaintext
+------------------+       +------------------+       +------------------+
|     Rockets      |       |     Launches     |       |     Payloads     |
+------------------+       +------------------+       +------------------+
| rocket_id (PK)   |<----->| mission_id (PK)  |<----->| payload_id (PK)  |
| name             |       | mission_name     |       | name             |
| type             |       | launch_date_utc  |       | kg               |
| company          |       | launch_year      |       | mission_id (FK)  |
| description      |       | details          |       | rocket_id (FK)   |
| first_flight     |       | rocket_id (FK)   |       +------------------+
| cost_per_launch  |       +------------------+
| diameter_meters  |
| mass_kg          |
| height_meters    |
| success_rate_%   |
| country          |
| active           |
+------------------+
```

### How to Run the ETL Pipeline

The ETL pipeline is executed via the `main.py` script. It performs the following:

1. Creates database tables if they don't exist.
2. Fetches data from the SpaceX API.
3. Cleans and transforms the data.
4. Loads the data into the database.

To run the pipeline:

```bash
python main.py
```

---

## Flask API

The Flask API provides endpoints to query and retrieve processed SpaceX data from the database. It is implemented in [`api/app.py`](api/app.py).

### Endpoints

- **`GET /api/launches/stats`**  
  Returns yearly launch statistics and rocket statistics.  
  Data is fetched using the `fetch_yearly_stats` and `fetch_rocket_stats` functions in [`api/database.py`](api/database.py).

- **`GET /api/metrix`**  
  Returns payload contribution by rocket, launch frequencies, and total launches.  
  Data is fetched using the `fetch_payload_contribution_by_rocket` and `fetch_launch_frequencies` functions in [`api/database.py`](api/database.py).

- **`GET /api/test`**  
  A test endpoint to verify that the API is running successfully.

### How to Run the Flask API

1. Install the required dependencies from `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

2. Start the Flask server:

   ```bash
   python api/app.py
   ```

The API will be available at [http://localhost:5000](http://localhost:5000).  
Use [http://localhost:5000/api/test](http://localhost:5000/api/test) for testing the API setup.

---

## Technologies Used

- **Python**: Core programming language for the ETL pipeline and API.
- **Flask**: Web framework for building the REST API.
- **PostgreSQL**: Database for storing processed SpaceX data.
- **SQLAlchemy**: ORM for database interactions.
- **Pandas**: Data manipulation and transformation.
- **GraphQL**: API for fetching SpaceX data.

---

## Setup Instructions

1. Clone the repository:

   ```bash
   git clone https://github.com/ItsNimmz/SpaceX.git
   cd SpaceX
   ```

2. Create a `.env` file with the following variables:

   ```env
   SPACEX_API_URL=https://spacex-production.up.railway.app/
   DATABASE_URL=postgresql://<user>:<password>@<host>/<database>
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the ETL pipeline:

   ```bash
   python main.py
   ```

5. Start the Flask API:

   ```bash
   python api/app.py
   ```

---
## Potential Improvements

Here are some potential improvements to enhance the project:

1. **Set a Cron Job for the ETL Pipeline**:  
   Automate the ETL pipeline to run at regular intervals using a cron job or a task scheduler like `cron` (Linux) or Task Scheduler (Windows). This ensures the database is always up-to-date with the latest SpaceX data.

2. **Batch Insert for Database Loading**:  
   Optimize the database loading process by implementing batch inserts. This will improve performance when inserting large amounts of data into the database.

3. **Unit Testing**:  
   Add unit tests for the ETL pipeline and API endpoints to ensure code reliability and catch potential bugs early. Use a testing framework like `pytest` for this purpose.

---
## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.