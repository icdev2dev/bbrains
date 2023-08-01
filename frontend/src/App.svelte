<!-- App.svelte -->
<script>
  import { Route, Router, Link } from "svelte-routing";
  import DataServices from "./DataServices.svelte";  


  import HomePage from "./lib/pages/HomePage.svelte";
  import TeamPage from "./lib/pages/TeamPage.svelte";
  import MembersPage from "./lib/pages/MembersPage.svelte";
  import WhoAmI from "./lib/pages/WhoAmI.svelte";

  import { isLoadingMyPersonasYaml} from "./dataservices.js"  
  import { onDestroy } from "svelte";
  
  let isLoading = true;

  const unsubs = isLoadingMyPersonasYaml.subscribe(value => {
    isLoading = value;
    console.log(value);

  })

  onDestroy(()=> {
    unsubs()
  })
  
  // let tabs = [
  //   {name:'Home', route: '/', component: HomePage},
  //   {name: 'Teams', route: '/teams', component: TeamPage},
  //   {name: 'Members', route: '/members', component: MembersPage},
  //   {name: 'About Me', route: '/aboutme', component: WhoAmI}
  // ]

  let tabs = [
    {name:'Home', route: '/', component: HomePage},
    {name: 'Members', route: '/members', component: MembersPage},
    {name: 'Teams', route: '/teams', component: TeamPage},
    {name: 'About Me', route: '/aboutme', component: WhoAmI}


  ]

</script>

<DataServices/>
{#if isLoading }

  <p> Loading</p>

{:else}

          <Router>
          <nav>
            <ul>
              {#each tabs as tab}
                <li><Link to={tab.route}>{tab.name}</Link></li>
              {/each}
            </ul>
          </nav>

          {#each tabs as tab}
            <Route path={tab.route} >
              <svelte:component this={tab.component} />
            </Route>
          {/each}
          </Router>
  {/if}


<style>


  nav {
      background-color: #f8f9fa;
      padding: 10px;
    }
  
    ul {
      display: flex;
      justify-content: space-around;
      list-style-type: none;
  
    }
  
    li {
      cursor: pointer;
      margin-left: 100px;
      margin-right: 100px;
  
    }
  
  
  
  
  </style>