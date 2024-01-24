<h1>0x02-redis_basic</h1>
<h1>Resources</h1>
<li><a href="https://intranet.alxswe.com/rltoken/lQ8ANhVfxDTxDr2UDSyQRA">Redis commands</a></li>
<li><a href="https://intranet.alxswe.com/rltoken/imfgFhAZPlg7YMZ_tHvFZw">Redis python client</a></li>
<li><a href="https://intranet.alxswe.com/rltoken/7SluvFvgckwVgsvrfOf1CQ">How to Use Redis With Python</a></li>
<li><a href="https://intranet.alxswe.com/rltoken/hJVo3XwMMFFoApyX8zPXvA">Redis Crash Course Tutorial</a></li>

<h1>Install Redis on Ubuntu 18.04</h1>
<pre>
$ sudo apt-get -y install redis-server
$ pip3 install redis
$ sed -i "s/bind .*/bind 127.0.0.1/g" /etc/redis/redis.conf
</pre>
<h1>Tasks</h1>
<h3>0. Writing strings to Redis</h3>
<p>
Create a Cache class. In the __init__ method, store an instance of the Redis client as a private variable named _redis (using redis.Redis()) and flush the instance using flushdb.
</p>
<p>
Create a store method that takes a data argument and returns a string. The method should generate a random key (e.g. using uuid), store the input data in Redis using the random key and return the key.
</p>
<p>
Type-annotate store correctly. Remember that data can be a str, bytes, int or float.
</p>
<pre>
bob@dylan:~$ cat main.py
#!/usr/bin/env python3
"""
Main file
"""
import redis

Cache = __import__('exercise').Cache

cache = Cache()

data = b"hello"
key = cache.store(data)
print(key)

local_redis = redis.Redis()
print(local_redis.get(key))

bob@dylan:~$ python3 main.py 
3a3e8231-b2f6-450d-8b0e-0f38f16e8ca2
b'hello'
bob@dylan:~$ 
</pre>
<b>Repo:</b>

<li>GitHub repository: alx-backend-storage</li>
<li>Directory: 0x02-redis_basic</li>
<li>File: exercise.py</li>
  
<h3>1. Reading from Redis and recovering original type</h3>
<p>
Redis only allows to store string, bytes and numbers (and lists thereof). Whatever you store as single elements, it will be returned as a byte string. Hence if you store "a" as a UTF-8 string, it will be returned as b"a" when retrieved from the server.
</p>
<p>
In this exercise we will create a get method that take a key string argument and an optional Callable argument named fn. This callable will be used to convert the data back to the desired format.
</p>
<p>
Remember to conserve the original Redis.get behavior if the key does not exist.
</p>
<p>
Also, implement 2 new methods: get_str and get_int that will automatically parametrize Cache.get with the correct conversion function.
</p>
<p>
The following code should not raise:
</p>
<pre>
cache = Cache()

TEST_CASES = {
    b"foo": None,
    123: int,
    "bar": lambda d: d.decode("utf-8")
}

for value, fn in TEST_CASES.items():
    key = cache.store(value)
    assert cache.get(key, fn=fn) == value
</pre>
<b>Repo:</b>

<li>GitHub repository: alx-backend-storage</li>
<li>Directory: 0x02-redis_basic</li>
<li>File: exercise.py</li>
  
<h3>2. Incrementing values</h3>
<p>
Familiarize yourself with the INCR command and its python equivalent.
</p>
<p>
In this task, we will implement a system to count how many times methods of the Cache class are called.
</p>
<p>
Above Cache define a count_calls decorator that takes a single method Callable argument and returns a Callable.
</p>
<p>
As a key, use the qualified name of method using the __qualname__ dunder method.
</p>
<p>
Create and return function that increments the count for that key every time the method is called and returns the value returned by the original method.
</p>
<p>
Remember that the first argument of the wrapped function will be self which is the instance itself, which lets you access the Redis instance.
</p>
<p>
Protip: when defining a decorator it is useful to use functool.wraps to conserve the original function’s name, docstring, etc. Make sure you use it as described here.
</p>
<p>
Decorate Cache.store with count_calls.
</p>
<pre>
bob@dylan:~$ cat main.py
#!/usr/bin/env python3
""" Main file """

Cache = __import__('exercise').Cache

cache = Cache()

cache.store(b"first")
print(cache.get(cache.store.__qualname__))

cache.store(b"second")
cache.store(b"third")
print(cache.get(cache.store.__qualname__))

