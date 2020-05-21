import subprocess
import urllib.request

def init():
  return subprocess.Popen(["python -m http.server"], shell = True)

def close_server(server):
  server.terminate()

def fetch_file(ip, port, from_path, to_path):
  response = urllib.request.urlopen("http://" + ip + ":" + port + from_path[2:])
  file = open(to_path, "wb+")
  file.write(response.read())
  file.close()
