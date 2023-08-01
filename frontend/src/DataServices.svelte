<script >
    import { onMount } from 'svelte';
    import { readYamlFromWebService } from './dataservices.js';
    export const isLoading = true;


    const url = 'http://127.0.0.1:5000/'; // Replace with the actual web service URL
    onMount(async () => {
      await readYamlFromWebService(url);
     // isLoading = false;

    });
  </script>
  