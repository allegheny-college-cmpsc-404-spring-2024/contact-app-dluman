from flask import Flask, redirect, request, render_template
from contacts_model import Contact

Contact.load_db()
app: Flask = Flask(__name__)

@app.route("/")
def index():
    return redirect(location = "/contacts")

@app.route("/contacts")
def contacts():
    search = request.args.get("q") or None
    if search is not None:
        contacts_set = Contact.search(search)
    else:
        contacts_set = Contact.all()
    return render_template(
        "index.html",
        contacts = contacts_set
    )

@app.route("/contacts/new", methods=['GET'])
def contacts_new_get():
   return render_template(
       "new.html",
       contact = Contact()
   )

@app.route("/contacts/new", methods=['POST'])
def contacts_new_post():
   c = Contact(None, request.form['first_name'],
               request.form['last_name'], request.form['phone'],
               request.form['email'])

if __name__ == "__main__":
    app.run(port = 5001)
