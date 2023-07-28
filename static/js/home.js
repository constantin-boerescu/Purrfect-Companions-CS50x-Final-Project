const selectOption1 = document.querySelector('.select-option1');
const selectOption2 = document.querySelector('.select-option2');
const selectOption3 = document.querySelector('.select-option3');
const selectLocations = document.querySelector('.locations');
const selectAges = document.querySelector('.ages');
const selectGenders = document.querySelector('.genders');


selectOption1.addEventListener('click', function(){
    selectLocations.classList.toggle('active');
});

selectOption2.addEventListener('click', function(){
    selectAges.classList.toggle('active');
});

selectOption3.addEventListener('click', function(){
    selectGenders.classList.toggle('active');
});


