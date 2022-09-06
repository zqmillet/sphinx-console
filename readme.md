# sphinx-console

A sphinx extention that can render command in console style.

## Install 

Simply `pip install sphinx-console` and add the extention to your `conf.py`:

```
extentions = ['sphinx_console']
```

# Usage

```
.. bash:: ping www.google.com -c 4
```

```
.. bash:: ping www.google.com
    :timeout: 4
```

```
.. bash:: python3
    :interactions: [[">>>", "1 + 2"], [">>>", "exit()"]]
```

```
.. python::

    def fib(n):
        if n == 1:
            return n
        if n == 2:
            return n
        return fib(n - 1) + fib(n - 2)

    fib(10)
```

```
.. python::
    :timeout: 10

    from time import sleep
    sleep(233)
    print('wake up')
```

<pre class="body_foreground body_background" style="font-size: 10pt;color: #AAAAAA;background-color: #000000;padding: 10px; margin-bottom: 24px;overflow-x:scroll;"><span style="font-weight: bold"></span><span style="font-weight: bold; color: #aa0000">$</span><span style="font-weight: bold; color: #F5F1DE"> ping www.baidu.com -c 4</span><span style="font-weight: bold"></span>
PING www.wshifen.com (183.232.231.173) 56(84) bytes of data.
64 bytes from 183.232.231.173 (183.232.231.173): icmp_seq=1 ttl=35 time=272 ms
64 bytes from 183.232.231.173: icmp_seq=4 ttl=35 time=297 ms

--- www.wshifen.com ping statistics ---
4 packets transmitted, 2 received, 50% packet loss, time 3032ms
rtt min/avg/max/mdev = 271.577/284.227/296.877/12.650 ms
</pre>
