document.addEventListener("DOMContentLoaded", function () {

    let step = 0;

    let data = {
        fever: "",
        cough: "",
        breath: ""
    };

    let questions = [
        "هل لديك حرارة؟",
        "هل لديك سعال؟",
        "هل لديك ضيق في التنفس؟"
    ];

    window.start = function () {
        document.getElementById("intro").style.display = "none";
        document.getElementById("loading").style.display = "flex";

        setTimeout(() => {
            document.getElementById("loading").style.display = "none";
            document.getElementById("main").style.display = "flex";

            step = 0;
            document.getElementById("question").innerText = questions[0];
        }, 1500);
    }

    window.answer = function (value) {

        if (step === 0) data.fever = value;
        if (step === 1) data.cough = value;
        if (step === 2) data.breath = value;

        step++;

        if (step < questions.length) {
            document.getElementById("question").innerText = questions[step];
        } else {
            sendToProlog();
        }
    }

    function sendToProlog() {

        fetch("/diagnose", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        })
        .then(res => res.json())
        .then(res => {

            document.getElementById("box").innerHTML = `
    <h2>🩺 نتيجة التشخيص</h2>

    <div class="result-card">

        <div class="result-title">
            ${res.result}
        </div>

        <div class="result-section">
            <h3>📋 التوصيات</h3>
            <p>${res.advice}</p>
        </div>

        <div class="result-section doctor-box">
            <h3>👨‍⚕️ ملاحظة طبية</h3>
            <p>
            هذا التشخيص مبدئي ويعتمد على الأعراض المدخلة فقط.
            إذا استمرت الأعراض أو ازدادت شدتها يرجى مراجعة الطبيب.
            </p>
        </div>

        <button onclick="location.reload()">
            🔄 إعادة الفحص
        </button>

    </div>
`;
        })
        .catch(err => {
            console.log(err);
            document.getElementById("box").innerHTML =
                "<p>حدث خطأ في النظام</p>";
        });
    }

});