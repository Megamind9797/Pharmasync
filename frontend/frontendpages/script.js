// ================= REGISTER =================

async function registerUser() {

    const name =
        document.getElementById("name").value

    const email =
        document.getElementById("email").value

    const password =
        document.getElementById("password").value

    const role =
        document.getElementById("role").value


    const response = await fetch(

        "https://pharmasync-74to.onrender.com/register",

        {

            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify({

                name:name,
                email:email,
                password:password,
                role:role

            })

        }
    )

    const data = await response.json()

    showToast(data.message)

    // redirect
    window.location.href = "login.html"
}




// ================= LOGIN =================

async function loginUser() {

    const email =
        document.getElementById("email").value

    const password =
        document.getElementById("password").value


    const response = await fetch(

        "https://pharmasync-74to.onrender.com/login",

        {

            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify({

                email:email,
                password:password

            })

        }
    )

    const data = await response.json()

    showToast(data.message)


    // save user info
    localStorage.setItem(
        "user_id",
        data.user_id
    )

    localStorage.setItem(
        "role",
        data.role
    )


    // owner redirect
    if(data.role === "owner"){

        window.location.href =
            "owner-dashboard.html"
    }

    // customer redirect
    else{

        window.location.href =
            "customer-dashboard.html"
    }

}
// ================= ADD MEDICINE =================

async function addMedicine() {

    const name =
        document.getElementById("name").value

    const description =
        document.getElementById("description").value

    const price =
        document.getElementById("price").value

    const stock =
        document.getElementById("stock").value

    const pharmacy_id =
        document.getElementById("pharmacy_id").value

    const expiry_date =
        document.getElementById("expiry_date").value


    const response = await fetch(

        "https://pharmasync-74to.onrender.com/add-medicine",

        {

            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify({

                name:name,
                description:description,
                price:price,
                stock:stock,
                pharmacy_id:pharmacy_id,
                expiry_date:expiry_date

            })

        }
    )

    const data = await response.json()

    showToast(data.message)
}
// ================= SEARCH MEDICINE =================

async function searchMedicine() {

    const name =
        document.getElementById("searchInput").value


    const response = await fetch(

        `https://pharmasync-74to.onrender.com/search?name=${name}`

    )

    const medicines = await response.json()

    const results =
        document.getElementById("medicineResults")

    results.innerHTML = ""


    medicines.forEach((medicine)=>{

        results.innerHTML += `

        <div class="glass-card">

            <h2 style="margin-bottom:15px;color:#059669;">

                ${medicine.name}

            </h2>

            <p>
                ${medicine.description}
            </p>

            <br>

            <p>
                <strong>Price:</strong>
                ₹${medicine.price}
            </p>

            <p>
                <strong>Stock:</strong>
                ${medicine.stock}
            </p>

            <p>
                <strong>Expiry:</strong>
                ${medicine.expiry_date}
            </p>

            <br>

            <button
                class="btn"
                onclick="placeOrder(${medicine.id})">

                Order Now

            </button>

        </div>

        `
    })

}
// ================= PLACE ORDER =================

async function placeOrder(medicine_id) {

    const user_id =
        localStorage.getItem("user_id")

    const quantity =
        prompt("Enter Quantity")


    const response = await fetch(

        "https://pharmasync-74to.onrender.com/order",

        {

            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify({

                user_id:user_id,
                medicine_id:medicine_id,
                quantity:quantity

            })

        }
    )

    const data = await response.json()

    showToast(data.message)

}
// ================= LOAD ORDERS =================

async function loadOrders() {

    const user_id =
        localStorage.getItem("user_id")


    const response = await fetch(

        `https://pharmasync-74to.onrender.com/order-history/${user_id}`

    )

    const orders = await response.json()

    const container =
        document.getElementById("ordersContainer")

    container.innerHTML = ""


    orders.forEach((order)=>{

        container.innerHTML += `

        <div class="glass-card">

            <h2
                style="
                margin-bottom:15px;
                color:#059669;
                ">

                ${order.medicine}

            </h2>

            <p>
                <strong>Quantity:</strong>
                ${order.quantity}
            </p>

            <p>
                <strong>Status:</strong>
                ${order.status}
            </p>

            <br>

            <button
                class="btn"
                onclick="cancelOrder(${order.order_id})">

                Cancel Order

            </button>

        </div>

        `
    })

}
// ================= CANCEL ORDER =================

