import pymongo
from flask import Flask, render_template, request

cluster = pymongo.MongoClient(
    "mongodb+srv://rye:6OsmTOMs4sGG8Z7n@cluster0.wraav5h.mongodb.net/?retryWrites=true&w=majority")

db = cluster["test"]
collection = db["test"]

app = Flask(__name__)

# TO DO:

# collection.find_one_and_replace({"temperature": 100}, {"temperature": 100.5})
# alert = collection.find(
#    {"$or": [{"temperature": {"$lt": 95}}, {"temperature": {"$gt": 100.4}}]})
# ADD TO MAKE ID = 0 IF COLLECTION IS EMPTY

lastID = 0
results = collection.find({"_id": {"$gt": 0}})
for result in results:
    lastID = result["_id"] + 1


@ app.route('/')
def index():
    return render_template('index.html')


@ app.route('/', methods=['POST'])
def getValue():
    input = request.form['input']
    if input.__contains__('INS'):
        data = convertI(input)
        post = {"_id": lastID, "name": str(
            data[0]), "temperature": float(data[1])}
        collection.insert_one(post)
    elif input.__contains__('FIND'):
        data = convertF(input)
        results = collection.find({"name": data[1]})
        for result in results:
            print(result["temperature"])
    elif input.__contains__('UPD'):
        data = convertF(input)
        if (data[1] == "N"):
            collection.update_one({"name": data[2]}, {
                                  "$set": {"name": data[3]}})
        elif (data[1] == "T"):
            sec = int(data[2])
            three = int(data[3])
            collection.update_one({"temperature": sec}, {
                                  "$set": {"temperature": three}})

    return render_template('index.html')


def convertI(inp):
    changed = inp.replace('INS', '')
    return changed.split()


def convertF(inp):
    return inp.split()


if __name__ == '__main__':
    app.run(debug=True, port=8080, use_reloader=False)
