<script>
    import { writable } from 'svelte/store';
     
    import { mypersonasYaml } from '../../dataservices';
    import { whoamiYaml } from '../../dataservices';

    let whoami = $whoamiYaml.whoami
    let mypersonas = $mypersonasYaml.personas
    let mypersonasStore = writable(mypersonas);

    
</script>
<h1> Who Am I </h1>
{whoami}
<h2> My Personas </h2>
<table>
    <tr>
        <th> Persona</th>
        <th> Persona Description</th>
    </tr>
    {#each $mypersonasStore as mypersona }
        <tr>
            <td> {mypersona.Persona}</td>
            <td> {mypersona.Description}</td>
        </tr>
        
    {/each}
</table>
