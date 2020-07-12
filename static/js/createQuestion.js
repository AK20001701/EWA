function changeTypeOfAnswer() {
    let value = document.getElementById("question_type").value;
    if (value === "option") {
        document.getElementById("optionAnswer").style.display = "block";
        document.getElementById("optionButton1").style.display = "block";
        document.getElementById("optionButton2").style.display = "block";
        document.getElementById("textAnswer").style.display = "none";
    } else if (value === "text") {
        document.getElementById("textAnswer").style.display = "block";
        document.getElementById("optionAnswer").style.display = "none";
        document.getElementById("optionButton1").style.display = "none";
        document.getElementById("optionButton2").style.display = "none";
    }
}

let count = 1;

function addOption() {
    let rootElement = document.getElementById("optionAnswer")
    count++;
    let countElement = document.getElementById("count")
    countElement.value = count;
    let newOption = document.createElement("div");
    newOption.className += "option"
    newOption.id = "option" + count;
    newOption.innerHTML =
        "<input class=\"question__cb\" type=\"checkbox\" id=\"cb" + count + "\" name=\"cb" + count + "\" value=\"" + count + "\"> " +
        "<input class=\"question__input\" type=\"text\" id=\"text" + count + "\" name=\"text" + count + "\" placeholder=\"Answer\">";
    rootElement.appendChild(newOption);
}

function remove() {
    let rootElement = document.getElementById("optionAnswer")
    let elementToRemove = document.getElementById("option" + count)
    rootElement.removeChild(elementToRemove)
    count--;
    let countElement = document.getElementById("count")
    countElement.value = count;
}