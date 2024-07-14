import os
import time
import statistics
from logging import getLogger, basicConfig, INFO
from datetime import datetime
#from elasticsearch.client import IndicesClient #Elastiのキャッシュ消すよう
from elasticsearch import Elasticsearch

# Ignore warning message
import warnings
from elasticsearch.exceptions import ElasticsearchWarning

logger = getLogger(__name__)

# CHAR_GREEN = '\033[32m'
# CHAR_RESET = '\033[0m'
# FORMAT = f"{CHAR_GREEN}%(asctime)s %(levelname)s %(name)s {CHAR_RESET}: %(message)s"
FORMAT = f"%(asctime)s %(levelname)s %(name)s : %(message)s"

current_time = datetime.now()
timestamp = current_time.strftime("%Y%m%d_%H%M%S")
filename = f"exp_{timestamp}.txt"
basicConfig(format=FORMAT, level=INFO, filename=filename, filemode='a')


warnings.simplefilter("ignore", ElasticsearchWarning)

# Create connection to elasticsearch
es_host = os.getenv("ES_HOST", "localhost")
es = Elasticsearch(f"http://{es_host}:31895")
es_index = os.getenv("ES_INDEX_NAME", "logstash")
#indices_client = IndicesClient(es)#キャッシュ消すよう

def clear_cache():　#キャッシュ削除
    logger.info("Start clear_cache()")
    res = es.indices.clear_cache(
        request=True,  # Purge request-cache
        fielddata=True,  # Purge field-data-cache
        query=True,  # Purge query-cache
    )
    #indices_client.clear_cache()
    logger.info("Finish clear_cache_result " + str(res))

def q_single_trace(trace_id: str):　#クエリ作成
    logger.info("Start q_single_trace()")
    _query = {
        "bool": {
            "must": [
                {
                    "term": {
                        "kubernetes.namespace": "wordpress"
                    }
                }
            ]
        }
    }

    start_time = time.time()
    resp = es.search(index=es_index, query=_query, size=10000)
    logger.info(f"Found: {resp['hits']['total']}")
    elapsed_time = time.time() - start_time
    return (elapsed_time, resp)

"""
Collection of sample data
0a6aedee1ab8e07bf2194750aea6cd17 14
1bab7367306bccb4df20d4b7104dd5f4 14
2ae99ad9d3f98a96b6860a71f53c4fcb 14
5b6f806669b0fc4b36919663569f8854 14
47e426b544f8d48b3c3904674e5e9590 13
5682508746d8551c09956a8cc93735c8 13
"""

def main():
    default_trace_id = "0a6aedee1ab8e07bf2194750aea6cd17"
    trace_id = os.getenv("TRACE_ID", default_trace_id)
    if trace_id == default_trace_id:
        logger.info("Detault trace_id")
    else:
        logger.info("trace_id: " + trace_id)

    logger.info("Start issuer")

    t_buffer = set()
    n_buffer = set()
    iteration = int(os.getenv("ISSUER_COUNT", 100))　#ここで測定回数指定
    

    for j in range(iteration):#なし版
        clear_cache()　#キャッシュ削除関数呼び出し
        n, res = q_single_trace(trace_id=trace_id)
        logger.info("_measure_ Cached nashi time: " + str(n))
        n_buffer.add(n)

    for i in range(iteration):
        t, res = q_single_trace(trace_id=trace_id)
        logger.info("_measure_ Cached time: " + str(t))
        t_buffer.add(t)
    #logger.info(f"Set contents: {n_buffer}")

    logger.info("_measure_ breakdown nashi: " + ",".join(map(str, n_buffer))) #なし版
    logger.info("_measure_ mean nashi: " + str(statistics.mean(n_buffer)))
    logger.info("_measure_ median nashi: " + str(statistics.median(n_buffer)))

    logger.info("_measure_ breakdown: " + ",".join(map(str, t_buffer)))
    logger.info("_measure_ mean: " + str(statistics.mean(t_buffer)))
    logger.info("_measure_ median: " + str(statistics.median(t_buffer)))


if __name__ == "__main__":
     main()
