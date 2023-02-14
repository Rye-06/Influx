import pymongo
from flask import Flask, render_template, request

cluster = pymongo.MongoClient(
    "mongodb+srv://rye:6OsmTOMs4sGG8Z7n@cluster0.wraav5h.mongodb.net/?retryWrites=true&w=majority")

db = cluster["test"]
collection = db["test"]

app = Flask(__name__)

# collection.find_one_and_replace({"temperature": 100}, {"temperature": 100.5})
# alert = collection.find(
#    {"$or": [{"temperature": {"$lt": 95}}, {"temperature": {"$gt": 100.4}}]})


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def getValue():
    input = request.form['input']
    if input.__contains__('INS'):
        data = convertI(input)
        post = {"_id": data[0], "name": data[1], "temperature": data[2]}
        collection.insert_one(post)
    elif input.__contains__('FIND'):
        data = convertF(input)
        results = collection.find({"name": data[1]})
        for result in results:
            print(result["_id"])
    elif input.__contains__('UPD'):
        data = convertF(input)
        if (data[1] == "ID"):
            collection.update_one({"ID": data[2]}, {"$set": {"ID": data[3]}})
        elif (data[1] == "N"):
            collection.update_one({"name": data[2]}, {
                                  "$set": {"name": data[3]}})
        elif (data[1] == "T"):
            collection.update_one({"temperature": float(data[2])}, {
                                  "$set": {"temperature": float(data[3])}})

    return render_template('index.html')


def convertI(input):
    input = input.replace('INS', '')
    return ''.join(input).split(", ")


def convertF(input):
    return ''.join(input).split()


if __name__ == '__main__':
    app.run(debug=True, port=8080, use_reloader=False)
