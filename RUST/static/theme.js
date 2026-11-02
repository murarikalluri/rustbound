(() => {
  const key='rustbound-theme';
  let theme='dark';
  try { theme=localStorage.getItem(key) || (window.matchMedia?.('(prefers-color-scheme: light)').matches?'light':'dark'); } catch {}
  if(!['light','dark'].includes(theme))theme='dark';
  const apply=()=>{document.documentElement.dataset.theme=theme;document.querySelectorAll('[data-theme-toggle]').forEach(b=>{b.textContent=theme==='dark'?'☀ Light theme':'☾ Dark theme';b.setAttribute('aria-label',`Switch to ${theme==='dark'?'light':'dark'} theme`);});};
  apply();
  document.addEventListener('DOMContentLoaded',()=>{apply();document.querySelectorAll('[data-theme-toggle]').forEach(b=>b.addEventListener('click',()=>{theme=theme==='dark'?'light':'dark';try{localStorage.setItem(key,theme);}catch{}apply();}));});
})();
