import json
from http.server import BaseHTTPRequestHandler, HTTPServer

# Your existing classes and functions (Patient, populate_waiting_list, etc.)
class Patient:
    '''Creates a class for a patient'''

    def __init__(self, waiting_position, nhs_number, email, age):
        self.waiting_position = waiting_position
        self.nhs_number = nhs_number
        self.email = email
        self.age = int(age) if age.isdigit() else None  # Convert to int only if age is a digit

    def __str__(self):
        return f"Waiting Position: {self.waiting_position}, NHS Number: {self.nhs_number}, Email: {self.email}, Age: {self.age}"

waiting_list = []

def populate_waiting_list():
    ''' reads the text file,
    instantiates each line as a separate Patient class
    adds to waiting list'''
    
    with open("inbound_referrals.txt", "r") as file:
        for line in file:
            fields = line.strip().split(',')
            waiting_position = fields[0]
            nhs_number = fields[1]
            email = fields[2]
            age = fields[3]
            patient = Patient(waiting_position, nhs_number, email, age)
            waiting_list.append(patient)

populate_waiting_list()

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        '''Handle GET requests.'''
        
        # Routing based on URL path
        if self.path.startswith("/api/"):
            email = self.path.split("/")[-1]  # Extract the email from URL
            user = None
            for patient in waiting_list:
                if email == patient.email:
                    user = patient
                    break

            if user:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                # Send user data as JSON
                self.wfile.write(json.dumps({
                    "waiting_position": user.waiting_position,
                    "nhs_number": user.nhs_number,
                    "email": user.email,
                    "age": user.age
                }).encode())
            else:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "User not found"}).encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"Page not found")

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}')
    httpd.serve_forever()

# Run the server
if __name__ == "__main__":
    run()
