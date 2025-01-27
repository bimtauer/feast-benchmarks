# Benchmarking Python Feature Server

Here we provide tools for benchmarking Python-based feature server with one online stores: Redis on a local Linux machine. Follow the instructions below to reproduce the benchmarks.

_Tested with: `feast 0.37.1`_

## 0. Prerequisites

`uv install`


## 1. Start local redis

`redis-server`

## 2. Generate Data

`python data_generator.py`

Please be aware that the timestamp of the generated parquet file has an experiation effect. If you try to use the generated data at a different day, it will fail the "feast materialize-increment" command in Step 4. Please generate this fake data again if no feature data is written into the Redis.  

The generated parquet file includes:  
1, 252 columns:  "entity" column, "event_timestamp" column and 250 fake "feature_[*]" columns.  
2, 10,000 rows.  
3, the value of the Datafame are randomg integers.  

The content of the parquet can be checked by following example commands:   
1, ```parquet-tools inspect generated_data.parquet```  
2, ```parquet-tools show --head 2 generated_data.parquet```  


## 3. Apply Feast Registry

Disable the USAGE feature. Apply feature definitions to create a Feast repo. 

```
export FEAST_USAGE=False
cd python_local/feature_repos/redis
feast apply
```

## 4. Materialize data to Redis

```
cd python_local/feature_repos/redis
feast materialize-incremental $(date -u +"%Y-%m-%dT%H:%M:%S")
```

## 5. Run Benchmark

```
cd python_local
pytest test.py
```

The report (or say results) of vegeta will be written to "pert.log" file.
