from flask import render_template,url_for,request,redirect
from application import app

from .forms import abstractForm
from .compare import compareData
from .details import projectDetails

result_set=[1,2,3,4]

@app.route("/")
def index():
  return render_template('page1.html')

@app.route("/input_abstract", methods=["POST", "GET"])
def input_abstract():
  global result_set
  if request.method == "POST":
    form = abstractForm(request.form)
    input_abstract = form.abstract.data
    ranked_docs = compareData(input_abstract)
    result_set = projectDetails(ranked_docs)
    return redirect(url_for('output_results'))
  else:
    form=abstractForm()
  return render_template('page2.html',form =form)

@app.route("/results")
def output_results():
  return render_template('page3.html',result_set=result_set)