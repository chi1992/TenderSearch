import json


class Holder_resources():

    def __init__(self):

        with open('./resources/resources.json', 'r', encoding = 'utf-8') as f:
            self.data = json.load(f)

        # with open('./resources/documents/documents.json', 'r', encoding = 'utf-8') as f:
        #     self.docs = json.load(f)

    def save_resource(self):

        with open('./resources/resources.json', 'w', encoding = 'utf-8') as f:
            json.dump(self.data, f, indent = 2, ensure_ascii = False)