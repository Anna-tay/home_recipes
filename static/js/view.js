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

function share_link(){
    // Get the current page URL
    var pageUrl = window.location.href;

    // Create a temporary input element
    var tempInput = document.createElement('input');
    tempInput.value = pageUrl;
    document.body.appendChild(tempInput);

    // Select the input value
    tempInput.select();
    tempInput.setSelectionRange(0, 99999); /* For mobile devices */

    // Copy the selected text to the clipboard
    document.execCommand('copy');

    // Remove the temporary input element
    document.body.removeChild(tempInput);

    // Optionally, provide user feedback (e.g., alert)
    alert('Link copied to clipboard: ' + pageUrl);
}

function go_qr(page_link){
    window.open(page_link, '_self');
}

// printing the recipe page
function printPage() {
    window.print();
}
