from flask import Flask,jsonify,request
app = Flask(__name__)
@app.route("/",methods = ["POST"])
def st():
    js = request.get_json()
    print(js)
    call = js['body']
    size = js['size']
    scale = js['scale']
    return f"{call}:{scale}:{size}"
if __name__ == "__main__":

    app.run()
