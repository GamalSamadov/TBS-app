const img = document.querySelector('.pasport_surati img');
const close = document.querySelector('.popup-image span');
img.addEventListener('click', () => {
  document.querySelector('.popup-image').style.display = 'block';
})
close.addEventListener('click', () => {
  document.querySelector('.popup-image').style.display = 'none';
})