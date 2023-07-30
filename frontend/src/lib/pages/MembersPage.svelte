
<script>
    import { usersYaml } from '../../dataservices';

    import { v4 as uuidv4 } from 'uuid';

    import axios from 'axios';
    let users = $usersYaml.users
    
    import EditUser from '../forms/EditUser.svelte';
    
    let editedUser = null;
    let opAddUser = false;

    let userPers = ''

    

    async function updateYamlData() {
      const updatedData = { users: users };
      const url = 'http://127.0.0.1:5000/update_users';
      const data = users

      try {
        const response = await axios.post(url, JSON.stringify(data), {headers: {'Content-Type': 'application/json'}})

        console.log('Response:', response.data);

       
      } catch (error) {
        console.error('Error:', error);
      }
    }



    async function getUserPerspective(userId) {
      const url = 'http://127.0.0.1:5000/get_user_perspective';
      const data = { userId: userId
                    }; // Replace with the data you want to send


      try {
        const response = await axios.post(url, JSON.stringify(data), {headers: {'Content-Type': 'application/json'}})

        console.log('Response:', response.data);

        userPers = response.data

        // Do something with the response data
        editedUser['perspective'] = userPers

      
      } catch (error) {
        console.error('Error:', error);
      }
    }

    function startEditing(user) {  

        removePotentiallyAddedUser()
        
        editedUser = { ...user }; // Make a copy so we don't edit the original item directly
        getUserPerspective(user['id'])
        
        
        console.log(editedUser)


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
        perspective: '',
        interactions: [],
      });
      editedUser = {...users[users.length - 1]}
    }

    function saveChanges() {
        console.log(editedUser.id)

        const originalUser = users.find(user => user.id === editedUser.id);
        Object.assign(originalUser, editedUser); // Save the changes
        console.log(originalUser);
        users = users;
        editedUser = null;
        // updateYamlData();   THIS IS NOT WORKING YET

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

