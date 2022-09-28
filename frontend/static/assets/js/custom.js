document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();

    document.querySelector(this.getAttribute('href')).scrollIntoView({
      behavior: 'smooth'
    });
  });
});

$(document).ready(function () {

  window.onscroll = function () { myFunction(), slow };

  // Get the header
  var header = document.getElementById("top");

  // Get the offset position of the navbar
  var sticky = header.offsetTop + 30;

  // Add the sticky class to the header when you reach its scroll position. Remove "sticky" when you leave the scroll position
  function myFunction() {
    if (window.pageYOffset > sticky) {
      header.classList.add("sticky");
    } else {
      header.classList.remove("sticky");
    }

    if ($(this).scrollTop() > 200) {
      $('#scrollToTop').fadeIn();
    } else {
      $('#scrollToTop').fadeOut();
    }
  }


  $('#scrollToTop').click(function () {
    $("html, body").animate({ scrollTop: 0 });
    return false;
  });

  $('.header-top .nav-item').on('show.bs.dropdown', function () {
    $("body").addClass("body-dropdown-top");
    $(".filter-data").removeClass("addlayer");

     // window.scrollTo(0, 0);
  })
  $('.header-top .nav-item').on('hidden.bs.dropdown', function () {
    $("body").removeClass("body-dropdown-top");
  })
  $('.header-bottom .nav-item').on('show.bs.dropdown', function () {
    $("body").addClass("body-dropdown-bottom");
    $(".filter-data").removeClass("addlayer");
    // window.scrollTo(0, 0);
  })
  $('.header-bottom .nav-item').on('hidden.bs.dropdown', function () {
    $("body").removeClass("body-dropdown-bottom");
  })

  // $('.header-top .nav-item').on('show.bs.dropdown', function () {
  //   $("body").addClass("body-dropdown-top");
  //   // window.scrollTo(0, 0);
  // })
  // $('.header-top .nav-item').on('hidden.bs.dropdown', function () {
  //   $("body").removeClass("body-dropdown-top");
  // })
  // $('.header-bottom .nav-item').on('show.bs.dropdown', function () {
  //   $("body").addClass("body-dropdown-bottom");
  //   // window.scrollTo(0, 0);
  // })
  // $('.header-bottom .nav-item').on('hidden.bs.dropdown', function () {
  //   $("body").removeClass("body-dropdown-bottom");
  // })

  // $(".category-list-ul a").on('click', function(event) {

  // // Make sure this.hash has a value before overriding default behavior
  //     if (this.hash !== "") {
  //       // Prevent default anchor click behavior
  //       event.preventDefault();

  //       // Store hash
  //       var hash = this.hash;

  //       // Using jQuery's animate() method to add smooth page scroll
  //       // The optional number (800) specifies the number of milliseconds it takes to scroll to the specified area
  //       $('html, body').animate({
  //         scrollTop: $(hash).offset().top - 110
  //       }, "slow", function(){

  //         // Add hash (#) to URL when done scrolling (default click behavior)
  //         window.location.hash = hash;
  //       });
  //     } // End if
  // });

  $("input.search.form-control").on('keyup', function () {
    // $(this).parents(".filter-data").addClass("addlayer");
    var count1 = $(".suggestions li").length;
    // alert(count1);
    if (count1 > 0) {
      $(".filter-data").addClass("addlayer");
    }
    else {
      $(".filter-data").removeClass("addlayer");
    }
  });

  $(".cookie_close_btn").on("click", function () {
    $(".cookie_wrapper").addClass("d-none");
    $(".footer_wrapper").removeClass("cookie_pad");
  });

  $(document).click(function (event) {
    if (!$(event.target).hasClass('suggestions')) {
      $(".filter-data").removeClass("addlayer");
    }
  });

  // const endpoint = 'https://gist.githubusercontent.com/Miserlou/c5cd8364bf9b2420bb29/raw/2bf258763cdddd704f8ffd3ea9a3e81d25e2c6f6/cities.json';

  const cities = [];

  // fetch(endpoint)
  //   .then(raw => raw.json())
  //   .then(data => cities.push(...data))

  // function findMatches(wordToMatch, cities) {
  //   return cities.filter(place => {
  //     const regex = new RegExp(wordToMatch, "gi");
  //     return place.city.match(regex) || place.state.match(regex)
  //   });
  // }

  // function numberWithCommas(x) {
  //   return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
  // }

  // function displayMatches() {

  //   const matchArray = findMatches(this.value, cities);
  //   const html = matchArray.map(place => {
  //     const regex = new RegExp(this.value, 'gi');
  //     const cityName = place.city.replace(regex, `<span class="hl">${this.value}</span>`);
  //     const stateName = place.state.replace(regex, `<span class="hl">${this.value}</span>`);
  //     return `
  //       <li>
  //         <span class="name">${cityName}, ${stateName}</span>
  //       </li>
  //     `;
  //   }).join('');
  //   suggestions.innerHTML = html;
  // }

  // const searchInput = document.querySelector(".search");
  // const suggestions = document.querySelector(".suggestions");
  // searchInput.addEventListener("change", displayMatches);
  // searchInput.addEventListener("keyup", displayMatches);

  $(document).on('click.bs.dropdown.data-api', '.header-bottom-drops', function (e) {
    e.stopPropagation();
  });
  // $(".category-item").click(function(){
  //     $(this).toggleClass("active_category");
  // })
});




