from flask import Flask, render_template, request

app = Flask(__name__)

# Function to assess abdominal trauma
def assess_abdominal_trauma(responses):
    trauma_score = 0

    if responses.get("abdominal_pain") == "yes":
        trauma_score += 1
    if responses.get("tenderness") == "yes":
        trauma_score += 1
    if responses.get("distension") == "yes":
        trauma_score += 1
    if responses.get("bruising") == "yes":
        trauma_score += 1
    if responses.get("history_trauma") == "yes":
        trauma_score += 1
    if responses.get("hemodynamic_instability") == "yes":
        trauma_score += 2  # Higher weight due to severity

    # Determine risk level
    if trauma_score >= 4:
        return {
            "level": "High Risk",
            "color": "danger",
            "icon": "⚠️",
            "message": "Immediate imaging (e.g., FAST ultrasound or CT scan) and surgical consultation recommended."
        }
    elif trauma_score == 3:
        return {
            "level": "Moderate Risk",
            "color": "warning",
            "icon": "⚠️",
            "message": "Consider imaging and close monitoring."
        }
    else:
        return {
            "level": "Low Risk",
            "color": "success",
            "icon": "✅",
            "message": "Continue monitoring and reassess as needed."
        }

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        responses = {key: request.form.get(key) for key in request.form}
        result = assess_abdominal_trauma(responses)
        return render_template("index.html", result=result)
    return render_template("index.html", result=None)

if __name__ == "__main__":
    app.run(debug=True)
