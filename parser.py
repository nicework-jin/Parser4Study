import sys
import os
import re
import json
import pandas as pd


class Parser(object):
    def __init__(self, problem, route):
        self.problem = problem
        self.route = route
        self.saving_route = f'./result/{self.problem}'
        self.names = []
        self.time_complexities = []
        self.space_complexities = []
        self.filenames = self.get_filenames
        self.read_file = iter(self.read_file())
        self.make_dirs(self.saving_route)

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
        for filename in self.filenames():
            with open(f'{self.route}/{filename}') as f:
                yield filename, f.read()

    def get_filenames(self):
        filenames = []
        try:
            for filename in os.listdir(f'{self.route}/'):
                if filename.startswith(self.problem):
                    filenames.append(filename)

            if len(filenames) == 0:
                raise Exception("해당 문제를 찾을 수 없습니다")
            return filenames

        except Exception as e:
            print(e)

        except FileNotFoundError:
            print("해당 문제를 찾을 수 없습니다")

    def save_to_json(self):
        with open(f'{self.saving_route}/{self.problem}.json', 'w') as f:
            f.write(self.load_json_format())

    def load_json_format(self):
        data = {"name": {}, "time_complexity": {}, "space_complexity": {}}
        for i in range(len(self.names)):
            data["name"][i] = self.names[i]
            data["time_complexity"][i] = self.time_complexities[i]
            data["space_complexity"][i] = self.space_complexities[i]
        return json.dumps(data, ensure_ascii=False)

    def save_to_html(self):
        self.load_table_format().to_html(f'{self.saving_route}/{self.problem}.html')

    def load_table_format(self):
        df = pd.read_json(f'./result/{self.problem}/{self.problem}.json')
        return df.sort_values(by=['time_complexity', "space_complexity"], ascending=True)

    def make_dirs(self, path):
        if not os.path.exists(path):
            os.makedirs(path)


def main():
    if len(sys.argv) == 1:
        print("문제 이름을 인자로 넣어주세요.")
        print("인자 [문제이름]과 [파일 경로]로 최대 2 개만 허용됩니다.")
        print("인자 이름에 띄어쓰기가 포함된 경우 쌍따옴표로 표현 해주세요.")

    elif len(sys.argv) == 2:
        sys.argv.append('.')
        print(f"현재 위치에서 [{sys.argv[1]}] 문제를 탐색합니다.")
        parser = Parser(sys.argv[1], sys.argv[2])
        parser.parse_name_and_complexities()
        parser.save_to_json()
        parser.save_to_html()
        print("통계 파일이 생성 됐습니다.")

    elif len(sys.argv) == 3:
        print(f"'{sys.argv[2]}' 경로의 [폴더]에서 [{sys.argv[1]}] 문제를 탐색합니다.")
        parser = Parser(sys.argv[1], sys.argv[2])
        parser.parse_name_and_complexities()
        parser.save_to_json()
        parser.save_to_html()
        print("통계 파일이 생성 됐습니다.")

    else:  # len(sys.argv) > 3
        print("너무 많은 인자가 포함 됐습니다.")
        print("인자 [문제이름]과 [파일 경로]로 최대 2 개만 허용됩니다.")
        print("인자 이름에 띄어쓰기가 포함된 경우 쌍따옴표로 표현 해주세요.")


if __name__ == "__main__":
    main()

