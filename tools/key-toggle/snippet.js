<script>
(function(){
var $=function(q){return document.querySelector(q)}, body=document.body;
if(location.search.indexOf('key')>-1)body.classList.add('key');
function syncKey(){$('#keybtn').classList.toggle('on',body.classList.contains('key'))}
$('#keybtn').onclick=function(){body.classList.toggle('key');syncKey()};
syncKey();
if(!document.querySelector('.ans'))$('#keybtn').hidden=true;
})();
</script>
