data = ["Иванов: 85", "Петров: 42", "Сидоров: abc", "Козлов: 90", ": 55", "Иванов: 70"]


def process_grades(records: list[str]) -> dict:
    valid_count, average, skipped = 0, 0, 0
    passed = set()
    for line in records:
        if ":" in line:
            a = line.split(":")
            surname, grade = a[0], a[1]
            if surname.strip().isalpha() and grade.strip().isdigit():
                valid_count += 1
                average += int(grade)
                if int(grade) >= 60:
                    passed.add(surname)
            else:
                skipped += 1
        else:
            skipped += 1
    return {
        "valid_count": valid_count,
        "average": round(average / valid_count, 1),
        "passed": list(passed),
        "skipped": skipped,
    }


nums = [1, 3, 2, 5, 8, 4, 7]


def longest_increasing_streak(nums: list[int]) -> dict:
    if not nums:
        return {"length": 0, "streak": []}
    max_arr = []
    temp_arr = [nums[0]]
    for num in range(1, len(nums)):
        if nums[num] > nums[num - 1]:
            temp_arr.append(nums[num])
        else:
            if len(temp_arr) > len(max_arr):
                max_arr = temp_arr.copy()
            temp_arr = [nums[num]]
    if len(temp_arr) > len(max_arr):
        max_arr = temp_arr.copy()
    return {"length": len(max_arr), "streak": max_arr}


print(longest_increasing_streak(nums))
