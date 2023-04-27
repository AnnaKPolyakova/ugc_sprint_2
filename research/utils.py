import logging
from datetime import datetime, timedelta
from logging.config import dictConfig

from research.test_settings import TESTS_COUNT

logging_config = {
    "version": 1,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
        }
    },
    "handlers": {
        "wsgi": {
            "class": "logging.StreamHandler",
            "stream": "ext://flask.logging.wsgi_errors_stream",
            "formatter": "default",
        }
    },
    "root": {"level": "INFO", "handlers": ["wsgi"]},
}

dictConfig(logging_config)


def measure_time(func):
    """
    Measure work time some funk with this function.

    Args:
        func (func): some funk.

    Returns:
        timedelta results.
    """
    def _wrapper(*args, **kwargs):
        try:
            max_value = timedelta(minutes=0)
            min_value = timedelta(minutes=0)
            all_result = []
            logging.info("start {name}".format(name=func.__name__))
            for count in range(TESTS_COUNT):
                logging.info(
                    "test number {count} from {TESTS_COUNT}".format(
                        TESTS_COUNT=TESTS_COUNT,
                        count=count
                    )
                )
                start = datetime.now()
                func(*args, **kwargs)
                timedelta_result = datetime.now() - start
                all_result.append(timedelta_result)
                if min_value > timedelta_result or min_value == timedelta(
                        minutes=0
                ):
                    min_value = timedelta_result
                if max_value < timedelta_result or max_value == timedelta(
                        minutes=0
                ):
                    max_value = timedelta_result
        except Exception as error:
            logging.error(
                "Test ({test}) error: {error}".format(
                    test=func.__name__,
                    error=error
                )
            )
        else:
            all_result.sort()
            all_result_len = len(all_result)
            if len(all_result) % 2 == 0:
                v1 = int(all_result_len / 2 - 1)
                v2 = int(all_result_len / 2)
                median = (all_result[v1] + all_result[v2]) / 2
            else:
                median = all_result[all_result_len // 2]
            res = (
                "Test: {func}, result: {min} - {max}, median: {median}\n".
                format(
                    func=func.__name__,
                    min=min_value,
                    max=max_value,
                    median=median
                )
            )
            with open("result.txt", "a") as result_file:
                result_file.write(
                    '{now} - {result}'.format(
                        now=str(datetime.now()),
                        result=res
                    )
                )
            logging.info(res)

    return _wrapper
