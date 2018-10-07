import logging
import os
import time

from mock import Mock, call

from common import logger_configuration
from http_monitor_builder import HttpMonitorBuilder

logger_configuration.configure_logging("regression_log.log", is_debug=True)
logger = logging.getLogger(__name__)


def init_file(log_file_path):
    open(log_file_path, 'w').write("First Line\n")


def write_log_lines(log_file_path):
    with open(log_file_path, 'a') as log_file:
        log_file.write(r'127.0.0.1 - james [09/May/2018:16:01:00 +0000] "GET /api HTTP/1.0" 200 1234' + '\n')
        log_file.write(r'127.0.0.1 - james [09/May/2018:16:01:00 +0000] "GET /api HTTP/1.0" 200 1234' + '\n')

        log_file.write(r'127.0.0.1 - james [09/May/2018:16:01:01 +0000] "GET /api HTTP/1.0" 200 1234' + '\n')
        log_file.write(r'127.0.0.1 - james [09/May/2018:16:01:01 +0000] "GET /api HTTP/1.0" 200 1234' + '\n')
        log_file.write(r'127.0.0.1 - james [09/May/2018:16:01:01 +0000] "GET /api HTTP/1.0" 200 1234' + '\n')
        log_file.write(r'127.0.0.1 - james [09/May/2018:16:01:01 +0000] "GET /api HTTP/1.0" 200 1234' + '\n')

        log_file.write(r'127.0.0.1 - james [09/May/2018:16:01:02 +0000] "GET /api HTTP/1.0" 200 1234' + '\n')
        log_file.write(r'127.0.0.1 - james [09/May/2018:16:01:02 +0000] "GET /api HTTP/1.0" 200 1234' + '\n')
        log_file.write(r'127.0.0.1 - james [09/May/2018:16:01:02 +0000] "GET /api HTTP/1.0" 200 1234' + '\n')
        log_file.write(r'127.0.0.1 - james [09/May/2018:16:01:02 +0000] "GET /api HTTP/1.0" 200 1234' + '\n')

        log_file.write(r'127.0.0.1 - james [09/May/2018:16:01:03 +0000] "GET /api HTTP/1.0" 200 1234' + '\n')
        log_file.write(r'127.0.0.1 - james [09/May/2018:16:01:03 +0000] "GET /api HTTP/1.0" 200 1234' + '\n')
        log_file.write(r'127.0.0.1 - james [09/May/2018:16:01:03 +0000] "GET /api HTTP/1.0" 200 1234' + '\n')

        log_file.write(r'127.0.0.1 - james [09/May/2018:16:01:04 +0000] "GET /api HTTP/1.0" 200 1234' + '\n')
        log_file.write(r'127.0.0.1 - james [09/May/2018:16:01:04 +0000] "GET /api HTTP/1.0" 200 1234' + '\n')

        log_file.write(r'127.0.0.1 - james [09/May/2018:16:01:05 +0000] "GET /api HTTP/1.0" 200 1234' + '\n')


def test_alert_is_triggered():
    log_file_path = "./tmp.log"
    init_file(log_file_path)
    http_monitor_builder = HttpMonitorBuilder(log_file_path)
    mocked_callback = Mock()
    http_monitor_builder.add_avg_alert(2, 3, mocked_callback)
    with http_monitor_builder.get_monitor():
        write_log_lines(log_file_path)
        time.sleep(1)
    calls = [
        call("High traffic generated an alert - hits = 3, triggered at 2018-05-09T18:01:01"),
        call("High traffic alert recovered at 2018-05-09T18:01:04")
    ]
    mocked_callback.assert_has_calls(calls)
    logger.debug("Removing file")
    if os.path.exists(log_file_path):
        os.remove(log_file_path)
