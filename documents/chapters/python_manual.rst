``python`` 命令
===============

``python`` 命令是通过交互模式调用 Python 解释器, 并将结果渲染在页面上的命令.

比如, 定义一个函数, 并运行.

.. code-block:: rst

    .. python::

        def fib(n):
            if n == 1:
                return n
            if n == 2:
                return n
            return fib(n - 1) + fib(n - 2)

        fib(10)

.. python::

    def fib(n):
        if n == 1:
            return n
        if n == 2:
            return n
        return fib(n - 1) + fib(n - 2)

    fib(10)

``python`` 命令提供两种风格的渲染风格, 分别是 ``dark`` 和 ``light``, 默认的渲染风格是 ``dark``, 如果你想使用 ``light`` 风格的渲染方式, 可以使用 ``:theme:`` 参数来指定渲染风格.

.. code-block:: rst

    .. python::
        :theme: light

        def fib(n):
            if n == 1:
                return n
            if n == 2:
                return n
            return fib(n - 1) + fib(n - 2)

        fib(10)

.. python::
    :theme: light

    def fib(n):
        if n == 1:
            return n
        if n == 2:
            return n
        return fib(n - 1) + fib(n - 2)

    fib(10)

如果你想修改渲染的字体大小, 你可以使用 ``:font-size:`` 参数来指定.

.. code-block:: rst

    .. python::
        :theme: light
        :font-size: 14px

        def fib(n):
            if n == 1:
                return n
            if n == 2:
                return n
            return fib(n - 1) + fib(n - 2)

        fib(10)

.. python::
    :theme: light
    :font-size: 14px

    def fib(n):
        if n == 1:
            return n
        if n == 2:
            return n
        return fib(n - 1) + fib(n - 2)

    fib(10)

如果你不喜欢 Python 解释器的启动信息, 你可以用 ``:hide-information:`` 参数.

.. code-block:: rst

    .. python::
        :hide-information:

        def fib(n):
            if n == 1:
                return n
            if n == 2:
                return n
            return fib(n - 1) + fib(n - 2)

        fib(10)

.. python::
    :hide-information:

    def fib(n):
        if n == 1:
            return n
        if n == 2:
            return n
        return fib(n - 1) + fib(n - 2)

    fib(10)

与 ``bash`` 命令类似, ``python`` 命令也提供 ``:overflow:`` 参数, 用于控制过长输出的渲染, 默认是添加横向滚动条, 如果你想让 ``python`` 命令自动换行, 可以将 ``:overflow:`` 的值设置成 ``wrap``.

.. code-block:: rst

    .. python::

        print(' '.join(['gouliguojiashengsiyi'] * 10))

.. python::

    print(' '.join(['gouliguojiashengsiyi'] * 10))

.. code-block:: rst

    .. python::
        :overflow: wrap

        print(' '.join(['gouliguojiashengsiyi'] * 10))

.. python::
    :overflow: wrap

    print(' '.join(['gouliguojiashengsiyi'] * 10))

同样的, ``python`` 命令也提供 ``:window-width:`` 和 ``:window-height:`` 参数, 可以设置控制台的大小.

.. code-block:: rst

    .. python::

        from os import get_terminal_size
        get_terminal_size()

.. python::

    from os import get_terminal_size
    get_terminal_size()

.. code-block:: rst

    .. python::
        :window-height: 20
        :window-width: 40

        from os import get_terminal_size
        get_terminal_size()

.. python::
    :window-height: 20
    :window-width: 40

    from os import get_terminal_size
    get_terminal_size()

``python`` 命令会在所有交互都结束后自动执行 :py:`exit()` 命令并退出, 当然, 你也可以显式调用 :py:`exit()`.

.. code-block:: rst

    .. python::

        for i in range(10):
            print(i)
            if i == 5:
                exit()

.. python::

    for i in range(10):
        print(i)
        if i == 5:
            exit()

.. code-block:: rst

    .. python::

        import this
        exit()
        print('苟利国家生死以')

.. python::

    import this
    exit()
    print('苟利国家生死以')

``python`` 命令也有超时机制, 默认是 30 秒, 如果你想修改这个值, 你可以通过 ``:timeout:`` 参数修改, 如果超时, 则超时后的内容均不会渲染.

.. code-block:: rst

    .. python::
        :timeout: 1

        from time import sleep
        print('begin')
        sleep(100)
        print('end')

.. python::
    :timeout: 1

    from time import sleep
    print('begin')
    sleep(100)
    print('end')

``python`` 命令也支持色彩.

.. code-block:: rst

    .. python::

        print('\033[1;33;1m字体变色, 但无背景色.\033[0m')
        print('\033[1;44m字体不变色, 有背景色.\33[0m')
        print('\033[1;32;45m字体有色, 且有背景色.\033[0m')
        print('\033[0;32;45m字体有色, 且有背景色.\033[0m')

.. python::

    print('\033[1;33;1m字体变色, 但无背景色.\033[0m')
    print('\033[1;44m字体不变色, 有背景色.\33[0m')
    print('\033[1;32;45m字体有色, 且有背景色.\033[0m')
    print('\033[0;32;45m字体有色, 且有背景色.\033[0m')

``python`` 同样也支持 ``:setup:`` 和 ``:teardown:`` 参数.
