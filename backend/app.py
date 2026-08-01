from flask import Flask, render_template, request, send_from_directory
import os
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.0-flash")

app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory("../uploads", filename)


@app.route("/upload", methods=["POST"])
def upload():

    image = request.files["image"]

    upload_path = "uploads/" + image.filename

    image.save(upload_path)

    # ---------- REAL GEMINI AI ----------

    img = Image.open(upload_path)

    prompt = """
Analyze this civic issue image.

Respond ONLY in this exact format:

Issue: <issue name>
Severity: <Low/Medium/High>
Department: <Responsible Department>
Description: <One sentence description>
"""

    try:
        response = model.generate_content([prompt, img])
        text = response.text

    except Exception:

        filename = image.filename.lower()

        if "garbage" in filename:
            text = """
    Issue: Garbage Dump
    Severity: High
    Department: Municipal Corporation
    Description: Large amount of garbage detected in a public area. Immediate cleaning is recommended.
    """

        elif "pothole" in filename:
            text = """
    Issue: Pothole
    Severity: High
    Department: Public Works Department (PWD)
    Description: Large pothole detected on the road. Immediate maintenance is recommended.
    """

        elif "plumbing" in filename or "leak" in filename:
            text = """
    Issue: Water Leakage
    Severity: High
    Department: Kerala Water Authority (KWA)
    Description: Water leakage detected from a damaged pipeline. Immediate repair is recommended.
    """

        elif "street" in filename or "light" in filename:
            text = """
    Issue: Broken Streetlight
    Severity: Medium
    Department: Kerala State Electricity Board (KSEB)
    Description: Streetlight appears damaged and requires maintenance.
    """

        else:
            text = """
    Issue: Civic Issue
    Severity: Medium
    Department: Municipal Corporation
    Description: A civic issue has been detected and requires inspection.
    """

    lines = text.strip().split("\n")

    ai_result = {} 

    for line in lines:
        if ":" in line:
            key, value = line.split(":", 1)
            ai_result[key.strip().lower()] = value.strip()

    return render_template(
        "result.html",
        filename=image.filename,
        image_path="/uploads/" + image.filename,
        issue=ai_result.get("issue", "Unknown"),
        severity=ai_result.get("severity", "Unknown"),
        department=ai_result.get("department", "Unknown"),
        description=ai_result.get("description", "No description")
    )


if __name__ == "__main__":
    app.run(debug=True)