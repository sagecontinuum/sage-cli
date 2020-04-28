# sage-cli


## install 

```bash
pip install  git+https://github.com/sagecontinuum/sage-cli.git
```

## usage

example:

```bash
sage-cli.py storage bucket create --datatype model
```



## testing


For a local test instance of the SAGE storage API use the docker-compose environment provided in the github repository of [sage-storage-api](https://github.com/sagecontinuum/sage-storage-api#getting-started)

a) With docker container
```bash
docker run -ti -e SAGE_HOST="http://sage-api:8080" -e SAGE_USER_TOKEN="user:testuser" --net sage-storage-api_default sagecontinuum/sage-cli 

sage-cli.py storage bucket create --datatype model
```

b) without docker
```bash
export SAGE_HOST="http://localhost:8080"
export SAGE_USER_TOKEN="user:testuser" 

sage-cli.py storage bucket create --datatype model
```
