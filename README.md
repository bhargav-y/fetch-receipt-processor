# fetch-receipt-processor

## Assumptions
- If a duplicate receipt is attempted to be inserted into the datastore we will return the **id** that already exists. To operate under the assumption that duplicate receipts are possible then we can remove lines 108-111 in `receipt_processor.py`
- When calculating points for purchase time we assume that purchases made at 2:00pm or 4:00pm are valid. This can be easily changed to make the bounds exclusive. 

## Runbook
1. Clone the repository to your local machine
