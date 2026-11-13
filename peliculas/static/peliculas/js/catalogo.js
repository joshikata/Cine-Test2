const searchInput = document.querySelector('#movie-search');
const movieCards = [...document.querySelectorAll('.movie-card')];
const noResults = document.querySelector('#search-empty');

if (searchInput && movieCards.length && noResults) {
    const normalize = (value) => value
        .normalize('NFD')
        .replace(/[\u0300-\u036f]/g, '')
        .toLowerCase()
        .trim();

    const filterMovies = () => {
        const query = normalize(searchInput.value);
        let visibleCount = 0;

        movieCards.forEach((card) => {
            const matches = normalize(card.dataset.search).includes(query);
            card.hidden = !matches;
            if (matches) visibleCount += 1;
        });

        noResults.hidden = visibleCount > 0;
    };

    searchInput.addEventListener('input', filterMovies);
    document.addEventListener('keydown', (event) => {
        if (event.key === '/' && document.activeElement !== searchInput) {
            event.preventDefault();
            searchInput.focus();
        }
    });
}
