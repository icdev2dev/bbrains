import { writable } from 'svelte/store';
import yaml from 'js-yaml';


export const usersYaml = writable({});
export const teamsYaml = writable({});

let usersUri = "users_yaml"
let teamsUri = "teams_yaml"

export async function readYamlFromWebService(url) {
    readYamlFileFromWebService(url+usersUri, usersYaml);
    readYamlFileFromWebService(url+teamsUri, teamsYaml);

}

export async function readYamlFileFromWebService(url, datastore) {
  try {
    const response = await fetch(url);
    if (response.ok) {
      const data = await response.text();
      const parsedData = yaml.load(data);

      datastore.set(parsedData);


    } else {
      console.error('Failed to fetch the YAML data:', response.status, response.statusText);
    }
  } catch (error) {
    console.error('Error fetching the YAML data:', error);
  }
}