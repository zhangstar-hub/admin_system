# try:
#     nums = [int(i) for i in input().split(' ')]
# except Exception:
#     print([])
# else:
#     nums2 = list(sorted(nums, reverse=True))
#     mid = (len(nums) + 1) // 2
#     height_set = nums2[:mid]
#
#     height_list = []
#     low_list = []
#
#     for i in nums:
#         if i in height_set and len(height_list) <= mid:
#             height_list.append(i)
#         else:
#             low_list.append(i)
#
#     right_list = []
#     for i in range(len(nums)):
#         if i % 2 == 0 or not low_list:
#             right_list.append(height_list.pop(0))
#         elif low_list:
#             right_list.append(low_list.pop(0))
#
#     print(" ".join(map(str, right_list)))

n = int(input())
nums = []
for i in range(n):
    nums.append([int(i) for i in input().split(" ")])

print(nums)
# nums = [
# [1, 0, 100],
# [5, 0, 200],
# [2, 0, 199],
# [3, 0, 200],
# [4, 0, 200],
# [6, 10, 200],
# [7, 11, 200],
# [8, 12, 200],
# [11, 100, 200],
# [12, 100, 200],
# ]

build = {}
m = {}
bosses = set()
for my, boss, slr in nums:
    m.setdefault(boss, []).append(my)
    build[my] = slr
    bosses.add(boss)
    build.setdefault(boss, 0)

boss_id = None
print(m, build, bosses)

while len(bosses) >= 1:
    # 收入计算
    for k, v in m.items():
        new_people = []
        for i in v:
            if i in bosses:
                new_people.append(i)
                continue
            build[k] += build[i] // 100 * 15
        if len(new_people) == 0:
            boss_id = k
            if k in bosses:
                bosses.remove(k)
        else:
            m[k] = new_people

print(build)
print(boss_id, build[boss_id])
