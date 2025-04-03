# import chardet

# with open('users.csv', 'rb') as f:
#     result = chardet.detect(f.read(5000))
#     print(result)  # {'encoding': 'Windows-1252', 'confidence': 0.99, ...}

import os

csv_file_path = 'orders.csv'
print("Absolute path to file:", os.path.abspath(csv_file_path))

with open(csv_file_path, 'rb') as f:
    raw = f.read(100)
    print("First 100 bytes:", raw)
