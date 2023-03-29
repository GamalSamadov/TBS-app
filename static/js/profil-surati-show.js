const imgProfil = document.querySelector('.profil_surati img');
const closeProfil = document.querySelector('.popup-image-profil span');
imgProfil.addEventListener('click', () => {
  document.querySelector('.popup-image-profil').style.display = 'block';
})
closeProfil.addEventListener('click', () => {
  document.querySelector('.popup-image-profil').style.display = 'none';
})