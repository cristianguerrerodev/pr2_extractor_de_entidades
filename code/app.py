
from flask import Flask,render_template,url_for,request
import pandas as pd
import spacy
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

nlp = spacy.load('es_core_news_md')

app = Flask(__name__)

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/process',methods=["POST"])
def process():
	if request.method == 'POST':
		taskoption = request.form['taskoption']
		rawtext = request.form['rawtext']
		doc = nlp(rawtext)
		entities = []
		for ent in doc.ents:
			entities.append((ent.label_, ent.text))
			df = pd.DataFrame(entities, columns=('tipo', 'resultado'))

		if taskoption == 'organization':
			results = df.loc[df['tipo'] == 'ORG']['resultado']
			num_of_results = len(results)
		elif taskoption == 'person':
			results = df.loc[df['tipo'] == 'PER']['resultado']
			num_of_results = len(results)
		elif taskoption == 'location':
			results = df.loc[df['tipo'] == 'LOC']['resultado']
			num_of_results = len(results)
		elif taskoption == 'misc':
			results = df.loc[df['tipo'] == 'MISC']['resultado']
			num_of_results = len(results)
		
	return render_template("index.html",results=results,num_of_results = num_of_results)


if __name__ == '__main__':
	app.run(debug=True)