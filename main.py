import pymongo
from flask import Flask, render_template, request

cluster = pymongo.MongoClient(
    "mongodb+srv://rye:6OsmTOMs4sGG8Z7n@cluster0.wraav5h.mongodb.net/?retryWrites=true&w=majority")

db = cluster["test"]
collection = db["test"]

app = Flask(__name__)

# TO DO:
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
        data = convert(input)
        post = {"_id": lastID, "name": str(
            data[1]), "temperature": float(data[2])}
        collection.insert_one(post)
    elif input.__contains__('FIND'):
        data = convert(input)
        if (data[1] == "N"):
            results = collection.find({"name": data[2]})
            for result in results:
                print(result["temperature"])
        elif (data[1] == "T"):
            firs = float(data[2])
            results = collection.find({"temperature": firs})
            for result in results:
                print(result["name"])
    elif input.__contains__('UPD'):
        data = convert(input)
        if (data[1] == "N"):
            collection.update_one({"name": data[2]}, {
                                  "$set": {"name": data[3]}})
        elif (data[1] == "T"):
            sec = float(data[2])
            three = float(data[3])
            collection.update_one({"temperature": sec}, {
                                  "$set": {"temperature": three}})
    elif input.__contains__('AND'):
        data = convert(input)
        first = float(data[1])
        second = float(data[2])
        results = collection.find(
            {"$and": [{"temperature": {"$gt": first}}, {"temperature": {"$lt": second}}]})
        for result in results:
            print(result["name"])

    return render_template('index.html')


def convert(inp):
    return inp.split()


if __name__ == '__main__':
    app.run(debug=True, port=8080, use_reloader=False)
