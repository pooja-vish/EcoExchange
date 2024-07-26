import json
import logging
from datetime import datetime
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)

class TrackUserVisitsMiddleware(MiddlewareMixin):
    def __init__(self, get_response=None):
        super().__init__(get_response)
        self.get_response = get_response
        logger.info("TrackUserVisitsMiddleware initialized")

    def process_request(self, request):
        logger.info("TrackUserVisitsMiddleware process_request called")
        if not hasattr(request, 'user'):
            request.user = None

        visits = request.COOKIES.get('visits', '[]')
        try:
            visits = json.loads(visits)
            if not isinstance(visits, list):
                visits = []
        except json.JSONDecodeError:
            visits = []

        logger.debug(f'Current visits: {visits}')

        visit = {
            'user': request.user.username if request.user and request.user.is_authenticated else 'Anonymous',
            'path': request.path,
            'timestamp': datetime.now().isoformat()
        }

        visits.append(visit)
        logger.debug(f'Updated visits: {visits}')

        request.visits = visits

    def process_response(self, request, response):
        logger.info("TrackUserVisitsMiddleware process_response called")
        visits = getattr(request, 'visits', [])
        logger.debug(f'Setting visits cookie: {visits}')

        response.set_cookie('visits', json.dumps(visits), max_age=365 * 24 * 60 * 60)
        return response
