const quantityField = document.getElementById('qty-field');
const addToCartBtn = document.getElementById('add-to-cart-btn');
const buyNowBtn = document.getElementById('by-now-btn');
const alertBox = document.getElementById("alert");
const copiedText = document.getElementById("copied-text");

let variantInfo;
let keyboardId;


document.addEventListener('DOMContentLoaded', () => {
	variantInfo = {
		"color" : document.body.dataset.color,
		"switch" : document.body.dataset.switch,
	}
	keyboardId = document.body.dataset.id;
});

function onVariantBtnClick(btn, variantType)  {
	const buttons = document.querySelectorAll("." + variantType + '-btn');
	buttons.forEach(otherBtn => otherBtn.classList.remove('active'));
	btn.classList.add('active');
	variantInfo[variantType] = btn.dataset.id;
}

quantityField.addEventListener("input", () => {
	quantityField.value = quantityField.value.replace(/(?!^-)-|[^-0-9]/g, '');
	console.log(quantityField.max);
	console.log(quantityField.value);
    if (parseInt(quantityField.value) > quantityField.max) {
      quantityField.value = quantityField.max;
    }
});

function onAddtoCartClick() {
	fetch(`/keyboard/add_to_cart`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
		},
		body: JSON.stringify({ keyboard_id: keyboardId, variant_info : variantInfo, quantity : quantityField.value }),
	})
	.then(response => response.json())
	.then(data => {
		if (data.success) {
			alertBox.classList.remove('d-none');
			alertBox.classList.add('show');
		} else {
			window.location.href = '/login';
		}
	});
}

function copyID(id) {
	navigator.clipboard.writeText(id);
	copiedText.style.display = "inline";
}