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
    const THRESHOLD = 70;

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

    // Left panel wheel
    if (leftPanel) {
      leftPanel.addEventListener('wheel', (e) => {
        if (window.innerWidth > 768) advanceFrames(e.deltaY);
      }, { passive: true });
    }

    // Right panel scroll — batch via rAF so rapid events don't stack
    const rightPanel = document.querySelector('.landing-panel-right');
    if (rightPanel && window.innerWidth > 768) {
      let lastScrollTop = 0;
      let pending = 0;
      let rafQueued = false;

      rightPanel.addEventListener('scroll', () => {
        const delta = rightPanel.scrollTop - lastScrollTop;
        lastScrollTop = rightPanel.scrollTop;
        pending += delta * 0.65;

        if (!rafQueued) {
          rafQueued = true;
          requestAnimationFrame(() => {
            advanceFrames(pending);
            pending = 0;
            rafQueued = false;
          });
        }
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
