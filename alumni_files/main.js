(function ($) {
    "use strict";
    
    /*------ SVG img active ----*/
    SVGInject($('.injectable'));
    
    /*----------------------------
     sticky active
    ------------------------------ */  
    
	const stickyBar = $('.sticky-bar');
	if(stickyBar.length > 0){
		var stickyTop = stickyBar.offset().top;
		var $window = $(window);
		$window.on('scroll', function () {
			if ($window.scrollTop() > stickyTop) {
				$('.sticky-bar').addClass('stick');
			} else {
				$('.sticky-bar').removeClass('stick');
			}
		});
	}

    
    /*====== QuickInfo ======*/
    function quickInfo() {
        var searchTrigger = $('.header-aside-button'),
            endTriggersearch = $('.aside-close'),
            container = $('.header-aside-active');
        searchTrigger.on('click', function(e) {
            e.preventDefault();
            container.addClass('inside');
        });
        endTriggersearch.on('click', function() {
            container.removeClass('inside');
        });
    };
    quickInfo();
    
    /*---------------------
        light Dark Mode active
    --------------------- */
    function lightDarkMode() {
        var trigger = $('.light-dark-btn'),
            container = $('.body-dark-mode-wrap'),
            container2 = $('.light-dark-mode-wrap');
        trigger.on('click', function(e) {
            e.preventDefault();
            container.toggleClass('dark-visible');
            container2.toggleClass('dark-visible');
        })
    }
    lightDarkMode();
    
    /*====== SidebarSearch ======*/
    function sidebarSearch() {
        var searchTrigger = $('.search-active'),
            endTriggersearch = $('.search-close'),
            container = $('.main-search-active');
        
        searchTrigger.on('click', function(e) {
            e.preventDefault();
            container.addClass('search-visible');
        });
        
        endTriggersearch.on('click', function() {
            container.removeClass('search-visible');
        });
        
    };
    sidebarSearch();
    
    /*====== menu ======*/
    const slinky = $('#menu').slinky();
    
    /*------ ScrollUp -------- */
    $.scrollUp({
        scrollText: '<i class="las la-angle-up"></i>',
        easingType: 'linear',
        scrollSpeed: 900,
        animation: 'fade'
    });
    
    /*------ Wow Active ----*/
    new WOW().init();
    
    /*-------------------------
      Scroll Animation
    --------------------------*/
    AOS.init({
        once: true,
        duration: 1000,
    });
    
    /*---------------------
        Video popup
    --------------------- */
    $('.video-popup-active').magnificPopup({
        type: 'iframe',
        mainClass: 'mfp-fade',
        removalDelay: 160,
        preloader: false,
        zoom: {
            enabled: true,
        }
    });
    
    
    /*--------------------------------
        Mouse Parallax
    -----------------------------------*/
    var scene = $('#scene');
    if(scene.length > 0) {
        var parallaxInstance = new Parallax(scene.get(0), {
            relativeInput: true,
            hoverOnly: true,
        });
        if(window.outerWidth < 992){parallaxInstance.disable()}
    }
    
    /*---------------------
        toggle item active
    --------------------- */
    function itemToggler2() {
        $(".toggle-item-active").slice(0, 9).show();
        $(".item-wrapper").find(".loadMore").on('click', function(e) {
            e.preventDefault();
            $(this).parents(".item-wrapper").find(".toggle-item-active:hidden").slice(0, 3).slideDown();
            if ($(".toggle-item-active:hidden").length == 0) {
                $(this).parent('.toggle-btn').fadeOut('slow');
            }
        });
    }
    itemToggler2();
    
    // Home 1 Slider
    var sliderActive = new Swiper('.slider-active', {
        loop: true,
        speed: 750,
        effect: 'fade',
        navigation: {
            nextEl: '.home-slider-next',
            prevEl: '.home-slider-prev',
        },
        on: {
            init: function () {
                SVGInject($('.injectable'));
            },
        },
    });
    
    // Home 1 Slider
    var sliderActiveTwo = new Swiper('.slider-active-2', {
        loop: true,
        navigation: {
            nextEl: '.home-slider-next-2',
            prevEl: '.home-slider-prev-2',
        },
        on: {
            init: function () {
                SVGInject($('.injectable'));
            },
        },
        breakpoints: {
            320: {
                slidesPerView: 1
            },
            576: {
                slidesPerView: 2
            },
            992: {
                slidesPerView: 3
            }
        },
    });
    
    var panelSliderThree = new Swiper('.slider-active-3', {
        loop: true,
        centeredSlides: true,
        spaceBetween: 11,
        navigation: {
            nextEl: '.home-slider-next-3',
            prevEl: '.home-slider-prev-3',
        },
        on: {
            init: function () {
                SVGInject($('.injectable'));
            },
        },
        breakpoints: {
            320:  { slidesPerView: 1 },
            576:  { slidesPerView: 2 },
            768:  { slidesPerView: 3 },
            992:  { slidesPerView: 4 },
            1200: { slidesPerView: 5 }
        }
    });
    
    var relatedProduct = new Swiper('.related-gallery-active', {
        loop: true,
        spaceBetween: 30,
        breakpoints: {
            320: {
                slidesPerView: 1
            },
            576: {
                slidesPerView: 2
            },
            768: {
                slidesPerView: 2
            },
            992: {
                slidesPerView: 3
            },
            1200: {
                slidesPerView: 4
            },
            1500: {
                slidesPerView: 5
            }
        }
    });
    
    
    
})(jQuery);

