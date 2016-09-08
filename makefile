run:
	python python/server.py

stop:
	- lsof -i tcp:8000|awk '{print $2}' |tail -1 |xargs kill i

.PONY:stop
