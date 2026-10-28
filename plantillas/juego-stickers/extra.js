(function(){
var h=document.getElementById('hora');
if(h){var t=function(){h.textContent=new Date().toLocaleTimeString('es-CO',{hour:'numeric',minute:'2-digit',second:'2-digit'}).toUpperCase()};t();setInterval(t,1000);}
})();
