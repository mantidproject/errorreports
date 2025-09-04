import logging
from services.tasks import send_logging_output_to_slack
import threading

logger = logging.getLogger(__name__)


class SlackHandler(logging.Handler):
    def emit(self, record):
        try:
            msg = self.format(record)
            notification_thread = threading.Thread(
                target=send_logging_output_to_slack, args=(msg,)
            )
            notification_thread.start()
        except Exception as e:
            # This logger is not Django logger so will
            # not come back here causing recurion.
            # Will instead be handled by the Root
            # logger which prints to console
            logger.error({e})
