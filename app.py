from flask import Flask, request, jsonify, render_template
from pyswip import Prolog
import os

app = Flask(__name__)

prolog = Prolog()

prolog.consult(
    os.path.join(os.path.dirname(__file__), "logic.pl")
)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/diagnose", methods=["POST"])
def diagnose():

    data = request.json

    fever = data["fever"]
    cough = data["cough"]
    breath = data["breath"]

    prolog.retractall("answered(_, _)")

    prolog.assertz(f"answered(fever, {fever})")
    prolog.assertz(f"answered(cough, {cough})")
    prolog.assertz(f"answered(breath, {breath})")

    result = list(prolog.query("diagnosis(D)"))

    if len(result) > 0:

        disease = str(result[0]["D"])

        if disease == "covid19":
            diagnosis_name = "كوفيد-19"
            advice = """
الراحة، شرب السوائل بكثرة، ومراقبة الأعراض.
يفضل تجنب مخالطة الآخرين حتى التحسن.
راجع الطبيب إذا ظهرت صعوبة شديدة في التنفس أو ارتفاع مستمر في الحرارة.
"""

        elif disease == "flu":
            diagnosis_name = "الإنفلونزا"
            advice = """
الحصول على قسط كافٍ من الراحة.
شرب السوائل الدافئة بكثرة.
يمكن استخدام خافضات الحرارة عند الحاجة.
راجع الطبيب إذا استمرت الأعراض أو ازدادت.
"""

        elif disease == "common_cold":
            diagnosis_name = "الزكام العادي"
            advice = """
الراحة وشرب السوائل الدافئة.
عادة تتحسن الأعراض خلال أيام قليلة.
راجع الطبيب إذا استمرت الأعراض لفترة طويلة.
"""

        else:
            diagnosis_name = "التشخيص غير معروف"
            advice = "يرجى مراجعة الطبيب لإجراء تقييم طبي أدق."

        return jsonify({
            "result": diagnosis_name,
            "advice": advice
        })

    return jsonify({
        "result": "التشخيص غير معروف",
        "advice": "يرجى مراجعة الطبيب لإجراء تقييم طبي أدق."
    })

from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)