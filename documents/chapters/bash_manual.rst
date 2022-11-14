``bash`` 命令
=============

.. caution::

    ``bash`` 命令的原理是在当前环境真实执行命令, 需要非常慎重, 请勿尝试危险的命令, 比如 :sh:`rm`, :sh:`reboot` 等命令.

- 如果你想渲染控制台的某条指令, 你可以使用 ``bash`` 命令, 比如如下 reST 代码,

  .. code-block:: rst

      .. bash:: ping www.baidu.com -c 4

  可以产生以下效果.

  .. bash:: ping www.baidu.com -c 4

- ``bash`` 命令提供两种风格的渲染风格, 分别是 ``dark`` 和 ``light``, 默认的渲染风格是 ``dark``, 如果你想使用 ``light`` 风格的渲染方式, 可以使用 ``:theme:`` 参数来指定渲染风格.

  .. code-block:: rst

      .. bash:: ping www.baidu.com -c 4
          :theme: light

  .. bash:: ping www.baidu.com -c 4
      :theme: light

- 如果你想修改渲染的字体大小, 你可以使用 ``:font-size:`` 参数来指定.

  .. code-block:: rst

      .. bash:: ping www.baidu.com -c 4
          :theme: light
          :font-size: 14px

  .. bash:: ping www.baidu.com -c 4
      :theme: light
      :font-size: 14px

- ``bash`` 命令默认会执行后面的这条指令, 如果你只想显示命令, 而不想执行, 可以使用 ``:do-not-run:`` 参数, 如下 reST 代码.

  .. code-block:: rst

      .. bash:: ping www.baidu.com -c 4
          :do-not-run:

  可以产生以下效果.

  .. bash:: ping www.baidu.com -c 4
      :do-not-run:

- 某些命令会无限循环, 比如 :sh:`ping www.baidu.com`, 这条命令会一直执行下去, 直到用户使用 :guilabel:`Ctrl + C` 组合键将其中断. ``bash`` 遇到这种命令会有超时机制, 默认是 30 秒, 也就是一条指令最多运行 30 秒, 30 秒后 ``bash`` 命令会终止该进程并输出其渲染结果.

  如果你想修改超时时间, 可以使用 ``:timeout:`` 参数来修改超时时间, 如下 reST 代码.

  .. code-block:: rst

      .. bash:: ping www.baidu.com
          :timeout: 4

  可以产生以下效果.

  .. bash:: ping www.baidu.com
      :timeout: 4

- 如果你想执行的命令和渲染的命令不同, 可以使用 ``:display-command:`` 参数来单独指定渲染的命令.

  .. code-block:: rst

      .. bash:: echo "+1s"
          :display-command: 苟利国家生死以 岂因祸福避趋之
          :caption: 2333

  可以产生以下效果 :numref:`python`.

  .. _python:

  .. bash:: echo "+1s"
      :display-command: 苟利国家生死以 岂因祸福避趋之
      :caption: 2333

- 如果你想在执行某些命令后需要一些交互, 那么可以使用 ``:interactions:`` 参数. ``:interactions:`` 参数是一个 JSON, 其格式为 :math:`n \times 2` 的字符串矩阵, 其中 :math:`n` 表示交互次数. 对于每一次交互, 都由两部分组成, 前半部分是匹配模式, 如果控制台输出满足该匹配模式, 则启动交互, 而后半部分为交互的输入\ [#f1]_.

  如下代码,

  .. code-block:: rst

      .. bash:: python3
          :interactions: [[">>>", "1 + 2"], [">>>", "exit()"]]

  可以产生如下效果.

  .. bash:: python3
      :interactions: [[">>>", "1 + 2"], [">>>", "exit()"]]

- 如果遇到输出非常长的命令, ``bash`` 命令会自动添加横向滚动条.

  .. code-block:: rst

      .. bash:: pip3 install requests

  .. bash:: pip3 install requests

  如果你不喜欢滚动条, 可以通过修改 ``:overflow:`` 参数的值来让 ``bash`` 自动换行.

  .. code-block:: rst

      .. bash:: pip3 install requests
          :overflow: wrap

  .. bash:: pip3 install requests
      :overflow: wrap

- 如果你想在运行某个命令前执行某个命令, 运行之后再执行另一个命令, 你可以使用 ``:setup:`` 和 ``:teardown:`` 参数.

  比如, 运行某个命令需要提前安装依赖, 如果没有安装就会报错.

  .. code-block:: rst

      .. bash:: python3 -m rich.panel

  直接运行会报错, 如下所示.

  .. bash:: python3 -m rich.panel

  你可以用 ``:setup:`` 参数提前安装 ``rich`` 库, 然后再安装. 安装完成后, 使用 ``:teardown:`` 参数卸载.

  .. code-block:: rst

      .. bash:: python3 -m rich.panel
          :setup: python3 -m pip install rich
          :teardown: python3 -m pip uninstall rich -y

  .. bash:: python3 -m rich.panel
      :setup: python3 -m pip install rich
      :teardown: python3 -m pip uninstall rich -y

- 如果你对 ``rich.panel`` 命令了解的话, 你应该知道 ``rich.panel`` 命令会填充整个控制台, 那么, 控制台的大小可以控制吗? 答案是可以的, ``bash`` 命令提供 ``:window_height:`` 和 ``:window-width:`` 两个参数来设置控制台的大小.

  你可以用如下代码将控制台的宽度缩小至 40 字符.

  .. code-block:: rst

      .. bash:: python3 -m rich.panel
          :setup: python3 -m pip install rich
          :teardown: python3 -m pip uninstall rich -y
          :window-width: 40

  .. bash:: python3 -m rich.panel
      :setup: python3 -m pip install rich
      :teardown: python3 -m pip uninstall rich -y
      :window-width: 40

  你可以用如下命令来查看当前窗口的大小.

  .. code-block:: rst

      .. bash:: python3 -c "import os; print(os.popen(\"stty size\", \"r\").read().strip())"
          :window-width: 40
          :window-height: 10

  .. bash:: python3 -c "import os; print(os.popen(\"stty size\", \"r\").read().strip())"
      :window-width: 40
      :window-height: 10

- 如果你想自定义命令的输出, 你可以为 ``bash`` 命令添加内容.

  .. code-block:: rst

      .. bash:: 说一句新年贺词

          春节玉快,
          合家欢络,
          谢谢大家.

  .. bash:: 说一句新年贺词

      春节玉快,
      合家欢络,
      谢谢大家.

  .. hint::

      如果自定义了命令的输出, 则命令不会被执行.

.. rubric:: footnotes

.. [#f1] 不需要手动添加 ``\n``, ``bash`` 的 ``:interactions:`` 参数会自动帮你添加 ``\n``.
