// Audio Manager for sound effects
const AudioManager = {
    audioContext: null,

    init: function() {
        // Create audio context on first user interaction
        if (!this.audioContext) {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        }
    },

    // Two-beat lower pitch sound for adding items
    playAddSound: function() {
        this.init();

        // First beat
        const osc1 = this.audioContext.createOscillator();
        const gain1 = this.audioContext.createGain();
        osc1.connect(gain1);
        gain1.connect(this.audioContext.destination);
        osc1.frequency.value = 400;
        osc1.type = 'sine';
        gain1.gain.setValueAtTime(0.3, this.audioContext.currentTime);
        gain1.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + 0.08);
        osc1.start(this.audioContext.currentTime);
        osc1.stop(this.audioContext.currentTime + 0.08);

        // Second beat (higher pitch)
        const osc2 = this.audioContext.createOscillator();
        const gain2 = this.audioContext.createGain();
        osc2.connect(gain2);
        gain2.connect(this.audioContext.destination);
        osc2.frequency.value = 500;
        osc2.type = 'sine';
        const startTime2 = this.audioContext.currentTime + 0.1;
        gain2.gain.setValueAtTime(0.3, startTime2);
        gain2.gain.exponentialRampToValueAtTime(0.01, startTime2 + 0.08);
        osc2.start(startTime2);
        osc2.stop(startTime2 + 0.08);
    },

    // Lower pitch beep for removing items
    playRemoveSound: function() {
        this.init();
        const oscillator = this.audioContext.createOscillator();
        const gainNode = this.audioContext.createGain();

        oscillator.connect(gainNode);
        gainNode.connect(this.audioContext.destination);

        oscillator.frequency.value = 400;
        oscillator.type = 'sine';

        gainNode.gain.setValueAtTime(0.3, this.audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + 0.15);

        oscillator.start(this.audioContext.currentTime);
        oscillator.stop(this.audioContext.currentTime + 0.15);
    },

    // Pleasant ascending tone for card scan
    playCardScanSound: function() {
        this.init();
        const times = [0, 0.08, 0.16];
        const frequencies = [523.25, 659.25, 783.99]; // C5, E5, G5 chord

        times.forEach((time, index) => {
            const oscillator = this.audioContext.createOscillator();
            const gainNode = this.audioContext.createGain();

            oscillator.connect(gainNode);
            gainNode.connect(this.audioContext.destination);

            oscillator.frequency.value = frequencies[index];
            oscillator.type = 'sine';

            const startTime = this.audioContext.currentTime + time;
            gainNode.gain.setValueAtTime(0.25, startTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, startTime + 0.3);

            oscillator.start(startTime);
            oscillator.stop(startTime + 0.3);
        });
    },

    // Cheerful jingle for checkout complete
    playCheckoutSound: function() {
        this.init();
        // Play a happy melody: C5, E5, G5, C6
        const melody = [
            { freq: 523.25, time: 0, duration: 0.15 },    // C5
            { freq: 659.25, time: 0.15, duration: 0.15 },  // E5
            { freq: 783.99, time: 0.3, duration: 0.15 },   // G5
            { freq: 1046.50, time: 0.45, duration: 0.4 }   // C6
        ];

        melody.forEach(note => {
            const oscillator = this.audioContext.createOscillator();
            const gainNode = this.audioContext.createGain();

            oscillator.connect(gainNode);
            gainNode.connect(this.audioContext.destination);

            oscillator.frequency.value = note.freq;
            oscillator.type = 'triangle';

            const startTime = this.audioContext.currentTime + note.time;
            gainNode.gain.setValueAtTime(0.3, startTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, startTime + note.duration);

            oscillator.start(startTime);
            oscillator.stop(startTime + note.duration);
        });
    }
};

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

// Adjust product card font size on load and when resizing
function adjustH5FontSize() {
    document.querySelectorAll(".product-card h5").forEach(h5 => {
        let parentWidth = h5.clientWidth;
        let fontSize = 38; // Start with the default font size
        h5.style.fontSize = fontSize + "px";
        h5.style.whiteSpace = "nowrap"; // Ensure single-line text

        // Create a temporary span to measure text width
        let span = document.createElement("span");
        span.style.position = "absolute";
        span.style.visibility = "hidden";
        span.style.whiteSpace = "nowrap";
        span.style.fontSize = fontSize + "px";
        span.innerText = h5.innerText;
        document.body.appendChild(span);

        // Reduce font size until text fits within the parent width
        while (span.offsetWidth > parentWidth && fontSize > 10) {
            fontSize--;
            span.style.fontSize = fontSize + "px";
            h5.style.fontSize = fontSize + "px";
        }

        document.body.removeChild(span); // Clean up temporary span
    });
}

// Adjust font size on load and when resizing
window.addEventListener("load", adjustH5FontSize);
window.addEventListener("resize", adjustH5FontSize);

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
                updateCart(current_cart);
                AudioManager.playAddSound();
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
                updateCart(current_cart);
                AudioManager.playRemoveSound();
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
                AudioManager.playCheckoutSound();
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

    // Set the cart's card number if we get 8 or 14 characters
    $("#hidden-input").on("input", function() {
        clearTimeout(inputTimer);
        inputTimer = setTimeout(() => {
            let inputValue = $(this).val();
            if (inputValue.length === 8 || inputValue.length === 14) {
        
                // Let the API know we got a valid card number
                $.ajax({
                    url: "card_scanned",
                    type: "POST",
                    dataType: "json",
                    headers: { "X-Requested-With": "XMLHttpRequest", "X-CSRFToken": getCookie("csrftoken") },
                    data: JSON.stringify({ 'cart_id': current_cart.id, 'card_number': inputValue, 'next': '/admin.' }),
                    success: (data) => {
                        current_cart = data;
                        updateCart(current_cart);
                        AudioManager.playCardScanSound();
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