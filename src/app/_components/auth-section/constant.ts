const logInForm: FormLoginType[] = [
	{
		name: "user_email", label: "Username", type: "text",
		on_change: async (value: string) => {
			const some_request = await fetch("http://127.0.0.1:8000/has_user", {
				method: "POST",
				headers: {
					"Content-Type": "application/json"
				},
				body: JSON.stringify({ nickname: value })
			})
				.then(response => response.json())
				.then(data => {
					console.log(data);
					console.log(data.invalidUser);
				})
		}
	},
	{ name: "password", label: "Password", type: "password" },
];
