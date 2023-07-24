from flask import render_template,url_for,request,redirect,flash
from api.index import app
from api.index import db
from bson import ObjectId

from .forms import abstractForm
from .form2 import detailForm
# from .form_details import ResultForm
from .compare import compareData
# from .compare_glove import compareData
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

@app.route("/results",methods=['POST','GET'])
def output_results():
  # form = ResultForm()
  # if request.method == 'POST' and form.validate_on_submit():
  #     result_id = form.result_value.data
  #     print(result_id)
  #     # Process the result_value here as needed
  #     return redirect(url_for('result_details'),id=result_id)
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

@app.route('/results/<id>', methods=['GET', 'POST'])
def result_details(id):
    print(type(id))
    
    result = db.Projects.find_one({'id':int(id)})
    print('results',result)
    print('id',int(id))
    project =  []
    project.append(result['id'])
    project.append(result['title'])
    project.append(result['abstract'])
    
    print(project)

    return render_template('project_details.html', project = project)
