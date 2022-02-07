# pycache
#### python3.9



# PYCACHE

## Start:

```python
pip install -r requirements.txt
python server.py
```

```bash
# post data
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
python3 -m pytest tests
```

## Further Implementation

this is only a cache server, will need a cache client, so the server could be scaled 

- [ ]  implement a client to call this server
- [ ]  implement cache data across distributed backend servers, like use gossip protocal to spread and backup data across the distributed systems etc