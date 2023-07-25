<script>
    import { createEventDispatcher } from 'svelte';
    export let interaction = { query: '', response: '' };
    export let index;
  
    const dispatch = createEventDispatcher();
  
    function update(key, e) {
      const inputElement = e.target;
      const value = inputElement.value;
      interaction[key] = value;
      dispatch('update', { index, interaction });
      
    }
  
    function deleteInteraction() {
      console.log(index);
      dispatch('delete', index);
    }
  </script>
  
  <table class="tbl1">

    <div id="userInteraction">
      <tr>
        <label>
            Query
            <textarea class="txtdata1" value={interaction.query} on:input={(e) => update('query', e)} />
        </label>
      </tr>
      <tr>
        <label>
             Response
            <textarea class="txtdata2" value={interaction.response} on:input={(e) => update('response', e)} />
        
        </label>
      </tr>
      <tr>
        <button type="button" on:click={deleteInteraction}>Delete Interaction</button>
      </tr>
    </div>

</table>

  <style>
    .tbl1 {
      width: 100%;
    }
    
    .txtdata1 {
      width: 650px;
      height: 50px;
    }

    .txtdata2 {
      width: 650px;
      height: 100px;
    }
    #userInteraction {
      width: 100%;
      max-width: 650px;
      margin: 0 auto;
      padding: 20px;
      border: 1px solid #ccc;
      border-radius: 4px;
  
    }
  </style>