<script>
  	import { fade, fly } from 'svelte/transition';
    import { writable } from 'svelte/store';
    import axios, { all } from 'axios';


    import { teamsYaml } from '../../dataservices';
    import { usersYaml } from '../../dataservices';
    import { mypersonasYaml } from '../../dataservices';
    import { whoamiYaml } from '../../dataservices';

    import {productsYaml} from "../../dataservices";

    import { isLoadingMyPersonasYaml} from "../../dataservices.js"  
    import { onDestroy } from "svelte";

    import MicAccess from '../components/MicAccess.svelte';
    
    let isLoading = true;

    const unsubs = isLoadingMyPersonasYaml.subscribe(value => {
     isLoading = value;
     console.log(value);

    })

  onDestroy(()=> {
    unsubs()
  })

    let newQuery = '';

    let interactions = [];
    let whoami = $whoamiYaml.whoami

    let members = $usersYaml.users
    let membersStore = writable(members)

    let teams = $teamsYaml.teams
    let teamsStore = writable(teams);

    let mypersonas = $mypersonasYaml.personas
    let mypersonasStore = writable(mypersonas);

    let products = $productsYaml.products;
    let productsStore = writable(products);

    let selectedPersona;
    let selectedModel = "gpt-3.5-turbo-16k"
    let selectedProduct = null

    let includeMyBackground = false;

    let includeProductUpdate = false;

    let visibleTeams = false;
    let visibleMembers = false;

    let isProcessing = false;

    
    async function onMicStop(audioBlob) {
      alert('cool');

      const url = 'http://127.0.0.1:5000/convert_audio_to_text';

      try {
        const response = await fetch(url, {
            method: 'POST',
            body: audioBlob,
            headers: {
                'Content-Type': 'application/octet-stream'  // This indicates that you're sending raw binary data
            }
        });
        
        const data = await response.json();
        console.log(data.text);
        newQuery = data.text;

      } catch (error) {
        console.error("There was an error sending the blob:", error);
      }



    }

    function onMicStart(message) {
      alert(message);
      newQuery = "";
    }


    function getTeamDescription (team) {
      let teamDescription = team.teamDescription + "\n";

      teamDescription = teamDescription + "The " + team.teamName + " has the following members: \n"
      team.members.forEach(teamMember => {
        teamDescription = teamDescription + teamMember.teamMemberName
        teamDescription = teamDescription + "\n";

      })

      teamDescription = teamDescription + " \n"

      return teamDescription

    }



    async function getUserPerspective(userId) {
      const url = 'http://127.0.0.1:5000/get_user_perspective';
      const data = { userId: userId
                    }; // Replace with the data you want to send

      try {
        const response = await axios.post(url, JSON.stringify(data), {headers: {'Content-Type': 'application/json'}})
        console.log('Response:', response.data);
        return response.data;
  
      } catch (error) {
          console.error('Error:', error);
          return error;
      }
    }

    

    async function postData() {
      const url = 'http://127.0.0.1:5000/post_endpoint';
      
      let selectedTeams = []
      let systemContextText = ""
      $teamsStore.forEach(element => {
        if (element.selected) {
          selectedTeams.push(element)
        }
      });
      if (selectedTeams.length > 1) {

        systemContextText = systemContextText + "You are a set of " + selectedTeams.length + " Teams. They are "
        let teamsSoFar = 1;

        selectedTeams.forEach(team => {
          if (teamsSoFar < selectedTeams.length) {
            systemContextText = systemContextText + team.teamName + ", "
          }
          else {
            systemContextText = systemContextText + team.teamName + ". "
          }
          teamsSoFar = teamsSoFar + 1
             
        });
        systemContextText = systemContextText + "\n";

        selectedTeams.forEach(team => {
          systemContextText = systemContextText + getTeamDescription(team)
        });     
        
        let allTeamMembers = new Set();
        selectedTeams.forEach(team => {
          team.members.forEach(member => {
            allTeamMembers.add(member.memberId)
          })
        })


        let teamMembersBackground = ""

          for (let memberinset of allTeamMembers) {
            const lookupMember = $membersStore.find(member => member.id === memberinset)
            let userPerspective = await getUserPerspective(lookupMember.id)
            teamMembersBackground = teamMembersBackground + lookupMember.name;
            teamMembersBackground = teamMembersBackground + " is a " + lookupMember.occupation + ". "
            teamMembersBackground = teamMembersBackground + userPerspective;
            teamMembersBackground = teamMembersBackground + " \n"
          }
          systemContextText = systemContextText + teamMembersBackground;


        if (includeMyBackground === true) {
          systemContextText = systemContextText + whoami;
        }

        const lookupPersona = $mypersonasStore.find(persona => persona.Id === selectedPersona)
        systemContextText = systemContextText + lookupPersona.Description
        
        if (includeProductUpdate == true) {
          const lookupProduct = $productsStore.find(product => product.id === selectedProduct)
          systemContextText = systemContextText + "\n Please ensure that each team member have their own opinions about the product as described below; but only those opinions that are relevant to me.\n"
          systemContextText = systemContextText + "PRODUCT DESCRIPTION: \n"
          systemContextText = systemContextText + lookupProduct.description
        }

      }
      else {
        if (selectedTeams.length == 1) {
          systemContextText = systemContextText + "You are the" + getTeamDescription(selectedTeams[0])


          selectedTeams.forEach(team => {
            systemContextText = systemContextText + getTeamDescription(team)
          });     
        
          let allTeamMembers = new Set();
          selectedTeams.forEach(team => {
            team.members.forEach(member => {
              allTeamMembers.add(member.memberId)
            })
          })


          let teamMembersBackground = ""


          for (let memberinset of allTeamMembers) {
            const lookupMember = $membersStore.find(member => member.id === memberinset)
            let userPerspective = await getUserPerspective(lookupMember.id)
            teamMembersBackground = teamMembersBackground + lookupMember.name;
            teamMembersBackground = teamMembersBackground + " is a " + lookupMember.occupation + ". "
            teamMembersBackground = teamMembersBackground + userPerspective;
            teamMembersBackground = teamMembersBackground + " \n"
          }
          systemContextText = systemContextText + teamMembersBackground;


          
          if (includeMyBackground) {
           systemContextText = systemContextText + whoami;
          }
          const lookupPersona = $mypersonasStore.find(persona => persona.Id === selectedPersona)
          systemContextText = systemContextText + lookupPersona.Description
          
          if (includeProductUpdate == true) {
              const lookupProduct = $productsStore.find(product => product.id === selectedProduct)
              systemContextText = systemContextText + "\n Please ensure that each team member have their own opinions about the product as described below; but only those opinions that are relevant to me.\n"
              systemContextText = systemContextText + "PRODUCT DESCRIPTION: \n"
              systemContextText = systemContextText + lookupProduct.description
          }


        }
        else {
          if (includeMyBackground) {
           systemContextText = systemContextText + whoami;
          }
          const lookupPersona = $mypersonasStore.find(persona => persona.Id === selectedPersona)
          systemContextText = systemContextText + lookupPersona.Description
          if (includeProductUpdate == true) {
              const lookupProduct = $productsStore.find(product => product.id === selectedProduct)
              systemContextText = systemContextText + "\n Please ensure that I have opinions about the product as described below; but only those opinions that are relevant to me.\n"
              systemContextText = systemContextText + "PRODUCT DESCRIPTION: \n"
              systemContextText = systemContextText + lookupProduct.description
          }
        }
      }

      const data = { model: selectedModel,
                     query: newQuery, 
                     systemContext: systemContextText 
                    }; // Replace with the data you want to send

      console.log(systemContextText)
      isProcessing = true;

      try {
        const response = await axios.post(url, data);

        let response_html = response.data.message.replace(/\n/g, "<br />")
        console.log('Response:', response.data);
        // Do something with the response data
        interactions = [{ query: newQuery, response: "", editing: false }, ...interactions];
        interactions[0].response += response_html;
        interactions = [...interactions];
        isProcessing = false;
      
      } catch (error) {
        console.error('Error:', error);
        isProcessing = false;
      }
    }

    async function* createBatchGenerator(query) {
      let response = '';
      for (let i = 0; i < 15; i++) {
        response += query.split('').reverse().join('') + '\n'.repeat(Math.floor(Math.random() * 4));
        await new Promise(r => setTimeout(r, 500)); // Wait for 0.5 seconds
        yield response;
      }
  }

  async function submitQuery() {
    if (!newQuery) return;

    const generator = createBatchGenerator(newQuery);
    interactions = [{ query: newQuery, response: "", editing: false }, ...interactions];
    
    for await (const batch of generator) {
      interactions[0].response += batch;
      interactions = [...interactions]; // trigger reactivity by creating a new copy
    }

    newQuery = '';
}

  function handleKeyDown(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
//      submitQuery();
      postData();

    }
  }
  function clearInteractions() {
    
     interactions = []
  }

