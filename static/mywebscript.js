let RunSentimentAnalysis = () => {
    let textToAnalyze = document.getElementById("textToAnalyze").value;
    let responseBox = document.getElementById("responseBox");
    let systemResponse = document.getElementById("system_response");

    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4) {
            responseBox.style.display = "block";
            systemResponse.innerHTML = this.responseText;
            if (this.status === 400) {
                systemResponse.className = "response-error";
            } else {
                systemResponse.className = "response-success";
            }
        }
    };
    xhttp.open("GET", "emotionDetector?textToAnalyze=" + encodeURIComponent(textToAnalyze), true);
    xhttp.send();
}
