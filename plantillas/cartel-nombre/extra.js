(function(){
var b=document.querySelector('.menu-b'),p=document.querySelector('.pastilla');
if(b&&p){b.addEventListener('click',function(){var o=p.classList.toggle('abierta');b.setAttribute('aria-expanded',o)});
  p.querySelectorAll('.menu a').forEach(function(a){a.addEventListener('click',function(){p.classList.remove('abierta');b.setAttribute('aria-expanded','false')})});}
})();
