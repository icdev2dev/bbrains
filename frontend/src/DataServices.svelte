<script>
    import { onMount } from 'svelte';
    import { readYamlFromWebService } from './dataservices.js';

    const url = 'http://127.0.0.1:5000/'; // Replace with the actual web service URL

    onMount(() => {
      readYamlFromWebService(url);
    });
  </script>
  