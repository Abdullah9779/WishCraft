(function () {
    // Small, reliable CSRF helper for Django AJAX/fetch requests.
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
        return null;
    }

    function getCSRFToken() {
        // Prefer standard cookie 'csrftoken' (Django default)
        return getCookie('csrftoken') || '';
    }

    // Expose globals for old templates
    window.getCSRFToken = getCSRFToken;
    window.csrf = window.csrf || {};
    window.csrf.getToken = getCSRFToken;

    // Setup fetch wrapper to automatically add X-CSRFToken for same-origin POST/PUT/DELETE
    const _fetch = window.fetch;
    window.fetch = function (input, init) {
        try {
            init = init || {};
            init.headers = init.headers || {};
            const method = (init.method || 'GET').toUpperCase();
            const sameOrigin = typeof input === 'string' ? input.startsWith(window.location.origin) || input.startsWith('/') : true;
            if (['POST', 'PUT', 'PATCH', 'DELETE'].includes(method) && sameOrigin) {
                if (!init.headers['X-CSRFToken'] && !init.headers['x-csrftoken']) {
                    init.headers['X-CSRFToken'] = getCSRFToken();
                }
            }
        } catch (err) {
            // ignore
        }
        return _fetch(input, init);
    };

    // If jQuery is present, set the default header
    if (window.jQuery) {
        window.jQuery.ajaxSetup({
            beforeSend: function (xhr, settings) {
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader('X-CSRFToken', getCSRFToken());
                }
            }
        });
    }
})();
