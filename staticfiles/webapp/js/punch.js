// let event_today = document.getElementById("aux").dataset.event;
// let firstbreak_today = document.getElementById("aux").dataset.firstbreak;
// let lunch_today = document.getElementById("aux").dataset.lunch;
// let secondbreak_today = document.getElementById("aux").dataset.secondbreak;
// let aux_url = document.getElementById("aux").dataset.url;
punch();
changeState();
changeAfk();
disabledBtn();

function punch() {
    $(".punchbtn").click(function (event) {
        event.preventDefault()
        var skip = 'False';
        var event_time_id = $(this).attr('id');
        if (event_time_id == 'end') { event_time_id = $(this).attr('name');}
        var event_id = $(this).attr('value');
        var name_event = $(this).attr('name');

        // For skip event
        if (event_time_id=='skip'){
            const steps = document.querySelectorAll(".step");
            steps.forEach((step, idx) =>{
                if(!step.disabled && step.name!='end'){
                    skip = 'True'
                    event_time_id = step.id;
                    event_id = step.value;
                }
            });
        }

        console.log('skip: '+skip);
        console.log('event_time_id: '+event_time_id);
        console.log('event_id: '+event_id);

        $.ajax({
            url: $(this).data('url'),
            type: 'POST',
            data: {
                'post_event_time_id': event_time_id,
                'post_event_id': event_id,
                'post_name_event': name_event,
                'csrfmiddlewaretoken': "{{ csrf_token }}",
                'action': 'post_event'
            },
            success: function (response) {
                // console.log(response);
                // document.getElementById("emp-punch").innerHTML = response;
                // swal("Good job!", "You clicked the button!", "success");
                window.location.reload();
            },
            error: function (rs, e) {
                console.log(rs.response);
                alert("Error!!!");
            }
        });
    });
}

function changeState() {
    const steps = document.querySelectorAll(".punchbtn");
    steps.forEach((step, idx) =>{
        if(step.name=='afk' || step.name=='skip'){
            changeText(step);
        }else{
            if(step.id === 'start'){
                step.disabled = false;
                document.getElementById("afk").disabled = true;
                document.getElementById("skip").disabled = true;
            }else if(step.dataset.flag==''){
                if(steps[idx-1].disabled && steps[idx-1].name=='start'){
                    step.disabled = false;
                }
                else if(steps[idx-1].dataset.flag=='True'){ 
                    step.disabled = false; 
                }else{
                    step.disabled = true; 
                }
            }else if(step.dataset.flag=='False'){
                if(step.name === 'start'){ 
                    step.disabled = true;
                }
                else{
                    step.disabled = false; 
                }
            }else{
                step.disabled = true;
            }
        }
        changeText(step);
    });
}

function changeText(btn) {
    if (btn.name!='skip'){
        if (btn.dataset.flag=='False'){
            if(btn.name!='start' && btn.name!='end')
                btn.innerText="End"
            else if(btn.name=='end')
                btn.innerText="End Shift";
            btn.classList.add("step-finish");
        }
        else {
            btn.classList.remove("step-finish");
        }
    }
}

function changeAfk() {
    let aux = document.querySelector(".afkbtn");
    if(aux.dataset.flag=='False'){
        const steps = document.querySelectorAll(".step");
        steps.forEach((step, idx) =>{
            step.disabled = true;
        });
        document.querySelector(".skipbtn").disabled = true;
        aux.innerText="End AFK";
    }
}

function disabledBtn() {
    let aux = document.querySelector(".endbtn");
    if(aux.dataset.flag=='True'){
        const steps = document.querySelectorAll(".step");
        steps.forEach((step, idx) =>{
            step.disabled = true;
        });
        document.querySelector(".afkbtn").disabled = true;
        document.querySelector(".skipbtn").disabled = true;
    }
}