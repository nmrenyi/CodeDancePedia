# coding=utf-8

'''Test RPC connecting time on docker.'''

import time
import logging
from rpc_client import test_rpc

if __name__ == "__main__":
    logging.basicConfig(level=logging.NOTSET)
    TIME_START = time.time()
    logging.info(test_rpc())
    TIME_END = time.time()
    logging.info("Elasped time: %.4fs", TIME_END-TIME_START)