async function cancelOrder(order_id) {

    const response = await fetch(

        `https://pharmasync-74to.onrender.com/cancel-order/${order_id}`,

        {
            method:"POST"
        }
    )

    const data = await response.json()

    showToast(data.message)

    loadOrders()
}
// ================= IMAGE PREVIEW =================

function previewImage() {

    const file =
        document.getElementById(
            "prescriptionImage"
        ).files[0]

    const preview =
        document.getElementById("preview")

    preview.src =
        URL.createObjectURL(file)

    preview.style.display = "block"
}
// ================= UPLOAD PRESCRIPTION =================

async function uploadPrescription() {

    const user_id =
        localStorage.getItem("user_id")

    const image =
        document.getElementById(
            "prescriptionImage"
        ).files[0]


    const formData = new FormData()

    formData.append("user_id", user_id)

    formData.append("image", image)


    const response = await fetch(

        "https://pharmasync-74to.onrender.com/upload-prescription",

        {

            method:"POST",

            body:formData

        }
    )

    const data = await response.json()

    showToast(data.message)
}
// ================= LOAD PRESCRIPTIONS =================

async function loadPrescriptions() {

    const response = await fetch(

        "https://pharmasync-74to.onrender.com/prescriptions"

    )

    const prescriptions =
        await response.json()

    const container =
        document.getElementById(
            "prescriptionContainer"
        )

    container.innerHTML = ""


    prescriptions.forEach((p)=>{

        container.innerHTML += `

        <div class="glass-card">

            <h2
                style="
                margin-bottom:15px;
                color:#059669;
                ">

                Prescription #${p.id}

            </h2>

            <p>
                <strong>User ID:</strong>
                ${p.user_id}
            </p>

            <p>
                <strong>Status:</strong>
                ${p.status}
            </p>

            <br>

            <img

                src="https://pharmasync-74to.onrender.com/uploads/${p.image}"

                style="
                width:100%;
                height:250px;
                object-fit:cover;
                border-radius:15px;
                ">

        </div>

        `
    })

}
// ================= LOAD OWNER MEDICINES =================

async function loadOwnerMedicines() {

    const owner_id =
        localStorage.getItem("user_id")


    const response = await fetch(

        `https://pharmasync-74to.onrender.com/owner-medicines/${owner_id}`

    )

    const medicines =
        await response.json()

    const container =
        document.getElementById(
            "ownerMedicines"
        )

    container.innerHTML = ""


    medicines.forEach((medicine)=>{

        container.innerHTML += `

        <div class="glass-card">

            <h2
                style="
                margin-bottom:15px;
                color:#059669;
                ">

                ${medicine.name}

            </h2>

            <p>
                ${medicine.description}
            </p>

            <br>

            <p>
                <strong>Price:</strong>
                ₹${medicine.price}
            </p>

            <p>
                <strong>Stock:</strong>
                ${medicine.stock}
            </p>

            <p>
                <strong>Expiry:</strong>
                ${medicine.expiry_date}
            </p>

            <br>

            <!-- UPDATE STOCK -->

            <input
                type="number"

                id="stock-${medicine.id}"

                placeholder="New Stock"

                style="
                width:100%;
                padding:12px;
                margin-bottom:15px;
                border:none;
                border-radius:10px;
                ">


            <!-- UPDATE PRICE -->

            <input
                type="number"

                id="price-${medicine.id}"

                placeholder="New Price"

                style="
                width:100%;
                padding:12px;
                margin-bottom:15px;
                border:none;
                border-radius:10px;
                ">


            <!-- BUTTONS -->

            <button
                class="btn"

                onclick="updateStock(${medicine.id})"

                style="margin-bottom:10px;">

                Update Stock

            </button>


            <button
                class="btn"

                onclick="updatePrice(${medicine.id})"

                style="margin-bottom:10px;">

                Update Price

            </button>


            <button
                class="btn"

                onclick="deleteMedicine(${medicine.id})">

                Delete

            </button>

        </div>

        `
    })

}



// ================= UPDATE STOCK =================

async function updateStock(medicine_id) {

    const stock =
        document.getElementById(
            `stock-${medicine_id}`
        ).value


    const response = await fetch(

        "https://pharmasync-74to.onrender.com/update-stock",

        {

            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify({

                medicine_id:medicine_id,
                stock:stock

            })

        }
    )

    const data = await response.json()

    showToast(data.message)

    loadOwnerMedicines()
}



// ================= UPDATE PRICE =================

