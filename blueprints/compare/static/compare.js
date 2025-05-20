document.querySelectorAll("`").forEach(element => {
	element.addEventListener("input", () => {
		const side = this.dataset.left;
		this.value = this.value.replace(/(?!^-)-|[^-0-9]/g, '');
		
		fetch(`compare/get_data`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify({ id: parseInt(this.value) }),
		})
		.then(response => response.json())
		.then(data => {
			if (data.valid == True) {
				document.getElementById(`cart-${side}`)
			} else {

			};
		});
	});
});