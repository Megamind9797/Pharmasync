const API = "https://pharmasync-74to.onrender.com";
const OWNER_ID = localStorage.getItem("user_id");



// ================= DELETE MEDICINE =================

async function deleteMedicine(id){

    const response = await fetch(

        `${API}/delete-medicine/${id}`,

        {
            method:"DELETE"
        }

    );

    const data = await response.json();

    alert(data.message);

    loadOwnerMedicines();

}

// ================= OWNER ORDERS =================
async function loadOwnerOrders(){

    const response = await fetch(
        `${API}/owner-orders/${OWNER_ID}`
    );

    const orders = await response.json();

    const container =
    document.getElementById("ordersTable");

    if(!container) return;

    container.innerHTML = "";

    orders.forEach(order => {

        container.innerHTML += `

        <tr>

            <td>${order.order_id}</td>

            <td>Customer</td>

            <td>${order.medicine}</td>

            <td>${order.quantity}</td>

            <td>${order.status}</td>

            <td>

                <button onclick="acceptOrder(${order.order_id})">
                    Accept
                </button>

                <button onclick="rejectOrder(${order.order_id})">
                    Reject
                </button>

            </td>

        </tr>

        `;
    });
}

// ================= ADD MEDICINE =================


async function addMedicine(event) {

    event.preventDefault();

    const ownerId =
    localStorage.getItem("user_id");

    const pharmacyResponse =
    await fetch(
        `${API}/owner-pharmacy/${ownerId}`
    );

    const pharmacyData =
    await pharmacyResponse.json();

    console.log("OWNER PHARMACY DATA:", pharmacyData);
console.log("PHARMACY ID:", pharmacyData.pharmacy_id);

    const medicine = {

        name:
        document.getElementById("medicineName").value,

        description:
        document.getElementById("medicineDescription").value,

        price:
        document.getElementById("medicinePrice").value,

        stock:
        document.getElementById("medicineStock").value,

        pharmacy_id:
        pharmacyData.pharmacy_id,

        expiry_date:
        document.getElementById("medicineExpiry").value

    };

    const response = await fetch(

        `${API}/add-medicine`,

        {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(medicine)

        }

    );

    const data = await response.json();

    alert(data.message);

    window.location.href =
    "owner-medicines.html";

}

// ================= NOTIFICATIONS =================



// ================= DASHBOARD STATS =================

async function loadDashboard(){

    const response = await fetch(
        `${API}/owner-medicines/${OWNER_ID}`
    );

    const medicines = await response.json();

    const totalMedicines =
    medicines.length;

    let totalStock = 0;

    medicines.forEach(m => {
        totalStock += m.stock;
    });

    const medBox =
    document.getElementById("totalMedicines");

    const stockBox =
    document.getElementById("totalStock");

    if(medBox){
        medBox.innerText = totalMedicines;
    }

    if(stockBox){
        stockBox.innerText = totalStock;
    }

}

// ================= AUTO LOAD =================



// ================= LOAD CUSTOMERS =================

async function loadCustomers(){

    try{

        const response = await fetch(

            `${API}/all-users`

        );

        const users = await response.json();

        const container =
        document.getElementById("customersTable");

        if(!container) return;

        container.innerHTML = "";

        users.forEach(user => {

            container.innerHTML += `

            <tr>

                <td>${user.id}</td>

                <td>${user.name}</td>

                <td>${user.email}</td>

                <td>${user.role}</td>

                <td>

                    <button class="view-btn">

                        View

                    </button>

                </td>

            </tr>

            `;

        });

    }

    catch(error){

        console.log(error);

    }

}

// ================= AUTO LOAD CUSTOMERS =================

loadCustomers();



