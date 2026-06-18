# import sqlite3

# conn = sqlite3.connect("database.db")
# cur = conn.cursor()

# medicines = [

#     ("Dolo 650", "Fever medicine", 40, 100, 1),
#     ("Crocin", "Cold and fever", 35, 80, 1),
#     ("Paracetamol", "Pain relief", 20, 120, 1),
#     ("Cetirizine", "Allergy tablet", 25, 60, 1),
#     ("Azee 500", "Antibiotic", 120, 40, 1),
#     ("Augmentin", "Infection medicine", 180, 30, 1),
#     ("Pantoprazole", "Acidity relief", 90, 50, 1),
#     ("ORS", "Hydration solution", 20, 70, 1),
#     ("Benadryl", "Cough syrup", 110, 25, 1),
#     ("Digene", "Gas relief", 35, 45, 1)

# ]

# cur.executemany(
#     """
#     INSERT INTO medicines
#     (name, description, price, stock, pharmacy_id)
#     VALUES (?,?,?,?,?)
#     """,
#     medicines
# )

# conn.commit()
# conn.close()

# print("Medicines Added Successfully 🚀")