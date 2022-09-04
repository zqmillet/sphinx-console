简介
====

在使用 sphinx 写文档的过程中, 尤其是 Linux 教程, 经常需要将控制台中的命令以及执行结果复制到文档中, 并修改格式, 非常的麻烦.

sphinx-console 是一个可以自动执行指定命令, 并对命令和输出进行自动渲染的 sphinx 扩展, 你可以非常方便的使用 sphinx-console 在你的 sphinx 文档中插入终端命令以及输出结果. 比如:

- 显示系统版本.

  .. bash:: python3 -c "from platform import platform; print(platform())"

- 执行 :sh:`ls -al` 命令.

  .. bash:: ls -al

- 启动 Python, 并执行 :py:`import this` 命令, 然后执行 :py:`exit()` 退出 Python.

  .. bash:: python3
      :interactions: [[">>>", "import this"], [">>>", "exit()"]]

- 执行 :sh:`ping` 命令.

  .. bash:: ping localhost -c 4

- 当然, 你可以只显示命令本身.

  .. bash:: ping localhost -c 4
      :do_not_run:

- 值得注意的是, sphinx-console 也支持持颜色显示\ [#f1]_.

  .. bash:: bash chapters/scripts/color_test.sh
      :display_command: bash color_test.sh

.. rubric:: footnotes

.. [#f1] :download:`点此下载测试脚本 <./scripts/color_test.sh>`.
