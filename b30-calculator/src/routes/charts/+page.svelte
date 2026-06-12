<title>Arcaea B30 Calculator :3</title>

<script>
	import {onMount} from "svelte";
	import {page} from '$app/state';
	import {goto} from '$app/navigation';
	import {user} from "$lib/auth";
	
	let table_data = $state([]);
	let shown_rows = $state([]);
	let columns = $state([]);
	const limit = 100;
	let offset = $state(0);
	let total_pages = $state(0);
	let page_input = $state("...");

	onMount(async () => {let page_num = Number(page.url.searchParams.get('page')) || 0;
						 const response = await fetch("http://127.0.0.1:8000/charts");
						 table_data = await response.json();
						 total_pages = Math.floor(table_data.length/limit)+1;
	                     if(page_num >= total_pages)
						 {
						     goto(`/invalid_chart_page`);
						 }
						 
						 table_data = table_data.map(row => ({Id: row.id,
														      Title: row.title,
															  Difficulty: row.difficulty,
															  Level: "0",
															  "Chart Constant": row.constant,
															  Score: row.score,
															  "Play Rating": 0.0,
															  "Play Potential": 0.0}));
						 columns = Object.keys(table_data[0]);
						 
						 for(let row of table_data)
						 {
                             if(row["Title"] == "dropdead" && row["Chart Constant"] == 9.1)
                             {
                                 row["Level"] = "8+";
                             }
                             else
                             if(row["Title"] == "INTERNET YAMERO" && row["Chart Constant"] == 9.9)
                             {
                                 row["Level"] = "10";
                             }
                             else
                             if(row["Title"] == "Tempestissimo" && row["Chart Constant"] == 11.7)
                             {
                                 row["Level"] = "11";
                             }
                             else
                             if(row["Chart Constant"] % 1 >= 0.7)
                             {
                                 row["Level"] = `${Math.trunc(row["Chart Constant"])}+`;
                             }
                             else
                             {
                                 row["Level"] = `${Math.trunc(row["Chart Constant"])}`;
                             }
                             
                             
                             if(row["Score"] >= 10000000)
                             {
                                 row["Play Rating"] = 2;
                                 row["Play Potential"] = Math.max(row["Chart Constant"] + row["Play Rating"], 0);
                             }
                             else
                             if(row["Score"] >= 9800000)
                             {
                                 row["Play Rating"] = 1+(row["Score"]-9800000)/200000;
                                 row["Play Potential"] = Math.max(row["Chart Constant"] + row["Play Rating"], 0);
                             }
                             else
                             if(row["Score"] > 0)
                             {
                                 row["Play Rating"] = (row["Score"] - 9500000)/300000;
                                 row["Play Potential"] = Math.max(row["Chart Constant"] + row["Play Rating"], 0);
                             }
                             else
                             {
                                 row["Play Rating"] = 0;
                                 row["Play Potential"] = 0;
                             }
						 }
						 });

    $effect(() => {offset = Number(page.url.searchParams.get('page')) || 0;
				   if(offset < total_pages)
	               {
				       shown_rows = table_data.slice(offset*limit, (offset+1)*limit);
				   }
				   });
					
	function recalculate_rating(row)
	{
		if(row["Score"] >= 10000000)
		{
			row["Play Rating"] = 2;
			row["Play Potential"] = Math.max(row["Chart Constant"] + row["Play Rating"], 0);
		}
		else
		if(row["Score"] >= 9800000)
		{
			row["Play Rating"] = 1+(row["Score"]-9800000)/200000;
			row["Play Potential"] = Math.max(row["Chart Constant"] + row["Play Rating"], 0);
		}
		else
		if(row["Score"] > 0)
		{
			row["Play Rating"] = (row["Score"] - 9500000)/300000;
			row["Play Potential"] = Math.max(row["Chart Constant"] + row["Play Rating"], 0);
		}
		else
		{
			row["Play Rating"] = 0;
			row["Play Potential"] = 0;
		}
	}
	
	function change_page(page)
	{
		goto(`/charts?page=${page}`);
		shown_rows = table_data.slice(page*limit, (page+1)*limit);
	}
	
	function left_pages()
	{
		return [Math.max(0, offset-2), Math.max(1, offset-1)].filter(p => p < offset);
	}
	
	function right_pages()
	{
		return [offset+1, offset+2].filter(p => p = total_pages).filter(p => p < total_pages);
	}
	
	function logout()
	{
		event.preventDefault();
	    user.set(null);
	    goto('/charts');
	}
