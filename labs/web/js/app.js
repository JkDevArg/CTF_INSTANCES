document.addEventListener('DOMContentLoaded', () => {
  const btns = document.querySelectorAll('.nav-btn');
  const panes = document.querySelectorAll('.pane');
  const accents = {'lab0':'#22c55e','lab1':'#3b82f6','lab2':'#f97316','lab3':'#a855f7','home':'#3b82f6'};

  function activate(id) {
    btns.forEach(b => b.classList.toggle('active', b.dataset.pane === id));
    panes.forEach(p => p.classList.toggle('active', p.id === 'pane-'+id));
    document.documentElement.style.setProperty('--acc', accents[id] || '#3b82f6');
  }

  btns.forEach(b => b.addEventListener('click', () => activate(b.dataset.pane)));
  activate('home');
});
