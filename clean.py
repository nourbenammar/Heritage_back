with open("objects.csv", "rb") as f:
    content = f.read()
    if b'\x00' in content:
        print("NULL bytes found in file.")
    else:
        print("No NULL bytes found.")