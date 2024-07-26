import json
import logging
from datetime import datetime
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)


class TrackUserVisitsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Ensure the user attribute is available
        if not hasattr(request, 'user'):
            request.user = None

        # Get the cookie value for visits or initialize it as a list
        visits = request.COOKIES.get('visits', '[]')
        try:
            visits = json.loads(visits)
            if not isinstance(visits, list):
                visits = []
        except json.JSONDecodeError:
            visits = []

        logger.debug(f'Current visits: {visits}')

        # Capture visit details
        visit = {
            'user': request.user.username if request.user and request.user.is_authenticated else 'Anonymous',
            'path': request.path,
            'timestamp': datetime.now().isoformat()
        }

        # Add the new visit to the list
        visits.append(visit)
        logger.debug(f'Updated visits: {visits}')

        # Store the updated visits back into the request
        request.visits = visits

    def process_response(self, request, response):
        # Get the visits from the request
        visits = getattr(request, 'visits', [])
        logger.debug(f'Setting visits cookie: {visits}')

        # Set the cookie with the updated visits
        response.set_cookie('visits', json.dumps(visits), max_age=365 * 24 * 60 * 60)  # Cookie expires in 1 year
        return response
