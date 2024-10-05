```
pip install -r requirements.txt
```

Run `locust` to start or run docker

```bash 
docker run \
-e SOURCE_ID=5b564e75-3bd6-4da2-897a-d6de654881c1 \
-e HOST=http://192.168.1.110:8686 \
-e TYPE_OF_STRESS=regular \
-p 8089:8089 tracardi/benchmark
```

```bash
docker run \
-e SOURCE_ID=5b564e75-3bd6-4da2-897a-d6de654881c1 \
-e HOST=http://192.168.1.110:8686 \
-e TYPE_OF_STRESS=queue \
-p 8089:8089 tracardi/benchmark
```


docker run \
-e SOURCE_ID=64989dae-07ba-4de6-a7c1-c0246eee9f0f \
-e HOST=http://demo.tracardi.com \
-e TYPE_OF_STRESS=regular \
-p 8089:8089 tracardi/benchmark