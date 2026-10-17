"""Pharmacy Management System.

A simple pharmacy stock and billing manager that handles medicine
inventory, prescriptions, dosage calculations, and stock persistence.
"""

import ast
from datetime import datetime, date
import hashlib
import json
import operator
import os
import secrets

# Global pharmacy state
medicines = {}

# Read the pharmacist password from the environment variable;
# fall back to a default only when no variable has been set.
DB_PASSWORD = os.environ.get("PHARMACY_PASSWORD", "pharma@123")


def add_medicine(name, qty=0, price=0.0, expiry="2099-12-31", audit=None):
    """Add a medicine to stock or increase its quantity in the inventory."""
    if audit is None:
        audit = []

    if not isinstance(name, str) or not name.strip():
        return None

    if qty < 0:
        return None

    if price < 0:
        return None

    try:
        datetime.strptime(expiry, "%Y-%m-%d")
    except ValueError:
        return None

    if name not in medicines:
        medicines[name] = {"qty": 0, "price": price, "expiry": expiry}

    medicines[name]["qty"] = medicines[name]["qty"] + qty
    audit.append(f"{datetime.now()}: Stocked {qty} units of {name}")
    return audit


def dispense_medicine(name, qty):
    """Dispense a quantity of medicine from stock with checks."""
    if name not in medicines:
        print(f"Cannot dispense: '{name}' not in stock.")
        return False

    if qty <= 0:
        print("Cannot dispense: quantity must be positive.")
        return False

    if medicines[name]["qty"] < qty:
        available = medicines[name]["qty"]
        print(
            f"Cannot dispense: only {available} units of '{name}' available."
        )
        return False

    medicines[name]["qty"] -= qty
    if medicines[name]["qty"] == 0:
        del medicines[name]
    return True


def get_quantity(name):
    """Return the current stock quantity for a medicine, or 0 if missing."""
    if name in medicines:
        return medicines[name]["qty"]
    return 0


def is_expired(name):
    """Check whether a medicine has passed its expiry date safely."""
    if name not in medicines:
        return False

    exp = datetime.strptime(medicines[name]["expiry"], "%Y-%m-%d").date()
    return exp < date.today()


def bill_amount(prescription):
    """Calculate the total bill for a prescription list of items."""
    total = 0
    for item in prescription:
        med_name, qty = item[0], item[1]
        if med_name not in medicines:
            print(f"Billing error: '{med_name}' not in stock.")
            return None
        if qty <= 0:
            print(f"Billing error: invalid quantity for '{med_name}'.")
            return None
        total = total + medicines[med_name]["price"] * qty
    return total


def calculate_dosage(formula):
    """Safely evaluate an arithmetic dosage formula using an AST parser."""
    allowed_operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
    }

    def _evaluate(node):
        if isinstance(node, ast.Expression):
            return _evaluate(node.body)

        if isinstance(node, ast.Constant) and isinstance(
            node.value, (int, float)
        ):
            return node.value

        if isinstance(node, ast.BinOp) and type(node.op) in allowed_operators:
            left = _evaluate(node.left)
            right = _evaluate(node.right)
            return allowed_operators[type(node.op)](left, right)

        raise ValueError("Unsupported dosage formula")

    return _evaluate(ast.parse(formula, mode="eval"))


def patient_id(name, phone):
    """Generate a patient identifier using SHA-256."""
    return hashlib.sha256((name + phone).encode()).hexdigest()


def generate_rx_number():
    """Generate an unpredictable prescription number using secrets module."""
    return "RX-" + str(secrets.randbelow(900000) + 100000)


def save_stock(filepath="pharmacy.dat"):
    """Save the current medicine stock to a JSON file."""
    with open(filepath, "w", encoding="utf-8") as fout:
        json.dump(medicines, fout, indent=2)


def load_stock(filepath="pharmacy.dat"):
    """Load medicine stock from a JSON file with structure validation."""
    global medicines  # pylint: disable=global-statement

    with open(filepath, "r", encoding="utf-8") as fin:
        data = json.load(fin)

    if not isinstance(data, dict):
        raise ValueError("Stock file must contain a JSON object.")

    for med_name, info in data.items():
        if not isinstance(info, dict):
            raise ValueError(f"Invalid entry for '{med_name}'.")
        if "qty" not in info or "price" not in info:
            raise ValueError(f"Missing fields for '{med_name}'.")

    medicines = data


def print_label(name):
    """Print a dispensing label safely without shell command invocation."""
    print(f"Dispensing label: {name}")


def expiring_soon(days=30):
    """Return a list of medicine names expiring within the days window."""
    result = []
    for med_name in medicines:
        exp = datetime.strptime(
            medicines[med_name]["expiry"], "%Y-%m-%d"
        ).date()
        if (exp - date.today()).days < days:
            result.append(med_name)
    return result


def pharmacist_login(password):
    """Verify pharmacist login credentials against configured password."""
    return password == DB_PASSWORD


def print_stock():
    """Print a formatted report of all medicines currently in stock."""
    print("===== Pharmacy Stock Report =====")
    for med_name in medicines:
        info = medicines[med_name]
        print(
            f"{med_name} -> {info['qty']} units, "
            f"Rs. {info['price']} exp {info['expiry']}"
        )


def main():
    """Run the pharmacy management system demo workflow."""
    add_medicine("Paracetamol 500mg", 200, 1.5, "2027-06-30")
    add_medicine("Amoxicillin 250mg", 40, 6.0, "2026-01-15")
    add_medicine("Cetirizine 10mg", 10, 2.0, "2027-03-31")
    add_medicine(404, 25)  # rejected: numeric name
    dispense_medicine("Paracetamol 500mg", 30)
    dispense_medicine("Insulin", 2)

    print("Paracetamol stock:", get_quantity("Paracetamol 500mg"))
    print("Amoxicillin expired?", is_expired("Amoxicillin 250mg"))
    print(
        "Bill:",
        bill_amount(
            [("Paracetamol 500mg", 10), ("Amoxicillin 250mg", 5)]
        ),
    )
    print("Dosage (mg/day):", calculate_dosage("250 * 2"))
    print("Patient ID:", patient_id("Asha", "9876543210"))
    print("Rx number:", generate_rx_number())
    print("Login:", pharmacist_login("pharma@123"))
    print_label("Paracetamol 500mg")

    save_stock()
    load_stock()
    print_stock()


if __name__ == "__main__":
    main()
