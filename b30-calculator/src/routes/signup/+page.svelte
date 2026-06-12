<div class = "top-bar">
	<a href = "/charts" class = "hikari charts-button">All Charts</a>
	<a href = "/charts" class = "hikari charts-button">All Charts</a>
</div>

<script>
	import {goto} from '$app/navigation';
	import {user} from "$lib/auth";
	
	let user_name = $state("");
	let pass = $state("");
	let signup_state = $state("");

	async function signup()
	{
		const response = await fetch("http://127.0.0.1:8000/signup", {method: "POST",
		                                                              headers: {"Content-Type": "application/json"},
																	  "body": JSON.stringify({username: user_name,
																	 		                 password: pass})});
		const data = await response.json();
		if(data.success)
		{
			signup_state = "Successfully Created ACcount!";
			goto('/b30');
		}
		else
		{
			signup_state = "User Already Exists!";
		}
	}
</script>

<div class = "auth-page">
	<div class = "auth-box hikari-bg">
		<input class = "blue-text" type = "text" placeholder = "Username" bind:value={user_name}/>
		<input class = "blue-text" type = "password" placeholder = "Password" bind:value={pass}/>
		<button class = "blue-text" onclick = {signup}>Sign Up</button>
		<p class = "state">{signup_state}</p>
	</div>
</div>

<div class = "bottom-bar">
	<a href = "/login" class = "luna charts-button">Log In</a>
</div>
<div class = "bottom-bar">
	<p class = "login-signup-msg">Have an account? Log In</p>
</div>