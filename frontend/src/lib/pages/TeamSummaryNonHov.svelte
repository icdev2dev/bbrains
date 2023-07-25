<script>
    import { teamsYaml } from '../../dataservices';
    let teams = $teamsYaml.teams ;   


    export const teamId = null
    let team = null

    
    function findTeamName(teamId) {
    
        team = teams.find(team => team.teamId === teamId);
        return team.teamId
    }

</script>

<label >
    <td>
        <input type="checkbox"/>
    </td>
    <td>
        
        <p>{findTeamName({teamId})}</p>
    </td>
</label>