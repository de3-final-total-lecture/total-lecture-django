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
    $('.what-do-i-learn-container').html(learn_html);

    // tag 구분자 제거
    var tagData = $('.tags').data('contents');
    if (tagData && tagData.trim() !== '') {
        var tags = tagData.split('|');
        var tag_html = '';
        tags.forEach(function(tag) {
            if (tag.trim() !== '') { // 태그 값이 빈 문자열이 아닌 경우에만 처리
                tag_html += '<button class="tag-item" data-tag="' + tag + '">' + '#' + tag + '</button>';
            }
        });
        $('.tags').html(tag_html);
    } else {
        $('.tags').html(''); // 태그 값이 없으면 HTML을 비움
    }

    var rating = parseFloat($('.lecture-rating').data('rating')); // rating 값을 data-attribute에서 가져옴
    $('#rating-stars').html(getStarRatingHtml(rating));

    $('#heart-icon, #sticky-heart-icon, #header-heart-icon').each(function() {
        const lectureId = $(this).data('lecture-id');
        const userId = window.currentUserId;

        console.log('Lecture ID:', lectureId); // 디버깅을 위한 로그

        // 로그인 여부와 관계없이 기본적으로 빈 하트를 설정
        $(this).removeClass('fa-solid fa-heart').addClass('fa-regular fa-heart');

        if (userId && lectureId) {
            // 사용자의 위시리스트에 강의가 있는지 확인
            $.ajax({
                url: `/wishlist/status/${lectureId}/`,
                method: 'GET',
                success: function(response) {
                    console.log('Response:', response); // 서버로부터의 응답을 로깅

                    if (response.is_in_wishlist) {
                        $(this).removeClass('fa-regular fa-heart').addClass('fa-solid fa-heart liked');
                    } else {
                        // 빈 하트를 명시적으로 설정
                        $(this).removeClass('fa-solid fa-heart').addClass('fa-regular fa-heart');
                    }
                }.bind(this), // 현재 요소에 'this'를 바인딩
                error: function(error) {
                    console.error('위시리스트 상태 확인 중 오류 발생:', error);
                }
            });
        }
    });

    $('#heart-icon, #sticky-heart-icon, #header-heart-icon').on('click', function() {
        console.log(this)
        const lectureId = $(this).data('lecture-id');
        const userId = window.currentUserId;

        if (!userId) {
            alert('로그인이 필요한 서비스입니다.');
            return;
        }

        const isLiked = $(this).hasClass('liked');
        const url = isLiked 
            ? `/user/${userId}/wishlist/remove/` 
            : `/user/${userId}/wishlist/add/`;

        // AJAX 요청을 통해 위시리스트 상태를 토글
        $.ajax({
            url: url,
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken') // CSRF 토큰을 가져오는 함수 사용
            },
            data: JSON.stringify({ lecture: lectureId }),
            success: function(response) {
                console.log(response)
                if (response.success) {
                    $(this).toggleClass('liked');
                    if ($(this).hasClass('liked')) {
                        $(this).removeClass('fa-regular fa-heart').addClass('fa-solid fa-heart');
                    } else {
                        $(this).removeClass('fa-solid fa-heart').addClass('fa-regular fa-heart');
                    }
                } else {
                    alert(response.message || '위시리스트 업데이트 중 오류가 발생했습니다.');
                }
            }.bind(this), // 현재 요소에 'this'를 바인딩
            error: function(error) {
                console.error('위시리스트 상태 업데이트 중 오류 발생:', error);
                alert('위시리스트 업데이트 중 오류가 발생했습니다.');
            }
        });
    });

    $('.price').each(function() {
        var price = $(this).text().replace('원', '').trim();
        var formattedPrice = price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        $(this).text(formattedPrice + '원');
    });

    $(document).on('click', '.num1', function() {
        var lectureId = $(this).data('lectureid');
        var lectureURL = base62Decode(lectureId);

        window.location.href = lectureURL;
    });

});

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

function toggleWishlist(lectureId, icon) {
    const csrftoken = getCookie('csrftoken');
    const userId = window.currentUserId;

    if (!userId) {
        alert('로그인이 필요한 서비스입니다.');
        return;
    }

    const isAdding = !icon.classList.contains('active');
    const url = isAdding 
        ? `/user/${userId}/wishlist/add/`
        : `/user/${userId}/wishlist/remove/`;

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            lecture: lectureId
        })
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else if (response.status === 403) {
            throw new Error('로그인이 필요합니다.');
        } else {
            throw new Error(isAdding ? '위시리스트 추가 실패' : '위시리스트 제거 실패');
        }
    })
    .then(data => {
        if (data.success) {
            icon.classList.toggle('active');
        } else {
            throw new Error(data.message || (isAdding ? '위시리스트 추가 실패' : '위시리스트 제거 실패'));
        }
    })
    .catch(error => {
        console.error('Error:', error);
        if (error.message === '로그인이 필요합니다.') {
            alert('로그인이 필요한 서비스입니다.');
            window.location.href = '/login/';
        } else {
            alert(isAdding ? '위시리스트 추가 중 오류가 발생했습니다.' : '위시리스트 제거 중 오류가 발생했습니다.');
        }
    });
}

// CSRF 토큰을 쿠키에서 가져오는 함수
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}