# Cache_Measurement

# 目的
 Elastisearchのキャッシュありとキャッシュなしの検索時間を測定する．

# 使い方
検索が終わるとexe~.txtファイルが作成されます．そこにキャッシュありとなしそれぞれのリスト，中央値，平均値が算出されます．

# 変更する所
自分のElastisearchサーバーのホスト名，ポート番号，検索したいindex名に変更する．
```
# Create connection to elasticsearch
es_host = os.getenv("ES_HOST", "localhost")
es = Elasticsearch(f"http://{es_host}:31895")
es_index = os.getenv("ES_INDEX_NAME", "logstash")
```
検索したいクエリに変更する．
```
def q_single_trace(trace_id: str):
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
```
検索したい回数に変更する．
```
iteration = int(os.getenv("ISSUER_COUNT", 100))
```

# 実行した際に作成されるファイルの中身の例

```
2024-07-28 17:02:15,613 INFO __main__ : Default trace_id
2024-07-28 17:02:15,613 INFO __main__ : Start issuer
2024-07-28 17:02:15,613 INFO __main__ : Start clear_cache()
2024-07-28 17:02:15,619 INFO elastic_transport.transport : POST http://localhost:30594/_cache/clear?fielddata=true&query=true&request=true [status:200 duration:0.006s]
2024-07-28 17:02:15,619 INFO __main__ : Finish clear_cache_result {'_shards': {'total': 4, 'successful': 4, 'failed': 0}}
2024-07-28 17:02:15,619 INFO __main__ : Start clear_cache()
2024-07-28 17:02:15,620 INFO elastic_transport.transport : POST http://localhost:30594/_cache/clear?fielddata=true&query=true&request=true [status:200 duration:0.001s]
2024-07-28 17:02:15,620 INFO __main__ : Finish clear_cache_result {'_shards': {'total': 4, 'successful': 4, 'failed': 0}}
2024-07-28 17:02:15,620 INFO __main__ : Start q_single_trace()
2024-07-28 17:02:15,867 INFO elastic_transport.transport : POST http://localhost:30594/eclog2/_search [status:200 duration:0.234s]
2024-07-28 17:02:15,871 INFO __main__ : Found: 984 hits
2024-07-28 17:02:15,871 INFO __main__ : _measure_ Cached nashi time: 0.2511575222015381
2024-07-28 17:02:15,871 INFO __main__ : Hits: 984
2024-07-28 17:02:15,871 INFO __main__ : Start q_single_trace()
2024-07-28 17:02:16,411 INFO elastic_transport.transport : POST http://localhost:30594/eclog2/_search [status:200 duration:0.539s]
2024-07-28 17:02:16,417 INFO __main__ : Found: 984 hits
2024-07-28 17:02:16,417 INFO __main__ : _measure_ Cached time: 0.5450534820556641
2024-07-28 17:02:16,417 INFO __main__ : Hits: 984
2024-07-28 17:02:16,417 INFO __main__ : _measure_ breakdown nashi: 0.2511575222015381
2024-07-28 17:02:16,417 INFO __main__ : _measure_ mean nashi: 0.2511575222015381
2024-07-28 17:02:16,417 INFO __main__ : _measure_ median nashi: 0.2511575222015381
2024-07-28 17:02:16,417 INFO __main__ : _measure_ breakdown: 0.5450534820556641
2024-07-28 17:02:16,417 INFO __main__ : _measure_ mean: 0.5450534820556641
2024-07-28 17:02:16,417 INFO __main__ : _measure_ median: 0.5450534820556641
```
