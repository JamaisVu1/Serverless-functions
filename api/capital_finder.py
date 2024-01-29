#GPT Assisted
from http.server import BaseHTTPRequestHandler
from urllib import request, parse
import json

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed_path = parse.urlparse(self.path)
        query_params = parse.parse_qs(parsed_path.query)

        country = query_params.get("country", [None])[0]
        capital = query_params.get("capital", [None])[0]
        message = "Invalid request"

        if country:
            with request.urlopen(f"https://restcountries.com/v3.1/name/{parse.quote(country)}") as response:
                data = json.loads(response.read().decode())
                capital_name = data[0]['capital'][0]
                message = f"The capital of {country} is {capital_name}"
        elif capital:
            with request.urlopen(f"https://restcountries.com/v3.1/capital/{parse.quote(capital)}") as response:
                data = json.loads(response.read().decode())
                country_name = data[0]['name']['common']
                message = f"{capital} is the capital of {country_name}"

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(message.encode())