</script>

{#if  isLoading}
    <p> Loading</p>
{:else} 
  <table>
      <tr>
        <div class="theteams">
          <td>
              <label>
                  <input type="checkbox" bind:checked={visibleTeams} />
                  Select Team
              </label>
          </td>
          <td>
              <label>
                  <input type="checkbox" bind:checked={visibleMembers} />
                  Select Members
              </label>
          </td>
        </div>
          <td>
            <div class="mypersona">
              <div>
                About Me
              </div>
              <div>
                <div>
                  <label>
                    <input type="checkbox" bind:checked={includeMyBackground}/>
                    Include My background?
                  </label>
                </div>
                <div>
                  My Persona
                  <select bind:value={selectedPersona}>
                      {#each $mypersonasStore as mypersona (mypersona.Id) }
                        <option value={mypersona.Id}> {mypersona.Persona}</option>
                        
                      {/each}
                  </select>
                </div>
              </div>
            </div>
            
              
          </td>

          
          <td>
            <div class="morecontext">  
              More Context
              <div>
                <div>
                  <div>
                    <label>
                      <input type="checkbox" bind:checked={includeProductUpdate}/>
                      Include Product Update?
                    </label>
                  </div>
                  <div>
                    <select bind:value={selectedProduct}>

                      {#each $productsStore as product (product.id) }
                        <option value={product.id}> {product.name}</option>
                      {/each}
  
                    </select>
                  </div>
                </div>
              </div>
            </div>
          </td>
          <div class="usemodel">
            <td>
                Use Model
                <select bind:value={selectedModel}>
                  <option value="gpt-3.5-turbo-16k">gpt-3.5-turbo-16k</option>
                  <option value="gpt-4">gpt-4</option>
                </select>
            </td>
          
            <td>
                <button on:click={clearInteractions}>Clear Interactions</button>
            </td>
          
          </div>
      </tr>
  </table>

  {#if visibleTeams}
      <table>
    <p in:fly={{ y: 200, duration: 2000 }} out:fade>
              {#each $teamsStore as team }
              <tr class="plr">
                  <div>
                      <input type="checkbox" bind:checked={team.selected} />
                      {team.teamName}
                  </div>
              </tr>
            {/each}
                  
      </p>
      </table>

  {/if}

  {#if visibleMembers}
      Individual Members
      <table>
    <p in:fly={{ y: 200, duration: 2000 }} out:fade>
          
              {#each $membersStore as member }
                  <tr class="plr">
                      <div>
                          <input type="checkbox" bind:checked={member.selected} />

                          {member.name} -> {member.occupation}
                      </div>
                  </tr>
              {/each}
      </p>
      </table>

  {/if}

  <h2> Prompt </h2>

  <div>
    {#each interactions as interaction, i (i)}
      <p>
        <strong>Query:</strong> 
          <div class="queryresponse" bind:innerHTML={interaction.query} contenteditable=false/>
      
        
      
      <strong>Response:</strong> 
      
        <div class="queryresponse" bind:innerHTML={interaction.response} contenteditable=false/>
      
      <hr/>
    {/each}
    
    {#if isProcessing}
      <img src="hourglass.jpg" alt="Loading" width="10px" height="20px"/>
    
    {/if}

    <div>
      <label for="newQuery">Your New Query:</label>
      <MicAccess onMicStart={onMicStart}, onMicStop={onMicStop} />

      <textarea id="newQuery" bind:value={newQuery} on:keydown={handleKeyDown}></textarea> 
      <button on:click={postData} disabled={!newQuery}>Submit</button>
    </div>
  </div>


{/if}






<style>
    .plr {
        place-items: left;
    }
    .mypersona {
      border: 1px solid gainsboro;
    }
    .theteams {
      border: 1px solid greenyellow;
    }
    .usemodel {
      border: 1px solid blue;
    }
    .morecontext {
      border: 1px solid orange;
      width: 100%;
    }

    #newQuery {
        width: 100%;
        min-height: 100px;
        place-content: center;
    }
    .queryresponse {
      overflow-wrap: break-word;
      width: 900px;
      border: 2px solid white;
    }
</style>