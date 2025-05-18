const colorContainer = document.getElementById("color-options");
const switchContainer = document.getElementById("switch-options");
const finalizeBtn = document.getElementById("finalize");	

let currentKeyboardId;
let variantInfo;

document.getElementById('price-selector').addEventListener('change', function () {
	const baseUrl = this.dataset.baseUrl;
	const ascending = this.value;
	window.location.href = `${baseUrl}?asc=${ascending}`;
});

document.querySelectorAll('.open-modal').forEach(btn => 
	btn.addEventListener('click', function () {
		currentKeyboardId = this.dataset.id;
		variantInfo = {};
		fetch(`keyboards/get_variants`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify({ keyboard_id: currentKeyboardId }),
		})
		.then(response => response.json())
		.then(data => {
			colorContainer.innerHTML = "";
			switchContainer.innerHTML = "";
			finalizeBtn.disabled = true;
			data.colors.forEach(e => {addButton(e.name, e.id, "color", colorContainer);});
			data.switches.forEach(e => {addButton(e.name, e.id, "switch", switchContainer);});
		});
	})
);

finalizeBtn.addEventListener('click', function () {
	fetch(`keyboards/add_to_cart`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
		},
		body: JSON.stringify({ keyboard_id: currentKeyboardId, variant_info : variantInfo }),
	})
	.then(response => response.json())
	.then(data => {
		alertBox.classList.remove('d-none');
		alertBox.classList.add('show');
		productNameText.textContent = data.keyboard_name;
	});
})

function addButton(text, id, variantType, container) {
	const newBtn = document.createElement('button');
	newBtn.className = "btn btn-outline-secondary " + variantType + "-btn";
	newBtn.id = variantType + "-btn-" + id;
	newBtn.dataset.id = id;
	newBtn.textContent = text;

	newBtn.onclick = () => {
		const buttons = document.querySelectorAll("." + variantType + '-btn');
		buttons.forEach(btn => btn.classList.remove('active'));
		newBtn.classList.add('active');
		variantInfo[variantType] = id;
		finalizeBtn.disabled = variantInfo["switch"] == null || variantInfo["color"] == null;
		
	}
	container.appendChild(newBtn);
}