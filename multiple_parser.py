import os
import sys
import re
import unicodedata
from collections import defaultdict
from parser import Parser
from datetime import datetime


class MultipleParser(object):
    def __init__(self, route):
        self.route = route
        self.problems = []

    def load_and_parse_files(self):
        kwd_with_filename_list = []
        for filename in os.listdir(self.route):
            if '.py' not in filename:
                continue

            kwd = re.findall('(.+)_.+\.py', filename)[0]
            kwd = kwd.replace(' ', '')
            kwd = unicodedata.normalize('NFC', kwd)
            kwd = kwd.lower()
            kwd_with_filename_list.append((kwd, filename))

        match_same_file = defaultdict(list)
        for kwd, filename in kwd_with_filename_list:
            match_same_file[kwd].append(filename)

        for problem in match_same_file.keys():
            self.problems.append(problem)
            parser = Parser(problem, self.route)
            parser.parse_name_and_complexities()
            parser.save_to_json()
            parser.save_to_html()

    def loads_and_combine_with_markdown(self):
        saving_path = './result/html'
        if not os.path.exists(saving_path):
            os.makedirs(saving_path)

        # "이중순위큐"를 실수로 "이중순위"로 입력했을 경우를 고려하여 가깝게 배치
        self.problems.sort()

        with open(f'{saving_path}/{datetime.today().strftime("%Y%m%d")}.html', 'w') as w:
            for problem in self.problems:
                target = ''
                for dir_name in os.listdir('./result'):
                    kwd = dir_name.replace(' ', '')
                    kwd = unicodedata.normalize('NFC', kwd)
                    kwd = kwd.lower()

                    if problem.lower() == kwd:
                        target = kwd
                        break

                if target == '':
                    continue

                with open(f'./result/{target}/{target}.html') as r:
                    w.write(f"{target} \n\n")
                    w.write(r.read())


if __name__ == "__main__":
    multiple_parser = MultipleParser(sys.argv[1])
    multiple_parser.load_and_parse_files()
    multiple_parser.loads_and_combine_with_markdown()
