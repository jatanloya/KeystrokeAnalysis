import flask
from flask import request, jsonify


app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/api/get/all', methods=['GET'])
def api_all():
    return jsonify("")



ret_result=[]
class Node:
    def __init__(self):
        self.next = {}
        self.leaf = False
        self.hit_score=0
    def add_item(self, item):
        i = 0
        while i < len(item):
            k = item[i]
            if not k in self.next:
                node = Node()
                self.next[k] = node
            self = self.next[k]
            if i == len(item) - 1:
                self.leaf = True
            else:
                self.leaf = False
            i += 1
    def search(self, item):
        if self.leaf and len(item) == 0:
            return True
        first = item[:1]
        str = item[1:]
        if first in self.next:
            return self.next[first].search(str)
        else:
            return False
    def traversal(self, item):
        if self.leaf:
        	ret_result.append(item)
        for i in self.next:
            s = item + i
            self.next[i].traversal(s)
    def autocomplete(self, item):
        i = 0
        s = ''
        while i < len(item):
            k = item[i]
            s += k
            if k in self.next:
                self = self.next[k]
            else:
                return 'NOT FOUND'
            i += 1
        self.traversal(s)
        return ret_result

file1=open('/home/tarun2611/mysite/words.txt',mode='r')
l=file1.read()
word=[]
s=""
count=0
for i in l:
	if(i != "\n"):
		s+=i
	else:
		word.append(s)
		count+=1
		s=""
x = Node()
for i in word:
    x.add_item(i)


@app.route('/api/get', methods=['GET'])
def api_id():
    if 'id' in request.args:
        id = str(request.args['id'])
        r=jsonify(x.autocomplete(id))
        json_result=r
        del(r)
        ret_result.clear()
        return json_result
    else:
        return "Error: No id field provided. Please specify an id."

@app.route('/', methods=['GET'])
def home():
    return "<h1>Autocomplete</h1><p>http://tarun2611.pythonanywhere.com/api/get?id=      PLace any id to get the word autocompleted</p>"




