const progress = document.getElementById("progress-step");
const next = document.getElementById("next");
const prev = document.getElementById("prev");
const circles = document.querySelectorAll(".circle");

let currentActive = 1;
next.addEventListener("click", ()=>{
	currentActive++;
	if(currentActive > circles.length){
		currentActive = circles.length;
	}
	update();
});

prev.addEventListener("click", ()=>{
	currentActive--;
	if(currentActive < 1){
		currentActive = 1;
	}
	update();
});

function update(argument) {
	console.log("currentActive: " + currentActive);
	circles.forEach((circle, idx) =>{
		if (idx < currentActive){
			circle.classList.add("active");
		}else{
			circle.classList.remove("active");
		}
	});

	const actives = document.querySelectorAll(".active");
	progress.style.width = (((actives.length -1) / (circles.length -1)) * 100) + "%";

	if(currentActive === 1){
		prev.disabled = true;
		prev.classList.add("disabled");
	}else if(currentActive === circles.length){
		next.disabled = true;
		next.classList.add("disabled");
	}
	else{
		prev.disabled = false;
		prev.classList.remove("disabled");
		next.disabled = false;
		next.classList.remove("disabled");
	}
}