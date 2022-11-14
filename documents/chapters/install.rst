安装
====

使用 :sh:`pip` 命令就可以安装 sphinx-console 库.

.. bash:: python3 -m pip install sphinx-console
   :setup: python3 -m pip uninstall sphinx-console

然后执行 :sh:`python3 -m sphinx_console`, 如果可以成功显示版本号, 则表示安装成功.

.. bash:: python3 -m sphinx_console
    :teardown: python3 -m pip uninstall sphinx-console -y
