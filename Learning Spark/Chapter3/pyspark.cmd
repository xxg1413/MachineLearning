In [1]: log = sc.textFile("nginx_log")

In [2]: log.count()
Out[2]: 5144

In [3]: misc_flag = log.filter(lambda x: "misc.flag" in x)


In [5]: misc_flag.count()
Out[5]: 254



In [6]: for line in misc_flag.take(3):
   ...:     print line
   ...:
192.168.52.1 - - [06/Nov/2015:19:33:05 -0800] "GET /phpcode/rctf/misc/index.php?id=1%20AND%203720%3DIF%28%28ORD%28MID%28%28SELECT%20IFNULL%28CAST%28COUNT%28%2A%29%20AS%20CHAR%29%2C0x20%29%20FROM%20misc.flag%29%2C1%2C1%29%29%3E51%29%2CSLEEP%281%29%2C3720%29 HTTP/1.1" 200 5 "-" "sqlmap/1.0-dev (http://sqlmap.org)" "-"
192.168.52.1 - - [06/Nov/2015:19:33:06 -0800] "GET /phpcode/rctf/misc/index.php?id=1%20AND%203720%3DIF%28%28ORD%28MID%28%28SELECT%20IFNULL%28CAST%28COUNT%28%2A%29%20AS%20CHAR%29%2C0x20%29%20FROM%20misc.flag%29%2C1%2C1%29%29%3E48%29%2CSLEEP%281%29%2C3720%29 HTTP/1.1" 200 5 "-" "sqlmap/1.0-dev (http://sqlmap.org)" "-"
192.168.52.1 - - [06/Nov/2015:19:33:06 -0800] "GET /phpcode/rctf/misc/index.php?id=1%20AND%203720%3DIF%28%28ORD%28MID%28%28SELECT%20IFNULL%28CAST%28COUNT%28%2A%29%20AS%20CHAR%29%2C0x20%29%20FROM%20misc.flag%29%2C1%2C1%29%29%3E49%29%2CSLEEP%281%29%2C3720%29 HTTP/1.1" 200 5 "-" "sqlmap/1.0-dev (http://sqlmap.org)" "-"


发现不同点： E51 E48 E49


