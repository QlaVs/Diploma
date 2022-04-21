import requests
import json
import re
# from bs4 import BeautifulSoup

arr = []
ml_data = {}


def check_strings(html_page, words, phishing):
    # url = "https://github.com/login"
    # req = requests.get(url)
    # html_page = req.text

    ml_data['phishing_url'] = phishing
    ml_data['password'] = 0
    ml_data['login'] = 0
    ml_data['diff'] = -1

    html_page = html_page.split(">")
    for l_num, line in enumerate(html_page):
        try:
            for match in re.findall(r'<input.*', line):
                for i in words['pwd']:
                    if i in match:
                        ml_data['password'] = 1
                        print(f"Line {l_num}: ", match)
                        arr.append(l_num)
                        break
                else:
                    continue
                break
        except:
            pass

        try:
            for match in re.findall(r'<input.*', line):
                for i in words['lgn']:
                    if i in match:
                        ml_data['login'] = 1
                        print(f"Line {l_num}: ", match)
                        arr.append(l_num)
                        break

                else:
                    continue  # only executed if the inner loop did NOT break
                break  # only executed if the inner loop DID break
            # print("No suspicious <input> found...")
        except:
            pass

    if len(arr) > 1:
        for i in range(len(arr) - 1):
            try:
                result = abs(arr[i + 1] - arr[i])
                print(f"Difference between lines: {result}")
                ml_data['diff'] = result

            except:
                pass
            print(ml_data)

    else:
        print(ml_data)
        # Add ML there??

    ml_data.fromkeys(ml_data, None)

    arr.clear()
