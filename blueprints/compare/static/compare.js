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

function loadProduct(productNum) {
    const productId = document.getElementById(`product${productNum}-id`).value;
    
    if (!productId) {
        alert('Please enter a product ID');
        return;
    }

    fetch(`/keyboard/details/${productId}`, {  // Changed API endpoint
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Product not found');
        }
        return response.json();
    })
    .then(data => {
        const keyboard = data.keyboard;  // Adjust based on your response structure
        document.getElementById(`product${productNum}-placeholder`).innerHTML = `
            <img src="/static/assets/xera87.jpg" alt="${keyboard.name}" class="product-image">
            <h3 class="product-name">${keyboard.name}</h3>
            <p class="product-price">Rp ${formatPrice(keyboard.price)}</p>
        `;
        
        // Update comparison details
        document.getElementById(`layout${productNum}`).textContent = keyboard.layout;
        document.getElementById(`connection${productNum}`).textContent = keyboard.connection;
        document.getElementById(`material${productNum}`).textContent = keyboard.case_material;
        document.getElementById(`switches${productNum}`).textContent = keyboard.switches.join(', ');
    })
    .catch(error => {
        alert('Error: Product not found');
        console.error('Error:', error);
    });
}

function formatPrice(price) {
    return price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
}