import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class RealIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        forwarded_ips = request.META.get("HTTP_X_FORWARDED_FOR")
        client_ip = forwarded_ips.split(",")[0].strip() if forwarded_ips else request.META.get("REMOTE_ADDR")
        request.META["REMOTE_ADDR"] = client_ip
        request.client_ip = client_ip

        response = self.get_response(request)
        self._log_request_response(request, response, client_ip)

        return response

    @staticmethod
    def _log_request_response(request, response, client_ip):
        """Log request and response details."""
        current_time = datetime.now().strftime("[%d/%b/%Y %H:%M:%S]")
        response_size = len(response.content) if hasattr(response, "content") else 0
        logger.info(
            f'{current_time} "{client_ip} {request.method} {request.path} HTTP/1.1" '
            f'{response.status_code} {response_size}'
        )
