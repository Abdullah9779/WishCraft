 

class CSPMiddleware:
    """Simple CSP middleware that sets a Content-Security-Policy header using
    the CSP_* settings defined in settings.py. This is intentionally conservative
    to avoid breaking existing inline scripts; it includes 'unsafe-inline' for
    style/script to preserve functionality but can be tightened later.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Content Security Policy has been removed by project configuration.
        # This middleware no longer injects a Content-Security-Policy header.
        # Keeping the middleware for cache-control header behavior.

        # Add cache control headers to prevent stale content
        if request.path.startswith('/s/') or request.path.startswith('/template-url/') or request.path.startswith('/api/'):
            # Dynamic content - no cache
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
        elif request.path.endswith('.js') or request.path.endswith('.css'):
            # Static assets - cache for 1 hour
            response['Cache-Control'] = 'public, max-age=3600'
        else:
            # HTML pages - cache for 5 minutes
            response['Cache-Control'] = 'public, max-age=300'

        return response
