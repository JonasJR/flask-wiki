from flask import Flask, render_template, json, request, jsonify
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/done', methods=['POST'])
def done():
    json_list  = []
    with open('database.json', mode='a+') as data_file:
        try:
            data_file.seek(0)
            data = json.load(data_file)
            json_list = data["articles"]
        except ValueError, e:
            pass
    data_file.close()
    with open("database.json", mode="w+") as f:
        article = {'title' : str(request.form['title']), 'content' : str(request.form['content']), 'date' : str(request.form['date']), 'author' : str(request.form['author']), 'comment' : str(request.form['comment'])}
        to_delete = None
        for item in json_list:
            if item["title"] == article["title"]:
                to_delete = item
        if to_delete:
            json_list.remove(to_delete)
        json_list.append(article)
        json_obj = { 'articles' : json_list }
        json.dump(json_obj, f)
    return render_template('done.html')

@app.route('/articles/')
@app.route('/articles/<title>')
def articles(title=None):
    articles = []
    with open("database.json", mode="a+") as f:
        try:
            f.seek(0)
            data = json.load(f)
            json_list = data["articles"]
        except ValueError, e:
            json_list = {}
    f.close()
    if title:
        temp = None
        for item in json_list:
            if item["title"] == title:
                temp = item
        if temp:
            return render_template('article.html', article=temp)
        else:
            return render_template('create.html')
    else:
        for item in json_list:
            articles.append(item)
        return render_template('articles.html', articles=articles)

@app.route('/api/articles/')
@app.route('/api/articles/<title>')
def api(title=None):
    articles = []
    with open("database.json", mode="a+") as f:
        try:
            f.seek(0)
            data = json.load(f)
            json_list = data["articles"]
            if title:
                for item in json_list:
                    if item["title"] == title:
                        articles.append(item)
            else:
                for item in json_list:
                    articles.append(item)
        except ValueError, e:
            pass
    f.close()
    return jsonify(articles)

@app.route('/edit/articles/<title>')
def edit(title=None):
    article=None
    if title:
        with open("database.json", mode="a+") as f:
            try:
                f.seek(0)
                data = json.load(f)
                json_list = data["articles"]
                for item in json_list:
                    if item["title"] == title:
                        article=item
            except ValueError, e:
                pass
    return render_template('create.html', article=article)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('doesnotexist.html'), 404

if __name__ == "__main__":
    app.run(debug=True)
