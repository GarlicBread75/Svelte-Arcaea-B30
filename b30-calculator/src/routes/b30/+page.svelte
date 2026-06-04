<title>Arcaea B30 Calculator :3</title>

<script>
	import {onMount} from "svelte";
	
	let table_data = $state([]);
	let columns = $state([]);

	onMount(async () => {const response = await fetch("http://127.0.0.1:8000/b30");
						 table_data = await response.json();
						 
						 table_data = table_data.map(row => ({No: row.id,
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
						 }
						 });
</script>

{#if table_data.length == 0}
	<p>Loading...</p>
{/if}

<div class = "top-bar">
	<a href = "/charts?page=1" class = "hikari charts-button">All Charts</a>
	<a href = "/charts?page=1" class = "hikari charts-button">All Charts</a>
</div>

{#if table_data.length > 0}
<table border = "1">
	<thead>
		<tr>
		{#each columns as col}
			<th>{col}</th>
		{/each}
		</tr>
	</thead>
	<tbody>
	{#each table_data as row, i}
		<tr class = {row["Difficulty"].toLowerCase()}>
		{#each columns as col}
			{#if col == "No"}
				<td>{i+1}</td>
			{:else}
				<td>{row[col]}</td>
			{/if}
		{/each}
		</tr>
	{/each}
	</tbody>
</table>
{/if}