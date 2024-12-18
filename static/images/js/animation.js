// Fade-in animation for the main content
document.addEventListener('DOMContentLoaded', function () {
    const mainContent = document.querySelector('.main-content');
    mainContent.style.opacity = 0;
    mainContent.style.transition = 'opacity 2s';

    // Apply the fade-in effect after a small delay
    setTimeout(() => {
        mainContent.style.opacity = 1;
    }, 5000);
});

// Navbar link hover animation
const navLinks = document.querySelectorAll('.navbar .nav-link');
navLinks.forEach(link => {
    link.addEventListener('mouseover', () => {
        link.style.color = '#ffcc00'; // Highlight color
        link.style.transition = 'color 0.3s';
    });

    link.addEventListener('mouseout', () => {
        link.style.color = 'white'; // Default color
    });
});
