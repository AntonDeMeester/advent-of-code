with open("06_customs_input.txt", "r") as input_file:
    input = input_file.read()


def part_one():
    per_group = input.split("\n\n")
    total = 0
    for group in per_group:
        per_person = group.split("\n")
        group_answer = set()
        for answer in per_person:
            group_answer |= set(answer)
        total += len(group_answer)
    print(total)


def part_two():
    per_group = input.split("\n\n")
    total = 0
    for group in per_group:
        per_person = group.split("\n")
        group_answer = None
        for answer in per_person:
            if group_answer is None:
                group_answer = set(answer)
            else:
                group_answer &= set(answer)
        total += len(group_answer)
    print(total)


part_one()
part_two()