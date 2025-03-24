// Create an empty cart
function createEmptyCart() {
    return{'id': -1, 'cart_items': [], 'total_price': "0.00", 'card_number': ''}
}

// Reusable function for getting out CSRF
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Re-render the cart and checkout information
function updateCart(current_cart) {
    let cart_list = "";
    console.log(current_cart)

    // Make Checkout button interactable or not
    if (current_cart.card_number === "") {
        $("#finish-btn").removeClass("checkout-button")
        $("#finish-btn").addClass("finish-button")
        $("#finish-btn").addClass("pulse")
        $("#finish-btn").html("Scan Card")
    } else {
        $("#finish-btn").addClass("checkout-button")
        $("#finish-btn").removeClass("pulse")
        $("#finish-btn").removeClass("finish-button")
        $("#finish-btn").html("Checkout")
    }

    // Show items in the cart
    current_cart.cart_items.forEach(item => {
        let money_color = "money-color"
        if (item.discount_text !== "") {
            money_color ="money-color-sale"
        }
        cart_list += `<li class="list-group-item d-flex justify-content-between align-items-center">
                        <span><span class="${money_color}">$${item.price}</span> - ${item.name}</span>
                        <button class="delete-item" data-cart-item-id="${item.id}" >X</button>
                        </li>`;
    });
    $("#cart-list").html(cart_list);
    
    // Update total price
    $("#total-price").text(current_cart.total_price);
}

function showNotification(notification_text) {
    $("#checkout-notification").html(notification_text);
    $("#checkout-notification").fadeIn(350).delay(2000).fadeOut(350);
}

$(document).ready(function() {
    // Initialize
    var current_cart = createEmptyCart();

    // Add item to cart
    $("#product-list").on("click", ".product-card", function() {
        $.ajax({
            url: "add_to_cart",
            type: "POST",
            dataType: "json",
            headers: { "X-Requested-With": "XMLHttpRequest", "X-CSRFToken": getCookie("csrftoken") },
            data: JSON.stringify({ 'cart_id': current_cart.id, 'product_id': $(this).data("product-id") }),
            success: (data) => {
                current_cart = data;
                updateCart(current_cart)
            },
            error: (error) => {
                console.log(error);
            }
        });
    });

    // Remove item from cart
    $("#cart-list").on("click", ".delete-item", function() {
        $.ajax({
            url: "remove_from_cart",
            type: "POST",
            dataType: "json",
            headers: { "X-Requested-With": "XMLHttpRequest", "X-CSRFToken": getCookie("csrftoken") },
            data: JSON.stringify({ 'cart_id': current_cart.id, 'cart_item_id': $(this).data("cart-item-id") }),
            success: (data) => {
                current_cart = data;
                updateCart(current_cart)
            },
            error: (error) => {
                console.log(error);
            }
        });
    });

    // Discard the cart
    $("#cancel-btn").click(function() {
        
        // Send the complete call
        $.ajax({
            url: "finish_cart",
            type: "POST",
            dataType: "json",
            headers: { "X-Requested-With": "XMLHttpRequest", "X-CSRFToken": getCookie("csrftoken") },
            data: JSON.stringify({ 'cart_id': current_cart.id, 'completion_status': 'canceled' }),
            success: (data) => {
                return_status = data;
                showNotification("Canceled");
            },
            error: (error) => {
                console.log(error);
            }
        });

        current_cart = createEmptyCart();
        updateCart(current_cart);
    });

    // Finish the checkout
    $("#finish-btn").click(function() {

        // This button only works if a card has been scanned
        if (! $(this).hasClass("checkout-button")) {return;}

        // Send the complete call
        $.ajax({
            url: "finish_cart",
            type: "POST",
            dataType: "json",
            headers: { "X-Requested-With": "XMLHttpRequest", "X-CSRFToken": getCookie("csrftoken") },
            data: JSON.stringify({ 'cart_id': current_cart.id, 'completion_status': 'complete' }),
            success: (data) => {
                return_status = data;
                showNotification("Complete!");
            },
            error: (error) => {
                console.log(error);
            }
        });
        
        current_cart = createEmptyCart();
        updateCart(current_cart);
    });

    // The hidden admin button sends you to the Django admin site
    $("#hidden-admin-button").click(function() {

        // A scanned card is required as it will be the username and password
        if (current_cart.card_number !== "") {

            document.getElementById("admin-username").value = current_cart.card_number;
            document.getElementById("admin-password").value = current_cart.card_number;
            document.getElementById("csrf-token").value = getCookie("csrftoken");

            // Submit the form
            document.getElementById("admin-login-form").submit();
        }

    });

    // Cosntantly refocus the hidden text input for scanning cards
    let inputTimer;
    function focusHiddenInput() {
        $("#hidden-input").focus();
    }
    setInterval(focusHiddenInput, 500);
    focusHiddenInput();

    // Set the cart's card number if we get 10 or 14 digits
    $("#hidden-input").on("input", function() {
        clearTimeout(inputTimer);
        inputTimer = setTimeout(() => {
            let inputValue = $(this).val();
            if (inputValue.length === 10 || inputValue.length === 14) {
        
                // Let the API know we got a valid card number
                $.ajax({
                    url: "card_scanned",
                    type: "POST",
                    dataType: "json",
                    headers: { "X-Requested-With": "XMLHttpRequest", "X-CSRFToken": getCookie("csrftoken") },
                    data: JSON.stringify({ 'cart_id': current_cart.id, 'card_number': inputValue, 'next': '/admin.' }),
                    success: (data) => {
                        current_cart = data;
                        updateCart(current_cart)
                    },
                    error: (error) => {
                        console.log(error);
                    }
                });

            }
            $(this).val(""); // Clear the input field after logging
        }, 200);
    });

});