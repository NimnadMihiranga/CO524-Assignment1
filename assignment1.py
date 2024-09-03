from flask import Flask, jsonify, request

app = Flask(__name__)

registrations = [
    {"registration_no": "E/18/180", "vehicle_number": "ABC1234", "owner_name": "Nimnad Mihiranga", "vehicle_type": "Car"},
    {"registration_no": "E/18/266", "vehicle_number": "XYZ5678", "owner_name": "Nisala Induwara", "vehicle_type": "Motorbike"},
]

# GET all registrations
@app.route('/registrations', methods=['GET'])
def get_registrations():
    return jsonify(registrations), 200

# GET a single registration
@app.route('/registration', methods=['GET'])
def get_registration_by_query():
    registration_no = request.args.get('registration_no')
    if registration_no:
        registration = next((reg for reg in registrations if reg["registration_no"] == registration_no), None)
        if registration:
            return jsonify(registration), 200
        return jsonify({"error": "Registration not found"}), 404
    return jsonify({"error": "No registration_no provided"}), 400

# POST a new registration
@app.route('/add-registration', methods=['POST'])
def create_registration():
    registration_no = request.args.get('registration_no')
    vehicle_number = request.args.get('vehicle_number')
    owner_name = request.args.get('owner_name')
    vehicle_type = request.args.get('vehicle_type')

    # Check if all required query parameters are provided
    if not all([registration_no, vehicle_number, owner_name, vehicle_type]):
        return jsonify({"error": "All fields are required: registration_no, vehicle_number, owner_name, vehicle_type"}), 400

    # Check if the registration number already exists
    if any(reg['registration_no'] == registration_no for reg in registrations):
        return jsonify({"error": "Registration number already exists"}), 400

    # Create new registration
    new_registration = {
        "registration_no": registration_no,
        "vehicle_number": vehicle_number,
        "owner_name": owner_name,
        "vehicle_type": vehicle_type
    }

    registrations.append(new_registration)
    return jsonify(new_registration), 201

# Update a registration
@app.route('/update-registration', methods=['PUT'])
def update_registration():
    registration_no = request.args.get('registration_no')

    if not registration_no:
        return jsonify({"error": "No registration_no provided"}), 400

    registration = next((reg for reg in registrations if reg["registration_no"] == registration_no), None)
    if registration is None:
        return jsonify({"error": "Registration not found"}), 404

    # Get the current values or use the provided values if they exist
    vehicle_number = request.args.get('vehicle_number', registration['vehicle_number'])
    owner_name = request.args.get('owner_name', registration['owner_name'])
    vehicle_type = request.args.get('vehicle_type', registration['vehicle_type'])

    # Update the registration with the new values or the existing ones if no new values were provided
    registration['vehicle_number'] = vehicle_number
    registration['owner_name'] = owner_name
    registration['vehicle_type'] = vehicle_type

    return jsonify(registration), 200

# DELETE a registration
@app.route('/delete-registration', methods=['DELETE'])
def delete_registration():
    registration_no = request.args.get('registration_no')
    if not registration_no:
        return jsonify({"error": "No registration_no provided"}), 400

    registration = next((reg for reg in registrations if reg["registration_no"] == registration_no), None)
    if registration is None:
        return jsonify({"error": "Registration not found"}), 404

    registrations.remove(registration)
    return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
