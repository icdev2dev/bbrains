
<script>
    import { usersYaml } from '../../dataservices';
    let users = $usersYaml.users

    import EditUser from '../forms/EditUser.svelte';
    
    let editedUser = null;
    let opAddUser = false;



    

    function updateYamlData() {
      const updatedData = { users: users };
      const yamlText = jsYaml.dump(updatedData);
      // Send the updated YAML data to the server or save it to a file as needed
      // For demonstration purposes, we're only logging the data to the console
      console.log(yamlText);
    }


    function startEditing(user) {      
        removePotentiallyAddedUser()
        editedUser = { ...user }; // Make a copy so we don't edit the original item directly
    }

    
    function cancelEditing(){
        removePotentiallyAddedUser()
        editedUser = null;
    }
    
    function removePotentiallyAddedUser() {
        if (opAddUser == true) {
          users = users.slice(0, users.length - 1)
          opAddUser = false;
        }
    }
  
    function addUser() {
      opAddUser = true;

      users.push({
        id: uuidv4(),
        name: '',
        email: '',
        occupation: '',
        background: '',
        interactions: [],
      });
      editedUser = {...users[users.length - 1]}
    }
  
    function saveChanges() {
        const originalUser = users.find(user => user.id === editedUser.id);
        Object.assign(originalUser, editedUser); // Save the changes
        console.log(originalUser);
        users = users;
        editedUser = null;
        updateYamlData();

    }

  </script>

    <table>
            <tr>
                <th> Name </th>
                <th> Email </th>
                <th> occupation</th>

            </tr>
            {#if users}
              {#each users as user}

                <tr on:click={() => startEditing(user)}>
                    
                    <td class="name"> {user.name}</td>
                    <td class="email"> {user.email}</td>                    
                    <td class="occupation"> {user.occupation}</td>
                </tr>

              {/each}
            {/if}
    </table>
 
{#if editedUser}
  <EditUser bind:user={editedUser} on:save={saveChanges} on:cancel={cancelEditing}/>
{/if}

  <button on:click={addUser}>Add User</button>
  
  <style>
    .user {
      margin-bottom: 20px;
    }
    .interaction {
      margin-bottom: 10px;
    }


    /* Give the table 100% width */
  table {
    width: 100%;
  }

  /* Style the table cells (td) */
  td {
    /* Add a border to visually separate cells */
    border: 1px solid #ddd;
    /* Add some padding to make the cells less crowded */
    padding: 8px;
    /* Add vertical alignment to the middle */
    vertical-align: middle;
  }

  /* Style the 'name' column to take up 20% of the width */
  .name {
    width: 40%;
  }

  /* Add a hover effect to rows */
  tr:hover {
    background-color: #ccdeac;
  }

  </style>

