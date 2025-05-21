document.addEventListener('DOMContentLoaded', () => {
    const burger = document.querySelector('.burger');
    const navLinksContainer = document.querySelector('.nav-links-container');
    const nav = document.querySelector('.navbar');

    if (burger && navLinksContainer) {
        burger.addEventListener('click', () => {
            // Toggle navigation
            navLinksContainer.classList.toggle('nav-active');
            burger.classList.toggle('toggle');
        });

        // Close menu when clicking outside
        document.addEventListener('click', (e) => {
            if (!nav.contains(e.target) && navLinksContainer.classList.contains('nav-active')) {
                navLinksContainer.classList.remove('nav-active');
                burger.classList.remove('toggle');
            }
        });
    }
});
