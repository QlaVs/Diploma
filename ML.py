import requests
import re
# from bs4 import BeautifulSoup

arr = []


def check_strings(html_page, words):
    # url = "https://github.com/login"
    # req = requests.get(url)
    # html_page = req.text
    html_page = html_page.split(">")
    for l_num, line in enumerate(html_page):
        # print(line)
        for match in re.findall(r'<input.*', line):
            for i in words:
                if i in match:
                    print(f"Line {l_num}: ", match)
                    arr.append(l_num)
                    break
            else:
                continue  # only executed if the inner loop did NOT break
            break  # only executed if the inner loop DID break
        # print("No suspicious <input> found...")

    for i in range(len(arr) - 1):
        try:
            result = abs(arr[i + 1] - arr[i])
            print(f"Difference between lines: {result}")
        except:
            pass


    arr.clear()
