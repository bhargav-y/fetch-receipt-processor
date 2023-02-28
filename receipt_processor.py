import datetime
import math
from typing import Any, Dict, List, Optional
import uuid

from flask import Flask
from flask import request, jsonify


app = Flask(__name__)

IN_MEMORY_DATASTORE = {}

'''
This function will prevent duplicate receipts from being inserted into the datastore

If we operate under the assumption that duplicate receipts are allowed:
"Two or more customers make the exact same purcahse at the same time from the same retailer..."
then we can remove this check from process_receipts and just have IN_MEMORY_DATASTORE[id] = data stand alone
'''
def get_key(data: Dict[str, Optional[Any]]) -> str:
    for k, v in IN_MEMORY_DATASTORE.items():
        if v == data:
            return k

# Using inclusive time range; can easily be changed to exclusive
def time_in_range(x, start=datetime.time(14, 0, 0), end=datetime.time(16, 0, 0)):
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end

def compute_item_description_points(items: List[str]) -> int:
    item_description_points = 0

    for item in items:
        shortDescription = item['shortDescription'].strip()
        price = float(item['price'])

        if len(shortDescription) % 3 == 0:
            item_description_points += int(math.ceil(price * 0.2))
    
    return item_description_points

def compute_purchase_time_points(purchase_time: str) -> int:
    purchase_time_points = 0

    start = datetime.time(14, 0)
    end = datetime.time(16, 0)
    purchase_time_components = purchase_time.split(':')
    hour = int(purchase_time_components[0])
    minute = int(purchase_time_components[1])

    if time_in_range(datetime.time(hour, minute), start, end):
        purchase_time_points += 10

    return purchase_time_points


def compute_points(retailer: str, 
                   total: str, 
                   purchase_date: str, 
                   purchase_time: str, 
                   items: List[str]) -> int:
    points = 0
    num_items = len(items)
    
    numbers = sum(c.isdigit() for c in retailer)
    letters = sum(c.isalpha() for c in retailer)
    num_alphanumeric = numbers + letters

    # Alphanumeric characters
    points += num_alphanumeric
    # Pairs of items 
    points += ((num_items // 2) * 5)
    
    # Ends with no cents
    if total.endswith('.00'):
        points += 50
    
    # Multiple of 0.25
    if (float(total) % 0.25) == 0:
        points += 25

    # Trimmed length of item description is multiple of 3
    item_description_points = compute_item_description_points(items)
    points += item_description_points

    # Odd day
    purchase_date_components = purchase_date.split('-')
    day = purchase_date_components[2]
    if int(day) % 2 == 1:
        points += 6
    
    # Purchase time within 2:00pm-4:00pm
    purchase_time_points = compute_purchase_time_points(purchase_time)
    points += purchase_time_points

    return points
 
@app.route('/receipts/process', methods=['POST'])
def process_receipts():
    data = request.get_json()
    
    unique_id = uuid.uuid4()
    id = str(unique_id)

    # Handle duplicate receipts
    if data in IN_MEMORY_DATASTORE.values():
        id = get_key(data)
    else:
        IN_MEMORY_DATASTORE[id] = data

    return jsonify({
        "id": id
    })

@app.route('/receipts/<string:id>/points', methods=['GET'])
def get_points(id: str):
    if id not in IN_MEMORY_DATASTORE:
        return jsonify({})
    
    data = IN_MEMORY_DATASTORE[id]

    retailer = data.get('retailer')
    total = data.get('total')
    items = data.get('items')
    purchase_date = data.get('purchaseDate')
    purchase_time = data.get('purchaseTime')

    points = compute_points(retailer, total, purchase_date, purchase_time, items)

    return jsonify({
        "points": points
    })
