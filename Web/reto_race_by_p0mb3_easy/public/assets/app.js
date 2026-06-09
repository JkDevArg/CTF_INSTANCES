const timer = document.querySelector('[data-timer]');
if (timer) {
  let remaining = Number(timer.dataset.timer || '0');
  window.setInterval(() => {
    remaining = Math.max(0, remaining - 1);
    timer.textContent = `${remaining}s`;
    if (remaining === 0) {
      window.location.reload();
    }
  }, 1000);
}
