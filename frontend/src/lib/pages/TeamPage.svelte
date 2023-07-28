<script>

    import { teamsYaml } from '../../dataservices';
    import { usersYaml } from '../../dataservices';

    import Hoverable from './Hoverable.svelte';
    
    let teams = $teamsYaml.teams ;   
    let members = $usersYaml.users;

    function findOcc(memberId) {
        let member = null;
        member = members.find(member => member.id === memberId)
        return member.occupation;
    }
</script>

{#each teams as team}
    <Hoverable let:hovering={active}>
        <div class:active>
            {#if active}
                <td class="alignr">
                    <label >
                        <td>
                            <input type="checkbox"/>
                        </td>
                        <td>
                            <p>{team.teamName}</p>
                        </td>
                    </label>
                </td>
                <td>
                    <table>
                        <tr>
                            <p>{team.teamDescription}</p>
                        </tr>
                        <tr>
                            {#each team.members  as member }
                                <tr>
                                    <td>
                                        {member.teamMemberName} 
                                    </td>
                                    <td>
                                        {findOcc(member.memberId)}
                                    </td>
                                </tr>                                        
                            {/each}              
                        </tr>
                    </table>
                </td>
            {:else}               
                {team.teamName}
            {/if}
        </div>
    </Hoverable>
{/each}



