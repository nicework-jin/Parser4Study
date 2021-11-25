import os
import sys
import re
from parser import Parser
from datetime import datetime


class MultipleParser(object):
    def __init__(self, route):
        self.route = route
        self.problems = []
        self.load_and_parse_files()
        self.loads_and_combine_with_markdown()

    def load_and_parse_files(self):
        for filename in os.listdir(self.route):
            problem = re.findall('(.+)_.+\.py', filename)

            if len(problem) > 0:
                self.problems.append(problem[0])
                parser = Parser(problem[0], self.route)
                parser.parse_name_and_complexities()
                parser.save_to_json()
                parser.save_to_html()

    def loads_and_combine_with_markdown(self):
        saving_path = './result/md'
        if not os.path.exists(saving_path):
            os.makedirs(saving_path)

        for problem in self.problems:
            with open(f'{saving_path}/{datetime.today().strftime("%Y%m%d")}.md', 'a') as w:
                with open(f'./result/{problem}/{problem}.html') as r:
                    w.write(f"{problem} \n")
                    w.write(r.read())


if __name__ == "__main__":
    MultipleParser(sys.argv[1])