</script>

{#if table_data.length == 0}
	<p>Loading...</p>
{/if}


<div class = "top-bar">
		<a href = "/b30" class = "tairitsu charts-button">B30 List</a>
		<a href = "/b30" class = "tairitsu charts-button">B30 List</a>
	</div>

{#if table_data.length > 0}
<div class = "nav">
	<div class="nav-left">
		{#each left_pages() as p}
			<button class = {`nav-button nav-size ${Math.abs(offset-p) == 2 ? "pst" : "prs"}`}
					onclick = {() => change_page(p)} > <span>{p+1}</span></button>
		{/each}
	</div>

	<div class="nav-center">
	    <input class = "ftr nav-button nav-size"
			   bind:value={page_input}
			   oninput = {(e) => {page_input = e.target.value.replace(/\D/g, '');}}
               onblur = {() => {const target_page = Number(page_input);
								if(Number.isInteger(target_page) && target_page >= 0 && target_page < total_pages)
								{
								    change_page(target_page);
								}
								page_input = "...";}}
			   onkeydown = {(e) => {if (e.key === "Enter")
									{
									    const target_page = Number(page_input);
										if(Number.isInteger(target_page) && target_page >= 1 && target_page <= total_pages)
										{
										    change_page(target_page);
										}
										page_input = "...";
									}}}
		/>
	</div>

	<div class="nav-right">
		{#each right_pages() as p}
			<button class = {`nav-button nav-size ${Math.abs(offset-p) == 2 ? "byd" : "etr"}`}
					onclick = {() => change_page(p)} > <span>{p+1}</span></button>
		{/each}
	</div>
</div>

<table border = "1">
	<thead>
		<tr>
		{#each columns as col}
			<th>{col}</th>
		{/each}
		</tr>
	</thead>
	<tbody>
		{#each shown_rows as row}
		<tr class = {row["Difficulty"].toLowerCase()}>
			{#each columns as col}
				{#if col == "Score"}
					<td>
					    <input bind:value = {row[col]}
							   oninput = {(e) => {e.target.value = e.target.value.replace(/\D/g, '');}}
							   onblur = {async () => {recalculate_rating(row);
							                          await fetch("http://127.0.0.1:8000/update_score", {method: "POST",
													                                                     headers: {"Content-Type": "application/json"},
																										 body: JSON.stringify({id: row.Id, score: row.Score})});}}
						/>
					</td>
				{:else if col == "Difficulty"}
					<td>☆{row[col]}☆</td>
				{:else}
					<td>{row[col]}</td>
				{/if}
			{/each}
		</tr>
		{/each}
	</tbody>
</table>

<div class = "left-bar">
	{#if $user}
		<p class = "logged-in-as">Logged in as: <br>{$user.username}</p>
		<a href = "/charts" class = "doro-c charts-button" onclick={logout}>Log Out</a>
		{#if $user?.role == "admin"}
			<a href = "/admin_panel" class = "saya charts-button">Admin Panel</a>
		{/if}
	{:else}
		<a href = "/signup" class = "eto charts-button">Sign Up</a>
		<a href = "/login" class = "luna charts-button">Log In</a>
	{/if}
</div>

<div class = "nav">
	<div class="nav-left">
		{#each left_pages() as p}
			<button class = {`nav-button nav-size ${Math.abs(offset-p) == 2 ? "pst" : "prs"}`}
					onclick = {() => change_page(p)} > <span>{p+1}</span></button>
		{/each}
	</div>

	<div class="nav-center">
	    <input class = "ftr nav-button nav-size"
			   bind:value={page_input}
			   oninput = {(e) => {page_input = e.target.value.replace(/\D/g, '');}}
               onblur = {() => {const target_page = Number(page_input);
								if(Number.isInteger(target_page) && target_page >= 0 && target_page < total_pages)
								{
								    change_page(target_page);
								}
								page_input = "...";}}
			   onkeydown = {(e) => {if (e.key === "Enter")
									{
									    const target_page = Number(page_input);
										if(Number.isInteger(target_page) && target_page >= 1 && target_page <= total_pages)
										{
										    change_page(target_page);
										}
										page_input = "...";
									}}}
		/>
	</div>

	<div class="nav-right">
		{#each right_pages() as p}
			<button class = {`nav-button nav-size ${Math.abs(offset-p) == 2 ? "byd" : "etr"}`}
					onclick = {() => change_page(p)} > <span>{p+1}</span></button>
		{/each}
	</div>
</div>
{/if}