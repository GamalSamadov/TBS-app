const usernameField = document.getElementById('username');
const usernameFeedBack = document.querySelector('.in_feedback_username')
const emailField = document.getElementById('email');
const emailFeedBack = document.querySelector('.in_feedback_email')
const usernameSuccessOutPut = document.querySelector('.usernameSuccessOutPut')
const emailSuccessOutPut = document.querySelector('.emailSuccessOutPut')
const showPassword = document.querySelector("#showPassword");
const hidePassword = document.querySelector("#hidePassword");
const password = document.querySelector("#password");

usernameField.addEventListener('keyup', (e) => {
  const usernameVal = e.target.value;
  usernameSuccessOutPut.textContent = `${usernameVal} tekshirilmoqda...`;
  usernameField.classList.remove("is-invalid");
  usernameField.classList.remove("is-valid");
  usernameFeedBack.classList.remove("invalid-feedback");
  usernameFeedBack.style.display = "none";

  if(usernameVal.length > 0) {
    fetch('/foydalanuvchi-nomini-tekshirish/', {
      body : JSON.stringify({username: usernameVal}),
      method: "POST", 
    })
    .then((res) => res.json())
    .then((data)=> {
      usernameSuccessOutPut.style.display = "none";
      if(data.username_error){
        usernameField.classList.add("is-invalid");
        usernameFeedBack.classList.add("invalid-feedback");
        usernameFeedBack.style.display = "block";
        usernameFeedBack.innerHTML = `<p>${data.username_error}</p>`;
      };
      if(data.username_valid){
        usernameField.classList.add("is-valid");
        usernameFeedBack.classList.add("valid-feedback");
        usernameFeedBack.style.display = "block";
        usernameFeedBack.innerHTML = `<p>To'g'ri tanlov</p>`;
      }
    });
  }
});

emailField.addEventListener('keyup', (e) => {
  const emailVal = e.target.value;
  emailSuccessOutPut.textContent = `${emailVal} tekshirilmoqda...`;
  emailField.classList.remove("is-invalid");
  emailField.classList.remove("is-valid");
  emailFeedBack.classList.remove("invalid-feedback");
  emailFeedBack.style.display = "none";

  if(emailVal.length > 0) {
    fetch('/emailni-tekshirish/', {
      body : JSON.stringify({email: emailVal}),
      method: "POST", 
    })
    .then((res) => res.json())
    .then((data)=> {
      emailSuccessOutPut.style.display = 'none';
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


showPassword.addEventListener("click", function () {
    // toggle the type attribute
    const type = password.getAttribute("type") === "password" ? "text" : "password";
    password.setAttribute("type", type);
    
    // toggle the icon
    showPassword.style.display = 'none';
    hidePassword.style.display = 'block';
});

hidePassword.addEventListener("click", function () {
  // toggle the type attribute
  const type = password.getAttribute("type") === "text" ? "password" : "text";
  password.setAttribute("type", type);
  
  // toggle the icon
  showPassword.style.display = 'block';
  hidePassword.style.display = 'none';
});

// prevent form submit
const form = document.querySelector("form");
form.addEventListener('submit', function (e) {
    e.preventDefault();
});