import urllib.request

def connect():
    try:
        urllib.request.urlopen('http://google.com') #Python 3.x
        return True
    except:
        return False

print( 'connected' if connect() else 'no internet!' )


import socket
IPaddress=socket.gethostbyname(socket.gethostname())
if IPaddress=="127.0.0.1":
    print("No internet, your localhost is "+ IPaddress)
else:
    print("Connected, with the IP address: "+ IPaddress )