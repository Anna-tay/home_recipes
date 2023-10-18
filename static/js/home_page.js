
const add_recipe = document.querySelector('#add_recipe');

add_recipe.addEventListener('click', function(){
    window.location.href = "/entry";
})



const clear_search = document.querySelector("#clear_button");

clear_search.addEventListener('click', function(){
    const button = document.querySelector('#search_button');
    button.value = "";
})