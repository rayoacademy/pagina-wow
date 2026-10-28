(function(){
/* cuenta regresiva: <div class="cuenta" data-fecha="2026-12-01T09:00:00-05:00"> */
var c=document.querySelector('.cuenta[data-fecha]');
if(c){var f=new Date(c.getAttribute('data-fecha')).getTime(),q=function(s){return c.querySelector('[data-u='+s+']')};
  var dos=function(n){return(n<10?'0':'')+n};
  var t=function(){var r=Math.max(0,f-Date.now()),d=Math.floor(r/864e5),h=Math.floor(r/36e5)%24,m=Math.floor(r/6e4)%60,s=Math.floor(r/1e3)%60;
    q('d').textContent=d;q('h').textContent=dos(h);q('m').textContent=dos(m);q('s').textContent=dos(s);if(r<=0)c.classList.add('listo');};
  t();setInterval(t,1000);}
})();
