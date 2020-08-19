
# Al0nnso - 2019
# Geolocator
# You have three ways to get the geo location

# With ipregistry
from ipregistry import IpregistryClient
client = IpregistryClient("tryout")  
ipInfo = client.lookup() 
print(ipInfo)

# With geocoder
'''
import geocoder,time
g = geocoder.ip('me')
print(g.latlng)
'''

# With the google geolocation TOKEN ( THE BEST )
'''
send_url = "http://api.ipstack.com/check?access_key=YOUR_ACCESS_KEY"
geo_req = requests.get(send_url)
geo_json = json.loads(geo_req.text)
latitude = geo_json['latitude']
longitude = geo_json['longitude']
city = geo_json['city']
time.sleep(10)
'''

