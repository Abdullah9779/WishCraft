// Service Worker Registration
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/service-worker.js?v=2')
            .then(registration => {
                console.log('SW registered');
                // Check for updates
                registration.addEventListener('updatefound', () => {
                    const newWorker = registration.installing;
                    newWorker.addEventListener('statechange', () => {
                        if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                            // New content available, refresh page
                            window.location.reload();
                        }
                    });
                });
            })
            .catch(error => console.log('SW registration failed'));
    });
}

const mobileMenuButton = document.getElementById('mobile-menu-button');
const mobileMenu = document.getElementById('mobile-menu');
// Guard in case elements are not present to avoid runtime errors
if (mobileMenuButton && mobileMenu) {
    mobileMenuButton.addEventListener('click', function () {
        const isHidden = mobileMenu.classList.toggle('hidden');
        // set aria-expanded to true when menu is visible
        mobileMenuButton.setAttribute('aria-expanded', (!isHidden).toString());
    });
}