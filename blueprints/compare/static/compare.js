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
				// document.getElementById(`img${side}`).src = "/static/assets/placeholder.png";
				document.getElementById(`name-${side}`).textContent = data.name;
				document.getElementById(`price-${side}`).textContent = `Rp. ${data.price}`;
				document.getElementById(`switch-type-${side}`).textContent = data.switch_type;
				document.getElementById(`keycaps-${side}`).textContent = data.keycaps;
				document.getElementById(`rating-${side}`).textContent = parseFloat(data.rating);
			} else {

			};
		});
	});
});

function resetProduct(productNum) {
	document.getElementById(`img${productNum}`).src = "/static/assets/placeholder.png";
	document.getElementById(`name${productNum}`).textContent = "-";
	document.getElementById(`price${productNum}`).textContent = "-";
	document.getElementById(`layout${productNum}`).textContent = "-";
	document.getElementById(`connection${productNum}`).textContent = "-";
	document.getElementById(`material${productNum}`).textContent = "-";
	document.getElementById(`switches${productNum}`).textContent = "-";
}

function formatPrice(price) {
	return price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
}