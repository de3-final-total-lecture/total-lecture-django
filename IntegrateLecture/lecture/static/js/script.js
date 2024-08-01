
$(document).ready(function() {

    $('.tab-button').click(function () {
        var target = $(this).data('target');
        var targetOffset = $('#' + target).offset().top - $('.tab-container').height();

        $('html, body').animate({
            scrollTop: targetOffset
        }, 500);

        // 클릭된 탭 버튼에 active 클래스 추가
        $('.tab-button').removeClass('active');
        $(this).addClass('active');
    });

    // 스크롤 시 탭 활성 상태 업데이트
    $(window).scroll(function () {
        var scrollPos = $(window).scrollTop();
        $('.tab-button').each(function () {
            var target = $(this).data('target');
            var targetOffset = $('#' + target).offset().top - $('.tab-container').height() - 10;

            if (scrollPos >= targetOffset) {
                $('.tab-button').removeClass('active');
                $(this).addClass('active');
            }
        });
    });

    // what_do_i_learn 구분자 제거
    var whatDoILearn = $('.lecture-whatlearn').data('contents');
    var learns = whatDoILearn.split('|');
    var learn_html = '';
    learns.forEach(function(learn) {
        learn_html += '<div class="item"> # ' + learn + '</div>';
    });
    $('#what-do-i-learn-container').html(learn_html);

    // tag 구분자 제거
    var tagData = $('.tags').data('contents');
    var tags = tagData.split('|');
    var tag_html = '';
    tags.forEach(function(tag) {
        tag_html += '<button>' + '#'+tag + '</button>';
    });
    $('.tags').html(tag_html);

    var rating = parseFloat($('.lecture-rating').data('rating')); // rating 값을 data-attribute에서 가져옴
    $('#rating-stars').html(getStarRatingHtml(rating));

    $('#heart-icon, #sticky-heart-icon, #header-heart-icon').on('click', function() {
        $(this).toggleClass('liked');
        if ($(this).hasClass('liked')) {
            $(this).removeClass('fa-regular fa-heart').addClass('fa-solid fa-heart');
        } else {
            $(this).removeClass('fa-solid fa-heart').addClass('fa-regular fa-heart');
        }
    });

    $('.price').each(function() {
        var price = $(this).text().replace('원', '').trim();
        var formattedPrice = price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        $(this).text(formattedPrice + '원');
    });

});

function searchLecture() {
    const query = encodeURIComponent(document.getElementById('searchInput').value.trim());
    if (query) {
        window.location.href = `/api/search/?q=${query}`;
    }
}

function getStarRatingHtml(rating) {
    const fullStar = '<i class="fa-solid fa-star"></i>';
    const halfStar = '<i class="fa-regular fa-star-half-stroke"></i>';
    const emptyStar = '<i class="fa-regular fa-star"></i>';
    
    let starsHtml = '';
    let fullStars = Math.floor(rating);
    let hasHalfStar = (rating % 1) >= 0.5;

    for (let i = 0; i < fullStars; i++) {
        starsHtml += fullStar+' ';
    }

    if (hasHalfStar) {
        starsHtml += halfStar+' ';
    }

    const totalStars = 5;
    const remainingStars = totalStars - fullStars - (hasHalfStar ? 1 : 0);
    for (let i = 0; i < remainingStars; i++) {
        starsHtml += emptyStar+' ';
    }

    return starsHtml;
}


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
