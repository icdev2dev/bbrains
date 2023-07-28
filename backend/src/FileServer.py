from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import openai
from os.path import exists

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
    print(exists(file_path))
    print("ok in teams")
    return send_file(file_path, as_attachment=True)

@app.route('/whoami_yaml', methods=['GET'])
def serve_file_whoami():
    file_path = 'public/whoami.yaml'
    print(exists(file_path))
    print("ok in whoami")
    return send_file(file_path, as_attachment=True)

@app.route('/mypersonas_yaml', methods=['GET'])
def serve_file_mypersonas():
    file_path = 'public/mypersonas.yaml'
    print(exists(file_path))
    print("ok in mypersonas")

    
    return send_file(file_path, as_attachment=True)


@app.route('/post_endpoint', methods=['POST'])
def handle_post_request():
    data = request.json  # Assuming the data is sent as JSON in the request body
    # Perform any processing or actions based on the data received
    # Return a response if needed
    print(data)
    res = invoke_openai(data['model'], data['systemContext'], data['query']);

    response_data = {'message': res.choices[0]["message"]["content"]}
    return jsonify(response_data)


def invoke_openai(model, s, q) :
    print(model)
    
    req = openai.ChatCompletion.create(model=model, messages=[
                 {"role": "system", "content": s},
                {"role": "user", "content": q}]
    )

    return req

if __name__ == '__main__':
    app.run()