async function loadMedicines() {

    try {

        const response = await fetch(
            `${API}/owner-medicines/${OWNER_ID}`
        );

        const medicines = await response.json();

        console.log("Medicines:", medicines);

        const tableBody =
        document.getElementById("medicinesTable");

        if (!tableBody) {
            console.log("tbody not found");
            return;
        }

        tableBody.innerHTML = "";

        medicines.forEach((med) => {

            const row = `

            <tr>

                <td>${med.name}</td>

                <td>₹${med.price}</td>

                <td>${med.stock}</td>

                <td>General</td>

                <td>${med.stock <= 10 ? "Low Stock" : "In Stock"}</td>

                <td>

    <button onclick="editMedicine(${med.id})">
        Edit
    </button>

    <button onclick="deleteMedicine(${med.id})">
        Delete
    </button>

</td>

            </tr>

            `;

            tableBody.innerHTML += row;
        });

    }

    catch(error) {

        console.log(error);
    }
}




// ================= DELETE =================

async function deleteMedicine(id) {

    await fetch(

        `https://pharmasync-74to.onrender.com/delete-medicine/${id}`,

        {
            method: "DELETE"
        }
    );

    loadMedicines();
}

// ================= AUTO LOAD =================

loadMedicines();
loadDashboard();
loadCustomers();

async function acceptOrder(orderId){

    const response = await fetch(

        `${API}/accept-order/${orderId}`,

        {
            method:"POST"
        }
    );

    const data = await response.json();

    alert(data.message);

    loadOwnerOrders();
}

async function rejectOrder(orderId){

    const response = await fetch(

        `${API}/reject-order/${orderId}`,

        {
            method:"POST"
        }
    );

    const data = await response.json();

    alert(data.message);

    loadOwnerOrders();
}

async function loadStock() {

    const response = await fetch(
        `https://pharmasync-74to.onrender.com/owner-medicines/${OWNER_ID}`
    );

    const medicines = await response.json();

    const table =
    document.getElementById("stockTable");

    if(!table) return;

    table.innerHTML = "";

    medicines.forEach(med => {

        let status = "Healthy Stock";

        if(med.stock <= 5){
            status = "Low Stock";
        }

        if(med.stock == 0){
            status = "Out Of Stock";
        }

        table.innerHTML += `

        <tr>

            <td>${med.name}</td>

            <td>${med.stock}</td>

            <td>${med.expiry_date}</td>

            <td>${status}</td>

            <td>Supplier</td>

            <td>
                <button>
                    Restock
                </button>
            </td>

        </tr>

        `;
    });
}

loadStock();

async function editMedicine(id){

    const name = prompt("New Medicine Name");

    const price = prompt("New Price");

    const stock = prompt("New Stock");

    const expiry_date = prompt("New Expiry Date");

    await fetch(
        `${API}/edit-medicine/${id}`,
        {
            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify({
                name:name,
                description:"",
                price:price,
                stock:stock,
                expiry_date:expiry_date
            })
        }
    );

    alert("Medicine Updated");

    loadMedicines();
}


// ================= PROFILE =================



async function loadProfile() {

    try {

        const response = await fetch(
            `${API}/profile/${OWNER_ID}`
        );

        const user = await response.json();

        const name =
        document.getElementById("profileName");

        const email =
        document.getElementById("profileEmail");

        const phone =
        document.getElementById("profilePhone");

        const address =
        document.getElementById("profileAddress");

        const orders =
        document.getElementById("profileTotalOrders");

        const role =
        document.getElementById("profileRole");

        if(name){
            name.innerText =
            user.name || "No Name";
        }

        if(email){
            email.innerText =
            user.email || "No Email";
        }

        if(phone){
            phone.innerText =
            user.phone || "Not Added";
        }

        if(address){
            address.innerText =
            user.address || "Not Added";
        }

        if(orders){
            orders.innerText =
            "0 Orders";
        }

        // if(role){
        //     role.innerText =
        //     `${user.role} • ${user.pharmacy_name || "PharmaSync Pharmacy"}`;
        // }

    }

    catch(error){

        console.log(
            "Profile Error:",
            error
        );

    }

}


// ================= EDIT PROFILE =================

