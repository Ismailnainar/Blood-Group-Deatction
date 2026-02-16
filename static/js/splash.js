document.addEventListener('DOMContentLoaded', () => {

    const SPLASH_DURATION = 4000; // Faster, cleaner
    const REDIRECT_URL = '/login/';

    // UI Elements
    const progressBar = document.querySelector('.loading-bar-fill');
    const loadingText = document.querySelector('.loading-text');
    const container = document.body;

    // --- Subtle ECG Animation ---
    const ecgCanvas = document.getElementById('ecgCanvas');
    if (ecgCanvas) {
        const ctx = ecgCanvas.getContext('2d');
        let width, height;

        const resize = () => {
            width = window.innerWidth;
            height = window.innerHeight;
            ecgCanvas.width = width;
            ecgCanvas.height = height;
        };
        window.addEventListener('resize', resize);
        resize();

        // State
        let x = 0;
        let y = height / 2;
        let lastY = y;
        let speed = 2; // Slower

        function animateECG() {
            // No fade trail, just clean line or slight fade
            // To be "clean", let's do a fade out rect
            ctx.fillStyle = 'rgba(3, 0, 0, 0.05)';
            ctx.fillRect(0, 0, width, height);

            ctx.lineWidth = 1;
            ctx.strokeStyle = "rgba(255, 0, 0, 0.2)"; // Very subtle
            ctx.shadowBlur = 0; // No glow for clean look

            ctx.beginPath();
            ctx.moveTo(x, lastY);

            x += speed;
            let nextY = height / 2;

            // Very simple beat
            const cycle = x % 600;
            if (cycle > 300 && cycle < 400) {
                if (cycle < 320) nextY -= 10;
                else if (cycle < 340) nextY += 10;
                else if (cycle < 360) nextY -= 40; // Soft spike
                else if (cycle < 380) nextY += 15;
            }

            ctx.lineTo(x, nextY);
            ctx.stroke();

            lastY = nextY;

            if (x > width) {
                x = 0;
                lastY = height / 2;
                ctx.moveTo(0, lastY);
            }
            requestAnimationFrame(animateECG);
        }
        animateECG();
    }

    // --- Smooth Progress ---
    let startTime = null;

    function updateBoot(timestamp) {
        if (!startTime) startTime = timestamp;
        const elapsed = timestamp - startTime;
        const progress = Math.min((elapsed / SPLASH_DURATION) * 100, 100);

        if (progressBar) progressBar.style.width = `${progress}%`;

        // Simple text updates
        if (loadingText) {
            if (progress < 30) loadingText.textContent = "Initializing System...";
            else if (progress < 60) loadingText.textContent = "Verifying Security...";
            else if (progress < 90) loadingText.textContent = "Connecting to Server...";
            else loadingText.textContent = "Ready.";
        }

        if (progress < 100) {
            requestAnimationFrame(updateBoot);
        } else {
            setTimeout(() => {
                // Smooth fade out
                document.body.style.transition = "opacity 0.8s ease";
                document.body.style.opacity = "0";
                setTimeout(() => window.location.replace(REDIRECT_URL), 800);
            }, 200);
        }
    }

    requestAnimationFrame(updateBoot);
});
