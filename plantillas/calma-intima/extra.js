(function(){
/* numeral gigante: cambia según el paso que está en pantalla */
var num=document.getElementById('numero'),pasos=document.querySelectorAll('.paso');
if(num&&pasos.length&&'IntersectionObserver' in window){
  var io=new IntersectionObserver(function(es){es.forEach(function(x){if(x.isIntersecting){num.textContent=x.target.getAttribute('data-n');x.target.classList.add('activo');}else x.target.classList.remove('activo');});},{rootMargin:'-45% 0px -45% 0px'});
  pasos.forEach(function(p){io.observe(p)});
}
/* testimonios: uno a la vez */
var tq=[].slice.call(document.querySelectorAll('.tq')),i=0;
function ver(n){if(!tq.length)return;i=(n+tq.length)%tq.length;tq.forEach(function(t,k){t.classList.toggle('on',k===i)});}
document.querySelectorAll('[data-tq]').forEach(function(b){b.addEventListener('click',function(){ver(i+(+b.getAttribute('data-tq')))})});
})();