bob@dylan:~$ ./main.py
b'1'
b'3'
bob@dylan:~$ 
</pre>
<b>Repo:</b>

<li>GitHub repository: alx-backend-storage</li>
<li>Directory: 0x02-redis_basic</li>
<li>File: exercise.py</li>
  
<h3>3. Storing lists</h3>
<p>
Familiarize yourself with redis commands RPUSH, LPUSH, LRANGE, etc.
</p>
<p>
In this task, we will define a call_history decorator to store the history of inputs and outputs for a particular function.
</p>
<p>
Everytime the original function will be called, we will add its input parameters to one list in redis, and store its output into another list.
</p>
<p>
In call_history, use the decorated function’s qualified name and append ":inputs" and ":outputs" to create input and output list keys, respectively.
</p>
<p>
call_history has a single parameter named method that is a Callable and returns a Callable.
</p>
<p>
In the new function that the decorator will return, use rpush to append the input arguments. Remember that Redis can only store strings, bytes and numbers. Therefore, we can simply use str(args) to normalize. We can ignore potential kwargs for now.
</p>
<p>
Execute the wrapped function to retrieve the output. Store the output using rpush in the "...:outputs" list, then return the output.
</p>
<p>
Decorate Cache.store with call_history.
</p>
<pre>
bob@dylan:~$ cat main.py
#!/usr/bin/env python3
""" Main file """

Cache = __import__('exercise').Cache

cache = Cache()

s1 = cache.store("first")
print(s1)
s2 = cache.store("secont")
print(s2)
s3 = cache.store("third")
print(s3)

inputs = cache._redis.lrange("{}:inputs".format(cache.store.__qualname__), 0, -1)
outputs = cache._redis.lrange("{}:outputs".format(cache.store.__qualname__), 0, -1)

print("inputs: {}".format(inputs))
print("outputs: {}".format(outputs))

bob@dylan:~$ ./main.py
04f8dcaa-d354-4221-87f3-4923393a25ad
a160a8a8-06dc-4934-8e95-df0cb839644b
15a8fd87-1f55-4059-86aa-9d1a0d4f2aea
inputs: [b"('first',)", b"('secont',)", b"('third',)"]
outputs: [b'04f8dcaa-d354-4221-87f3-4923393a25ad', b'a160a8a8-06dc-4934-8e95-df0cb839644b', b'15a8fd87-1f55-4059-86aa-9d1a0d4f2aea']
bob@dylan:~$ 
</pre>
<b>Repo:</b>

<li>GitHub repository: alx-backend-storage</li>
<li>Directory: 0x02-redis_basic</li>
<li>File: exercise.py</li>
  
<h3>4. Retrieving lists</h3>
<p>
In this tasks, we will implement a replay function to display the history of calls of a particular function.
</p>
<p>
Use keys generated in previous tasks to generate the following output:
</p>
<pre>
>>> cache = Cache()
>>> cache.store("foo")
>>> cache.store("bar")
>>> cache.store(42)
>>> replay(cache.store)
Cache.store was called 3 times:
Cache.store(*('foo',)) -> 13bf32a9-a249-4664-95fc-b1062db2038f
Cache.store(*('bar',)) -> dcddd00c-4219-4dd7-8877-66afbe8e7df8
Cache.store(*(42,)) -> 5e752f2b-ecd8-4925-a3ce-e2efdee08d20
</pre>
<p>
Tip: use lrange and zip to loop over inputs and outputs.
</p>
<b>Repo:</b>

<li>GitHub repository: alx-backend-storage</li>
<li>Directory: 0x02-redis_basic</li>
<li>File: exercise.py</li>
  
<h3>5. Implementing an expiring web cache and tracker</h3>
<p>
In this tasks, we will implement a get_page function (prototype: def get_page(url: str) -> str:). The core of the function is very simple. It uses the requests module to obtain the HTML content of a particular URL and returns it.
</p>
<p>
Start in a new file named web.py and do not reuse the code written in exercise.py.
</p>
<p>
Inside get_page track how many times a particular URL was accessed in the key "count:{url}" and cache the result with an expiration time of 10 seconds.
</p>
<p>
Tip: Use http://slowwly.robertomurray.co.uk to simulate a slow response and test your caching.
</p>
<p>
Bonus: implement this use case with decorators.
</p>
<b>Repo:</b>

<li>GitHub repository: alx-backend-storage</li>
<li>Directory: 0x02-redis_basic</li>
<li>File: web.py</li>
