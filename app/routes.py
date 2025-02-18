from flask import Blueprint, jsonify, request, render_template
from app.gemini_integration import generate_content

# Create a Blueprint for routes
main = Blueprint("main", __name__)

# Sample data (Replace with actual database queries later)
universities = [
    {"id": 1, "name": "University A", "deadline": "2025-01-15", "programs": ["CS", "Business"], "reviews": ["Great professors!", "Nice campus."], "career_paths": ["Software Developer", "Data Scientist"]},
    {"id": 2, "name": "University B", "deadline": "2025-02-10", "programs": ["Engineering", "Arts"], "reviews": ["Excellent faculty.", "Very challenging."], "career_paths": ["Civil Engineer", "Architect"]},
]

# Route: Home - Display the main page (index.html)
@main.route("/", methods=["GET"])
def home():
    if request.method == "POST":
        university_name = request.form.get("university_name")
        major_name = request.form.get("major_name")
        
        if not university_name or not major_name:
            return render_template("index.html", error="Please provide both university and major.")

        # Generate AI responses based on the inputs
        university_prompt = f"Which university would you like to explore? {university_name}"
        major_prompt = f"Which program would you like to explore? {major_name}"

        university_response = generate_content(university_prompt)
        major_response = generate_content(major_prompt)

        return render_template("index.html", university_response=university_response, major_response=major_response)

    # If GET request, just display the home page with the prompt
    prompt = "Which university would you like to explore?"
    major_prompt = "What major would you like to pursue?"
    return render_template("index.html", prompt=prompt, major_prompt=major_prompt)

# Route: Select a university and program, then provide details
@main.route("/explore", methods=["POST"])
def explore_university():
    data = request.json
    university_name = data.get("university_name")
    
    if not university_name:
        return jsonify({"error": "University name is required"}), 400

    # Find the university by name
    university = next((u for u in universities if u["name"].lower() == university_name.lower()), None)
    if not university:
        return jsonify({"error": f"University '{university_name}' not found."}), 404

    # Ask for program selection after selecting university
    prompt = f"Which program would you like to explore at {university_name}?"
    ai_response = generate_content(prompt)

    return jsonify({
        "university": university_name,
        "programs": university["programs"],
        "ai_prompt": ai_response
    })

# Route: Provide full university details after selecting program
@main.route("/university-details", methods=["POST"])
def university_details():
    data = request.json
    university_name = data.get("university_name")
    program_name = data.get("program_name")
    
    if not university_name or not program_name:
        return jsonify({"error": "Both university name and program name are required"}), 400

    # Find the university by name
    university = next((u for u in universities if u["name"].lower() == university_name.lower()), None)
    if not university:
        return jsonify({"error": f"University '{university_name}' not found."}), 404

    # Check if the program is offered at the university
    if program_name not in university["programs"]:
        return jsonify({"error": f"Program '{program_name}' is not offered at {university_name}."}), 404

    # Generate the overview of the university, deadlines, reviews, experiences, and career paths
    overview = f"Here's what you need to know about the {program_name} program at {university_name}."
    ai_response = generate_content(overview)

    return jsonify({
        "university_name": university_name,
        "program_name": program_name,
        "deadline": university["deadline"],
        "reviews": university["reviews"],
        "career_paths": university["career_paths"],
        "ai_overview": ai_response
    })
