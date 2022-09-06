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
