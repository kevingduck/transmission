import logging
from calendar import monthrange
from datetime import datetime
from influxdb_metrics.loader import log_metric

from rest_framework import throttling

LOG = logging.getLogger('transmission')


class MonthlyRateThrottle(throttling.SimpleRateThrottle):
    def __init__(self):
        now = datetime.now()
        # Rate limit is dynamically extracted from JWT
        self.duration = monthrange(now.year, now.month)[1] * 86400
        # Initialize here to avoid pylint error
        self.key = None
        self.history = None
        self.now = None

    def get_cache_key(self, request, view):
        if not request.user.is_authenticated:
            return None

        return request.user.token.get('organization_id', None)

    def allow_request(self, request, view):
        if request.method == 'GET':
            return True

        self.key = cache_key = self.get_cache_key(request, view)

        if not self.key:
            return True

        self.num_requests = request.user.token.get('monthly_rate_limit', None)

        if not self.num_requests:
            return True

        self.history = self.cache.get(cache_key, [])
        self.now = datetime.now().timestamp()

        # Drop any requests from the history which have now passed the
        # throttle duration
        while self.history and self.history[-1] <= self.now - self.duration:
            self.history.pop()

        if len(self.history) >= self.num_requests:
            return self.throttle_failure()

        return self.throttle_success()

    def throttle_success(self):
        """
        Inserts the current request's timestamp along with the key
        into the cache.
        """
        log_metric('transmission.info', tags={'method': 'throttling.MonthlyRateThrottle', 'module': __name__,
                                              'organization_id': self.key, 'success': True})

        return super(MonthlyRateThrottle, self).throttle_success()

    def throttle_failure(self):
        """
        Called when a request to the API has failed due to throttling.
        """
        log_metric('transmission.info', tags={'method': 'throttling.MonthlyRateThrottle', 'module': __name__,
                                              'organization_id': self.key, 'success': False})
        return super(MonthlyRateThrottle, self).throttle_failure()
