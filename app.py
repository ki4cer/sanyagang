from flask import Flask, render_template, request, redirect, url_for
from log_collector import log_collector

app = Flask(__name__)

@app.route('/')
def index():
    logs = log_collector.get_logs()
    return render_template('index.html', logs=logs)

@app.route('/add_log', methods=['POST'])
def add_log():
    log_level = request.form.get('log_level')
    message = request.form.get('message')
    log_collector.add_log(log_level, message)
    return redirect(url_for('index'))

@app.route('/delete_log/<int:log_id>', methods=['POST'])
def delete_log(log_id):
    log_collector.delete_log(log_id)
    return redirect(url_for('index'))

@app.route('/filter_logs', methods=['GET'])
def filter_logs():
    log_level = request.args.get('log_level')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    logs = log_collector.filter_logs(log_level, start_date, end_date)
    return render_template('index.html', logs=logs)

@app.route('/archive_logs', methods=['POST'])
def archive_logs():
    log_collector.archive_logs()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
