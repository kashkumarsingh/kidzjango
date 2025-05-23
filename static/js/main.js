document.addEventListener('DOMContentLoaded', () => {
    console.log("Kidz Runz JS loaded");

    // Dark Mode Toggle
    const toggleDarkMode = () => {
        document.body.classList.toggle('dark-mode');
        const sections = document.querySelectorAll('[data-dark-mode-bg]');
        sections.forEach(section => {
            section.style.background = section.getAttribute('data-dark-mode-bg');
        });
    };

    // Attach event listener to the dark mode toggle button
    document.querySelector('.nav__link--button')?.addEventListener('click', toggleDarkMode);
});