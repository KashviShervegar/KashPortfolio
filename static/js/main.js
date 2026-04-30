/* =============================================
   KASHVI SHERVEGAR — Portfolio JS
   ============================================= */

document.addEventListener('DOMContentLoaded', () => {

  // ── Stop-motion frame cycling ─────────────────
  // Wheel events on the left panel advance (scroll down) or reverse
  // (scroll up) Theo's frames. Hover/move has no effect.
  const animContainer = document.querySelector('.animation-container');
  const frames = animContainer ? Array.from(animContainer.querySelectorAll('.frame')) : [];
  const leftPanel = document.querySelector('.landing-panel-left');

  if (animContainer && frames.length > 0) {
    let currentFrame = 0;
    let accumulator = 0;
    const THRESHOLD = 40;

    const advanceFrames = (deltaY) => {
      accumulator += deltaY;

      while (accumulator >= THRESHOLD) {
        accumulator -= THRESHOLD;
        if (currentFrame < frames.length - 1) {
          frames[currentFrame].classList.remove('active');
          frames[++currentFrame].classList.add('active');
        }
      }
      while (accumulator <= -THRESHOLD) {
        accumulator += THRESHOLD;
        if (currentFrame > 0) {
          frames[currentFrame].classList.remove('active');
          frames[--currentFrame].classList.add('active');
        }
      }
    };

    // Desktop: wheel on left panel only
    if (leftPanel) {
      leftPanel.addEventListener('wheel', (e) => {
        if (window.innerWidth > 768) advanceFrames(e.deltaY);
      }, { passive: true });
    }

  }

  // ── Active nav link on interior pages ────────
  const currentPath = window.location.pathname;
  document.querySelectorAll('.header-nav-right a').forEach(link => {
    if (currentPath.endsWith(link.getAttribute('href'))) {
      link.classList.add('active');
    }
  });

  // ── Force-play sidequest videos on mobile ────
  if (window.innerWidth <= 768) {
    const videos = document.querySelectorAll('.sidequests-grid video');
    if (videos.length > 0) {
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) entry.target.play();
        });
      }, { threshold: 0.1 });
      videos.forEach(v => { v.play().catch(() => {}); observer.observe(v); });
    }
  }

});
