from flask import Flask, request, jsonify
from geopy.distance import geodesic
from datetime import datetime

app = Flask(__name__)

# Global variable to store the geofence data
geofence_data = {
    'latitude_of_center': None,
    'longitude_of_center': None,
    'radius': None
}


def gephync(employee_latitude, employee_longitude):

    if geofence_data['latitude_of_center'] is None or geofence_data['longitude_of_center'] is None or geofence_data['radius'] is None:
        return "Geofence has not been set yet."

    center = (geofence_data['latitude_of_center'], geofence_data['longitude_of_center'])
    radius=geofence_data["radius"]
    # radius = 100  # in meters

    # Employee's current location
    employee_location = (employee_latitude, employee_longitude)

    # Calculate the distance between employee and geofence center
    distance = geodesic(center, employee_location).meters

    # Check if the employee is inside the geofence
    if distance <= radius:
        return "Tourist  is inside the zone"
    else:        
         return "Tourist  is outside the zone"


def geoalerts(employee_latitude, employee_longitude):

    if geofence_data['latitude_of_center'] is None or geofence_data['longitude_of_center'] is None or geofence_data['radius'] is None:
        return "Geofence has not been set yet."

    center = (geofence_data['latitude_of_center'], geofence_data['longitude_of_center'])
    radius=geofence_data["radius"]
    # radius = 100  # in meters

    # Employee's current location
    employee_location = (employee_latitude, employee_longitude)

    # Calculate the distance between employee and geofence center
    distance = geodesic(center, employee_location).meters

    edgeofgeo=abs(radius- distance)

    # Check if the employee is inside the geofence
    
    if edgeofgeo <= 10 :
        return {"status":"red alert" , "msg":"tourist is within 10,meters of the risk zone", "distance_from_center":distance ,"Distance_from_edge": edgeofgeo}
    elif  edgeofgeo <= 25 :
        return {"status":"orange alert" , "msg":"tourist is with in 25 ,meters of the risk zone", "distance_from_center":distance ,"Distance_from_edge": edgeofgeo}
    elif  edgeofgeo <= 50 :
        return {"status":"yellow alert" , "msg":"tourist is with in 50,meters of the risk zone", "distance_from_center":distance ,"Distance_from_edge": edgeofgeo}
    else :
        return {"status":"green zone" , "msg":"tourist is within the safe area","distance_from_center": distance , "distance_from_edge":edgeofgeo}
    
@app.route('/api/set_geofence', methods=['POST'])
def set_geofence():
    data = request.get_json()

    latitude_of_center = data.get('lat')
    longitude_of_center = data.get('lon')
    radius = data.get('radius')

    if latitude_of_center is None or longitude_of_center is None or radius is None:
        return jsonify({"error": "Missing latitude, longitude or radius"}), 400

    geofence_data['latitude_of_center'] = latitude_of_center
    geofence_data['longitude_of_center'] = longitude_of_center
    geofence_data['radius'] = radius

    return jsonify({
        "status": "success",
        "message": f"Geofence set at ({latitude_of_center}, {longitude_of_center}) with radius of {radius} meters."
    }), 200

@app.route('/api/check_location', methods=['POST'])
def check_location():
    data = request.get_json()
    # print(data)

    employee_lat = data.get('tour_lat')
    employee_lon = data.get('tour_lon')
    employee_id=data.get("tour_id")
    # device_info = data.get('topic')
    # timestamp=data.get('tst')

    if not employee_lat or not employee_lon:
        return jsonify({"error": "Missing latitude or longitude for employee"})

    result = gephync(employee_lat, employee_lon)

# # Convert milliseconds to seconds
#     timestamp_s = timestamp / 1000

#     # Convert to a datetime object
#     dt_object = datetime.fromtimestamp(timestamp_s)

#     # Extract date and time
#     date = dt_object.strftime('%Y-%m-%d')  # Extracts date in 'YYYY-MM-DD' format
#     time = dt_object.strftime('%H:%M:%S')  # Extracts time in 'HH:MM:SS' format

#     print(result,device_info,date,time)

    return jsonify({
        "status": "success",
        "message": result,
        "touristId" : employee_id
    }), 200

@app.route('/api/check_alerts', methods=['POST'])
def check_alerts():
    data = request.get_json()
    # print(data)

    employee_lat = data.get('tour_lat')
    employee_lon = data.get('tour_lon')
    employee_id=data.get("tour_id")
    # device_info = data.get('topic')
    # timestamp=data.get('tst')

    if not employee_lat or not employee_lon:
        return jsonify({"error": "Missing latitude or longitude for employee"})

    result = geoalerts(employee_lat, employee_lon)

# Convert milliseconds to seconds
    # timestamp_s = timestamp / 1000

    # # Convert to a datetime object
    # dt_object = datetime.fromtimestamp(timestamp_s)

    # # Extract date and time
    # date = dt_object.strftime('%Y-%m-%d')  # Extracts date in 'YYYY-MM-DD' format
    # time = dt_object.strftime('%H:%M:%S')  # Extracts time in 'HH:MM:SS' format

    return jsonify({
        "status": "success",
        "message": result,
        "touristID": employee_id
    }), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)  # Change host and port as necessary
    