from flask import Blueprint, jsonify
from services.objects_service import ObjectsService
import pandas as pd

# Create a Blueprint for objects
objects_bp = Blueprint('objects', __name__)

# Instantiate ObjectsService
objects_service = ObjectsService()

@objects_bp.route('/get-all-data', methods=['GET'])
def get_all_data():
    # Path to the single CSV file
    file_path = "objects_data.csv"  # Adjust this path to point to your specific CSV file
    all_data = objects_service.retrieve_all_fields_from_csv(file_path)
   
    return jsonify(all_data)
