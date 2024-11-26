# keyValueStore
customized in memory key value store


### Docker build

1. build key value store API:
```sh
docker build -t bohuang910407/kvstore -f Dockerfile.kvstore .
```

2. build proxy API:
```sh
docker build -t bohuang910407/proxy -f Dockerfile.proxy .
```