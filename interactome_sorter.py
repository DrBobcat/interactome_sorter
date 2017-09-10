import csv

good_lines = list()
saw_one = False

with open("./sample.csv", "rb") as f:
    for line in f:
        if line[0][0] == "1":
            saw_one = True

        if saw_one:
            processed_line = line.strip().split("|")
            good_lines.append(processed_line)

good_lines = good_lines[0:-2]

print good_lines[0]
