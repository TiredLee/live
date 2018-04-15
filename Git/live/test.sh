#!/bin/bash

mysql -uroot -proot << EOF
use live;
truncate room;
EOF

scrapy crawl douyu &
scrapy crawl longzhu &
scrapy crawl yy &
scrapy crawl zhanqi &
scrapy crawl panda &
wait

echo 'db is ok'

cd web
gunicorn -w 4 -b 127.0.0.1:8080 live:app






