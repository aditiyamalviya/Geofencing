from geopy.distance import geodesic

# Define geofence center and radius (in meters)

def gephync(employee_latitude, employee_longitude,latitude_of_center,longitude_of_center,radius):
    center = (latitude_of_center, longitude_of_center)
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
    elif distance <= radius:
        print("Tourist  is inside the zone")
    else:        
        print("Tourist  is outside the zone")


if __name__=="__main__":
    location_lat=22.9487162 #yha pr jis jgh ka fence banana hai uska latitude dalega
    location_lon=76.0129413 #yha pr jis jgh ka fence banana hai uska lognitude dalega
    person_lat=22.9487162 #yha pr jis bhi insan ka geofensing chek kerna h k voo ander hai k bhar uska latude
    person_lon=76.0129413 #yha pr jis bhi insan ka geofensing chek kerna h k voo ander hai k bhar uska lotitude
    area=10 #area of geofencing yha pr jis bhi location ka area dalna hai uska radius dalna hai meter m
    gephync(employee_latitude=person_lat,employee_longitude=person_lon,latitude_of_center=location_lat,longitude_of_center=location_lon,radius=area)

