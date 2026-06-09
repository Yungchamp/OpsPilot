async function fetchIncidents(){
  const r = await fetch('/incidents');
  const data = await r.json();
  const el = document.getElementById('incidents');
  el.innerHTML = '<pre>'+JSON.stringify(data, null, 2)+'</pre>';
}
window.onload = ()=>{ fetchIncidents(); }
