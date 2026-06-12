<div class = "top-bar">
	<a href = "/charts" class = "hikari charts-button">All Charts</a>
	<a href = "/charts" class = "hikari charts-button">All Charts</a>
</div>

<script>
	import {goto} from '$app/navigation';
	import {user} from "$lib/auth";
	
	let user_name = $state("");
	let pass = $state("");
	let login_state = $state("");

	async function login()
	{
		const response = await fetch("http://127.0.0.1:8000/login", {method: "POST",
		                                                             headers: {"Content-Type": "application/json"},
																	 "body": JSON.stringify({username: user_name,
																			                 password: pass})});
		const data = await response.json();
		if(data.success)
		{
			user.set({username: data.username, role: data.role});
			login_state = "Successfully Logged In!";
			goto('/b30');
		}
		else
		{
			login_state = "Wrong username or password!";
		}
	}
</script>

<div class = "auth-page">
	<div class = "auth-box tairitsu-bg">
		<input class = "pink-text" type = "text" placeholder = "Username" bind:value={user_name}/>
		<input class = "pink-text" type = "password" placeholder = "Password" bind:value={pass}/>
		<button class = "pink-text" onclick = {login}>Log in</button>
		<p class = "state">{login_state}</p>
	</div>
</div>

<div class = "bottom-bar">
	<a href = "/signup" class = "eto charts-button">Sign Up</a>
</div>
<div class = "bottom-bar">
	<p class = "login-signup-msg">New around here? Sign Up</p>
</div>