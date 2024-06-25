import sys

class S3Facade():

    def __init__(self):
        print("Initializing S3 facade object")

    def Object(self, bucket_name, file_name):
        return S3ObjectFacade(bucket_name, file_name)

class S3ObjectFacade():

    def __init__(self, bucket_name, file_name):
        print("Creating S3 Object facade with bucket: " + bucket_name + ", and file: " + file_name)

    def put(self, Body):
        print(f"S3 object written to with a body of size: {sys.getsizeof(Body)}")
