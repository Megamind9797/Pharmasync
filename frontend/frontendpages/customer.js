// customer-dashboard.js

console.log("Customer Dashboard Loaded");

// Customer Profile Load

const profile =
JSON.parse(
localStorage.getItem("customerProfile")
);

if(profile){

    const heading =
    document.querySelector(".navbar h1");

    if(heading){

        heading.innerHTML =
        `Welcome Back, ${profile.name} 👋`;

    }

}

// Cart Count

const cart =
JSON.parse(
localStorage.getItem("cart")
) || [];

const cartCard =
document.querySelectorAll(".card h2");

if(cartCard.length > 3){

    cartCard[3].innerText =
    cart.length;

}

// Recent Orders Load

const orders =
JSON.parse(
localStorage.getItem("orders")
) || [];

const table =
document.querySelector(".orders table");

if(orders.length > 0){

    table.innerHTML = `

    <tr>

        <th>Order ID</th>
        <th>Medicine</th>
        <th>Status</th>

    </tr>

    `;

    orders.forEach(order => {

        table.innerHTML += `

        <tr>

            <td>${order.id}</td>

            <td>${order.medicine}</td>

            <td>${order.status}</td>

        </tr>

        `;

    });

}

// Notification Bell

const bell =
document.querySelector(
".fa-bell"
);

if(bell){

    bell.addEventListener(
        "click",
        function(){

            window.location.href =
            "notifications.html";

        }
    );

}