from flask import Blueprint, render_template, redirect, url_for, request, send_file
from flask_login import login_user, login_required, logout_user, current_user, UserMixin
from app.utils import mock_users
from app.scanners.nmap_scan import run_nmap
from app.scanners.nikto_scan import run_nikto
import os

main_blueprint = Blueprint('main_blueprint', __name__)

# Route for home page
@main_blueprint.route('/')
def home():
    return render_template('login.html')

# Route for login
@main_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in mock_users and mock_users[username] == password:
            user = User(username)
            login_user(user)
            return redirect(url_for('main_blueprint.dashboard'))
        return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

# Route for dashboard
@main_blueprint.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

# Route for running Nmap scan
@main_blueprint.route('/run_nmap_scan', methods=["GET", "POST"])
@login_required
def run_nmap_scan():
    if request.method == "POST":
        target = request.form.get('target_ip')
        if target:
            try:
                result_file = run_nmap(target)
                return send_file(result_file, as_attachment=True)
            except Exception as e:
                return f"An error occurred: {e}"
        else:
            return "Target IP is missing."
    return render_template("nmap_form.html")

# Route for running Nikto scan
@main_blueprint.route('/run_nikto_scan', methods=["GET", "POST"])
@login_required
def run_nikto_scan():
    if request.method == "POST":
        target = request.form["target"]
        result_file = run_nikto(target)
        return send_file(result_file, as_attachment=True)
    return render_template("nikto_form.html")

# Route for viewing reports
@main_blueprint.route('/view_reports')
@login_required
def view_reports():
    report_folder = "app/static/reports"
    report_files = os.listdir(report_folder)
    return render_template("reports.html", reports=report_files)

# Route for logout
@main_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main_blueprint.login'))

# User class for handling user authentication
class User(UserMixin):
    def __init__(self, id):
        self.id = id
