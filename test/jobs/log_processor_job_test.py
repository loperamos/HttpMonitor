import datetime
import heapq

from bom.log import Log
from jobs.log_processor_job import LogProcessorJob
from processors.avg_stats_processor import AvgStatsProcessor


def test_process_average():
    bom_log_pq = [
        Log(timestamp=datetime.datetime(2018, 5, 9, 16, 0, 50, 200)),
        Log(timestamp=datetime.datetime(2018, 5, 9, 16, 0, 51, 200)),
        Log(timestamp=datetime.datetime(2018, 5, 9, 16, 0, 51, 300)),
        Log(timestamp=datetime.datetime(2018, 5, 9, 16, 0, 52, 400)),
    ]
    time_period = 2
    avg_stats_pqueue = []
    calculators = [AvgStatsProcessor(avg_stats_pqueue, time_period)]
    log_processor = LogProcessorJob(bom_log_pq, calculators, 0.1)
    log_processor.loop(blocking=False)
    assert heapq.heappop(avg_stats_pqueue) == (int(datetime.datetime(2018, 5, 9, 16, 0, 50).timestamp()), 1 / 2)
    assert heapq.heappop(avg_stats_pqueue) == (int(datetime.datetime(2018, 5, 9, 16, 0, 51).timestamp()), 3 / 2)
