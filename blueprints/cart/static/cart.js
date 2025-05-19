const totalLabel = document.getElementById("total");
const cartContainer = document.getElementById("cart-container");

document.querySelectorAll('.qty-field').forEach(field => {
	field.addEventListener('input', () => {
		field.value = field.value.replace(/(?!^-)-|[^-0-9]/g, '');
		updateQuantity({ cart_id: field.dataset.id, value: field.value, type: "set" });
	})
});

document.querySelectorAll('.qty-btn').forEach(btn => {
	btn.addEventListener('click', function() {
		updateQuantity({ cart_id: this.dataset.id, action: this.dataset.action, type: "increment" });
	});
});

document.querySelectorAll('.remove').forEach(remove_btn => {
	remove_btn.addEventListener('click', function () {
		const cartID = this.dataset.id;
		fetch(`cart/remove`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify({ cart_id: parseInt(cartID) }),
		})
		.then(response => response.json())
		.then(data => {
			document.getElementById(`cart-item-${cartID}`).remove();
			totalLabel.textContent  = data.new_total;
			if (document.getElementsByClassName('cart-item').length == 0) {
				document.getElementById("checkout").disabled = true;
				const emptyLabel = document.createElement('div');
				emptyLabel.className = "cart-item"
				emptyLabel.textContent = "Cart is Empty"
				cartContainer.appendChild(emptyLabel);
			}
		});
	});
});

function updateQuantity(body_data) {
	fetch(`cart/update_quantity`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
		},
		body: JSON.stringify(body_data),
	})
	.then(response => response.json())
	.then(data => {
		updatePriceDisplay(data, body_data.cart_id);
	});
}

function onCheckoutBtnClick() {
	document.location.href = "/payment";
}

function updatePriceDisplay(data, cartID) {
	document.getElementById(`qty-${cartID}`).value = data.new_quantity;
	document.getElementById(`price-qty-${cartID}`).textContent  = data.new_quantity;
	document.getElementById(`subtotal-${cartID}`).textContent  = data.new_subtotal;
	document.getElementById(`qty-down-${cartID}`).disabled = (data.status == "min");
	document.getElementById(`qty-up-${cartID}`).disabled = (data.status == "max");
	totalLabel.textContent  = data.new_total;
}
