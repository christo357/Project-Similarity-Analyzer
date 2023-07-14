from application import db

def projectDetails(result_docs):
  docs=[]
  for id,score in result_docs:
    print(id,score)
    record = db.Projects.find_one({"id":id})
    docs.append((record['id'],record['title'],record['abstract'],score))
  
  return docs