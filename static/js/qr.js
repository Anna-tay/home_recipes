// Function to generate QR code
function generateQRCode(link) {
    var qrcode = new QRCode(document.getElementById("qr-code"), {
        text: link,
        width: 128,
        height: 128
    });
}

// Function to print page
function printPage(url) {
    generateQRCode(url); // Replace with your link
    window.print();
}