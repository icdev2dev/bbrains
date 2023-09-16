from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import openai
from pathlib import Path
import yaml
import json

import uuid

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

yaml_dir = "src/public/"
users_yaml = yaml_dir + "users.yaml"
yaml_userinteractions_dir = yaml_dir + "/userinteractions/"

# Define a route to serve the file
@app.route('/users_yaml', methods=['GET'])
def serve_file_users():
    file_path = 'public/users.yaml'
    return send_file(file_path, as_attachment=True)

@app.route('/teams_yaml', methods=['GET'])
def serve_file_teams():
    file_path = 'public/teams.yaml'
    return send_file(file_path, as_attachment=True)

@app.route('/whoami_yaml', methods=['GET'])
def serve_file_whoami():
    file_path = 'public/whoami.yaml'
    return send_file(file_path, as_attachment=True)

@app.route('/mypersonas_yaml', methods=['GET'])
def serve_file_mypersonas():
    file_path = 'public/mypersonas.yaml'    
    return send_file(file_path, as_attachment=True)

@app.route('/products_yaml', methods=['GET'])
def serve_file_products():
    file_path = 'public/products.yaml'    
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


@app.route('/update_users', methods=['POST'])  # bc even a get_user_perspective might change state
def handle_post_update_users():
    data = request.json
    with open(users_yaml, "w") as file:
        yaml.dump(data, file)
    return data

@app.route('/get_user_perspective', methods=['POST'])  # bc even a get_user_perspective might change state
def handle_post_get_user_perspective() :
    data = request.json  # Assuming the data is sent as JSON in the request body
    
    print(data)
    print(type(data))


    # The path here is different than send_file thing
    yaml_file_path = yaml_dir + str(data['userId']) + ".yaml"

    print(yaml_file_path)

    if Path(yaml_file_path).is_file():
        with open(yaml_file_path, 'r') as file:
            yaml_data = yaml.safe_load(file)
            perspective = yaml_data['perspective']
    else: 
        with open(users_yaml, 'r') as usersFile:
            yaml_users = yaml.safe_load(usersFile)
            
            for user in yaml_users['users']:
                if user['id'] == str(data['userId']):
                    perspective = user['background']
                    data = {'perspective': perspective  }
                    with open(yaml_file_path, "w") as file:
                        yaml.dump(data, file)
    return perspective


@app.route('/convert_audio_to_text', methods=['POST'])
def handle_convert_audio_to_text():
    audio_blob=request.data

    fileName = uuid.uuid4();
    fileName = str(fileName) +".wav"

    with open(fileName, "wb") as writeFile:
        writeFile.write(audio_blob)
    
    with open(fileName, "rb") as audio_file:
     transcript = openai.Audio.transcribe("whisper-1", audio_file)

    print(transcript.to_dict())
    return jsonify(transcript.to_dict())



@app.route('/update_user_perspective', methods=['POST'])
def handle_post_update_user_perspective() :
    data = request.json  # Assuming the data is sent as JSON in the request body
    
    print(data)
    print(type(data))
    data = json.loads(data)

    print(data["id"])

    # The path here is different than send_file thing
    yaml_file_path = yaml_dir + str(data["id"]) + ".yaml"
    yaml_userinteractions_file_path = yaml_userinteractions_dir + str(data["id"]) + ".yaml"

    if Path(yaml_userinteractions_file_path).is_file(): 
        with open(yaml_userinteractions_file_path) as file:
            yaml_userinteractions = yaml.safe_load(file)
    else:
        yaml_userinteractions =  {'interactions': []}

    
    yaml_userinteractions['interactions'] = yaml_userinteractions['interactions'] + data['interactions']

    with open(yaml_userinteractions_file_path, "w") as file:
        _ = yaml.dump(yaml_userinteractions, file)
        


    if Path(yaml_file_path).is_file():
        with open(yaml_file_path, 'r') as file:
            yaml_data = yaml.safe_load(file)
            current_perspective = yaml_data['perspective']
    else: 
        with open(users_yaml, 'r') as usersFile:
            yaml_users = yaml.safe_load(usersFile)
            
            for user in yaml_users['users']:
                if user['id'] == data['id']:
                    current_perspective = user['background']
    
    prompt = f"Can you update the current perspective of the person with the interactions that I and others have had \
        with the person with the intent of being able to use the current backgrouund to better predict the concerns \
            that that person might bring forward as well as reasoning that might persuade him to relinquish his concerns? \
                 \n CURRENT PERSPECTIVE: \n {current_perspective} \n "
    prompt = prompt + " \n INTERACTIONS: \n"    
    
    for interaction in data['interactions']:
        prompt = prompt + f"      Query: {interaction['query']} -> Response: {interaction['response']}"
    
    prompt = prompt + " \n\n Need ONLY the updated current perspective. \n"    
    
    print(prompt)

    updated_perspective = invoke_openai_no_s("gpt-4", prompt)

    print(updated_perspective)

    updated_perspective = updated_perspective['choices'][0]['message']['content']
    print(updated_perspective)

    yaml_data = {'perspective': updated_perspective}

    with open(yaml_file_path, 'w') as file:
        yaml_data = yaml.dump(yaml_data,file)

    return updated_perspective;


def invoke_openai_no_s(model, q) :
    print(model)
    
    req = openai.ChatCompletion.create(model=model, messages=[
                            {"role": "user", "content": q}]
    )

    return req

def invoke_openai(model, s, q) :
    print(model)
    
    req = openai.ChatCompletion.create(model=model, messages=[
                 {"role": "system", "content": s},
                {"role": "user", "content": q}]
    )

    return req

if __name__ == '__main__':
    app.run()
