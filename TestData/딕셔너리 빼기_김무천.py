"""
https://programmers.co.kr/learn/courses/30/lessons/42578

테스트 27 〉	통과 (0.01ms, 10.2MB)
테스트 28 〉	통과 (0.01ms, 10.2MB)
"""


def solution(clothes):
    type_num_dict = {}

    for _, type in clothes:
        type_num_dict[type] = type_num_dict.get(type, 0) + 1

    res = 1
    for value in type_num_dict.values():
        res *= value + 1
    return res - 1


if __name__ == "__main__":
    # 5
    clothes = [["yellowhat", "headgear"], ["bluesunglasses", "eyewear"], ["green_turban", "headgear"]]

    # 3
    clothes = [["crowmask", "face"], ["bluesunglasses", "face"], ["smoky_makeup", "face"]]
    print(solution(clothes))