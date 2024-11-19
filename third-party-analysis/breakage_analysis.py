from pathlib import Path
from datetime import datetime

total_update_rate = 0.0
bridges = 0

f = open("bridge_data.txt", "a")

for child in Path('glogs').glob('*.txt'):
    name = child.name.split(".txt")[0]

    text = child.read_text()
    lines = text.split('\n')

    if len(lines) == 0:
        continue

    dates = []

    for line in lines:
        l = line.split()
        # line takes the form of 'Date:[something]'
        if len(l) == 0:
            continue

        if l[0] == "Date:":
            d_str = ' '.join(l[1:-1])
            date_obj = datetime.strptime(d_str, '%c')
            dates.append(date_obj)

    num_updates = len(dates)
    num_days = (datetime.now() - dates[-1]).days
    update_rate = num_days / num_updates

    f.write(f"name: {name} | # updates: {num_updates} | days/update: {update_rate}\n")

    total_update_rate += update_rate
    bridges += 1

f.close()
print(total_update_rate / bridges)
    # print(name, update_rate)