
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

        // Create a canvas for image preview
        const canvas = document.createElement('canvas');
        canvas.width = 100; // Set the desired width for the preview
        canvas.height = 100; // Set the desired height for the preview
        listItem.appendChild(canvas);

        // Get the canvas element's 2D rendering context
        const ctx = canvas.getContext("2d");

        // Create an image element
        const img = new Image();

        // Set the source of the image (URL)
        const fileURL = URL.createObjectURL(file);
        img.src = fileURL;

        // Wait for the image to load before drawing it on the canvas
        img.onload = function() {
            // Draw the image on the canvas
            ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
        };
    }
}
