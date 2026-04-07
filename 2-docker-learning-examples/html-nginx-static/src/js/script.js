const button = document.getElementById('changeTextButton');
const message = document.getElementById('message');

if (button && message) {
    button.addEventListener('click', () => {
        message.textContent = 'Status: JavaScript berjalan dengan baik.';
    });
}
