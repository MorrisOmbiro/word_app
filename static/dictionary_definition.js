const get_def = async(btn) => {
    let word = btn.innerHTML;

    const resp = await fetch(`/proxy/${word}`);
    const data = await resp.json();
    if (resp.status !== 200) {
        // 404 or some error 
        // Told not to worry, browser will do this 
    } else {
        var pop_up = document.getElementById("pop_up");
        pop_up.style.display = "block";

        let def = document.getElementById("defs");
        if(typeof(data[0].shortdef) !== 'undefined') { // secure check 
            if (`${data[0].shortdef[0]}` == 'undefined')
                if(`${data[0].hwi.hw}` != 'undefined')
                    def.innerHTML = `${word}: Related in tense to: ${data[1].hwi.hw}`;
                else
                    def.innerHTML = `${word} not found in dictionary`;
            else 
                def.innerHTML = `${word}: ${data[0].shortdef[0]}`;  
        }else 
            def.innerHTML = `${word}: not found as an actual word\n`;         
    }
};

function close_popup() {
    document.getElementById("pop_up").style.display = "none";
}

window.onclick = function(event) {
    let pop_up = document.getElementById("pop_up");
    if (event.target == pop_up) 
        pop_up.style.display = "none";
}