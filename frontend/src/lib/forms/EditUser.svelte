<script>
    import EditUserInteractions from './EditUserInteractions.svelte';
    import axios from 'axios';   

    import { createEventDispatcher } from 'svelte';

    const dispatch = createEventDispatcher();

    let isProcessing = false;

    let value = '';

    export let user = {
        id: '',
        name: '',
        email: '',
        occupation: '',
        background: '',
        perspective: '',
        interactions: []
    };

    async function updateUserPerspective(){
        console.log(JSON.stringify(user))

        const url = 'http://127.0.0.1:5000/update_user_perspective';
        const data = JSON.stringify(user)

        isProcessing = true;

        try {
            const response = await axios.post(url, JSON.stringify(data), {headers: {'Content-Type': 'application/json'}})
            value = response.data;
            user['perspective'] = value;

            console.log('Response:', response.data);
            isProcessing = false;
            
        } catch (error) {
            console.error('Error:', error);
            isProcessing = false;
        }
    }    

    

    function save() {
      user = {...user}; // Emitting new value for two-way binding
      dispatch('save');
    }
    function cancel() {
        user = null
        dispatch('cancel');
    }

    function addInteraction() {
        user.interactions = [...user.interactions, { query: '', response: '' }];

    }
    
    function updateInteraction(event,i) {
        user.interactions[i] = event.detail.interaction;

    }
    function deleteInteraction(index) {

        user.interactions = [ ...user.interactions.slice(0, index), ...user.interactions.slice(index+1)];
    } 

  </script>

    {#if isProcessing}
        <img src="hourglass.jpg" alt="Loading" width="10px" height="20px"/>
    {/if}

  <form class="editForm" on:submit|preventDefault={save} on:reset={cancel}>
    <h2>Edit User</h2>
    <div id="inputFields">
        <div id="mainFields">
            <label>
            Name:
            <input bind:value={user.name} />
            </label>
            <label>
            Email:
            <input bind:value={user.email} />
            </label>
            <label>
            Occupation:
            <input bind:value={user.occupation} />
            </label>
        </div>
        <p/>

        <div id="backgroundField">
            <label>
                Background:
                <textarea id="backgroundField_textarea" bind:value={user.background} />
            </label>

                <p> Updated Perspective:</p>
                <p> {user.perspective} </p>
        
        </div>

        <h3>User Interactions</h3>
        <table id="tbl1">
            <div id="userInteractions">
                {#each user.interactions as interaction, index (index)}
                <EditUserInteractions {interaction} {index}  on:update={(event) => updateInteraction(event, index)} on:delete={() => deleteInteraction(index)} />
                {/each}
                <button type="button" on:click={addInteraction}>Add User Interaction</button>
                <button on:click={updateUserPerspective}>Update User Perspective</button>  

            </div>
        </table>
    </div>
    <button type="submit">Save User</button>
    <button type="reset">Cancel Edit</button>
  </form>
  
  <style>
    #tbl1 {
        width: 100%;
    }
    #perspectiveField_textarea {
        width: 100%;
        height: 200px;
        padding: 10px;
        font-size: 16px;
        line-height: 1.5;
        border-radius: 4px;
        border: 1px solid #ccc;
        box-shadow: inset 0 1px 2px rgba(0,0,0,.1);
        resize: vertical;
        
    }
    #backgroundField_textarea {
        width: 100%;
        height: 100px;
        padding: 10px;
        font-size: 16px;
        line-height: 1.5;
        border-radius: 4px;
        border: 1px solid #ccc;
        box-shadow: inset 0 1px 2px rgba(0,0,0,.1);
        resize: vertical;
        
    }
    .editForm {
        width: 100%;
        max-width: 750px;
        margin: 0 auto;
        padding: 20px;
        border: 1px solid #ccc;
        border-radius: 4px;
    }

    #inputFields {
        margin: 0 auto;
        padding: 20px;
        border: 1px solid #ccc;
        border-radius: 4px;

    }
    #userInteractions {
        margin: 0 auto;
        width: 100%;
        border: 1px solid #ccc;
        border-radius: 4px;

    }
  </style>