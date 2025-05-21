const slider = document.querySelector(".slider");
const slides = document.querySelectorAll(".slide");
const dots = document.querySelectorAll(".dot");

let currentIndex = 1; // Karena kita tambah dummy slide di awal
const totalSlides = slides.length + 2; // Tambah dummy awal & akhir

// Duplikasi slide pertama & terakhir
const firstClone = slides[0].cloneNode(true);
const lastClone = slides[slides.length - 1].cloneNode(true);

slider.appendChild(firstClone);
slider.insertBefore(lastClone, slider.firstChild);

// Geser ke slide pertama (bukan dummy) pas awal
slider.style.transform = `translateX(-100%)`;

function moveSlide(step) {
    currentIndex += step;
    updateSlider();
}

function updateSlider() {
    slider.style.transition = "transform 0.5s ease-in-out";
    slider.style.transform = `translateX(${-currentIndex * 100}%)`;

    // Reset posisi setelah animasi selesai (untuk efek infinite loop)
    slider.addEventListener("transitionend", () => {
        if (currentIndex === totalSlides - 1) {
            slider.style.transition = "none";
            currentIndex = 1;
            slider.style.transform = `translateX(-100%)`;
        } else if (currentIndex === 0) {
            slider.style.transition = "none";
            currentIndex = totalSlides - 2;
            slider.style.transform = `translateX(${-currentIndex * 100}%)`;
        }
    });

    dots.forEach((dot, i) => {
        dot.classList.toggle("active", i === currentIndex - 1); // Karena ada dummy di depan
    });
}

function currentSlide(index) {
    currentIndex = index + 1; // Sesuaikan karena dummy slide
    updateSlider();
}

document.addEventListener('DOMContentLoaded', function() {
    const track = document.querySelector('.carousel-track');
    const images = Array.from(track.children);
    const imageWidth = images[0].getBoundingClientRect().width;

    // Clone the images to create an infinite loop effect
    images.forEach(image => {
        const clone = image.cloneNode(true);
        track.appendChild(clone);
    });

    // Set the animation duration based on the number of images
    const totalWidth = imageWidth * images.length;
    track.style.width = `${totalWidth * 2}px`;
    track.style.animationDuration = `${images.length * 5}s`;

    // Function to reset the animation
    function resetAnimation() {
        track.style.animation = 'none';
        track.offsetHeight; // Trigger reflow
        track.style.animation = `scroll ${images.length * 5}s linear infinite`;
    }

    // Add event listener to reset animation when it ends
    track.addEventListener('animationiteration', resetAnimation);
});

var copy = document.querySelector(".logos-slide").cloneNode(true);
document.querySelector(".logos").appendChild(copy);

function enableDragScroll(selector) {
    const containers = document.querySelectorAll(selector);
    containers.forEach(container => {
        let isDown = false;
        let startX;
        let scrollLeft;

        container.addEventListener('mousedown', (e) => {
            isDown = true;
            container.classList.add('active');
            startX = e.pageX - container.offsetLeft;
            scrollLeft = container.scrollLeft;
        });
        container.addEventListener('mouseleave', () => {
            isDown = false;
            container.classList.remove('active');
        });
        container.addEventListener('mouseup', () => {
            isDown = false;
            container.classList.remove('active');
        });
        container.addEventListener('mousemove', (e) => {
            if (!isDown) return;
            e.preventDefault();
            const x = e.pageX - container.offsetLeft;
            const walk = (x - startX) * 1.5; // scroll-fast
            container.scrollLeft = scrollLeft - walk;
        });

        // Touch events for mobile
        container.addEventListener('touchstart', (e) => {
            isDown = true;
            startX = e.touches[0].pageX - container.offsetLeft;
            scrollLeft = container.scrollLeft;
        });
        container.addEventListener('touchend', () => {
            isDown = false;
        });
        container.addEventListener('touchmove', (e) => {
            if (!isDown) return;
            const x = e.touches[0].pageX - container.offsetLeft;
            const walk = (x - startX) * 1.5;
            container.scrollLeft = scrollLeft - walk;
        });
    });
}

// Enable drag-scroll for both containers
document.addEventListener('DOMContentLoaded', function() {
    enableDragScroll('.trending-items-container');
    enableDragScroll('.newest-items-container');
});