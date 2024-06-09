console.log('1')
let body = document.querySelector('body');
let slctBtn = document.querySelector('.select-btn')
let menu = document.querySelector('.main-nav')
let reg = document.querySelector('.register')
let dark = document.querySelector('.dark');
let light = document.querySelector('.light');
if (localStorage.getItem("dark")) {
  body.style.backgroundColor = '#595B82';
  slctBtn.style.backgroundColor = '#595B82';
  reg.style.backgroundColor = '#595B82';
  menu.style.color = '#fff';
 
}
dark.addEventListener('click', () => {
  body.style.backgroundColor = '#595B82';
  body.style.color = '#fff';
  slctBtn.style.backgroundColor = '#595B82';
  reg.style.backgroundColor = '#595B82';
  menu.style.color = '#fff';
  
  localStorage.setItem("dark", JSON.stringify(dark));
})
light.addEventListener('click', () => {
  body.style.backgroundColor = '#fff';
  body.style.color = '#000';
  slctBtn.style.backgroundColor = '#fff';
  reg.style.backgroundColor = '#fff';
  menu.style.color = '#595B82';
  localStorage.removeItem('dark');
})
