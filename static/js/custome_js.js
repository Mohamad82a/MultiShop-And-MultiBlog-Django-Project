// Dropdown categories

// document.addEventListener("DOMContentLoaded", function () {
//     document.querySelectorAll(".dropdown-icon").forEach(icon => {
//         icon.addEventListener("click", function (event) {
//             event.preventDefault();
//             let dropdownMenu = this.parentElement.nextElementSibling;
//
//             if (dropdownMenu) {
//                 dropdownMenu.style.display = dropdownMenu.style.display === "none" ? "block" : "none";
//             }
//         });
//     });
//
//     document.addEventListener("click", function (event) {
//         document.querySelectorAll(".dropdown-menu").forEach(menu => {
//             if (!menu.contains(event.target) && !menu.previousElementSibling.contains(event.target)) {
//                 menu.style.display = "none";
//             }
//         });
//     });
// });


// Dropdown Profile


// Dropdown sortings
// $(document).ready(function () {
//     $('.dropdown-toggle').dropdown();
// });
//
// $(document).ready(function () {
//     $('.dropdown-item').click(function () {
//         $('.dropdown-menu').removeClass('show');  // Hide dropdown after click
//     });
// });
//
//
// $(document).ready(function () {
//     $('.dropdown-item').click(function () {
//         $('.dropdown-menu').removeClass('show');
//         $('.dropdown-toggle').dropdown('hide');
//     });
// });

$(document).ready(function () {
    $('.dropdown-item').click(function () {
        let dropdown = $(this).closest('.dropdown');
        dropdown.find('.dropdown-toggle').dropdown('hide'); // Use Bootstrap's method to hide it properly
    });
});


// liked message

setTimeout(function () {
    document.getElementById("alert-message").style.display = "none";
}, 3000);


// price range filter
//  Script.js
const rangevalue =
    document.querySelector(".slider-container .price-slider");
const rangeInputvalue =
    document.querySelectorAll(".range-input input");

// Set the price gap
let priceGap = 500;

// Adding event listners to price input elements
const priceInputvalue =
    document.querySelectorAll(".price-input input");
for (let i = 0; i < priceInputvalue.length; i++) {
    priceInputvalue[i].addEventListener("input", e => {

        // Parse min and max values of the range input
        let minp = parseInt(priceInputvalue[0].value);
        let maxp = parseInt(priceInputvalue[1].value);
        let diff = maxp - minp

        if (minp < 0) {
            alert("minimum price cannot be less than 0");
            priceInputvalue[0].value = 0;
            minp = 0;
        }

        // Validate the input values
        if (maxp > 10000) {
            alert("maximum price cannot be greater than 10000");
            priceInputvalue[1].value = 10000;
            maxp = 10000;
        }

        if (minp > maxp - priceGap) {
            priceInputvalue[0].value = maxp - priceGap;
            minp = maxp - priceGap;

            if (minp < 0) {
                priceInputvalue[0].value = 0;
                minp = 0;
            }
        }

        // Check if the price gap is met
        // and max price is within the range
        if (diff >= priceGap && maxp <= rangeInputvalue[1].max) {
            if (e.target.className === "min-input") {
                rangeInputvalue[0].value = minp;
                let value1 = rangeInputvalue[0].max;
                rangevalue.style.left = `${(minp / value1) * 100}%`;
            } else {
                rangeInputvalue[1].value = maxp;
                let value2 = rangeInputvalue[1].max;
                rangevalue.style.right =
                    `${100 - (maxp / value2) * 100}%`;
            }
        }
    });

    // Add event listeners to range input elements
    for (let i = 0; i < rangeInputvalue.length; i++) {
        rangeInputvalue[i].addEventListener("input", e => {
            let minVal =
                parseInt(rangeInputvalue[0].value);
            let maxVal =
                parseInt(rangeInputvalue[1].value);

            let diff = maxVal - minVal

            // Check if the price gap is exceeded
            if (diff < priceGap) {

                // Check if the input is the min range input
                if (e.target.className === "min-range") {
                    rangeInputvalue[0].value = maxVal - priceGap;
                } else {
                    rangeInputvalue[1].value = minVal + priceGap;
                }
            } else {

                // Update price inputs and range progress
                priceInputvalue[0].value = minVal;
                priceInputvalue[1].value = maxVal;
                rangevalue.style.left =
                    `${(minVal / rangeInputvalue[0].max) * 100}%`;
                rangevalue.style.right =
                    `${100 - (maxVal / rangeInputvalue[1].max) * 100}%`;
            }
        });
    }
}


// dynamic price filter
document.addEventListener("DOMContentLoaded", function () {
    let minPriceInput = document.getElementById("min-price");
    let maxPriceInput = document.getElementById("max-price");
    let minPriceRange = document.getElementById("min-price-range");
    let maxPriceRange = document.getElementById("max-price-range");

    function updateProducts() {
        let minPrice = minPriceInput.value;
        let maxPrice = maxPriceInput.value;

        // Send AJAX request to update products
        fetch(`/filter-products/?min_price=${minPrice}&max_price=${maxPrice}`)
            .then(response => response.text())
            .then(data => {
                document.getElementById("product-list").innerHTML = data;
            })
            .catch(error => console.error("Error fetching products:", error));
    }

    // Sync range sliders with input fields
    minPriceRange.addEventListener("input", function () {
        minPriceInput.value = this.value;
        updateProducts();
    });

    maxPriceRange.addEventListener("input", function () {
        maxPriceInput.value = this.value;
        updateProducts();
    });

    minPriceInput.addEventListener("input", function () {
        minPriceRange.value = this.value;
        updateProducts();
    });

    maxPriceInput.addEventListener("input", function () {
        maxPriceRange.value = this.value;
        updateProducts();
    });
});

// ########################################

