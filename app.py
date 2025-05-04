from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime

# Create the Flask application instance
app = Flask(__name__)

# Configure the SQLite database URI; the database file will be 'test.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

# Initialize the SQLAlchemy extension, binding it to our app
db = SQLAlchemy(app)

# Define the Todo model, which maps to a table in the database
class Todo(db.Model):
    # Primary key column, unique integer for each task
    id = db.Column(db.Integer, primary_key=True)
    # Content column, stores the task text (up to 200 characters), cannot be empty
    content = db.Column(db.String(200), nullable=False)
    # Timestamp column for when the task was created; defaults to current UTC time
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        # How this object is printed; useful for debugging
        return '<Task %r>' % self.id

# Route for the home page, handles both displaying tasks and adding a new one
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        # When the form is submitted, grab the 'content' field
        task_content = request.form.get('content')
        # Create a new Todo instance
        new_task = Todo(content=task_content)

        try:
            # Add to the database session and commit
            db.session.add(new_task)
            db.session.commit()
            # Redirect back to the home page to display updated list
            return redirect('/')
        except:
            # If something goes wrong, return an error message
            return 'There was an issue with your task'
    else:
        # For GET requests: query all tasks, ordered by creation time
        tasks = Todo.query.order_by(Todo.date_created).all()
        # Render the template, passing in the list of tasks
        return render_template('index.html', tasks=tasks)

# Route to delete a task by its ID
@app.route('/delete/<int:id>')
def delete(id):
    # Retrieve the task or return a 404 if not found
    task_to_delete = Todo.query.get_or_404(id)

    try:
        # Remove from session and commit
        db.session.delete(task_to_delete)
        db.session.commit()
        # Redirect back to home after deletion
        return redirect('/')
    except: 
        # On error, show a message
        return 'There was an issue with your task'
    
# Route stub for updating a task—handles both showing the edit form and saving changes
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    # TODO: implement logic to retrieve the task, render an edit form on GET,
    # and update + commit the task on POST.
    return ''

# Only run the server if this script is executed directly
if __name__ == "__main__":
    app.run(debug=True)
