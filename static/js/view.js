// getting the big and small buttons
const make_small = document.querySelector('#big');
const make_big = document.querySelector('#small');
let recipe = document.getElementsByClassName('recipe_img')

for (let i = 0; i < recipe.length; i++) {
    recipe[i].style.height = '300px';
};

// adding event listers to them
make_big.addEventListener('click', function(){

    for (let i = 0; i < recipe.length; i++) {
        let height = recipe[i].style.height;
        let number = height.slice(0,-2);
        number = parseInt(number);
        recipe[i].style.height = number + 35 +"px";
    };
});

make_small.addEventListener('click', function(){

    for (let i = 0; i < recipe.length; i++) {
        let height = recipe[i].style.height;
        let number = height.slice(0,-2);
        number = parseInt(number);
        recipe[i].style.height = number - 35 +"px";
    };
});

