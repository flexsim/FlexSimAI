import json
from stable_baselines3 import PPO
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import numpy as np

class FlexSimInferenceServer(BaseHTTPRequestHandler):

    def do_GET(self):
        params = parse_qs(urlparse(self.path).query)
        self._handle_reply(params)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        params = parse_qs(body)
        self._handle_reply(params)

    def _handle_reply(self, params):
        if len(params):
            observation = []
            if b'observation' in params.keys():
                observationBytes = params[b'observation'][0]
                observation = np.array(json.loads(observationBytes))
            elif 'observation' in params.keys():
                observationBytes = params['observation'][0]
                observation = np.array(json.loads(observationBytes))
            if isinstance(observation, list):
                observation = np.array(observation)
            action, _states = FlexSimInferenceServer.model.predict(observation)
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(json.dumps(action, cls=NumpyEncoder), "utf-8"))
            return
      
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("", "utf-8"))


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


def main():
    print("Loading model...")
    model = PPO.load("MyTrainedModel")
    FlexSimInferenceServer.model = model
    
    # Create server object
    print("Starting server...")
    hostName = "localhost"
    serverPort = 80
    webServer = HTTPServer((hostName, serverPort), FlexSimInferenceServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    # Start the web server
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")


if __name__ == "__main__":
    main()