const lectureListElement = document.getElementById('lectureList');
const prevPageButton = document.getElementById('prevPage');
const nextPageButton = document.getElementById('nextPage');
const mainCategorySelect = document.getElementById('mainCategory');
const midCategorySelect = document.getElementById('midCategory');
const sortTypeSelect = document.getElementById('sortType');
const pageNumbersElement = document.getElementById('pageNumbers');

const searchButton = document.getElementById('searchButton');
const searchInput = document.getElementById('searchInput');  
const searchButton2 = document.getElementById('searchButton2');
const searchInput2 = document.getElementById('searchInput2'); 

const levelSelect = document.getElementById('levelSelect');


mainCategorySelect.addEventListener('change', (e) => {
    populateMidCategories(e.target.value);
    loadPage(1);
});
midCategorySelect.addEventListener('change', () => loadPage(1));
sortTypeSelect.addEventListener('change', () => loadPage(1));
levelSelect.addEventListener('change', () => loadPage(1));
searchButton.addEventListener('click', () => loadPage(1));
searchInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {loadPage(1);}
});
searchButton2.addEventListener('click', () => loadPage(1));
searchInput2.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {loadPage(1);}
});
let currentPage = 1;
let categories = {};



async function fetchCategories() {
    const response = await fetch('/api/categories/');
    categories = await response.json();
    populateMainCategories();
}

function populateMainCategories() {
    mainCategorySelect.innerHTML = '<option value="">분야 선택</option>';
    Object.keys(categories).forEach(main => {
        const option = document.createElement('option');
        option.value = main;
        option.textContent = main;
        mainCategorySelect.appendChild(option);
    });
}

function populateMidCategories(main) {
    midCategorySelect.innerHTML = '<option value="">기술 선택</option>';
    if (main && categories[main]) {
        categories[main].forEach(mid => {
            const option = document.createElement('option');
            option.value = mid;
            option.textContent = mid;
            midCategorySelect.appendChild(option);
        });
    }
}

function toggleSearch() {
    const searchElement = document.getElementById('searchContainer');
    if (searchElement) {
        searchElement.classList.toggle('hidden');
    }
}

async function fetchLectures(page) {
    const mainCategory = mainCategorySelect.value;
    const midCategory = midCategorySelect.value;
    const sortType = sortTypeSelect.value;
    const level = levelSelect.value;
    const searchQuery = searchInput.value.trim() || searchInput2.value.trim();;
    
    console.log(searchInput)

    let url = `/api/lecture/?page=${page}`;
    if (mainCategory) url += `&main_category=${encodeURIComponent(mainCategory)}`;
    if (midCategory) url += `&mid_category=${encodeURIComponent(midCategory)}`;
    if (sortType) url += `&sort_type=${sortType}`;
    if (searchQuery) url += `&q=${encodeURIComponent(searchQuery)}`;
    if (level) url += `&level=${level}`;

    const response = await fetch(url);
    const data = await response.json();
    return data;
}

function renderLectures(lectures) {
    lectureListElement.innerHTML = '';
    lectures.forEach(lecture => {
        const lectureElement = document.createElement('div');
        lectureElement.classList.add('lecture-item');
        lectureElement.dataset.lectureId = lecture.lecture_id;
        lectureElement.innerHTML = `
            <div>
                <img src="${lecture.thumbnail_url}">
                <div class="info-container">
                    <p class="lecture-name">${lecture.lecture_name}</p>
                    <p class="teacher">${lecture.teacher}</p>
                    <p class="price">₩${lecture.price}</p>
                    <div class="review-container">
                        <i class="fa-solid fa-star" style="color: #FFD700"></i>
                        <p class="review-scope">${lecture.scope}</p>
                        <p class="review-count">(${lecture.review_count})</p>
                        <p class="level level-${lecture.level}">${lecture.level}</p>
                    </div>
                </div>
            </div>
        `;
        lectureListElement.appendChild(lectureElement);
    });


    document.querySelectorAll('.lecture-item').forEach(item => {
        item.addEventListener('click', () => {
            const lectureId = item.dataset.lectureId;
            window.location.href = `/lecture/detail/${lectureId}/`; // 상세 페이지로 이동
        });
    });
}

function updatePagination(data) {
    prevPageButton.disabled = !data.previous;
    nextPageButton.disabled = !data.next;

    pageNumbersElement.innerHTML = '';

    const totalPages = data.total_pages; 
    const currentPage = data.current_page;

    const maxPagesToShow = 5;
    let startPage = Math.max(1, currentPage - Math.floor(maxPagesToShow / 2));
    let endPage = startPage + maxPagesToShow - 1;

    if (endPage > totalPages) {
        endPage = totalPages;
        startPage = Math.max(1, endPage - maxPagesToShow + 1);
    }

    if (startPage > 1) {
        addPageButton(1);
        if (startPage > 2) addEllipsis();
    }

    for (let i = startPage; i <= endPage; i++) {
        addPageButton(i, i === currentPage);
    }

    if (endPage < totalPages) {
        if (endPage < totalPages - 1) addEllipsis();
        addPageButton(totalPages);
    }
}

function addPageButton(page, isActive = false) {
    const pageButton = document.createElement('button');
    pageButton.textContent = page;
    pageButton.classList.add('page-number');
    if (isActive) {
        pageButton.classList.add('active');
    }
    pageButton.addEventListener('click', () => loadPage(page));
    pageNumbersElement.appendChild(pageButton);
}

function addEllipsis() {
    const ellipsis = document.createElement('button');
    ellipsis.textContent = '...';
    ellipsis.disabled = true;
    pageNumbersElement.appendChild(ellipsis);
}

async function loadPage(page) {
    
    const data = await fetchLectures(page);
    renderLectures(data.results);
    updatePagination(data);
    currentPage = page;
    
}


prevPageButton.addEventListener('click', () => {
    if (currentPage > 1) {
        loadPage(currentPage - 1);
    }
});

nextPageButton.addEventListener('click', () => {
    loadPage(currentPage + 1);
});

fetchCategories().then(() => loadPage(1));
