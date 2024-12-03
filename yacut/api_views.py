from . import app, db



@app.route('/api/<int:id>/', methods = ['POST'])
def create_short_link(id):
    pass

@app.route('/api/id/<short_id>', methods = ['GET'])
def get_short_link(id):
    pass
