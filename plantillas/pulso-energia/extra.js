(function(){
/* mazo de tarjetas del equipo */
var cs=[].slice.call(document.querySelectorAll('.carta')),i=0;
function ver(n){if(!cs.length)return;i=(n+cs.length)%cs.length;cs.forEach(function(c,k){var d=(k-i+cs.length)%cs.length;c.style.setProperty('--d',d);c.classList.toggle('on',d===0);});}
document.querySelectorAll('[data-mazo]').forEach(function(b){b.addEventListener('click',function(){ver(i+(+b.getAttribute('data-mazo')))})});
ver(0);
})();
