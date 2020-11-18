# Bot Server
This is where you will write your code for this project.

## Running the Bot server
```
$ bash run.sh
```

## Accessing the server from your local computer
After running the server, you will be able to send HTTP requests to `http://localhost:5000`

Your can test the server locally by running the following command in your terminal:
```
$ http get http://localhost:5000/
HTTP/1.0 200 OK
Content-Length: 32
Content-Type: text/html; charset=utf-8
Date: Wed, 18 Nov 2020 08:26:43 GMT
Server: Werkzeug/1.0.1 Python/3.8.5

Hello from the cs10 message bot!
```

## Accessing the server from another computer
Another computer on the same wifi network can access your bot server by using your IP address.

On a Mac, find your IP address by running the following command in your terminal:
```
$ ipconfig getifaddr en0
192.168.XX.XX
```

Give your IP address to your friend, and on their computer they can run the following command in their terminal:
(Be sure to replace the XXX with the numbers you found for your IP address!)
```
$ http get http://192.168.XXX.XX:5000/
HTTP/1.0 200 OK
Content-Length: 32
Content-Type: text/html; charset=utf-8
Date: Wed, 18 Nov 2020 08:26:43 GMT
Server: Werkzeug/1.0.1 Python/3.8.5

Hello from the cs10 message bot!
```

## Files
Here's an overview of the files in the directory and what you should do with them.

### `bot_server.py`

### `services.py`

### `helpers.py`
