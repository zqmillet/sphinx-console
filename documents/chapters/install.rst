安装
====

使用 :sh:`pip` 命令就可以安装 sphinx-console 库, 如 :numref:`install_sphinx_console` 所示.

.. _install_sphinx_console:

.. bash:: python3 -m pip install sphinx-console
    :setup: python3 -m pip uninstall sphinx-console && python3 -m pip install css-inline
    :caption: 安装 sphinx-console

然后执行 :sh:`python3 -m sphinxcontrib.console`, 如果可以成功显示版本号, 则表示安装成功, 如 :numref:`show_version` 所示.

.. _show_version:

.. bash:: python3 -m sphinxcontrib.console
    :teardown: python3 -m pip uninstall sphinx-console -y
    :caption: 显示 sphinx-console 版本
