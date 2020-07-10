function flagChange(id) {
            let flagOff = document.getElementById(id);
            let flagOn = document.getElementById(id + "On");

            if (flagOff.style.display === "block") {
                flagOff.style.display = "none"
                flagOn.style.display = "block"
            } else {
                flagOff.style.display = "block"
                flagOn.style.display = "none"
            }
        }