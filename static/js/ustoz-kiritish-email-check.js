const emailField = document.getElementById('email');
const emailFeedBack = document.querySelector('.in_feedback_email')

emailField.addEventListener('keyup', (e) => {
  const emailVal = e.target.value;
  emailField.classList.remove("is-invalid");
  emailFeedBack.classList.remove("invalid-feedback");
  emailFeedBack.style.display = "none";

  if(emailVal.length > 0) {
    fetch('/ustozlar/kiritish/emailni-tekshirish/', {
      body : JSON.stringify({email: emailVal}),
      method: "POST", 
    })
    .then((res) => res.json())
    .then((data)=> {
      if(data.email_error){
        emailField.classList.add("is-invalid");
        emailFeedBack.classList.add("invalid-feedback");
        emailFeedBack.style.display = "block";
        emailFeedBack.innerHTML = `<p>${data.email_error}</p>`;
      };
      if(data.email_valid){
        emailField.classList.add("is-valid");
        emailFeedBack.classList.add("valid-feedback");
        emailFeedBack.style.display = "block";
        emailFeedBack.innerHTML = `<p>To'g'ri tanlov</p>`;
      }
    });
  }
});