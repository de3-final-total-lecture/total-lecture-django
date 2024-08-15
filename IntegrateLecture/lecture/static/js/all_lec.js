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
const tagBoxes = document.querySelectorAll('.tag-box');
let start = 0;
let press = false;
let now = 1;
$('.banner-box').eq(0).on('mousedown', function(e){
    start = e.clientX;
    press = true;
});

$('.banner-box').eq(0).on('mousemove', function(e){
    if (press === true) {
        $('.banner-container').css('transform', 
        `translateX( ${e.clientX - start}px )`)
    }
});
$('.banner-box').eq(0).on('mouseup', function(e){
    press = false;
    if (e.clientX - start < -100) {
        $('.banner-container').css('transition', 
        'all 0.5s').css('transform', 'translateX(-100vw)');
    } else {
        $('.banner-container').css('transition', 
        'all 0.5s').css('transform', 'translateX(0vw)');
    }
    setTimeout(()=>{
        $('.banner-container').css('transition', 'none')
    }, 500)
});


// $('.next').on('click', function(){
//     if(now == 1){
//         $('.banner-container').css('transform', 'translateX(-100vw)');
//         now++;
//     }else if(now == 2){
//         $('.banner-container').css('transform', 'translateX(-200vw)');
//         now++;
//     }
// })
// $('.before').on('click', function(){
//     if(now == 2){
//         $('.banner-container').css('transform', 'translateX(0vw)');
//         now = 1;
//     }else if(now == 3){
//         $('.banner-container').css('transform', 'translateX(-100vw)');
//         now = 2;
//     }
// })

let currentIndex = 0;
const totalBanners = Math.min($('.banner-box').length, 9); // 최대 9개의 배너까지만 허용

$('.next').on('click', function() {
    if (currentIndex < totalBanners - 1) {
        currentIndex++;
    } else {
        currentIndex = 0; // 9번째에서 다시 첫 번째로 이동
    }
    $('.banner-container').css('transform', `translateX(-${100 * currentIndex}vw)`);
});

$('.before').on('click', function() {
    if (currentIndex > 0) {
        currentIndex--;
    } else {
        currentIndex = totalBanners - 1; // 첫 번째에서 마지막으로 이동
    }
    $('.banner-container').css('transform', `translateX(-${100 * currentIndex}vw)`);
});

mainCategorySelect.addEventListener('change', (e) => {
    populateMidCategories(e.target.value);
    loadPage(1);
});
midCategorySelect.addEventListener('change', () => loadPage(1));
sortTypeSelect.addEventListener('change', () => loadPage(1));
levelSelect.addEventListener('change', () => loadPage(1));
searchButton.addEventListener('click', () => loadPage(1));
searchInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        const searchValue = searchInput.value.trim();

        $.ajax({
            url: searchUrl,
            method: 'POST',
            data: {
                'searchKeyword': searchValue,
                'user_id': window.currentUserId
            },
            success: function(response) {
                console.log(response.message);
            },
            error: function(xhr, status, error) {
                console.error(error);
            }
        });
        loadPage(1);}
});
searchButton2.addEventListener('click', () => loadPage(1));
searchInput2.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {loadPage(1);}
});
let currentPage = 1;
let categories = {};
let sQuery = '';




tagBoxes.forEach(tagBox => {
    tagBox.addEventListener('click', () => {
        const tag = tagBox.getAttribute('data-tag'); // 클릭한 태그의 값을 가져오기
        console.log(tag);
        sQuery = tag;
        loadPage(1);
    });
});


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
    const searchQuery = searchInput.value.trim() || searchInput2.value.trim() || sQuery;

    //api 호출용 url
    let url = `/api/lecture/?page=${page}`;
    if (mainCategory) url += `&main_category=${encodeURIComponent(mainCategory)}`;
    if (midCategory) url += `&mid_category=${encodeURIComponent(midCategory)}`;
    if (sortType) url += `&sort_type=${encodeURIComponent(sortType)}`;
    if (searchQuery) url += `&q=${encodeURIComponent(searchQuery)}`;
    if (level) url += `&level=${level}`;

    //화면에 보여지는 url에도 변경사항 반영
    let displayUrl = `/main/?page=${page}`;
    if (mainCategory) displayUrl += `&main_category=${encodeURIComponent(mainCategory)}`;
    if (midCategory) displayUrl += `&mid_category=${encodeURIComponent(midCategory)}`;
    if (sortType) displayUrl += `&sort_type=${encodeURIComponent(sortType)}`;
    if (searchQuery) displayUrl += `&q=${encodeURIComponent(searchQuery)}`;
    if (level) displayUrl += `&level=${encodeURIComponent(level)}`;

    window.history.pushState({}, null, displayUrl);

    const response = await fetch(url);
    const data = await response.json();
    return data;
}

function checkUrl(strUrl) {
    let expUrl = /^http[s]?:\/\/([\S]{3,})/i;
    return expUrl.test(strUrl);
}

function checkLectureData(lecture) {
    if (!checkUrl(lecture.lecture_url) || !checkUrl(lecture.thumbnail_url))
        return false;
    if (lecture.platform_name !== "coursera") {
        if (lecture.origin_price == null || lecture.price == null)
            return false;
    }
    if (lecture.description == null || lecture.description === "")
        return false;
    if (lecture.what_do_i_learn == null || lecture.what_do_i_learn === "")
        return false;
    return true;
}

function renderLectures(lectures) {
    lectureListElement.innerHTML = '';
    lectures.forEach(lecture => {
        if (!checkLectureData(lecture)) {
            console.log(lecture.lecture_url + " " + checkUrl(lecture.lecture_url))
            console.log(lecture.thumbnail_url + " " + checkUrl(lecture.thumbnail_url))
            console.log(lecture.platform_name + " " + lecture.origin_price + " " + lecture.price)
            console.log("description: " + lecture.description)
            console.log("what do i learn: " + lecture.what_do_i_learn)
            console.log(lecture.lecture_name + " was except from lecture list");
            return;
        }

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

function getCSRFToken() {
    return csrfToken;
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", getCSRFToken());
        }
    }
});