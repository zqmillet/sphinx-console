# sphinx-console

[![sphinx-console](https://img.shields.io/badge/pypi-sphinx--console-brightgreen)](https://pypi.org/project/sphinx-console/)

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

The sphinx-console extention provides `bash` directive.
You can use the following reST code to execute the command `ping www.google.com -c 4`, and render it and its output in your document.

``` rst
.. bash:: ping www.google.com -c 4
```

If you want to terminate the command after 4 seconds, you can specify the `timeout` parameter.

``` rst
.. bash:: ping www.google.com
    :timeout: 4
```

If you want do some interactions with the command, you can specify the `interactions` parameter.

``` rst
.. bash:: python3
    :interactions: [[">>>", "1 + 2"], [">>>", "exit()"]]
```

The sphinx-console extention also provides `python` directive.
You can can use it to execute Python expressions in the Python interpreter.

``` rst
.. python::

    def fib(n):
        if n == 1:
            return n
        if n == 2:
            return n
        return fib(n - 1) + fib(n - 2)

    fib(10)
```

You can read [the manual of sphinx-console](https://sphinx-console.readthedocs.io/) for more detail.
