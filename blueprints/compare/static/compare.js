
document.querySelectorAll("product-id-input").forEach(element => {
	element.addEventListener("input", () => {
		const side = this.dataset.side;
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
				// document.getElementById(`img${side}`).src = "/static/assets/placeholder.png";
				document.getElementById(`name-${side}`).textContent = data.keyboard_data.keyboard.name;
				document.getElementById(`price-${side}`).textContent = `Rp. ${data.keyboard_data.discounted_price}`;
				document.getElementById(`switch-type-${side}`).textContent = data.keyboard_data.switch_type;
				document.getElementById(`keycaps-${side}`).textContent = data.keyboard_data.keycaps;
				document.getElementById(`review-${side}`).textContent = data.keyboard_data.reviews.sum;
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