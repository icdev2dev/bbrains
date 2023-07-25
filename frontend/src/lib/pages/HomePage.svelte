<script>
  	import { fade, fly } from 'svelte/transition';
    import { writable } from 'svelte/store';

    import { teamsYaml } from '../../dataservices';
    import { usersYaml } from '../../dataservices';

    let newQuery = '';
    let interactions = [];


    let members = $usersYaml.users
    let membersStore = writable(members)

    let teams = $teamsYaml.teams
    let teamsStore = writable(teams);
    

    let visibleTeams = false;
    let visibleMembers = false;
    

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
      submitQuery();
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
      <strong>Query:</strong> {interaction.query}
    </p>
    <strong>Response:</strong> <pre>{interaction.response}</pre>
    <hr/>
  {/each}
  
  <div>
    <label for="newQuery">Your New Query:</label>
    <textarea id="newQuery" bind:value={newQuery} on:keydown={handleKeyDown}></textarea>
    <button on:click={submitQuery} disabled={!newQuery}>Submit</button>
  </div>
</div>





<style>
    .plr {
        place-items: left;
    }
    #newQuery {
        width: 100%;
        min-height: 100px;
        place-content: center;
    }
</style>