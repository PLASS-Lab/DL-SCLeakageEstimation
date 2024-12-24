import pandas as pd

data = pd.read_csv('/home/sal/HDModel/assemblyfiles/output.csv')

def calculate_signed_distance(binary1, binary2):
    return sum((int(b2) - int(b1)) for b1, b2 in zip(binary1, binary2))

def calculate_switching_distance(binary1, binary2):
    # Calculate the switching distance as the count of bits that differ
    return sum(b1 != b2 for b1, b2 in zip(binary1, binary2))

# Calculate signed distances and switching distances between consecutive binary numbers
signed_distances = []
switching_distances = []
for i in range(len(data) - 1):
    signed_dist = calculate_signed_distance(data['BinaryCode'][i], data['BinaryCode'][i + 1])
    switching_dist = calculate_switching_distance(data['BinaryCode'][i], data['BinaryCode'][i + 1])
    signed_distances.append(signed_dist)
    switching_distances.append(switching_dist)

# Append the last element as NaN or zero since there's no next element
signed_distances.append(None)  # or 0 if that makes sense in your context
switching_distances.append(None)  # or 0 if that makes sense in your context

data['SHD'] = signed_distances
data['SD'] = switching_distances

data.to_csv('SCBDdataset.csv', index=False)

print("Data has been saved to 'SCBDdataset.csv'.")
