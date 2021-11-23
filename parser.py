import sys
import os
import re
import json
from datetime import datetime
import pandas as pd


class Parser4Study(object):
    def __init__(self, problem="위장"):
        self.problem = problem
        self.names = []
        self.time_complexities = []
        self.space_complexities = []
        self.read_file = iter(self.read_file())

    def save_to_html(self):
        year_month = datetime.today().strftime("%Y%m")
        self.load_table_format().to_html(f'./{year_month}_{self.problem}.html')

    def load_table_format(self):
        year_month = datetime.today().strftime("%Y%m")

        df = pd.read_json(f'./{year_month}_{self.problem}.json')
        return df.sort_values(by=['time_complexity', "space_complexity"], ascending=True)

    def parse_name_and_complexities(self):
        while True:
            try:
                filename, text = next(self.read_file)
                time_records = []
                space_records = []
            except StopIteration:
                break

            name = re.findall('_(\w+)', filename)[0]
            complexities = re.findall('통과\s\((\d*\.?\d*)ms,\s(\d*\.?\d*)MB\)', text)
            for time, space in complexities:
                time_records.append(float(time))
                space_records.append(float(space))

            if length := len(time_records) > 0:
                self.names.append(name)
                self.time_complexities.append(sum(time_records) / length)
                self.space_complexities.append(sum(space_records) / length)

    def read_file(self):
        for filename in self.get_filenames():
            with open(f'./{filename}') as f:
                yield filename, f.read()

    def get_filenames(self):
        return [filename for filename in os.listdir('./') if filename.startswith(self.problem)]

    def save_to_json(self):
        year_month = datetime.today().strftime("%Y%m")
        with open(f'./{year_month}_{self.problem}.json', 'w') as f:
            f.write(self.load_json_format())

    def load_json_format(self):
        data = {"name": {}, "time_complexity": {}, "space_complexity": {}}
        for i in range(len(self.names)):
            data["name"][i] = self.names[i]
            data["time_complexity"][i] = self.time_complexities[i]
            data["space_complexity"][i] = self.space_complexities[i]
        return json.dumps(data, ensure_ascii=False)


if __name__ == "__main__":
    if len(sys.argv) > 2:
        print("인자는 한 개만 허용됩니다. 문제 이름에 띄어쓰기가 포함된 경우 쌍따옴표로 표현 해주세요")
    else:
        parser = Parser4Study(sys.argv[1])
        parser.parse_name_and_complexities()
        parser.save_to_json()
        parser.save_to_html()

        print(parser.load_table_format())