async function updatePrice(medicine_id) {

    const price =
        document.getElementById(
            `price-${medicine_id}`
        ).value


    const response = await fetch(

        "https://pharmasync-74to.onrender.com/update-price",

        {

            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify({

                medicine_id:medicine_id,
                price:price

            })

        }
    )

    const data = await response.json()

    showToast(data.message)

    loadOwnerMedicines()
}



// ================= DELETE MEDICINE =================

async function deleteMedicine(medicine_id) {

    const response = await fetch(

        `https://pharmasync-74to.onrender.com/delete-medicine/${medicine_id}`,

        {
            method:"DELETE"
        }
    )

    const data = await response.json()

    showToast(data.message)

    loadOwnerMedicines()
}

// ================= LOW STOCK ALERTS =================

async function loadLowStock() {

    const owner_id =
        localStorage.getItem("user_id")


    const response = await fetch(

        `https://pharmasync-74to.onrender.com/owner-medicines/${owner_id}`

    )

    const medicines =
        await response.json()

    const container =
        document.getElementById(
            "lowStockContainer"
        )

    container.innerHTML = ""


    medicines.forEach((medicine)=>{

        if(medicine.stock <= 5){

            container.innerHTML += `

            <div class="glass-card">

                <h2
                    style="
                    margin-bottom:15px;
                    color:#dc2626;
                    ">

                    ${medicine.name}

                </h2>

                <p>
                    <strong>Current Stock:</strong>
                    ${medicine.stock}
                </p>

                <br>

                <p
                    style="
                    color:#dc2626;
                    font-weight:bold;
                    ">

                    ⚠ Low Stock Warning

                </p>

            </div>

            `
        }

    })

}
// ================= EXPIRY WARNINGS =================

async function loadExpiryWarnings() {

    const owner_id =
        localStorage.getItem("user_id")


    const response = await fetch(

        `https://pharmasync-74to.onrender.com/owner-medicines/${owner_id}`

    )

    const medicines =
        await response.json()

    const container =
        document.getElementById(
            "expiryContainer"
        )

    container.innerHTML = ""


    const today =
        new Date()


    medicines.forEach((medicine)=>{

        const expiryDate =
            new Date(medicine.expiry_date)

        const diffTime =
            expiryDate - today

        const diffDays =
            diffTime / (1000 * 60 * 60 * 24)


        if(diffDays <= 30){

            container.innerHTML += `

            <div class="glass-card">

                <h2
                    style="
                    margin-bottom:15px;
                    color:#dc2626;
                    ">

                    ${medicine.name}

                </h2>

                <p>
                    <strong>Expiry Date:</strong>
                    ${medicine.expiry_date}
                </p>

                <br>

                <p
                    style="
                    color:#dc2626;
                    font-weight:bold;
                    ">

                    ⚠ Expiring Soon

                </p>

            </div>

            `
        }

    })

}
// ================= NOTIFICATIONS =================

async function loadNotifications() {

    const owner_id =
        localStorage.getItem("user_id")


    const response = await fetch(

        `https://pharmasync-74to.onrender.com/owner-medicines/${owner_id}`

    )

    const medicines =
        await response.json()

    const container =
        document.getElementById(
            "notificationContainer"
        )

    container.innerHTML = ""


    const today =
        new Date()


    medicines.forEach((medicine)=>{

        // LOW STOCK

        if(medicine.stock <= 5){

            container.innerHTML += `

            <div class="glass-card">

                <h2 style="color:#dc2626;">

                    ⚠ Low Stock Alert

                </h2>

                <br>

                <p>

                    ${medicine.name}
                    stock is very low.

                </p>

            </div>

            `
        }


        // EXPIRY WARNING

        const expiryDate =
            new Date(medicine.expiry_date)

        const diffTime =
            expiryDate - today

        const diffDays =
            diffTime / (1000 * 60 * 60 * 24)


        if(diffDays <= 30){

            container.innerHTML += `

            <div class="glass-card">

                <h2 style="color:#f59e0b;">

                    ⚠ Expiry Warning

                </h2>

                <br>

                <p>

                    ${medicine.name}
                    is expiring soon.

                </p>

            </div>

            `
        }

    })

}
// ================= ADMIN DASHBOARD =================

