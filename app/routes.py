from flask import Blueprint, render_template, request, redirect, url_for
from app.gemini_integration import generate_content
import requests

# Create a Blueprint for routes
main = Blueprint("main", __name__)

# Sample data (Replace with actual database queries later)
universities = [
    {"id": 1, "name": "University A", "deadline": "2025-01-15", "programs": ["CS", "Business"], "reviews": ["Great professors!", "Nice campus."], "career_paths": ["Software Developer", "Data Scientist"]},
    {"id": 2, "name": "University B", "deadline": "2025-02-10", "programs": ["Engineering", "Arts"], "reviews": ["Excellent faculty.", "Very challenging."], "career_paths": ["Civil Engineer", "Architect"]},
]

APPLICANT_TYPES = ['International student', 'Canadian student', 'Ontarian student']

# Route: Home - Display the main page (index.html)
@main.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        university_name = request.form.get("university_name")
        major_name = request.form.get("major_name")
        applicant_type = request.form.get("applicant_type")
        
        if not university_name or not major_name or not applicant_type:
            return render_template("index.html", error="Please provide university, major, and applicant type.")

        # Redirect to the next page to select between overview, prerequisites, and deadlines
        return redirect(url_for("main.select_option", university_name=university_name, major_name=major_name, applicant_type=applicant_type))

    # If GET request, just display the home page with the prompt
    prompt = "Which university would you like to explore?"
    major_prompt = "What major would you like to pursue?"
    return render_template("index.html", prompt=prompt, major_prompt=major_prompt)

# Route: Select option between overview, prerequisites, and deadlines
@main.route("/select-option", methods=["GET"])
def select_option():
    university_name = request.args.get("university_name")
    major_name = request.args.get("major_name")
    applicant_type = request.args.get("applicant_type")

    if not university_name or not major_name or not applicant_type:
        return redirect(url_for("main.home"))

    return render_template("select_option.html", university_name=university_name, major_name=major_name, applicant_type=applicant_type)

# Route: Overview - Display the university and major overview
@main.route("/overview", methods=["GET"])
def overview():
    university_name = request.args.get("university_name")
    major_name = request.args.get("major_name")
    applicant_type = request.args.get("applicant_type")

    if not university_name or not major_name or not applicant_type:
        return redirect(url_for("main.home"))

    # Generate overview based on university, major, and applicant type
    ai_overview = generate_content(f"Tell me about the {major_name} program at {university_name} for {applicant_type} students.")
    
    return render_template("overview.html", university_name=university_name, major_name=major_name, ai_overview=ai_overview)

# Route: Prerequisites - Display the prerequisites for the program
@main.route("/prerequisites", methods=["GET"])
def prerequisites():
    university_name = request.args.get("university_name")
    major_name = request.args.get("major_name")
    applicant_type = request.args.get("applicant_type")

    if not university_name or not major_name or not applicant_type:
        return redirect(url_for("main.home"))

    # Generate prerequisites based on university, major, and applicant type
    ai_prerequisites = generate_content(f"What are the prerequisites for the {major_name} program at {university_name} for {applicant_type} students?")
    
    return render_template("prerequisites.html", university_name=university_name, major_name=major_name, ai_prerequisites=ai_prerequisites)

    # Example: Building the query string to specify details
    query = f"Please provide the application deadlines for {applicant_type} applicants applying to the {program} program for the {intake} intake at McMaster University."

    # Call the Gemini API (replace this URL with the actual Gemini API endpoint)
    response = requests.get("https://gemini-api-url.com/deadlines", params={"query": query})
    
@main.route("/deadlines", methods=["GET"])
def deadlines():
    university_name = request.args.get("university_name")
    major_name = request.args.get("major_name")
    applicant_type = request.args.get("applicant_type")

    if not university_name or not major_name or not applicant_type:
        return redirect(url_for("main.home"))

    # Generate deadlines based on university, major, and applicant type
    ai_deadlines = generate_content(f"What are the application deadlines for the {major_name} program at {university_name} for {applicant_type} students?")
    
    # Print the ai_deadlines to check if it's returning content
    print("AI Deadlines:", ai_deadlines)

    return render_template("deadlines.html", university_name=university_name, major_name=major_name, ai_deadlines=ai_deadlines)
