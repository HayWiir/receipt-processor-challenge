
## Implementation Details and Instructions

From the root directory run the following command to create a docker image:
```
docker build -t receipt-processor . 
```
Then run this command to run the image:
```
docker run -p 80:80 receipt-processor
```
The API will be accessible at `http://127.0.0.1:80`

# Implementation

The implementation consists of 3 parts.

- API
- Database
- Receipt Service

## API
The API layer has the required endpoints.
- `/receipts/process` which accepts a POST request with receipt JSON and returns `receipt_id` for valid inputs.
- `/receipts/{id}/points` which accepts a GET request and returns points if the `id` exists in the DB.

## Database
I used SQLAlchemy library to create an in-memory SQLite DB. The tables **Receipts** and **Items** are defined here based on `api.yml`. There are also some DB specific validation functions.

## Receipt Service
This service is responsible for parsing the input, additional validations, calculating points and storing all the parsed data in the DB.
It also has a getter method for the Get Points API.

## Tests
I used Python's unittest module to write tests. They test multiple validation functions as well as different aspects of the scoring system.

The tests can be run from the root directory with this command:

```
python3 -m unittest tests/test*  
```
