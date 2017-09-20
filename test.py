# -*- coding: utf-8 -*-

from colorama import init,Fore
init(autoreset=True) 
 #通过使用autoreset参数可以让变色效果只对当前输出起作用，输出完成后颜色恢复默认设置
print(Fore.RED + 'welcome to www.jb51.net')
print('automatically back to default color again')

from colorama import Back, Style
print(Fore.RED + 'some red text')
print(Back.GREEN + Fore.WHITE + 'and with a green background')
print(Style.DIM + 'and in dim text')
print(Style.RESET_ALL)
print('back to normal now')

print(Fore.YELLOW + Back.BLACK + " Red "),
print(Fore.GREEN + "color")

# Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
# Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
# Style: DIM, NORMAL, BRIGHT, RESET_ALL