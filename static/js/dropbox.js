
function chooseFile() {
    // Trigger the hidden file input
    document.getElementById('upload-btn').click();
}

function handleFile(files) {
    // Display the list of uploaded files
    const fileList = document.getElementById('file-list');
    fileList.innerHTML = '';

    for (let i = 0; i < files.length; i++) {
        const file = files[i];
        const listItem = document.createElement('div');
        listItem.textContent = file.name;
        fileList.appendChild(listItem);
    }
}