import time

with open("activities.txt", "a") as f:
    for i in range(10):
        f.write("FindMe" + "\n")
        time.sleep(1)

    