"""
https://programmers.co.kr/learn/courses/30/lessons/42586

테스트 1 〉	통과 (1ms, 10.2MB)
통과 (0.02ms, 10.3MB)
"""


def solution(progresses, speeds):
    progresses = progresses[::-1]
    speeds = speeds[::-1]

    res = []
    while progresses:
        for idx, progress_speed_pair in enumerate(zip(progresses, speeds)):
            progresses[idx] = progress_speed_pair[0] + progress_speed_pair[1]

        cnt = 0
        while progresses and progresses[-1] >= 100:
            progresses.pop()
            speeds.pop()
            cnt += 1

        if cnt > 0:
            res.append(cnt)
    return res


if __name__ == "__main__":
    # [2, 1]
    progresses = [93, 30, 55]
    speeds = [1, 30, 5]

    # [1, 3, 2]
    # progresses = [95, 90, 99, 99, 80, 99]
    # speeds = [1, 1, 1, 1, 1, 1]

    print(solution(progresses, speeds))