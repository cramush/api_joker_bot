from flask import Flask, jsonify, request
import pymongo
from pymongo.errors import DuplicateKeyError
import config

app = Flask(__name__)

client = pymongo.MongoClient(f"mongodb://{config.login}:{config.password}@{config.host}/{config.db_name}")
db = client["jokes_db"]
collection = db["jokes"]
collection.drop()


@app.route("/add/one", methods=["POST"])
def add_jokes():
    joke_id = request.json["id"]
    tag = request.json["tag"]
    data = request.json["data"]
    content = request.json["content"]
    joke = {
            "_id": joke_id,
            "tag": tag,
            "data": data,
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
            tag = element["tag"]
            data = element["data"]
            content = element["content"]
            joke = {
                "_id": joke_id,
                "tag": tag,
                "data": data,
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
    tag = request.json["tag"]
    data = request.json["data"]
    content = request.json["content"]
    update = {
        "tag": tag,
        "data": data,
        "content": content
    }
    collection.update_one({"_id": int(joke_id)}, {"$set": update})

    response = jsonify("Updated successfully")
    response.status_code = 200

    return response


@app.route("/all", methods=["GET"])
def all_jokes():
    container = collection.find().sort("tag", pymongo.ASCENDING)
    container = [{"id": el["_id"], "tag": el["tag"], "data": el["data"], "content": el["content"]} for el in container]

    response = jsonify({"jokes": container})
    response.status_code = 200

    return response


if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True)
