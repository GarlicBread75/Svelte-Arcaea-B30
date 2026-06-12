<title>Arcaea B30 Calculator :3</title>

<script>
	import {onMount} from "svelte";
	import {page} from '$app/state';
	import {goto} from '$app/navigation';
	import {user} from "$lib/auth";

    onMount(async () => {if ($user?.role != "admin")
                         {
                             goto('/charts');
                         }})

	let new_title = $state("");
    let new_difficulty = $state("");
    let new_constant = $state("");
    let delete_id = $state("");
    
    async function addChart()
    {
        const res = await fetch("http://127.0.0.1:8000/add_chart", {method: "POST",
                                                                    headers: {"Content-Type": "application/json"},
                                                                    body: JSON.stringify({title: new_title,
                                                                                          difficulty: new_difficulty,
                                                                                          constant: new_constant,
                                                                                          score: 0})});
        const data = await res.json();
        new_title = "";
        new_difficulty = "";
        new_constant = "";
    }
    
    async function deleteChart()
    {
        const res = await fetch("http://127.0.0.1:8000/delete_chart", {method: "POST",
		                                                               headers: {"Content-Type": "application/json"},
																	   body: JSON.stringify({id: Number(delete_id)})});
    
        const data = await res.json();
        delete_id = "";
    }
	
	function logout()
	{
		event.preventDefault();
	    user.set(null);
	    goto('/charts');
	}
</script>

<div class = "top-bar">
	<a href = "/b30" class = "tairitsu charts-button">B30 List</a>
	<a href = "/charts" class = "hikari charts-button">All Charts</a>
</div>

<div class = "left-bar">
	{#if $user}
		<p class = "logged-in-as">Logged in as: <br>{$user.username}</p>
		<a href = "/charts" class = "doro-c charts-button" onclick={logout}>Log Out</a>
	{/if}
</div>

<div class = "admin-page">
    <div class = "admin-panel">
        <h2>Add Chart</h2>
        <input class = "blue-text" placeholder = "Title" bind:value = {new_title}/>
        <input class = "blue-text" placeholder = "Difficulty" bind:value = {new_difficulty}/>
        <input class = "blue-text" placeholder = "Constant" bind:value = {new_constant}/>
        <button class = "pink-text" onclick = {addChart}>Add Chart</button>
    </div>
    <div class = "admin-panel">
        <h2>Delete Chart</h2>
        <input class = "pink-text" placeholder = "Chart ID" bind:value = {delete_id}/>
        <button class = "blue-text" onclick = {deleteChart}>Delete Chart</button>
    </div>
</div>