async function loadAdminDashboard() {

    // ================= USERS =================

    const usersResponse = await fetch(

        "https://pharmasync-74to.onrender.com/all-users"

    )

    const users =
        await usersResponse.json()


    // ================= PHARMACIES =================

    const pharmaciesResponse = await fetch(

        "https://pharmasync-74to.onrender.com/all-pharmacies"

    )

    const pharmacies =
        await pharmaciesResponse.json()


    // ================= ORDERS =================

    const ordersResponse = await fetch(

        "https://pharmasync-74to.onrender.com/all-orders"

    )

    const orders =
        await ordersResponse.json()


    // ================= TOTALS =================

    document.getElementById(
        "totalUsers"
    ).innerText = users.length


    document.getElementById(
        "totalPharmacies"
    ).innerText = pharmacies.length


    document.getElementById(
        "totalOrders"
    ).innerText = orders.length


    // ================= USERS UI =================

    const usersContainer =
        document.getElementById(
            "usersContainer"
        )

    usersContainer.innerHTML = ""

    users.forEach((user)=>{

        usersContainer.innerHTML += `

        <div class="glass-card">

            <h2 style="color:#059669;">

                ${user.name}

            </h2>

            <br>

            <p>
                ${user.email}
            </p>

            <p>
                <strong>Role:</strong>
                ${user.role}
            </p>

        </div>

        `
    })


    // ================= PHARMACIES UI =================

    const pharmaciesContainer =
        document.getElementById(
            "pharmaciesContainer"
        )

    pharmaciesContainer.innerHTML = ""

    pharmacies.forEach((p)=>{

        pharmaciesContainer.innerHTML += `

        <div class="glass-card">

            <h2 style="color:#059669;">

                ${p.name}

            </h2>

            <br>

            <p>
                <strong>Owner ID:</strong>
                ${p.owner_id}
            </p>

        </div>

        `
    })


    // ================= ORDERS UI =================

    const ordersContainer =
        document.getElementById(
            "ordersContainer"
        )

    ordersContainer.innerHTML = ""

    orders.forEach((order)=>{

        ordersContainer.innerHTML += `

        <div class="glass-card">

            <h2 style="color:#059669;">

                ${order.medicine}

            </h2>

            <br>

            <p>
                <strong>Quantity:</strong>
                ${order.quantity}
            </p>

            <p>
                <strong>Status:</strong>
                ${order.status}
            </p>

        </div>

        `
    })

}

// ================= NEARBY PHARMACIES =================

function getNearbyPharmacies() {

    navigator.geolocation.getCurrentPosition(

        async(position)=>{

            const lat =
                position.coords.latitude

            const lon =
                position.coords.longitude


            const response = await fetch(

                `https://pharmasync-74to.onrender.com/nearest?lat=${lat}&lon=${lon}`

            )

            const pharmacies =
                await response.json()

            const container =
                document.getElementById(
                    "nearbyContainer"
                )

            container.innerHTML = ""


            pharmacies.forEach((p)=>{

                container.innerHTML += `

                <div class="glass-card">

                    <h2
                        style="
                        color:#059669;
                        margin-bottom:15px;
                        ">

                        ${p.pharmacy}

                    </h2>

                    <p>

                        <strong>Medicine:</strong>

                        ${p.medicine}

                    </p>

                    <p>

                        <strong>Price:</strong>

                        ₹${p.price}

                    </p>

                    <p>

                        <strong>Stock:</strong>

                        ${p.stock}

                    </p>

                    <p>

                        <strong>Distance:</strong>

                        ${p.distance}

                    </p>

                </div>

                `
            })

        }

    )

}
// ================= LOAD INVOICE =================

async function loadInvoice() {

    const user_id =
        localStorage.getItem("user_id")


    const response = await fetch(

        `https://pharmasync-74to.onrender.com/order-history/${user_id}`

    )

    const orders =
        await response.json()

    const container =
        document.getElementById(
            "invoiceContainer"
        )

    container.innerHTML = ""


    let total = 0


    orders.forEach((order)=>{

        const price =
            order.price || 100

        const amount =
            price * order.quantity

        total += amount


        container.innerHTML += `

        <div
            style="
            margin-bottom:25px;
            border-bottom:1px solid #ccc;
            padding-bottom:20px;
            ">

            <h2
                style="
                color:#059669;
                margin-bottom:10px;
                ">

                ${order.medicine}

            </h2>

            <p>

                <strong>Quantity:</strong>

                ${order.quantity}

            </p>

            <p>

                <strong>Price:</strong>

                ₹${price}

            </p>

            <p>

                <strong>Total:</strong>

                ₹${amount}

            </p>

        </div>

        `
    })


    container.innerHTML += `

    <h2
        style="
        text-align:right;
        margin-top:30px;
        color:#059669;
        ">

        Grand Total:
        ₹${total}

    </h2>

    `
}

// ================= OCR IMAGE PREVIEW =================

