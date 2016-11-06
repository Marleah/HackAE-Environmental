from flask import Flask, render_template, request
import geopy
from geopy.geocoders import Nominatim
from math import radians, cos, sin, asin, sqrt
import twilio
from twilio.rest import TwilioRestClient


app = Flask(__name__)


dictOfCoordinates = {'Casey': ((40.77498495, -73.9859719946164), "+13473224975"),\
                     'Marleah': ((40.77498495, -73.9859719946164), "+19173999127"),\
                     'Ben': ((40.77418400, -73.9859719946164),"+16466730050"),\
                     'Sana': ((40.77416495, -73.9859719946164),"+17819274632"),\
                     'John': ((40.77415495, -73.9859719946164),"+16466730050")}
ACCOUNT_SID = "AC8e6cf2a6b5fda889fa57b90bda8cc332" 
AUTH_TOKEN = "40af59c99b250d3293596173f8bd614a" 
client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 

    # 6367 km is the radius of the Earth
    km = 6367 * c
    return km 


@app.route('/',methods=("GET", "POST"))
def index():
    if request.method == 'POST':
        #print(request.form.items()[0][0])
        address = request.form.items()[0][1]
        print(address)
        geolocator = Nominatim()

        location = geolocator.geocode(address)
        where = location.address
        description = request.form.items()[1][1]
        extraComments = request.form.items()[2][1]
        #print(where)
        #print(description)
        #print(extraComments)
        coordinates = location.latitude, location.longitude
        #print(coordinates)
        for helper in dictOfCoordinates:
            print(helper)
            latA = dictOfCoordinates.get(helper)[0][0]
            longB = dictOfCoordinates.get(helper)[0][1]
            if haversine(coordinates[0], coordinates[1], latA, longB) <= 5: 
                miles = haversine(coordinates[0], coordinates[1], latA, longB)
                number = dictOfCoordinates.get(helper)[1]
                print(miles)
                print(description)
                print(extraComments)
                print(number)
                loadTwilioConfig(miles, description ,extraComments, number)
        return "Your request is being processed."
        #replyMessage()
    return render_template("index.html")



def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 

    # 6367 km is the radius of the Earth
    km = 6367 * c
    return km

def loadTwilioConfig(miles, description, extraComments, number):

    answer = "Hello there, there is someone " + str(miles) +\
             " miles away who needs help " + str(description)\
             + "Some extra comments included: " + str(extraComments)
    message = client.messages.create(to=number, from_="+16467592786",
                                 body=str(answer)) 
    return message




if __name__ == "__main__":
    app.run(debug=True)
