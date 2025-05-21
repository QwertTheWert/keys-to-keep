const colorContainer = document.getElementById("color-options");
const switchContainer = document.getElementById("switch-options");
const finalizeBtn = document.getElementById("finalize");	
const alertBox = document.getElementById("alert");
const productNameText = document.getElementById("product-name");

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
		fetch(`marketplace/get_variants`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify({ keyboard_id: currentKeyboardId }),
		})
		.then(response => response.json())
		.then(data => {
			if (data.success) {
				colorContainer.innerHTML = "";
				switchContainer.innerHTML = "";
				finalizeBtn.disabled = true;
				data.colors.forEach(e => {addButton(e.name, e.id, "color", colorContainer);});
				data.switches.forEach(e => {addButton(e.name, e.id, "switch", switchContainer);});
			}  else {
				window.location.href = '/login';
			}
		});
	})
);

finalizeBtn.addEventListener('click', function () {
	fetch(`/keyboard/add_to_cart`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
		},
		body: JSON.stringify({ keyboard_id: currentKeyboardId, variant_info : variantInfo, quantity : 1 }),
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

document.addEventListener('DOMContentLoaded', function () {
    // Get all product containers
    const productContainers = document.querySelectorAll('.product-container');
    
    productContainers.forEach(container => {
        // Check if we're in compare mode
        if (container.dataset.compareEnabled === 'true') {
            container.addEventListener('click', function(e) {
                // Prevent default link behavior 
                e.preventDefault();
                
                // Get keyboard ID
                const keyboardId = this.dataset.keyboardId;
                
                // Get compare slot from session storage
                const compareSlot = sessionStorage.getItem('compareSlot');
                
                // Add to compare products
                let compareProducts = JSON.parse(sessionStorage.getItem('compareProducts') || '[]');
                
                if (compareSlot) {
                    // Set product for specific slot
                    compareProducts[parseInt(compareSlot) - 1] = keyboardId;
                } else {
                    // Add as next available product
                    if (compareProducts.length < 2) {
                        compareProducts.push(keyboardId);
                    }
                }
                
                // Save back to session storage
                sessionStorage.setItem('compareProducts', JSON.stringify(compareProducts));
                
                // Clear compare slot
                sessionStorage.removeItem('compareSlot');
                
                // Redirect back to compare page
                window.location.href = '/compare';
            });
        }
    });
});