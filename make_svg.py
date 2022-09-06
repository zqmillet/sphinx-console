from ansi2html import Ansi2HTMLConverter
from colorama import Style
from colorama import Fore

from sphinx_console.execute import execute

convertor = Ansi2HTMLConverter(dark_bg=True, line_wrap=False, inline=True, font_size='10pt')
command = 'ping www.baidu.com -c 4'
header = f'{Style.BRIGHT}{Fore.RED}${Fore.WHITE} {command}{Fore.RESET}{Style.RESET_ALL}'
output = execute(command)
html = convertor.convert(header + '\n' + output)

print(html)
svg = f'''
<svg xmlns="http://www.w3.org/2000/svg">
<foreignObject width="100" height="100">
    <div xmlns="http://www.w3.org/1999/xhtml">
        {html}
    </div>
</foreignObject>
</svg>
'''
with open('xxx.svg', 'w', encoding='utf8') as file:
    file.write(svg)
