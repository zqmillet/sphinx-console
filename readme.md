# sphinx-console

A Sphinx extention that can render command in console style.

This repository contains:

- The source code of sphinx-console extention.
- The source code of sphinx-console document.
- The test cases of sphinx-console extention.

## Backgroud

I'm writting a book about Python with the [Sphinx](https://www.sphinx-doc.org/en/master/). I have to copy the command and its output from terminal into my `rst` file, again and again.

It's boring and stupid. So, I made it, an extention of Sphinx, which can render command and output in console style automatically.

## Install 

Simply `pip install sphinx-console` and add the extention to your `conf.py`:

``` python
extentions = ['sphinx_console']
```

## Usage

``` rst
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
