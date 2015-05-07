import os
from flask import Flask, url_for, jsonify, request, render_template, abort
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, '../birds.sqlite')

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path

db = SQLAlchemy(app)


class ValidationError(ValueError):
    pass


class Bird(db.Model):
    __tablename__ = 'yaybirds' 
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer)
    score = db.Column(db.Integer)
    domain = db.Column(db.String)
    _id = db.Column(db.Integer)
    title = db.Column(db.String)
    author = db.Column(db.String)
    ups = db.Column(db.Integer)
    downs = db.Column(db.Integer)
    num_comments = db.Column(db.Integer)
    permalink = db.Column(db.String)
    name = db.Column(db.String)
    url = db.Column(db.String)

    def get_url(self):
        return url_for('get_bird', id=self.id, _external=True)

    def export_data(self):
        return {
            'self_url': self.get_url(),
            'name': self.name,
            'time': self.time,
            'score': self.score,
            'domain': self.domain,
            '_id': self._id,
            'title': self.title,
            'author': self.author,
            'ups': self.ups,
            'downs': self.downs,
            'num_comments':self.num_comments,
            'permalink':self.permalink,
            'name' : self.name,
            'url':self.url
        }

    def import_data(self, data):
        try:
            self.name =data['name']
            self.time =data['time']
            self.score =data['score']
            self.domain =data['domain']
            self._id =data['_id']
            self.title =data['title']
            self.author =data['author']
            self.ups =data['ups']
            self.downs =data['downs']
            self.num_comments =data['num_comments']
            self.permalink =data['permalink']
            self.name =data['name']
            self.url =data['url']
        except KeyError as e:
            raise ValidationError('Invalid bird: missing ' + e.args[0])
        return self


@app.route('/yaybirds/', methods=['GET'])
def get_birds():
    return jsonify({'birds': [bird.get_url() for bird in Bird.query.all()]})

@app.route('/yaybirds/<int:id>', methods=['GET'])
def get_bird(id):
    return jsonify(Bird.query.get_or_404(id).export_data())

@app.route('/yaybirds/', methods=['POST'])
def new_bird():
    bird = Bird()
    bird.import_data(request.json) # imports data from the req json to the bird object
    db.session.add(bird)
    db.session.commit()
    return jsonify({}), 201, {'Location': bird.get_url()}

@app.route('/yaybirds/<int:id>', methods=['PUT'])
def edit_bird(id):
    bird = Bird.query.get_or_404(id)
    bird.import_data(request.json)
    db.session.add(bird)
    db.session.commit()
    return jsonify({})


# todo: implement this template
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', error = e), 404

@app.route('/')
def index():
    highlight = {'min': 1, 'max': 2}
    birds = Bird.query.all()
    return render_template('index.html', birds=birds, highlight=highlight)

@app.route('/top10')
def top10():
     birds = Bird.query.order_by(Bird.ups.desc()).limit(10).all()
     return render_template('top10.html', birds=birds)

@app.route('/bottom10')
def bottom10():
     birds = Bird.query.order_by(Bird.downs.desc()).limit(10).all()
     return render_template('bottom10.html', birds=birds)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

