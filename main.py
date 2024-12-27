import pymongo
from flask import Flask, render_template, request

cluster = pymongo.MongoClient(
    "mongodb+srv://rye:6OsmTOMs4sGG8Z7n@cluster0.wraav5h.mongodb.net/?retryWrites=true&w=majority")
db = cluster["test"]

app = Flask(__name__)


@ app.route('/')
def index():
    return render_template('index.html')


@ app.route('/', methods=['POST'])
def getValue():
    input1 = request.form['input1']
    input2 = request.form['input2']

    sections = []

    collection = db["sections"]

    results = collection.find({"_id": {"$gt": -1}})

    for result in results:
        # access from new database instead
        sections.append(result["section-name"])

    print(sections)

    if(len(input1) > 1):
        lastID = 0

        results = collection.find({"_id": {"$gt": -1}})
        for result in results:
            lastID = result["_id"] + 1

        if input1.__contains__('INS'):
            data = convert(input1)

            lowestPeople = 0
            results = collection.find({"_id": 0})
            for result in results:
                lowestPeople = result["people"]
            sect = ""
            results = collection.find({"_id": {"$gt": 0}})
            for result in results:
                if(result["people"] < lowestPeople):
                    lowestPeople = result["people"]
                    sect = result["section-name"]
            if sect in sections:
                post = {"_id": lastID, "name": str(
                    data[1]), "temperature": float(data[2]), "section": sect}
                collection.insert_one(post)
        elif input1.__contains__('FIND'):
            data = convert(input1)
            if (data[1] == "N"):
                results = collection.find({"name": data[2]})
                for result in results:
                    print(result["temperature"])
            elif (data[1] == "T"):
                firs = float(data[2])
                results = collection.find({"temperature": firs})
                for result in results:
                    print(result["name"])
        elif input1.__contains__('UPD'):
            data = convert(input1)
            if (data[1] == "N"):
                collection.update_one({"name": data[2]}, {
                    "$set": {"name": data[3]}})
            elif (data[1] == "T"):
                sec = float(data[2])
                three = float(data[3])
                collection.update_one({"temperature": sec}, {
                    "$set": {"temperature": three}})
        elif input1.__contains__('AND'):
            data = convert(input1)
            first = float(data[1])
            second = float(data[2])
            results = collection.find(
                {"$and": [{"temperature": {"$gt": first}}, {"temperature": {"$lt": second}}]})
            for result in results:
                print(result["name"])
    else:
        if input2.__contains__('INS'):
            data = convert(input2)
            if str(data[1]) not in sections:
                print("h")
                sections.append(str(data))  # store inside database instead

    return render_template('index.html')


def convert(inp):
    return inp.split()


if __name__ == '__main__':
    app.run(debug=True, port=8080, use_reloader=False)


# OTHER TO DO:

# Add update function to section
# Add error check for inputting the same section again
