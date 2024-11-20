filterButton.addEventListener('click', () => {
    filterButton.classList.toggle('active');
    if (filterButton.classList.contains('active')) {
        console.log('Фильтр активирован');
    } else {
        console.log('Фильтр деактивирован');
    }
});