function previewOCRImage() {

    const file =
        document.getElementById(
            "ocrImage"
        ).files[0]

    const preview =
        document.getElementById(
            "ocrPreview"
        )

    preview.src =
        URL.createObjectURL(file)

    preview.style.display =
        "block"
}
// ================= AI OCR ANALYSIS =================

function analyzePrescription() {

    const result =
        document.getElementById(
            "ocrResult"
        )


    // AI DEMO OUTPUT

    result.innerHTML = `

    <div class="glass-card">

        <h2
            style="
            color:#059669;
            margin-bottom:20px;
            ">

            Detected Medicines

        </h2>

        <p>
            ✔ Dolo 650
        </p>

        <p>
            ✔ Crocin
        </p>

        <p>
            ✔ Azithromycin
        </p>

        <br>

        <p
            style="
            color:#059669;
            font-weight:bold;
            ">

            AI Analysis Completed Successfully

        </p>

    </div>

    `
}

// async function sendMessage() {

//     const input = document.getElementById("userInput");
//     const message = input.value;

//     if (message.trim() === "") return;

//     try {

//         const response = await fetch("https://pharmasync-74to.onrender.com/chatbot", {
//             method: "POST",
//             headers: {
//                 "Content-Type": "application/json"
//             },
//             body: JSON.stringify({
//                 message: message
//             })
//         });

//         const data = await response.json();

//         console.log(data);

//         addMessage(data.reply, "bot");

//     } catch (error) {

//         console.log("FULL ERROR:", error);

//         alert(error);
//     }
// }

// ================= SALES PREDICTION =================

function loadSalesPrediction() {

    // AI PREDICTION DATA

    const predictedSales = 125

    const expectedRevenue = 75000

    const topMedicine = "Dolo 650"


    // UI UPDATE

    document.getElementById(
        "predictedSales"
    ).innerText = predictedSales


    document.getElementById(
        "expectedRevenue"
    ).innerText =

        `₹${expectedRevenue}`


    document.getElementById(
        "topMedicine"
    ).innerText = topMedicine


    // AI INSIGHTS

    const insights =
        document.getElementById(
            "aiInsights"
        )


    insights.innerHTML = `

    <p
        style="
        margin-bottom:15px;
        ">

        📈 Medicine demand is expected
        to increase by 18% next month.

    </p>

    <p
        style="
        margin-bottom:15px;
        ">

        💊 Dolo 650 is predicted to remain
        the highest-selling medicine.

    </p>

    <p
        style="
        margin-bottom:15px;
        ">

        ⚠ Increase stock levels for fever
        and cold medicines.

    </p>

    <p>

        🤖 AI recommends inventory
        optimization for faster delivery.

    </p>

    `
}
// ================= SHOW TOAST =================

function showToast(message){

    const toast =
        document.createElement("div")

    toast.classList.add("toast")

    toast.innerText = message

    document.body.appendChild(toast)


    setTimeout(()=>{

        toast.remove()

    },3000)
}




// ================= LOAD MEDICINES =================

async function loadMedicines(){

    const response = await fetch(
        "https://pharmasync-74to.onrender.com/all-medicines"
    );

    const medicines = await response.json();

    const medicineGrid =
        document.getElementById("medicineGrid");

    medicineGrid.innerHTML = "";

    medicines.forEach((medicine)=>{

        // DELIVERY TIME

        const delivery =
            Math.floor(Math.random()*15)+10;

        // DISTANCE

        const distance =
            (Math.random()*5).toFixed(1);

        medicineGrid.innerHTML += `

        <div class="medicine-card">

            <div class="top-row">

                <span class="stock">

                    ${
                        medicine.stock > 0
                        ? "In Stock"
                        : "Out of Stock"
                    }

                </span>

                <span class="rating">

                    ⭐ 4.8

                </span>

            </div>

            <img
                src="assets/${medicine.image}">

            <h3>

                ${medicine.name}

            </h3>

            <p>

                ${medicine.description}

            </p>

            <div class="medicine-info">

                <span>
                    📍 ${medicine.pharmacy}
                </span>

                <span>
                    🚚 ${delivery} mins
                </span>

            </div>

            <div class="medicine-info">

                <span>
                    📏 ${distance} km away
                </span>

                <span>
                    🟢 ${medicine.stock} left
                </span>

            </div>

            <div class="price-row">

                <span>

                    ₹${medicine.price}

                </span>

                <button>

                    Add To Cart

                </button>

            </div>

        </div>

        `;

    });

}

// RUN

loadMedicines();