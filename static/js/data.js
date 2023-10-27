function add_recipe_card(){
    let recipe_card = document.querySelector('#recipe-card');
    let add_button = document.querySelector('#recipe-button-add');

    recipe_card.setAttribute('style', 'display: content;');
    add_button.setAttribute('style', 'display: none;');
}

function recipe_alert(){
    // Scroll to the top of the page
    window.scrollTo(0, 0);

    let recipe_save = document.querySelector('#recipe_save');
    recipe_save.style.setProperty("display", "none");

    let confirm_message = document.querySelector('#confirm_message');
    confirm_message.style.setProperty("display", "block");

    let confirm_save = document.querySelector('#confirm_save');
    confirm_save.style.setProperty("display", "block");

}
