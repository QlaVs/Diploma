import json
import random
import re
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

arr = []
ml_data = {}
iter_data = []

df = pd.read_csv('ml_dataset.csv')

X = df.iloc[:, :-1]
y = df.iloc[:, -1]

Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, random_state=2)
model = DecisionTreeClassifier()
model.fit(Xtrain, ytrain)
print("ML instance is ready")

# f = open('data.json')
# data = json.load(f)


def writing():
    with open('data.json') as fl:
        data = json.load(fl)
        if ml_data not in data:
            print("WRITING DATA")
            data.append(ml_data)
    with open('data.json', 'w') as js:
        json.dump(data, js, indent=4, separators=(',', ': '))


def check_strings(html_page, words, phishing, rank, sus):
    # url = "https://github.com/login"
    # req = requests.get(url)
    # html_page = req.text
    global iter_data

    lgn_form = 0
    pwd_form = 0

    ml_data["phishing_url"] = phishing
    ml_data["rank"] = rank
    ml_data["sus"] = sus
    ml_data["password"] = 0
    ml_data["login"] = 0
    ml_data["diff"] = 0

    html_page = html_page.split(">")
    if iter_data == html_page:
        return 0
    else:
        iter_data = html_page
        for l_num, line in enumerate(html_page):
            try:
                for match in re.findall(r'<input.*', line):
                    for i in words['pwd']:
                        if i in match:
                            ml_data['password'] = 1
                            print(f"Line {l_num}: ", match)
                            arr.append(l_num)
                            lgn_form = 1
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
                            pwd_form = 1
                            break

                    else:
                        continue  # only executed if the inner loop did NOT break
                    break  # only executed if the inner loop DID break
                # print("No suspicious <input> found...")
            except:
                pass

        if lgn_form == 0 and pwd_form == 0 and ml_data["phishing_url"] != 1:
            ml_data["phishing_url"] = -1

        if ml_data["phishing_url"] != -1 and len(arr) > 1:
            for i in range(len(arr) - 1):
                try:
                    result = abs(arr[i + 1] - arr[i])
                    print(f"Difference between lines: {result}")
                    ml_data['diff'] = result

                except:
                    pass
                print(ml_data)
                # writing()

        else:
            print(ml_data)
            # writing()

            # test = StringIO("""phishing_url,rank,sus,password,login,diff
            # 0,1,-1,1,1,25
            # """)
            # test_formated = pd.read_csv(test, sep=",")
            # print(test_formated)

        result = model.predict(pd.DataFrame(ml_data, index=[0]))
        print(result)

        ml_data.fromkeys(ml_data, None)

        arr.clear()

        if result == 1:
            return 1
        return -1
