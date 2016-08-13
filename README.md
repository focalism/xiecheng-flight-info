# xiecheng-flight-info
python 抓取携程国内航班机票信息

#说明
南京到青岛航班：http://flights.ctrip.com/booking/nkg-tao-day-1.html?ddate1=2016-08-17

查看网页源代码，发现并没有航班信息。用chrome浏览器的开发工具，发现请求下面路径：

http://flights.ctrip.com/domesticsearch/search/SearchFirstRouteFlights?DCity1=nkg&ACity1=tao&SearchType=S&DDate1=2016-8-14&IsNearAirportRecommond=0

可以得到航班的json数据，然后解析数据就行了。

但是携程的反爬也很厉害，请求太频繁就会限制ip，所以请求不能太快。
