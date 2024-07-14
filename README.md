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
