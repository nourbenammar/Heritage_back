from flask import Blueprint, jsonify
from services.coloration_service import ColorationService
import pandas as pd

# Create a Blueprint for objects
coloration_bp = Blueprint('coloration', __name__)

# Instantiate ObjectsService
coloration_service = ColorationService()

@coloration_bp.route('/get-all-data', methods=['GET'])
def get_all_data():
    # Path to the single CSV file
    file_path = "Coloration-dat.csv"  # Adjust this path to point to your specific CSV file
    all_data = coloration_service.retrieve_all_fields_from_csv(file_path)
   
    return jsonify(all_data)
