import requests
import re
from bs4 import BeautifulSoup
url = "https://vk.com"
req = requests.get(url)
html_page = req.text
html_page = html_page.split("\n")
for l_num, line in enumerate(html_page):
    # print(line)
    for match in re.findall(r'<input.*>', line):
        print(f"Line {l_num}: ", match)
# if found:
#     print(found)
# else:
#     print("Nothing found")
