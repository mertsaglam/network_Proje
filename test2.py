import time

with open('activities.txt', 'r') as file:
    for i in range(10):
        for line in file:
            line = line.strip()
            if line=="FindMe\n" or line=="FindMe" or line=="\nFindMe":
                print("I have found you.")
                break
        time.sleep(3)