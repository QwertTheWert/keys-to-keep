
document.querySelectorAll("`").forEach(element => {
	element.addEventListener("input", () => {
		const side = this.dataset.left;
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
				document.getElementById(`cart-${side}`)
			} else {

			};
		});
	});
});

document.addEventListener('DOMContentLoaded', function() {
    // Fetch keyboards and populate dropdowns
    fetch('/api/keyboards')
        .then(response => response.json())
        .then(keyboards => {
            const select1 = document.getElementById('select1');
            const select2 = document.getElementById('select2');
            
            keyboards.forEach(keyboard => {
                select1.innerHTML += `
                    <option value="${keyboard.id}">${keyboard.name}</option>
                `;
                select2.innerHTML += `
                    <option value="${keyboard.id}">${keyboard.name}</option>
                `;
            });
        });

    // Check for products in session storage
    const compareProducts = JSON.parse(sessionStorage.getItem('compareProducts') || '[]');
    
    // Load products if they exist
    if (compareProducts[0]) {
        updateProductDetails(compareProducts[0], '1');
    }
    if (compareProducts[1]) {
        updateProductDetails(compareProducts[1], '2');
    }
});

function updateProduct1(keyboardId) {
    if (keyboardId === document.getElementById('select2').value) {
        alert('Please select a different keyboard');
        document.getElementById('select1').value = "0";
        return;
    }
    updateProductDetails(keyboardId, '1');
}

function updateProduct2(keyboardId) {
    if (keyboardId === document.getElementById('select1').value) {
        alert('Please select a different keyboard');
        document.getElementById('select2').value = "0";
        return;
    }
    updateProductDetails(keyboardId, '2');
}

function updateProductDetails(keyboardId, productNum) {
    if (keyboardId === "0") {
        resetProduct(productNum);
        return;
    }

    fetch(`/api/keyboards/${keyboardId}`)
        .then(response => response.json())
        .then(keyboard => {
            document.getElementById(`img${productNum}`).src = keyboard.image_url;
            document.getElementById(`name${productNum}`).textContent = keyboard.name;
            document.getElementById(`price${productNum}`).textContent = `Rp ${formatPrice(keyboard.price)}`;
            document.getElementById(`layout${productNum}`).textContent = keyboard.layout;
            document.getElementById(`connection${productNum}`).textContent = keyboard.connection;
            document.getElementById(`material${productNum}`).textContent = keyboard.case_material;
            document.getElementById(`switches${productNum}`).textContent = keyboard.switch_options.join(', ');
        });
}

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

function addToCompare(productId) {
    let compareProducts = JSON.parse(sessionStorage.getItem('compareProducts') || '[]');
    
    if (compareProducts.length === 0) {
        compareProducts.push(productId);
        sessionStorage.setItem('compareProducts', JSON.stringify(compareProducts));
        showModal();
    } else if (compareProducts.length === 1) {
        if (compareProducts[0] === productId) {
            alert('This product is already selected for comparison');
            return;
        }
        compareProducts.push(productId);
        sessionStorage.setItem('compareProducts', JSON.stringify(compareProducts));
        window.location.href = '/compare';
    }
}

function showModal() {
    const modal = document.createElement('div');
    modal.className = 'compare-modal';
    modal.innerHTML = `
        <div class="compare-modal-content">
            <h3>Product added for comparison</h3>
            <button onclick="window.location.href='/keyboards?compare=true'">
                Select another product
            </button>
            <button onclick="window.location.href='/compare'">
                View comparison
            </button>
        </div>
    `;
    document.body.appendChild(modal);
}

function resetComparison() {
    sessionStorage.removeItem('compareProducts');
    location.reload();
}
