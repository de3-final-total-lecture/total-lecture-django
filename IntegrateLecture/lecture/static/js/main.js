const lectureListElement = document.getElementById('lectureList');
const prevPageButton = document.getElementById('prevPage');
const nextPageButton = document.getElementById('nextPage');
const currentPageSpan = document.getElementById('currentPage');
const mainCategorySelect = document.getElementById('mainCategory');
const midCategorySelect = document.getElementById('midCategory');
const sortTypeSelect = document.getElementById('sortType');

let currentPage = 1;
let categories = {};

async function fetchCategories() {
    const response = await fetch('/api/categories/');
    categories = await response.json();
    populateMainCategories();
}

function populateMainCategories() {
    mainCategorySelect.innerHTML = '<option value="">All Main Categories</option>';
    Object.keys(categories).forEach(main => {
        const option = document.createElement('option');
        option.value = main;
        option.textContent = main;
        mainCategorySelect.appendChild(option);
    });
}

function populateMidCategories(main) {
    midCategorySelect.innerHTML = '<option value="">All Mid Categories</option>';
    if (main && categories[main]) {
        categories[main].forEach(mid => {
            const option = document.createElement('option');
            option.value = mid;
            option.textContent = mid;
            midCategorySelect.appendChild(option);
        });
    }
}

async function fetchLectures(page) {
    const mainCategory = mainCategorySelect.value;
    const midCategory = midCategorySelect.value;
    const sortType = sortTypeSelect.value;
    
    let url = `/api/lecture/?page=${page}`;
    if (mainCategory) url += `&main_category=${encodeURIComponent(mainCategory)}`;
    if (midCategory) url += `&mid_category=${encodeURIComponent(midCategory)}`;
    if (sortType) url += `&sort_type=${sortType}`;

    const response = await fetch(url);
    const data = await response.json();
    return data;
}

function renderLectures(lectures) {
    lectureListElement.innerHTML = '';
    lectures.forEach(lecture => {
        const lectureElement = document.createElement('div');
        lectureElement.classList.add('lecture-item');
        lectureElement.innerHTML = `
            <h2>${lecture.lecture_name}</h2>
            <p>${lecture.thumbnail_url}</p>
            <p>${lecture.review_count}</p>
            <p>${lecture.teacher}</p>
            <p>${lecture.level}</p>
            <p>${lecture.price}</p>
        `;
        lectureListElement.appendChild(lectureElement);
    });
}

function updatePagination(data) {
    prevPageButton.disabled = !data.previous;
    nextPageButton.disabled = !data.next;
    currentPageSpan.textContent = `Page ${currentPage}`;
}

async function loadPage(page) {
    try {
        const data = await fetchLectures(page);
        renderLectures(data.results);
        updatePagination(data);
        currentPage = page;
    } catch (error) {
        console.error('Error loading lectures:', error);
    }
}

mainCategorySelect.addEventListener('change', (e) => {
    populateMidCategories(e.target.value);
    loadPage(1);
});

midCategorySelect.addEventListener('change', () => loadPage(1));
sortTypeSelect.addEventListener('change', () => loadPage(1));

prevPageButton.addEventListener('click', () => {
    if (currentPage > 1) {
        loadPage(currentPage - 1);
    }
});

nextPageButton.addEventListener('click', () => {
    loadPage(currentPage + 1);
});

// 초기 로드
fetchCategories().then(() => loadPage(1));