async function editProfile(){

    const OWNER_ID=localStorage.getItem("user_id")

    const newName =
    prompt("Enter Name");

    if(!newName) return;

    const newPhone =
    prompt("Enter Phone Number");

    if(!newPhone) return;

    const newAddress =
    prompt("Enter Address");

    if(!newAddress) return;

    // const newPharmacy =
    // prompt("Enter Pharmacy Name");

    // if(!newPharmacy) return;

    const newEmail=
    prompt("Enter Email");

    if(!newEmail) return;

   

    try{

        const response = await fetch(

            `${API}/update-profile/${OWNER_ID}`,

            {

                method:"POST",

                headers:{
                    "Content-Type":"application/json"
                },

                body:JSON.stringify({

                    name:newName,
                    email:newEmail,
                    phone:newPhone,
                    address:newAddress,
                    // pharmacy_name:newPharmacy

                })

            }

        );

        const data =
        await response.json();

        alert(data.message);

        loadProfile();

    }

    catch(error){

        console.log(error);

        alert(
            "Failed To Update Profile"
        );

    }

}


// ================= BUTTON EVENT =================

const editBtn =
document.querySelector(
    ".edit-profile-btn"
);

if(editBtn){

    editBtn.addEventListener(
        "click",
        editProfile
    );

}


// ================= PAGE LOAD =================

loadProfile();

async function loadAnalytics(){

    try{

        const response =
        await fetch(
            `${API}/analytics/${OWNER_ID}`
        );

        const data =
        await response.json();

        const revenue =
        document.getElementById(
            "analyticsRevenue"
        );

        const orders =
        document.getElementById(
            "analyticsOrders"
        );

        const lowStock =
        document.getElementById(
            "analyticsLowStock"
        );

        if(revenue){
            revenue.innerText =
            `₹${data.total_revenue}`;
        }

        if(orders){
            orders.innerText =
            data.total_orders;
        }

        if(lowStock){
            lowStock.innerText =
            data.low_stock;
        }

    }

    catch(error){

        console.log(error);

    }

}
if(document.getElementById("salesChart")){
const salesChart = new Chart(
    document.getElementById("salesChart"),
    {
        type: "line",
        data: {
            labels: [],
            datasets: [{
                label: "Revenue",
                data: [],
                borderColor: "#0984e3",
                backgroundColor: "rgba(9,132,227,0.1)",
                fill: true,
                tension: 0.4
            }]
        }
    }
);
loadSalesAnalytics();
}


if(document.getElementById("medicineChart")){
const medicineChart = new Chart(
    document.getElementById("medicineChart"),
    {
        type: "doughnut",
        data: {
            labels: [],
            datasets: [{
                data: [],
                backgroundColor: [
                    "#00b894",
                    "#0984e3",
                    "#6c5ce7",
                    "#fdcb6e",
                    "#e17055"
                ]
            }]
        }
    }
);
loadTopMedicines();
}

async function loadSalesAnalytics(){

    const response =
    await fetch(`https://pharmasync-74to.onrender.com/sales-analytics/${OWNER_ID}`);

    const data =
    await response.json();

    salesChart.data.labels =
    data.labels;

    salesChart.data.datasets[0].data =
    data.revenue;

    salesChart.update();
}

async function loadTopMedicines(){

    const response =
    await fetch(`https://pharmasync-74to.onrender.com/top-medicines/${OWNER_ID}`);

    const data =
    await response.json();

    medicineChart.data.labels =
    data.medicines;

    medicineChart.data.datasets[0].data =
    data.sales;

    medicineChart.update();
}


async function loadNotifications(){

    const response = await fetch(
        `${API}/notifications`
    );

    const notifications = await response.json();

    console.log("Notifications:", notifications);

    const container =
    document.getElementById("notificationContainer");

    console.log("Container:", container);

    if(!container) return;

    // container.innerHTML = "";

    notifications.forEach(n => {

        container.innerHTML += `
        <div class="notification-card">
            <i class="fa-solid fa-bell"></i>
            ${n.message}
        </div>
        `;
    });

}