const labels = [
  'Jan',
  'Feb',
  'Mar',
  'Apr',
  'May',
  'Jun',
  'Jul',
];

const data = {
  labels: labels,
  datasets: [{
    label: 'My First dataset',
    data: [65, 59, 80, 81, 56, 55, 40],
    backgroundColor: [
      'rgba(255, 99, 132, 0.2)',
      'rgba(255, 159, 64, 0.2)',
      'rgba(255, 205, 86, 0.2)',
      'rgba(75, 192, 192, 0.2)',
      'rgba(54, 162, 235, 0.2)',
      'rgba(153, 102, 255, 0.2)',
      'rgba(201, 203, 207, 0.2)'
    ],
    borderColor: [
      'rgb(255, 99, 132)',
      'rgb(255, 159, 64)',
      'rgb(255, 205, 86)',
      'rgb(75, 192, 192)',
      'rgb(54, 162, 235)',
      'rgb(153, 102, 255)',
      'rgb(201, 203, 207)'
    ],

  }]
};

const config = {
  type: 'bar',
  data: data,
  options: {
    scales: {
      y: {
        beginAtZero: true
      }
    }
  },
};
const myChart = new Chart(
  document.getElementById('myChart'),
  config
);

var thumbsize = 14;

function draw(slider, splitvalue) {

  /* set function vars */
  var min = slider.querySelector('.min');
  var max = slider.querySelector('.max');
  var lower = slider.querySelector('.lower');
  var upper = slider.querySelector('.upper');
  var legend = slider.querySelector('.legend');
  var thumbsize = parseInt(slider.getAttribute('data-thumbsize'));
  var rangewidth = parseInt(slider.getAttribute('data-rangewidth'));
  var rangemin = parseInt(slider.getAttribute('data-rangemin'));
  var rangemax = parseInt(slider.getAttribute('data-rangemax'));

  /* set min and max attributes */
  min.setAttribute('max', splitvalue);
  max.setAttribute('min', splitvalue);

  /* set css */
  min.style.width = parseInt(thumbsize + ((splitvalue - rangemin) / (rangemax - rangemin)) * (rangewidth - (2 * thumbsize))) + 'px';
  max.style.width = parseInt(thumbsize + ((rangemax - splitvalue) / (rangemax - rangemin)) * (rangewidth - (2 * thumbsize))) + 'px';
  min.style.left = '0px';
  max.style.left = parseInt(min.style.width) + 'px';
  min.style.top = lower.offsetHeight + 'px';
  max.style.top = lower.offsetHeight + 'px';
  legend.style.marginTop = min.offsetHeight + 'px';
  slider.style.height = (lower.offsetHeight + min.offsetHeight + legend.offsetHeight) + 'px';

  /* correct for 1 off at the end */
  if (max.value > (rangemax - 1)) max.setAttribute('data-value', rangemax);

  /* write value and labels */
  max.value = max.getAttribute('data-value');
  min.value = min.getAttribute('data-value');
  lower.innerHTML = min.getAttribute('data-value');
  upper.innerHTML = max.getAttribute('data-value');

}

function init(slider) {
  /* set function vars */
  var min = slider.querySelector('.min');
  var max = slider.querySelector('.max');
  var rangemin = parseInt(min.getAttribute('min'));
  var rangemax = parseInt(max.getAttribute('max'));
  var avgvalue = (rangemin + rangemax) / 2;
  var legendnum = slider.getAttribute('data-legendnum');

  /* set data-values */
  min.setAttribute('data-value', rangemin);
  max.setAttribute('data-value', rangemax);

  /* set data vars */
  slider.setAttribute('data-rangemin', rangemin);
  slider.setAttribute('data-rangemax', rangemax);
  slider.setAttribute('data-thumbsize', thumbsize);
  slider.setAttribute('data-rangewidth', slider.offsetWidth);

  /* write labels */
  var lower = document.createElement('span');
  var upper = document.createElement('span');
  lower.classList.add('lower', 'value');
  upper.classList.add('upper', 'value');
  lower.appendChild(document.createTextNode(rangemin));
  upper.appendChild(document.createTextNode(rangemax));
  slider.insertBefore(lower, min.previousElementSibling);
  slider.insertBefore(upper, min.previousElementSibling);

  /* write legend */
  var legend = document.createElement('div');
  legend.classList.add('legend');
  var legendvalues = [];
  for (var i = 0; i < legendnum; i++) {
    legendvalues[i] = document.createElement('div');
    var val = Math.round(rangemin + (i / (legendnum - 1)) * (rangemax - rangemin));
    legendvalues[i].appendChild(document.createTextNode(val));
    legend.appendChild(legendvalues[i]);

  }
  slider.appendChild(legend);

  /* draw */
  draw(slider, avgvalue);

  /* events */
  min.addEventListener("input", function () { update(min); });
  max.addEventListener("input", function () { update(max); });
}

function update(el) {
  /* set function vars */
  var slider = el.parentElement;
  var min = slider.querySelector('#min');
  var max = slider.querySelector('#max');
  var minvalue = Math.floor(min.value);
  var maxvalue = Math.floor(max.value);

  /* set inactive values before draw */
  min.setAttribute('data-value', minvalue);
  max.setAttribute('data-value', maxvalue);

  var avgvalue = (minvalue + maxvalue) / 2;

  /* draw */
  draw(slider, avgvalue);
}

var sliders = document.querySelectorAll('.min-max-slider');
sliders.forEach(function (slider) {
  init(slider);
});