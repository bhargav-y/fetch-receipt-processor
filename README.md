# fetch-receipt-processor

## Assumptions
- If a duplicate receipt is attempted to be inserted into the datastore we will return the **id** that already exists. To operate under the assumption that duplicate receipts are possible then we can remove lines 108-111 in `receipt_processor.py`
- When calculating points for purchase time we assume that purchases made at 2:00pm or 4:00pm are valid. This can be easily changed to make the bounds exclusive. 

## Runbook
This project was developed using Python version `3.9.6`
1. Clone the repository to your local machine using `https://github.com/bhargav-y/fetch-receipt-processor.git`
2. Install `python3` using any installation method (homebrew, python website, etc)
3. `cd` into the repository
4. Create a virtual environment using `python3 -m venv .venv`
5. Activate virtual environment using `.venv/bin/activate`
6. Install requirements using `pip3 install -r requirements.txt`
7. Start Flask application using `flask --app receipt-processor run --debug` (debug flag is optional)
8. Now you can use the API using `curl`!

## Testing
1. To run the unit testing suite run you must be at the root of the project
2. Run `python3 -m unittest tests.test_point_calculation`
