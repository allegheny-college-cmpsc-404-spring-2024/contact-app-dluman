from flask import Flask, redirect, request, render_template
from contacts_model import Contact

Contact.load_db()
app: Flask = Flask(__name__)

@app.route("/")
def index():
    return redirect(location = "/contacts")

@app.route("/contacts/<contacts_id>", methods = ["GET"])
def contacts_view_get(*args, **kwargs):
    contact = Contact.find(kwargs["contacts_id"])
    return render_template("show.html", contact=contact)

@app.route("/contacts")
def contacts():
    search = request.args.get("q")
    print(search)
    if search:
        contacts_set = Contact.search(search)
        if request.headers.get('HX-Trigger') == 'search':
            return render_template("rows.html", contacts = contacts_set)
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
   if c.save():
      return redirect("/contacts")
   else:
      return render_template("new.html", contact = c)

@app.route("/contacts/<contact_id>/edit", methods = ["GET"])
def contacts_edit_get(contact_id = 0):
    contact = Contact.find(contact_id)
    return render_template("edit.html", contact=contact)

@app.route("/contacts/<contact_id>/edit", methods = ["POST"])
def contacts_edit_post(contact_id = 0):
    c = Contact.find(contact_id)
    c.update(request.form['first_name'], request.form['last_name'],
             request.form['phone'], request.form['email'])
    if c.save():
       return redirect(f"/contacts/{str(contact_id)}")
    else:
       return render_template("edit.html", contact=c)

@app.route("/contacts/<contact_id>", methods = ["DELETE"])
def contact_delete(contact_id = 0):
    contact = Contact.find(contact_id)
    contact.delete()
    if request.headers.get('HX-Trigger') == 'delete-link':
        return("/contacts", 303)
    else:
        return ""

if __name__ == "__main__":
    app.run(port = 5001)
