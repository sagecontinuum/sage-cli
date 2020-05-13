# sage-cli


## install 

```bash
pip install  git+https://github.com/sagecontinuum/sage-cli.git
```

## Usage examples

```bash
export SAGE_HOST="http://localhost:8080"
export SAGE_USER_TOKEN="user:testuser" 

sage-cli.py storage bucket create --datatype model
```


Optionally wit docker (`--net` only for local test instance):
```bash
docker run -ti -e SAGE_HOST="http://sage-api:8080" -e SAGE_USER_TOKEN="user:testuser" --net sage-storage-api_default sagecontinuum/sage-cli 

sage-cli.py storage bucket create --datatype model
```



## testing

Create test environment:
```bash
git clone https://github.com/sagecontinuum/sage-storage-api.git
cd sage-storage-api
docker-compose up -d
cd ..
```

Wait a few seconds, run test:
```bash
export SAGE_USER_TOKEN=user:testuser
export SAGE_HOST=http://localhost:8080
./tests.sh
```

Clean-up:
```bash
cd sage-storage-api
docker-compose down
cd ..
rm -rf ./sage-storage-api
```



