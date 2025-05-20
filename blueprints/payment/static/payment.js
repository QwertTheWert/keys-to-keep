const deliveryFeeLabel = document.getElementById("delivery-fee");
const deliveryOption = document.getElementById("delivery-option");
const totalPriceLabel = document.getElementById("total-price");
const purchaseButton = document.getElementById("purchase-button");

document.addEventListener("DOMContentLoaded", () => {
	deliveryOption.value = "";
});

function onDeliverySelect(selectValue) {
	if (selectValue == "") {
		purchaseButton.disabled = true;
		return;
	} else {
		purchaseButton.disabled = false;
	}
	fetch(`payment/get_delivery_data`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
		},
		body: JSON.stringify({ value: parseInt(selectValue) }),
	})
	.then(response => response.json())
	.then(data => {
		deliveryFeeLabel.textContent = formatMoney(data.price);
		console.log(totalPriceLabel.dataset.total);
		totalPriceLabel.textContent = formatMoney(data.price + parseInt(totalPriceLabel.dataset.total));
	});
}

function onPurchaseClick() {
	fetch(`payment/create_transaction`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
		},
		body: JSON.stringify({ delivery_id: parseInt(deliveryOption.value) }),
	})
	.then(response => response.json())
	.then(data => {
		const form = document.createElement('form');
		form.method = 'POST';
		form.action = '/complete'; 
		const transactionIdInput = document.createElement('input');
		transactionIdInput.name = "transaction_id";
		transactionIdInput.value = data.transaction_id;
		transactionIdInput.type = 'hidden';
		form.appendChild(transactionIdInput);


		// Append form to body and submit
		document.body.appendChild(form);
		form.submit();
		});
}

function formatMoney(num) {
  return "Rp. " + num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
}