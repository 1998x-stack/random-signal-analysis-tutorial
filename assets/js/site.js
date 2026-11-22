(()=>{"use strict";
const cards=[...document.querySelectorAll(".chapter-card")],search=document.getElementById("chapter-search"),status=document.getElementById("search-status"),empty=document.getElementById("empty-state");
if(search){search.addEventListener("input",()=>{const q=search.value.trim().toLowerCase();let n=0;for(const card of cards){const show=card.dataset.search.includes(q);card.hidden=!show;if(show)n++}for(const group of document.querySelectorAll(".catalog-group")){group.hidden=![...group.querySelectorAll(".chapter-card")].some(c=>!c.hidden)}status.textContent="匹配 "+n+" / "+cards.length+" 章";empty.hidden=n!==0})}
const prior=document.getElementById("prior"),posterior=document.getElementById("posterior");
if(prior&&posterior){const update=()=>{const p=Number(prior.value)/100;const post=.9*p/(.9*p+.05*(1-p));posterior.value=(100*post).toFixed(2)+"%";document.getElementById("prior-view").textContent=prior.value+"%"};prior.addEventListener("input",update);update()}
const upper=document.getElementById("upper"),area=document.getElementById("area");
if(upper&&area){const update=()=>{const b=Number(upper.value);document.getElementById("upper-view").textContent=b.toFixed(1);area.value=(Math.max(0,b-.5)/2).toFixed(3)};upper.addEventListener("input",update);update()}
const sigma=document.getElementById("sigma"),coverage=document.getElementById("coverage");
if(sigma&&coverage){const erf=x=>{const s=x>=0?1:-1,a=Math.abs(x),t=1/(1+.3275911*a),v=1-(((((1.061405429*t-1.453152027)*t)+1.421413741)*t-.284496736)*t+.254829592)*t*Math.exp(-a*a);return s*v};const update=()=>{const s=Number(sigma.value);document.getElementById("sigma-view").textContent=s.toFixed(1);coverage.value=(100*erf(1/(Math.sqrt(2)*s))).toFixed(2)+"%"};sigma.addEventListener("input",update);update()}
})();