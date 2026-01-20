function togglePassword(fieldName, icon) {
    const field = document.querySelector(`input[name="${fieldName}"]`);

    if (field.type === "password") {
        field.type = "text";
        icon.textContent = "Hide";
    } else {
        field.type = "password";
        icon.textContent = "Show";
    }
}



const sendOtpBtn = document.getElementById("sendOtpBtn");
const verifyOtpBtn = document.getElementById("verifyOtpBtn");
const otpSection = document.getElementById("otpSection");
const passwordSection = document.getElementById("passwordSection");
const otpStatus = document.getElementById("otpStatus");
const verifyStatus = document.getElementById("verifyStatus");
const signupBtn = document.getElementById("signupBtn");

sendOtpBtn.addEventListener("click", () => {
    const email = document.getElementById("id_email").value.trim();
    const fname = document.getElementById("id_first_name").value.trim();
    const lname = document.getElementById("id_last_name").value.trim();

    if (!fname || !lname) {
        otpStatus.textContent = "Enter your full name first";
        return;
    }

    if (!email) {
        otpStatus.textContent = "Enter email first";
        return;
    }

    const formData = new FormData();
    formData.append("email", email);
    formData.append("first_name", fname);
    formData.append("last_name", lname);

    fetch("/singup/send_otp_mail/", {
        method: "POST",
        headers: {
            "X-CSRFToken": getCSRFToken()
        },
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        otpStatus.textContent = data.message || data.error;
        otpSection.style.display = "block";
        sendOtpBtn.disabled = true; // prevent spam
    });
});

verifyOtpBtn.addEventListener("click", () => {
    const otp = document.getElementById("otpInput").value.trim();
    const email = document.getElementById("id_email").value.trim();

    if (!otp) {
        verifyStatus.textContent = "Enter OTP";
        return;
    }

    fetch("/singup/validate_otp_mail/", {
        method: "POST",
        headers: {
            "X-CSRFToken": getCSRFToken(),
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: `email=${encodeURIComponent(email)}&otp=${encodeURIComponent(otp)}`
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            verifyStatus.textContent = "Email verified ✔";
            passwordSection.style.display = "block";
            signupBtn.style.display = "block";
            verifyOtpBtn.disabled = true;
        } else {
            verifyStatus.textContent = data.message || data.error;
        }
    });
});

function getCSRFToken() {
    return document.querySelector("[name=csrfmiddlewaretoken]").value;
}
