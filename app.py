from flask import Flask, jsonify, request
import pymongo
from pymongo.errors import DuplicateKeyError

app = Flask(__name__)

client = pymongo.MongoClient("mongodb://admin:admin@localhost:27017/jokes_db")
db = client["jokes_db"]
collection = db["jokes"]
# collection.drop()


@app.route("/add/one", methods=["POST"])
def add_jokes():
    joke_id = request.json["id"]
    title = request.json["title"]
    content = request.json["content"]
    joke = {
            "_id": joke_id,
            "title": title,
            "content": content
        }

    try:
        collection.insert_one(joke)

        response = jsonify("Added successfully")
        response.status_code = 200

        return response

    except pymongo.errors.DuplicateKeyError:
        message = {
            "status": 404,
            "message": "DuplicateKeyError: " + request.url
        }
        response = jsonify(message)
        response.status_code = 404

        return response


@app.route("/add/many", methods=["POST"])
def add_many():
    json = request.json
    joke_list = json["jokes"]

    try:
        for element in joke_list:
            joke_id = element["id"]
            title = element["title"]
            content = element["content"]
            joke = {
                "_id": joke_id,
                "title": title,
                "content": content
            }
            collection.insert_one(joke)

        response = jsonify("Added successfully")
        response.status_code = 200

        return response

    except pymongo.errors.DuplicateKeyError:
        message = {
            "status": 404,
            "message": "DuplicateKeyError: " + request.url
        }
        response = jsonify(message)
        response.status_code = 404

        return response


@app.route("/sort", methods=["PUT"])
def sort_jokes():
    sort = collection.find().sort("_id", 1)

    for raw in sort:
        print(raw)
        joke_id = raw["_id"]
        collection.delete_one({"_id": joke_id})
        collection.insert_one(raw)

    response = jsonify("Sorted successfully")
    response.status_code = 200

    return response


@app.route("/delete/one/<joke_id>", methods=["DELETE"])
def delete_joke(joke_id):
    collection.delete_one({"_id": int(joke_id)})

    response = jsonify("Deleted successfully")
    response.status_code = 200

    return response


@app.route("/delete/all", methods=["DELETE"])
def delete_jokes():
    collection.drop()

    response = jsonify("Deleted successfully")
    response.status_code = 200

    return response


@app.route("/update/<joke_id>", methods=["PUT"])
def update_joke(joke_id):
    title = request.json["title"]
    content = request.json["content"]
    update = {
        "title": title,
        "content": content
    }
    collection.update_one({"_id": int(joke_id)}, {"$set": update})

    response = jsonify("Updated successfully")
    response.status_code = 200

    return response


@app.route("/all", methods=["GET"])
def all_jokes():
    _container = collection.find()
    container = [{"id": elem["_id"], "title": elem["title"], "content": elem["content"]} for elem in _container]

    response = jsonify({"jokes": container})
    response.status_code = 200

    return response


if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True)
