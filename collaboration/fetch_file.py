import os

def init():
  os.system("python -m http.server")

def fetch_file(ip, port, from_path, to_path):
  import urllib.request
  response = urllib.request.urlopen("http://" + ip + ":" + port + from_path[2:])
  file = open(to_path, "wb+")
  file.write(response.read())
  file.close()
