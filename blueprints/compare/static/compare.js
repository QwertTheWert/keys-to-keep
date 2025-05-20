document.addEventListener("DOMContentLoaded", () => {
	
	document.querySelectorAll(".product-id-input").forEach(element => element.value = "");
	document.getElementById(`invalid-1`).style.display = "none";
	document.getElementById(`invalid-2`).style.display = "none";

})

document.querySelectorAll(".product-id-input").forEach(element => {
	element.addEventListener("input", () => {
		const side = element.dataset.side;
		element.value = element.value.replace(/(?!^-)-|[^-0-9]/g, '');
		console.log();
		fetch(`compare/get_data`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify({ id: parseInt(element.value) }),
		})
		.then(response => response.json())
		.then(data => {
			if (data.valid == true) {
				document.getElementById(`invalid-${side}`).style.display = "none";
				writeText(side, data.image_url, data.name, data.price, data.switch_type, data.keycaps, data.rating)
			} else {
				if (element.value != "") {
					document.getElementById(`invalid-${side}`).style.display = "block";
				};
				writeText(side, "", "-", "-", "-", "-", "-")
			};
		});
	});
});

function writeText(side, image_url, name, price, switch_type, keycaps, rating) {
	document.getElementById(`img-${side}`).src = image_url;
	document.getElementById(`name-${side}`).textContent = name;
	document.getElementById(`price-${side}`).textContent = `Rp. ${price}`;
	document.getElementById(`switch-type-${side}`).textContent = switch_type;
	document.getElementById(`keycaps-${side}`).textContent = keycaps;
	document.getElementById(`rating-${side}`).textContent = rating;
}