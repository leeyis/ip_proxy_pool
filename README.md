# ip_proxy_pool

A dynamic configurable proxy IP crawler based on Scrapy. It makes it easy to crawl hundreds of thousands of proxy IPs in a short time. By maintaining a spider code and a few groups of website data extraction rules you can easily grab lots of proxy IPs of these sites. See the [blogs](http://jinbitou.net/2016/12/05/2244.html) for more detail.

##Main Requirements
For more details see requirements.txt
- Scrapy 1.2.1
- MySQL-python 1.2.5
- Redis 2.10.5
- SQLAlchemy 1.1.4

##Install in development

**CentOS**

```bash
$ sudo yum install python-devel
$ sudo yum install gcc libffi-devel openssl-devel
$ pip install scrapy
$ pip install SQLAlchemy
$ pip install redis
```
