# pycache
#### python3.9



# PYCACHE

## Start:

```python
python3 setup.py install# python server.py # for api
pythonsrc/pyredis.py # for redis-cli server
redis-cli # must install redis cli client
```

or try the api:

```bash
# post data
python3 server.py
curl --location --request POST 'http://127.0.0.1:5000/messages' \
--header 'Content-Type: application/json' \
--data-raw '{"id":1, "message":"test"}'
# get date
curl --location --request GET 'http://127.0.0.1:5000/messages/1'

# flush db
curl --location --request DELETE 'http://127.0.0.1:5000/messages/delete_all'
```

## Run test:

```python
python3 -m unittest discover -s tests/ -p 'test_*.py'
```

## Further Implementation

this is only a cache server, will need a cache client, so the server could be scaled 

- [ ]  implement a client to call this server
- [ ]  implement cache data across distributed backend servers, like use gossip protocal to spread and backup data across the distributed systems etc