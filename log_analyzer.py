from tabulate import tabulate


class Analyzer:
    warning = 0
    info = 0
    critical = 0
    cites = []

    def __init__(self, log):
        self.log = open(log, 'r')
        self.words = self.log.read().splitlines()

    def start(self):
        for i in self.words:
            if "INFO" in i:
                self.info += 1
                if "URL Changed:" in i:
                    temp = i
                    temp = temp.split("Changed: ", 1)[-1]
                    if temp not in self.cites:
                        self.cites.append(temp)
            elif "WARNING" in i:
                self.warning += 1
            elif "CRITICAL" in i:
                self.critical += 1

        self.conclusion()

            # if "INFO" in i or "WARNING" in i or "CRITICAL" in i:
            #     print(i)

    def conclusion(self):
        print(tabulate([['INFO', self.info], ['WARNING', self.warning], ['CRITICAL', self.critical]],
                       headers=['Messages', 'Count'], tablefmt='orgtbl'))
        print()
        print("Visited pages: ")
        print(*self.cites, sep="\n")
