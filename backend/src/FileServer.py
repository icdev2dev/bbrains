from flask import Flask, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Define a route to serve the file
@app.route('/users_yaml', methods=['GET'])
def serve_file_users():
    file_path = 'public/users.yaml'
    print("ok in users")
    return send_file(file_path, as_attachment=True)

@app.route('/teams_yaml', methods=['GET'])
def serve_file_teams():
    file_path = 'public/teams.yaml'
    print("ok in teams")
    return send_file(file_path, as_attachment=True)


if __name__ == '__main__':
    app.run()