---
title: Redis小入门
date: 2016-08-21 14:19:13
tags:
- Redis
- 数据库
---

两年前买了<redis 设计与实现>， 可是一直都没有拿起来研究，最近team使用Redis，才开始有所了解，捡回来重新看看。

总结一些基本的不能更基本的知识：

## 数据结构

* 字符串 - String

  string类型是二进制安全的。意思是redis的string可以包含任何数据。比如jpg图片或者序列化的对象 。
  string类型是Redis最基本的数据类型，一个键最大能存储512MB。
  ```
  set key value [EX seconds] [PX milliseconds] [NX|XX]
  get key
  ```

  例：
  ```
  127.0.0.1:6379> set string 'hello'
  OK
  127.0.0.1:6379> get string 
  "hello"
  ```
<!-- more -->
* 哈希 - Hash

  Redis hash 是一个键值对集合。
  Redis hash是一个string类型的field和value的映射表，hash特别适合用于存储对象。
  每个 hash 可以存储 232 - 1 键值对（40多亿）。
  ```
  hset key field value    
  hget key field
  hgetall key
  
  hmset key field value [field value ...]
  hmget key field [field ...]
  ```

  例：
  ```
  127.0.0.1:6379> hset hash name 'redis'
  (integer) 1   -- 返回添加hash的键值对数
  127.0.0.1:6379> hget hash key2
  "value3"
  127.0.0.1:6379> hgetall hash
  1) "key2"
  2) "value3"
  3) "name"
  4) "redis"
  127.0.0.1:6379> hmset hash age 24 gender male
  OK
  127.0.0.1:6379> hmget hash key2 name
  1) "value3"
  2) "redis"
  ```

## 列表 List

Redis 列表是简单的字符串列表，按照插入顺序排序。你可以添加一个元素导列表的头部（左边）或者尾部（右边）。
列表最多可存储 2^32 - 1 元素 (4294967295, 每个列表可存储40多亿)。
```
lpush key value [value ...]
rpush key value [value ...]
lrange key start stop
```

例：
```
127.0.0.1:6379> lpush userlist user1
(integer) 1
127.0.0.1:6379> rpush userlist user2 user3
(integer) 3  -- 返回 list的大小
127.0.0.1:6379> lrange userlist 0 -1
1) "user1"
2) "user2"
3) "user3"    
```

## 集合 -- Set
Redis的Set是string类型的无序集合。
集合是通过哈希表实现的，所以添加，删除，查找的复杂度都是O(1)
根据集合内元素的唯一性，第二次插入的元素将被忽略。
集合中最大的成员数为 2^32 -1(4294967295,每个集合可存储40多亿个成员)
```
sadd key member [member ...]
smembers key
```

例：
```
127.0.0.1:6379> sadd set card1
(integer) 1
127.0.0.1:6379> sadd set card1
(integer) 0
127.0.0.1:6379> smembers set
1) "item2"
2) "item3"
3) "card1"
```

## 有序集合 Zset
Redis zset 和 set一样也是string类型元素的集合,且不允许重复的成员。
不同的是每个元素都会关联一个double类型的分数。redis正是通过分数来为集合中的成员进行从小到大的排序。

zset的成员是唯一的,但分数(score)却可以重复。

```
zadd key [NX|XX] [CH] [INCR] score member [score member ...]
zrange key start stop [WITHSCORES]
zrangebyscore key min max [WITHSCORES] [LIMIT offset count]
```

例：
```
127.0.0.1:6379> zadd test 97 math
(integer) 1
127.0.0.1:6379> zadd test 98 chinese
(integer) 1
127.0.0.1:6379> zrange test  0 10 withscores
1) "math"
2) "97"
3) "chinese"
4) "98"
127.0.0.1:6379> zrangebyscore test 98 100
1) "chinese"
```
