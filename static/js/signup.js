document.addEventListener('DOMContentLoaded', () => {

    // --- OTP Logic ---
    const otpInputs = document.querySelectorAll('.otp-box');
    const fullOtpInput = document.getElementById('full_otp');

    if (otpInputs.length > 0) {
        otpInputs.forEach((input, index) => {
            input.addEventListener('input', (e) => {
                if (e.target.value.length === 1) {
                    if (index < otpInputs.length - 1) {
                        otpInputs[index + 1].focus();
                    }
                }
                updateFullOtp();
            });

            input.addEventListener('keydown', (e) => {
                if (e.key === 'Backspace' && e.target.value === '') {
                    if (index > 0) {
                        otpInputs[index - 1].focus();
                    }
                }
            });

            // Add 'active' class on focus to simulate the red border
            input.addEventListener('focus', () => {
                otpInputs.forEach(i => i.classList.remove('active'));
                input.classList.add('active');
            });
        });

        function updateFullOtp() {
            let otp = '';
            otpInputs.forEach(input => otp += input.value);
            if (fullOtpInput) fullOtpInput.value = otp;
        }

        // Timer Logic
        const timerElement = document.getElementById('timer');
        if (timerElement) {
            let timeLeft = 120; // 2 minutes
            const timer = setInterval(() => {
                if (timeLeft <= 0) {
                    clearInterval(timer);
                    timerElement.textContent = "00:00";
                } else {
                    let minutes = Math.floor(timeLeft / 60);
                    let seconds = timeLeft % 60;
                    timerElement.textContent = `0${minutes}:${seconds < 10 ? '0' + seconds : seconds}`;
                    timeLeft--;
                }
            }, 1000);
        }
    }

    // --- Password Logic ---
    const passInput = document.getElementById('password');
    const togglePass = document.getElementById('togglePass');
    const toggleConf = document.getElementById('toggleConfPass');
    const confInput = document.getElementById('confirm_password');

    function toggleVisibility(icon, input) {
        if (!input) return;
        const type = input.getAttribute('type') === 'password' ? 'text' : 'password';
        input.setAttribute('type', type);
        if (type === 'password') {
            icon.classList.remove('fa-eye');
            icon.classList.add('fa-eye-slash');
        } else {
            icon.classList.remove('fa-eye-slash');
            icon.classList.add('fa-eye');
        }
    }

    if (togglePass && passInput) {
        togglePass.addEventListener('click', () => toggleVisibility(togglePass, passInput));
    }
    if (toggleConf && confInput) {
        toggleConf.addEventListener('click', () => toggleVisibility(toggleConf, confInput));
    }

    // Strength Meter Logic
    if (passInput) {
        passInput.addEventListener('input', () => {
            const val = passInput.value;
            const len = val.length >= 8;
            const num = /\d/.test(val);
            const sym = /[!@#$%^&*(),.?":{}|<>]/.test(val);

            // Update Requirements
            updateReq('req-len', len);
            updateReq('req-num', num);
            updateReq('req-sym', sym);

            // Update Meter
            let score = 0;
            if (len) score++;
            if (num) score++;
            if (sym) score++;

            const bars = [document.getElementById('bar1'), document.getElementById('bar2'), document.getElementById('bar3')];
            const label = document.getElementById('strengthVal');

            bars.forEach(b => b.classList.remove('filled'));

            if (score >= 1) bars[0].classList.add('filled');
            if (score >= 2) bars[1].classList.add('filled');
            if (score >= 3) bars[2].classList.add('filled');

            if (score === 0) { label.textContent = 'WEAK'; label.style.color = '#cc3333'; }
            else if (score === 1) { label.textContent = 'WEAK'; label.style.color = '#cc3333'; }
            else if (score === 2) { label.textContent = 'MEDIUM'; label.style.color = '#ff9900'; }
            else if (score === 3) { label.textContent = 'STRONG'; label.style.color = '#00ff00'; }
        });
    }

    function updateReq(id, met) {
        const el = document.getElementById(id);
        if (met) {
            el.classList.add('met');
            el.querySelector('i').classList.remove('fa-circle');
            el.querySelector('i').classList.add('fa-circle-check');
        } else {
            el.classList.remove('met');
            el.querySelector('i').classList.add('fa-circle');
            el.querySelector('i').classList.remove('fa-circle-check');
        }
    }
});
