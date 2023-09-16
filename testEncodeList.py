import pickle

# Loading the encodeList from a file
def loadEncodeList(file_name):
    with open(file_name, 'rb') as file:
        encodeList = pickle.load(file)
    return encodeList

# Loading the image_encodings dictionary from a file
def loadImageEncodings(file_name):
    with open(file_name, 'rb') as file:
        encodings = pickle.load(file)
    return encodings

print(loadEncodeList("encodeList.pkl"))
print(loadImageEncodings("image_encodings.pkl"))