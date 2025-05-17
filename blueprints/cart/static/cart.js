document.querySelectorAll('.qty-field').forEach(field => {
		field.addEventListener('keydown', function (event) {
			if (event.key === "Enter") {
				
				onQuantityFieldSet(this);
			}
		});
	});

	document.querySelectorAll('.qty-btn').forEach(btn => {
		btn.addEventListener('click', function() {
			const action = this.dataset.action;
			const cartID = this.dataset.id;
			const total = document.getElementById("total").textContent.replace(/\./g, '');

			fetch(`cart/increment_quantity`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({ cart_id: cartID, action: action, total : total }),
			})
			.then(response => response.json())
			.then(data => {
				update_price_display(data, cartID);
			});
		});
	});

	document.querySelectorAll('.remove').forEach(remove_btn => {
		remove_btn.addEventListener('click', function () {
		const cartID = this.dataset.id;
		const total = document.getElementById("total").textContent.replace(/\./g, '');

		fetch(`cart/remove`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify({ cart_id: this.dataset.id, total : total }),
		})
		.then(response => response.json())
		.then(data => {
			document.getElementById(`cart-item-${cartID}`).remove();
			document.getElementById(`total`).textContent  = data.new_total;
			if (document.getElementsByClassName('.cart-item').length == 0) {
				document.getElementById("checkout").disabled = true;
			}
		});
	});
	});

	function onQuantityFieldSet(field) {
		const value = field.value;
		const cartID = field.dataset.id;
		const total = document.getElementById("total").textContent.replace(/\./g, '');

		
		fetch(`cart/set_quantity`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify({ cart_id: cartID, value: value, total : total }),
		})
		.then(response => response.json())
		.then(data => {
			update_price_display(data, cartID);
		});
	}

	function update_price_display(data, cartID) {
		document.getElementById(`qty-${cartID}`).value = data.new_quantity;
		document.getElementById(`price-qty-${cartID}`).textContent  = data.new_quantity;
		document.getElementById(`subtotal-${cartID}`).textContent  = data.new_subtotal;
		document.getElementById(`total`).textContent  = data.new_total;
		document.getElementById(`qty-down-${cartID}`).disabled = (data.status == "min");
		document.getElementById(`qty-up-${cartID}`).disabled = (data.status == "max");
	}