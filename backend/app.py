from flask import Flask, render_template, request, redirect

app = Flask(__name__)
taskList = []

@app.route('/add', methods=['POST'])
def add_task():
    task = request.form['user_input']
    taskList.append(task)
    return redirect('/')

@app.route('/')
def home():
    return render_template('index.html', taskList=taskList)

if __name__ == "__main__":
    app.run(debug=True) 