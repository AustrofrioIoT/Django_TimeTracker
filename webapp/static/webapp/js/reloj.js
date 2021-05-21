// JavaScript code
showTime();

function showTime(){
    myDate = new Date();
    hours = myDate.getHours();
    minutes = myDate.getMinutes();
    seconds = myDate.getSeconds();

    if (hours < 10) hours = 0 + hours;

    if (minutes < 10) minutes = "0" + minutes;

    if (seconds < 10) seconds = "0" + seconds;

    $("#HoraActual").text(hours+ ":" +minutes+ ":" +seconds);

    d = myDate.getDate();
    dia = (d < 10) ? '0' + d : d;
    m = myDate.getMonth() + 1;
    mes = (m < 10) ? '0' + m : m;
    anio = myDate.getFullYear();
    $("#FechaActual").text(dia+ "/" +mes+ "/" +anio);

    setTimeout("showTime()", 1000);
}