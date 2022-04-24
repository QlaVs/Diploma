import requests
import json
import re
# from bs4 import BeautifulSoup

arr = []
ml_data = {}

# f = open('data.json')

# data = json.load(f)


def writing():
    with open('data.json') as fl:
        data = json.load(fl)
        if ml_data not in data:
            print("WRITING")
            data.append(ml_data)
        # if ml_data not in data:
        #     print('WRITING')
        #     data.append(ml_data)
    with open('data.json', 'w') as js:
        json.dump(data, js, indent=4, separators=(',', ': '))


def check_strings(html_page, words, phishing, sus):
    # url = "https://github.com/login"
    # req = requests.get(url)
    # html_page = req.text

    ml_data["phishing_url"] = phishing
    ml_data["sus"] = sus
    ml_data["password"] = 0
    ml_data["login"] = 0
    ml_data["diff"] = -1

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
            writing()

    else:
        print(ml_data)
        writing()
        # Add ML there??

    ml_data.fromkeys(ml_data, None)

    arr.clear()
