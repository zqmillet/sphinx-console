简介
====

sphinx-console 是一个可以自动渲染终端的 sphinx 扩展, 你可以非常方便的使用 sphinx 渲染你的控制台指令以及输出.

比如:

- 显示系统版本.

  .. bash::

      python3 -c "from platform import platform; print(platform())"

- 执行 :sh:`ls -al` 命令.

  .. bash::

      ls -al

- 启动 Python, 并执行 :py:`import this` 命令, 然后执行 :py:`exit()` 退出 Python.

  .. bash::
      :interactions: [[">>>", "import this"], [">>>", "exit()"]]

      python3

- 执行 :sh:`ping` 命令.

  .. bash::

      ping localhost -c 4

- 当然, 你可以只显示命令本身.

  .. bash::
      :do_not_run:

      ping localhost -c 4

- 当然, 也可以支持颜色显示.

  .. bash::

      pip3 install rich

  .. bash::

      python3 -m rich
