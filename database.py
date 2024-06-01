from pymongo import MongoClient

client = MongoClient("mongodb://mongo:27017/")
db = client.bucket_status_db
collection = db.results

def insert_result(result):
    if collection.count_documents({'name': result['name'], 'status_code': result['status_code']}) == 0:
        try:
            insert_result = collection.insert_one(result)
            return str(insert_result.inserted_id)
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
    else:
        print("Document already exists, not inserting duplicate.")
        return None