async function clearNotifications(){

    const response =
    await fetch(
        `${API}/clear-notifications`,
        {
            method:"DELETE"
        }
    );

    const data =
    await response.json();
    

    alert(data.message);

     await loadNotifications();

     loadNotificationCount();
}
async function loadExpiryAlerts(){

    const response =
    await fetch(
    `https://pharmasync-74to.onrender.com/expiry-alerts/${OWNER_ID}`
    );

    const data =
    await response.json();

    const container =
    document.getElementById(
    "notificationContainer"
    );

    if(!container) return;
//     container.innerHTML += `
// <div class="notification-card">
//    ${message}
// </div>
// `;




   data.forEach(alert => {

    let message = "";

    if(alert.days_left < 0){

        message = `
        ❌ ${alert.medicine}
        expired ${Math.abs(alert.days_left)}
        days ago
        `;

    }else{

        message = `
        ⚠ ${alert.medicine}
        expires in ${alert.days_left}
        days
        `;
    }

    container.innerHTML += `
    <div class="notification-card">
        ${message}
    </div>
    `;
});




    const bellCount =
document.querySelector("notification-count");

if(bellCount){
    bellCount.innerText = data.length;
}
}



async function refreshAllNotifications(){

    const container =
    document.getElementById("notificationContainer");

    container.innerHTML = "";   // sirf ek baar clear

    await loadNotifications();
    await loadExpiryAlerts();
}






async function loadNotificationCount(){

    const response = await fetch(
        `${API}/notifications`
    );

    const notifications =
    await response.json();

    const count =
    document.getElementById(
        "notificationCount"
    );

    if(count){
        count.innerText =
        notifications.length;
    }

}
loadAnalytics();

console.log("AUTO NOTIFICATION LOAD")
loadNotificationCount();
refreshAllNotifications();

loadOrders();

async function loadOrders(){

    const response = await fetch(
        `https://pharmasync-74to.onrender.com/owner-orders/${OWNER_ID}`
    );

    const orders = await response.json();

    let html = "";

    orders.forEach(order => {

        html += `

        <tr>

            <td>${order.order_id}</td>

            <td>Customer</td>

            <td>${order.medicine}</td>

            <td>${order.quantity}</td>

            <td>${order.status}</td>

           <td>
<button onclick="acceptOrder(${order.order_id})">
Accept
</button>

<button onclick="rejectOrder(${order.order_id})">
Reject
</button>

<button onclick="assignDelivery(${order.order_id})">
Assign
</button>

<button onclick="outForDelivery(${order.order_id})">
Out
</button>

<button onclick="deliverOrder(${order.order_id})">
Delivered
</button>
</td>

        </tr>

        `;
    });

    document.getElementById(
        "ordersTable"
    ).innerHTML = html;
}
async function acceptOrder(orderId){

    const response = await fetch(

        `https://pharmasync-74to.onrender.com/accept-order/${orderId}`,

        {
            method:"POST"
        }

    );

    const data = await response.json();

    alert(data.message);

    loadOrders();
}

async function rejectOrder(orderId){

    const response = await fetch(

        `https://pharmasync-74to.onrender.com/reject-order/${orderId}`,

        {
            method:"POST"
        }

    );

    const data = await response.json();

    alert(data.message);

    loadOrders();
}

async function assignDelivery(id){

    await fetch(
        `https://pharmasync-74to.onrender.com/assign-delivery/${id}`,
        {
            method:"POST"
        }
    );

    location.reload();
}
async function outForDelivery(id){

    await fetch(
        `https://pharmasync-74to.onrender.com/out-for-delivery/${id}`,
        {
            method:"POST"
        }
    );

    location.reload();
}
async function deliverOrder(id){

    await fetch(
        `https://pharmasync-74to.onrender.com/deliver-order/${id}`,
        {
            method:"POST"
        }
    );

    location.reload();
}

function logout(){

    localStorage.clear();

   window.location.href =
"https://pharmasync-74to.onrender.com//frontend/frontendpages/login2.html";
}

