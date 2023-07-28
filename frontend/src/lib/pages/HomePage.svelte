<script>
  	import { fade, fly } from 'svelte/transition';
    import { writable } from 'svelte/store';
    import axios, { all } from 'axios';


    import { teamsYaml } from '../../dataservices';
    import { usersYaml } from '../../dataservices';
    import { mypersonasYaml } from '../../dataservices';
    import { whoamiYaml } from '../../dataservices';

    let newQuery = '';

    let interactions = [];
    let whoami = $whoamiYaml.whoami

    let members = $usersYaml.users
    let membersStore = writable(members)

    let teams = $teamsYaml.teams
    let teamsStore = writable(teams);

    let mypersonas = $mypersonasYaml.personas
    let mypersonasStore = writable(mypersonas);
    let selectedPersona;


    let visibleTeams = false;
    let visibleMembers = false;

    let isProcessing = false;

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

        allTeamMembers.forEach(memberinset => {
          const lookupMember = $membersStore.find(member => member.id === memberinset)
          teamMembersBackground = teamMembersBackground + lookupMember.name;

          teamMembersBackground = teamMembersBackground + " is a " + lookupMember.occupation + ". "
          teamMembersBackground = teamMembersBackground + lookupMember.background
          teamMembersBackground = teamMembersBackground + " \n"          
        });

        systemContextText = systemContextText + teamMembersBackground;

        systemContextText = systemContextText + whoami;


        

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

          allTeamMembers.forEach(memberinset => {
            const lookupMember = $membersStore.find(member => member.id === memberinset)
            teamMembersBackground = teamMembersBackground + lookupMember.name;

            teamMembersBackground = teamMembersBackground + " is a " + lookupMember.occupation + ". "
            teamMembersBackground = teamMembersBackground + lookupMember.background
            teamMembersBackground = teamMembersBackground + " \n"          
          });

          systemContextText = systemContextText + teamMembersBackground;
          systemContextText = systemContextText + whoami;
        

        }
        else {
          systemContextText = systemContextText + whoami;
        }
      }

      const data = { query: newQuery, systemContext: systemContextText }; // Replace with the data you want to send

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


<table>
    <tr>
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
        <td>
          <div class="mypersona">
            <div>
              My Persona
            </div>
            <div>
              <select bind:value={selectedPersona}>
                  {#each $mypersonasStore as mypersona (mypersona.Id) }
                    <option value={mypersona.Id}> {mypersona.Persona}</option>
                    
                  {/each}
              </select>
            </div>
          </div>
          
            
        </td>
        <td>
            <button on:click={clearInteractions}>Clear Interactions</button>
        </td>
    
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
    <textarea id="newQuery" bind:value={newQuery} on:keydown={handleKeyDown}></textarea>
    <button on:click={postData} disabled={!newQuery}>Submit</button>
  </div>
</div>





<style>
    .plr {
        place-items: left;
    }
    .mypersona {
      border: 1px solid gainsboro;
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