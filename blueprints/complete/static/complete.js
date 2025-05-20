const deliveryFeeLabel = document.getElementById("delivery-fee");
const deliveryOption = document.getElementById("delivery-option");
const totalPriceLabel = document.getElementById("total-price");

document.addEventListener("DOMContentLoaded", () => {
	deliveryOption.value = "";
});

function onDeliverySelect(selectValue) {
	if (selectValue == "") return;
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

function formatMoney(num) {
  return "Rp. " + num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
}