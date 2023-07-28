# BBRAINS

This thing relies on Open-AI's gpt-4. You must have an OPENAI_API_KEY and you must have that set in your environment. The code makes implicit use of the key. 

This project is essentially split into backend and frontend
## Prerequisites
You must have python and node installed on your computer. I have python 3.10.6 and node 8.15.0 and npm 9.5.0


## Backend
This stuff is written in Python and essentially serves the data files (teams and users ) to the front end as well as it makes the relevant calls to openai. It sets a LOT of system context to make the responses meaningful wrt query. By default, the port is 5000

### Installation 
You should create a virtual environment and install the required packages in there. requirements.txt is your friend. pip install requirements.txt and then activate that stuff.

### Running 
Pretty simple. 
python src/FileServer.py

### Modifications
Currently update users.yaml and teams.yaml and restart to see changes


## Frontend 
This stuff is written in svelte. Default port is 5173. Access at https://localhost:5173.

### Installation 
npm install 
npm run dev








