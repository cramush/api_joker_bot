from flask import Flask, jsonify, request
from bson.objectid import ObjectId
from datetime import datetime
import pymongo
import config

app = Flask(__name__)

client = pymongo.MongoClient(f"mongodb://{config.login}:{config.password}@{config.host}/{config.db_name}")
db = client["jokes_db"]
collection = db["jokes"]
if collection.estimated_document_count() == 0:
    collection.drop()
    collection.create_index([("tag", pymongo.ASCENDING), ("date", pymongo.ASCENDING)])


@app.route("/add/one", methods=["POST"])
def add_joke():
    tag = request.json["tag"]
    data = request.json["data"]
    content = request.json["content"]
    date = datetime.now()
    joke = {
            "tag": tag,
            "data": data,
            "content": content,
            "date": date
        }
    collection.insert_one(joke)

    response = jsonify("Added successfully")
    response.status_code = 200
    return response


@app.route("/add/many", methods=["POST"])
def add_many():
    json = request.json
    joke_list = json["jokes"]
    date = datetime.now()

    for element in joke_list:
        tag = element["tag"]
        data = element["data"]
        content = element["content"]
        joke = {
            "tag": tag,
            "data": data,
            "content": content,
            "date": date
        }
        collection.insert_one(joke)

    response = jsonify("Added successfully")
    response.status_code = 200
    return response


@app.route("/update/<joke_id>", methods=["PUT"])
def update_joke(joke_id):
    tag = request.json["tag"]
    data = request.json["data"]
    content = request.json["content"]
    date = datetime.now()
    update = {
        "tag": tag,
        "data": data,
        "content": content,
        "date": date
    }
    collection.update_one({"_id": ObjectId(joke_id)}, {"$set": update})

    response = jsonify("Updated successfully")
    response.status_code = 200
    return response


@app.route("/all", methods=["GET"])
def all_jokes():
    box = collection.find().sort([("tag", pymongo.ASCENDING), ("date", pymongo.ASCENDING)])
    box = [{
        "id": str(el["_id"]),
        "tag": el["tag"],
        "data": el["data"],
        "content": el["content"],
        "date": el["date"]
        } for el in box]

    response = jsonify({"jokes": box})
    response.status_code = 200
    return response


@app.route("/delete/one/<joke_id>", methods=["DELETE"])
def delete_joke(joke_id):
    collection.delete_one({"_id": ObjectId(joke_id)})

    response = jsonify("Deleted successfully")
    response.status_code = 200
    return response


@app.route("/delete/all", methods=["DELETE"])
def delete_jokes():
    collection.drop()

    response = jsonify("Deleted successfully")
    response.status_code = 200
    return response


if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True)
