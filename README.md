# Alerts Service

This service provides functionality to configure financial alerts for a banks customers (also known as Borrowers).

Banks who make commercial loans use systems like this to monitor their loan portfolios and detect issues with their borrower's reported financial statements. An example alert could be: DSCR (debt service coverage ratio) is above 1.25.

## Usage

Install the dependencies. Requires Python 3.11 or above.

`poetry install`

Run the tests

`make test`

Format the code

`make format`

Build the docker image

`make build`

Run service locally in Docker. NB Docker must be running. The code is mounted in the container, and auto-reload is enabled, so code changed will cause the service to restart.

`make run`

When the service is running you can visit http://localhost:8000/docs to view the API schema. This page also allows you to try out some requests.

## Code Organisation

All code is in `alerts_service` directory except tests which are in `tests`. Within `alerts_service`, the most important modules in order are:

- `rest.py`: The handlers for the API endpoints
- `models.py`: SQLAlchemy database models
- `types.py`: Pydantic models representing the API schema
- `app.py`: Where the FastAPI application is created