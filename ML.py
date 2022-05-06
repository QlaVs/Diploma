import csv
import json
import time
import seaborn as sns
import re
import pandas as pd
from matplotlib import pyplot as plt
from sklearn import metrics
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_graphviz

arr = []
ml_data = {}
iter_data = []

df = pd.read_csv('ml_dataset.csv')

X = df.iloc[:, :-1]
y = df.iloc[:, -1]

Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, random_state=2)
model = DecisionTreeClassifier()
model.fit(Xtrain, ytrain)

# ypred = model.predict(Xtest)
# print(metrics.classification_report(ypred, ytest))
# print("\n\nAccuracy Score:", metrics.accuracy_score(ytest, ypred).round(2)*100, "%")
#
# confusion_matrix_file = 'confusion_matrix.png'
# dot_file = 'tree.dot'
#
# mat = confusion_matrix(ytest, ypred)
# sns.heatmap(mat.T, square=True, annot=True, fmt='d', cbar=False)
# plt.xlabel('true label')
# plt.ylabel('predicted label')
# plt.savefig(confusion_matrix_file)
# #
# export_graphviz(model, out_file=dot_file, feature_names=X.columns.values)

print("ML instance is ready")


# f = open('data.json')
# data = json.load(f)


# def writing():
#     with open('data.json') as fl:
#         data = json.load(fl)
#         if ml_data not in data:
#             print("WRITING DATA")
#             data.append(ml_data)
#     with open('data.json', 'w') as js:
#         json.dump(data, js, indent=4, separators=(',', ': '))


def check_strings(html_page, words, phishing, rank, sus, iqs_phishing, iqs_sus, iqs_risk_score):
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
    ml_data["iqs_phishing"] = iqs_phishing
    ml_data["iqs_sus"] = iqs_sus
    ml_data["iqs_risk_score"] = iqs_risk_score

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

        with open("ml_dataset.csv", "r+", newline='') as f:
            temp = list(ml_data.values())
            # x = int(input("Bad or Good (1 or -1)?: "))
            # result = x
            skip = False
            #
            # temp.append(x)
            # print(temp, '\n')
            #
            # # ln = ','.join(str(e) for e in temp)
            # # print(ln)
            # read = csv.reader(f)
            # next(read, None)
            # for line in read:
            #     line = [int(v) for v in line]
            #     if temp == line:
            #         print(line)
            #         print("Already in file")
            #         skip = True
            #         break
            #
            # if not skip:
            #     print('Writing')
            #     # f.write(','.join(str(e) for e in temp))
            #     write = csv.writer(f)
            #     write.writerow(temp)

            time.sleep(0.1)
            while True:
                x = input("True prediction? (Y/N): ")
                if x.lower() == "y":
                    temp.append(int(result))
                    read = csv.reader(f)
                    next(read, None)
                    for line in read:
                        line = [int(v) for v in line]
                        if temp == line:
                            print(line)
                            print("Already in file")
                            skip = True
                            break

                    if not skip:
                        print('Writing')
                        # f.write(','.join(str(e) for e in temp))
                        write = csv.writer(f)
                        write.writerow(temp)
                    break
                elif x.lower() == "n":
                    if result == 1:
                        temp.append(-1)
                    else:
                        temp.append(1)
                    read = csv.reader(f)
                    next(read, None)
                    for line in read:
                        line = [int(v) for v in line]
                        if temp == line:
                            print(line)
                            print("Already in file")
                            skip = True
                            break

                    if not skip:
                        print('Writing')
                        # f.write(','.join(str(e) for e in temp))
                        write = csv.writer(f)
                        write.writerow(temp)
                    break
                else:
                    print("Incorrect input (Must be Y or N)")

            temp.clear()

        ml_data.fromkeys(ml_data, None)

        arr.clear()
        #
        # if result == 1:
        #     return 1
        return result
