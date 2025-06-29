(function ($) {
    "use strict";

    // Spinner
    var spinner = function () {
        setTimeout(function () {
            if ($('#spinner').length > 0) {
                $('#spinner').removeClass('show');
            }
        }, 1);
    };
    spinner();
    
    
    // Initiate the wowjs
    new WOW().init();


    // Sticky Navbar
    $(window).scroll(function () {
        if ($(this).scrollTop() > 45) {
            $('.navbar').addClass('sticky-top shadow-sm');
        } else {
            $('.navbar').removeClass('sticky-top shadow-sm');
        }
    });
    
    
    // Dropdown on mouse hover
    const $dropdown = $(".dropdown");
    const $dropdownToggle = $(".dropdown-toggle");
    const $dropdownMenu = $(".dropdown-menu");
    const showClass = "show";
    
    $(window).on("load resize", function() {
        if (this.matchMedia("(min-width: 992px)").matches) {
            $dropdown.hover(
            function() {
                const $this = $(this);
                $this.addClass(showClass);
                $this.find($dropdownToggle).attr("aria-expanded", "true");
                $this.find($dropdownMenu).addClass(showClass);
            },
            function() {
                const $this = $(this);
                $this.removeClass(showClass);
                $this.find($dropdownToggle).attr("aria-expanded", "false");
                $this.find($dropdownMenu).removeClass(showClass);
            }
            );
        } else {
            $dropdown.off("mouseenter mouseleave");
        }
    });
    
    
    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 300) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({scrollTop: 0}, 1500, 'easeInOutExpo');
        return false;
    });


document.querySelectorAll('.btn-remove').forEach(button => {
    button.addEventListener('click', function() {
      const itemId = this.dataset.id;

      fetch("{% url 'admin_remove_from_cart' 0 %}".replace('0', itemId), {
        method: 'POST',
        headers: {
          'X-CSRFToken': '{{ csrf_token }}',
          'Accept': 'application/json',
        },
        credentials: 'same-origin',
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          const row = document.getElementById('cart-item-' + itemId);
          if (row) row.remove();
        } else {
          alert('Error: ' + (data.error || 'Unknown error'));
        }
      })
      .catch(err => {
        alert('Request failed. Try again.');
        console.error(err);
      });
    });
  });

    // Facts counter
    $('[data-toggle="counter-up"]').counterUp({
        delay: 10,
        time: 2000
    });


    // Modal Video
    $(document).ready(function () {
        var $videoSrc = "";
        $('.btn-play').click(function () {
            $videoSrc = $(this).data("src");
            console.log("Video source set to: " + $videoSrc);
        });

        $('#videoModal').on('shown.bs.modal', function (e) {
            console.log("Modal shown, setting video src to: " + $videoSrc + "?autoplay=1&modestbranding=1&showinfo=0");
            $("#video").attr('src', $videoSrc + "?autoplay=1&modestbranding=1&showinfo=0");
        });

        $('#videoModal').on('hidden.bs.modal', function (e) {
            console.log("Modal hidden, clearing video src");
            $("#video").attr('src', "");
        });
    });

document.querySelectorAll('.toast').forEach(toastEl => {
    new bootstrap.Toast(toastEl, { delay: 4000 }).show();
});


    // Testimonials carousel
    $(".testimonial-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 1000,
        center: true,
        margin: 24,
        dots: true,
        loop: true,
        nav : false,
        responsive: {
            0:{
                items:1
            },
            768:{
                items:2
            },
            992:{
                items:3
            }
        }
    });
    
})(jQuery);

