from flask import render_template,url_for,request,redirect,flash
from api.index import app
from api.index import db
from bson import ObjectId

from .forms import abstractForm
from .form2 import detailForm
from .compare import compareData
from .details import projectDetails

result_set=[]
input_abstract =''

@app.route("/")
def index():
  return render_template('index.html')

@app.route("/input_abstract", methods=["POST", "GET"])
def input_abstract():
  global result_set
  global input_abstract
  if request.method == "POST":
    form = abstractForm(request.form)
    input_abstract = form.abstract.data
    ranked_docs = compareData(input_abstract)
    result_set = projectDetails(ranked_docs)
    return redirect(url_for('output_results'))
  else:
    form=abstractForm()
  return render_template('search.html',form =form)

@app.route("/results")
def output_results():
  return render_template('results.html',result_set=result_set)

@app.route("/add_abstract", methods=['POST','GET'])
def add_abstract():
  global input_abstract
  if request.method == 'POST':
    form2 = detailForm(request.form)
    input_title = form2.title.data
    input_abstract = form2.abstract.data
    input_id = db.Projects.count() +1;
    
    db.Projects.insert_one({
      'id': input_id,
      'title': input_title,
      'abstract':input_abstract,
      'sentence':input_title+input_abstract
    })
    flash("Added to the database successfully!","success")
    return redirect("/input_abstract")
  else:
    form2 = detailForm()
    
   
    
    form2.abstract.data = input_abstract
  
  return render_template("add_details.html",form = form2)