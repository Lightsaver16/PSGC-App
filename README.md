# PSGC APP
This is a FastAPI app that provides basic CRUD functionality for regions and provinces of the Philippines.

## Models Overview
### 1. Region
- Represent regions in the Philippines
Fields:
- `id` - Unique identifier of each region / Integer / Auto-incrementing
- `name` - Name of the region / String / Unique
- `date_created` - Timestamp to when the record of region was created.
- `date_updated` - Timestamp to when the record of region was modified.


### 2. Province
- Represent provinces in the Philippines
Fields:
- `id` - Unique identifier of each province / Integer / Auto-incrementing
- `name` - Name of the region / String / Unique for each region
- `region_id` - Foreign key id of region to which the province belongs to.
- `date_created` - Timestamp to when the record of region was created.
- `date_updated` - Timestamp to when the record of region was modified.

## Project structure
```
├── app
│   ├── db
│   │   ├── core.py # For database-related settings
│   ├── provinces
│   │   ├── models.py
│   │   ├── router.py
│   │   ├── schema.py
│   │   ├── service.py
│   └── regions
│   │   ├── models.py
│   │   ├── router.py
│   │   ├── schema.py
│   │   ├── service.py
│   └── static
│   │   ├── styles.css # styles just for the homepage/root directory (e.g. http://localhost:8000/)
│   └── templates
│   │   ├── home.html # index html just for the homepage/root directory (e.g. http://localhost:8000/)
│   ├── __init__.py
│   ├── auth.py  
│   ├── exception.py  # global exceptions
│   ├── main.py 
│   ├── models.py  # global models
│   └── pagination.py # settings for pagination
├── .dockerignore
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
```
1. Project main setup
   - `app` -> directory contains that contains the whole implementation of app including models, routers, schema, etc.
   - `main.py`-> entrypoint which initializes the FastAPI app
2. The two models have their own packages / directories with that contains the following file:
   - `models.py` -> contains Database models
   - `router.py` -> contains actual API endpoints for the resources
   - `schema.py` -> pydantic validation for serialization/deserialization
   - `service.py` -> contains validations or business logic
  
## Setting up the app
The project lives in a docker container. Alongside with it is a docker container that contains a Postgresql instance.
### Pre-requisites:
1. Clone the project
```
git clone https://github.com/Lightsaver16/PSGC-App.git
```
2. Make an `.env` file with the following content and replace the values inside the angle brackets:
```
POSTGRES_USER=<your username>
POSTGRES_PASSWORD=<username password>
POSTGRES_DB=<db name>
POSTGRES_HOST=<db host>
POSTGRES_PORT=<db port>
API_KEY_NAME=<API KEY HEADER>
API_KEY=<API KEY>
```
### Running the containers
To run the the FastAPI app container and the Postgresql instance container:
```
docker-compose up --build -d
```
### Postman API Documentation
To view the postman API Documentation, kindly visit this [link.](https://tinyurl.com/3h9z7fu7)
