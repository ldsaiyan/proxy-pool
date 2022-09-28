## ProxyPool
简单爬虫代理池项目，提供如下功能：

- 爬取免费代理网站，可扩展。
- 提供代理API，方便获取可用代理。
- 使用Redis存储代理，并对代理进行分值存储。
- 评分方式，多次验证代理可用性并进行评分。

## 运行项目
#### 安装依赖:
```bash
pip install -r requirements.txt
```

### 启动项目:
程序分为: schedule调度程序 和 Api服务

常规运行：
```bash
# 启动schedule程序
python main.py schedule
# 启动webApi服务
python main.py api
```


## 使用

- Schedule服务

调度程序为周期执行的程序，可在setting.py设置执行周期HOUR，默认为每6小时执行一次。

- Api服务

启动web服务后, 默认配置下会开启 http://127.0.0.1:9999 的api接口服务，只需启动一次，具体接口信息如下：

| api | method | Description | params|
| ----| ---- | ---- | ----|
| / | GET | 获取api列表 | None |
| /get | GET | 获取指定类型的所有代理| 参数: `?type=http`|
| /random | GET | 获取指定类型的一个高分值代理| 参数: `?type=http`|
| /all | GET | 获取所有代理 |可选参数: `?type=http`|
| /count | GET | 获取所有代理数量或指定类型的代理数量 |可选参数: `?type=http`|
| /delete | GET | 暂不实现  |None|



## 免费代理源

   目前使用爬取的免费代理网站有：
   
  |   代理名称   |  状态  |  可用率  |  地址 |
  | ---------   |  ---- | ------  | ----- |
  | 66代理     |  ✔    |   *     | [地址](http://www.66ip.cn/)
  | 云代理       |  ✔    |   *     | [地址](http://www.ip3366.net/)     
  | 89代理      |  ✔    |   *     | [地址](https://www.89ip.cn/)     

## 可设置选项
可自定义设置一些环境变量参数


### Redis连接
- REDIS_HOST：指定Redis服务IP
- REDIS_PORT：指定Redis服务端口
- REDIS_PASSWORD：指定Redis服务连接密码
- MAX_SCORE：指定Redis有序集合中代理的最大分数
- MIN_SCORE：指定Redis有序集合中代理的最小分数
- INITIAL_SCORE：指定Redis有序集合中代理的初始分数
- REDIS_KEY：指定Redis 储存代理使用的键


### Api服务
- API_HOST：指定API服务的IP
- API_PORT：指定API服务的端口


## ToDo List
- 新增多种代理协议


## LICENSE
MIT