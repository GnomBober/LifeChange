function openCatalog() {
    document.getElementById('catalog-modal').style.display = 'flex';

    window.addEventListener('click',handleOutsideClick);
}

function closeCatalog() {
     document.getElementById('catalog-modal').style.display = 'none';

     window.removeEventListener('click',handleOutsideClick);
}

function handleOutsideClick(event) {
    const modal = document.getElementById('catalog-modal');
    const modalContent = document.querySelector('.modal-content');

    if(event.target == modal) {
        closeCatalog();
    }
}