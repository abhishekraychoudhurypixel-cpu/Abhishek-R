# ============================================================
# CA3 PRACTICE PROJECT
# PYTHON-BASED BUSINESS CHATBOT
# OFFICE SUPPLIES PROCUREMENT CHATBOT
# ============================================================
#
# Version 7
#
# Features:
# 1. Greeting
# 2. Multiple product identification
# 3. Accurate product matching
# 4. Quantity collection one-by-one
# 5. Multiple product quantities
# 6. Total cost calculation
# 7. Budget checking
# 8. Quantity reduction when over budget
# 9. Add more products
# 10. Add missing quantities
# 11. Delivery requirement
# 12. Bulk order detection
# 13. Final structured summary
# 14. Conversation continues until "bye"
# ============================================================


import re


# ============================================================
# 1. PRODUCT DATABASE
# ============================================================

PRODUCTS = {

    "ball pen": {
        "category": "Writing Supplies",
        "price": 10,
        "unit": "piece"
    },

    "gel pen": {
        "category": "Writing Supplies",
        "price": 20,
        "unit": "piece"
    },

    "pencil": {
        "category": "Writing Supplies",
        "price": 8,
        "unit": "piece"
    },

    "notebook": {
        "category": "Paper Supplies",
        "price": 60,
        "unit": "piece"
    },

    "printer paper": {
        "category": "Paper Supplies",
        "price": 300,
        "unit": "ream"
    },

    "sticky notes": {
        "category": "Desk Supplies",
        "price": 50,
        "unit": "pack"
    },

    "stapler": {
        "category": "Desk Supplies",
        "price": 120,
        "unit": "piece"
    },

    "staples": {
        "category": "Desk Supplies",
        "price": 40,
        "unit": "box"
    },

    "file folder": {
        "category": "Filing Supplies",
        "price": 30,
        "unit": "piece"
    },

    "marker": {
        "category": "Writing Supplies",
        "price": 25,
        "unit": "piece"
    },

    "envelope": {
        "category": "Paper Supplies",
        "price": 5,
        "unit": "piece"
    },

    "calculator": {
        "category": "Desk Supplies",
        "price": 350,
        "unit": "piece"
    }
}


# ============================================================
# 2. PRODUCT ALIASES
# ============================================================

ALIASES = {

    "pen": "ball pen",
    "pens": "ball pen",
    "ball pens": "ball pen",

    "gel pen": "gel pen",
    "gel pens": "gel pen",

    "pencil": "pencil",
    "pencils": "pencil",

    "notebook": "notebook",
    "notebooks": "notebook",

    "paper": "printer paper",
    "papers": "printer paper",
    "printer paper": "printer paper",
    "printer papers": "printer paper",

    "sticky note": "sticky notes",
    "sticky notes": "sticky notes",

    "stapler": "stapler",
    "staplers": "stapler",

    "staple": "staples",
    "staples": "staples",

    "folder": "file folder",
    "folders": "file folder",
    "file folder": "file folder",
    "file folders": "file folder",

    "marker": "marker",
    "markers": "marker",

    "envelope": "envelope",
    "envelopes": "envelope",

    "calculator": "calculator",
    "calculators": "calculator"
}


# ============================================================
# 3. ACCURATE PRODUCT EXTRACTION
# ============================================================
#
# IMPORTANT:
# Uses WORD BOUNDARIES.
#
# Therefore:
# "pencils" will NOT match "pen"
# "markers" will NOT accidentally match another word
# ============================================================

def extract_products(text):

    text = text.lower()

    found_products = []

    # --------------------------------------------------------
    # Check actual product names first
    # --------------------------------------------------------

    sorted_products = sorted(
        PRODUCTS.keys(),
        key=len,
        reverse=True
    )

    for product in sorted_products:

        pattern = r'\b' + re.escape(product) + r'\b'

        if re.search(pattern, text):

            if product not in found_products:

                found_products.append(product)

    # --------------------------------------------------------
    # Check aliases using word boundaries
    # --------------------------------------------------------

    sorted_aliases = sorted(
        ALIASES.keys(),
        key=len,
        reverse=True
    )

    for alias in sorted_aliases:

        pattern = r'\b' + re.escape(alias) + r'\b'

        if re.search(pattern, text):

            product = ALIASES[alias]

            if product not in found_products:

                found_products.append(product)

    return found_products


# ============================================================
# 4. QUANTITY EXTRACTION
# ============================================================

def extract_quantity(text):

    text = text.lower()

    match = re.search(
        r'\b(\d+(?:\.\d+)?)\b',
        text
    )

    if match:

        quantity = float(match.group(1))

        if quantity.is_integer():

            quantity = int(quantity)

        return quantity

    return None


# ============================================================
# 5. BUDGET EXTRACTION
# ============================================================

def extract_budget(text):

    text = text.lower()

    match = re.search(
        r'(?:₹|rs\.?|rupees)?\s*(\d+(?:,\d+)*)',
        text
    )

    if match:

        value = match.group(1).replace(",", "")

        return float(value)

    return None


# ============================================================
# 6. DELIVERY EXTRACTION
# ============================================================

def extract_delivery(text):

    text = text.lower().strip()

    # Correct common spelling mistake
    text = text.replace("tommorow", "tomorrow")

    if "tomorrow" in text:

        return "Tomorrow"

    if "today" in text:

        return "Today"

    if "urgent" in text or "asap" in text:

        return "Urgent / ASAP"

    if "fast" in text:

        return "Fast Delivery"

    match = re.search(
        r'within\s+(\d+)\s+days?',
        text
    )

    if match:

        return "Within " + match.group(1) + " days"

    match = re.search(
        r'in\s+(\d+)\s+days?',
        text
    )

    if match:

        return "In " + match.group(1) + " days"

    if "standard" in text:

        return "Standard Delivery"

    return text.capitalize()


# ============================================================
# 7. YES / NO DETECTION
# ============================================================

def is_yes(text):

    text = text.lower().strip()

    return text in [
        "yes",
        "y",
        "yeah",
        "yep",
        "sure",
        "okay",
        "ok",
        "of course"
    ]


def is_no(text):

    text = text.lower().strip()

    return text in [
        "no",
        "n",
        "nope",
        "not now"
    ]


# ============================================================
# 8. ADD MORE PRODUCT REQUEST
# ============================================================

def wants_to_add_more(text):

    text = text.lower().strip()

    phrases = [

        "add more",
        "add another",
        "add another product",
        "add more products",
        "i need to add more",
        "i want to add more",
        "need more products",
        "add one more",
        "forgot a product",
        "forgot some products",
        "include another",
        "include more"
    ]

    for phrase in phrases:

        if phrase in text:

            return True

    return False


# ============================================================
# 9. INTENT IDENTIFICATION
# ============================================================

def identify_intent(text, stage):

    text_lower = text.lower().strip()

    if text_lower in [
        "bye",
        "goodbye",
        "exit",
        "quit"
    ]:

        return "GOODBYE"

    if text_lower in [
        "hi",
        "hello",
        "hey",
        "good morning",
        "good afternoon",
        "good evening"
    ]:

        return "GREETING"

    if wants_to_add_more(text):

        return "PRODUCT_SEARCH"

    if stage == "PRODUCTS":

        return "PRODUCT_SEARCH"

    if stage == "QUANTITY":

        return "QUANTITY"

    if stage == "BUDGET":

        return "PRICE"

    if stage == "DELIVERY":

        return "DELIVERY"

    if "category" in text_lower:

        return "CATEGORY"

    if "bulk" in text_lower:

        return "BULK_ENQUIRY"

    return "UNKNOWN"


# ============================================================
# 10. CHATBOT CLASS
# ============================================================

class OfficeSuppliesChatbot:

    def __init__(self):

        self.stage = "PRODUCTS"

        # Products selected by user
        self.selected_products = []

        # Product -> quantity
        self.order_items = {}

        # Current quantity index
        self.current_product_index = 0

        # Budget
        self.budget = None

        # Delivery
        self.delivery = None

        # Whether chatbot is asking about reducing quantity
        self.reducing_quantity = False

        # Whether chatbot is asking which product to reduce
        self.asking_reduction_product = False

        # Whether chatbot is asking new quantity
        self.reduction_product = None

        # Whether chatbot is adding more products
        self.adding_more = False


    # ========================================================
    # SHOW PRODUCTS
    # ========================================================

    def show_products(self):

        print("\nAvailable Office Supplies:")
        print("-" * 65)

        for product, details in PRODUCTS.items():

            print(
                f"{product.title():20} | "
                f"{details['category']:18} | "
                f"₹{details['price']} per {details['unit']}"
            )

        print("-" * 65)


    # ========================================================
    # CALCULATE TOTAL
    # ========================================================

    def calculate_total(self):

        total = 0

        for product, quantity in self.order_items.items():

            price = PRODUCTS[product]["price"]

            total += quantity * price

        return total


    # ========================================================
    # GET CURRENT PRODUCT
    # ========================================================

    def get_current_product(self):

        if self.current_product_index < len(
            self.selected_products
        ):

            return self.selected_products[
                self.current_product_index
            ]

        return None


    # ========================================================
    # ASK QUANTITY
    # ========================================================

    def ask_next_quantity(self):

        product = self.get_current_product()

        if product is None:

            return

        details = PRODUCTS[product]

        print(
            f"\nBot: How many {details['unit']}s of "
            f"{product.title()} would you like?"
        )


    # ========================================================
    # PROCESS PRODUCTS
    # ========================================================

    def process_products(self, text):

        products = extract_products(text)

        if not products:

            print(
                "\nBot: I could not identify any valid "
                "office supply."
            )

            print(
                "Bot: Please enter products such as "
                "pencils, notebooks, markers or printer paper."
            )

            return

        # ----------------------------------------------------
        # Add only products that are not already selected
        # ----------------------------------------------------

        new_products = []

        for product in products:

            if product not in self.selected_products:

                self.selected_products.append(product)

                new_products.append(product)

        if not new_products:

            print(
                "\nBot: Those products are already in your order."
            )

            if self.stage == "PRODUCTS":

                self.ask_next_quantity()

            return

        print(
            f"\nBot: I identified {len(new_products)} product(s):"
        )

        for product in new_products:

            details = PRODUCTS[product]

            print(
                f"     • {product.title()} "
                f"({details['category']})"
            )

        # ----------------------------------------------------
        # If this is a new product addition
        # ----------------------------------------------------

        if self.adding_more:

            print(
                "\nBot: I have added the new product(s) "
                "to your order."
            )

            self.adding_more = False

        self.stage = "QUANTITY"

        # ----------------------------------------------------
        # Find first product without quantity
        # ----------------------------------------------------

        self.current_product_index = 0

        while (
            self.current_product_index
            < len(self.selected_products)
            and self.selected_products[
                self.current_product_index
            ] in self.order_items
        ):

            self.current_product_index += 1

        if self.current_product_index < len(
            self.selected_products
        ):

            self.ask_next_quantity()

        else:

            self.all_quantities_collected()


    # ========================================================
    # PROCESS QUANTITY
    # ========================================================

    def process_quantity(self, text):

        quantity = extract_quantity(text)

        if quantity is None or quantity <= 0:

            print(
                "\nBot: Please enter a valid quantity."
            )

            return

        product = self.get_current_product()

        if product is None:

            self.all_quantities_collected()

            return

        self.order_items[product] = quantity

        details = PRODUCTS[product]

        item_total = quantity * details["price"]

        print(
            f"\nBot: {quantity} {details['unit']}(s) "
            f"of {product.title()} added."
        )

        print(
            f"Bot: Estimated cost: ₹{item_total:,.2f}"
        )

        self.current_product_index += 1

        # ----------------------------------------------------
        # Check for remaining products
        # ----------------------------------------------------

        while (
            self.current_product_index
            < len(self.selected_products)
            and self.selected_products[
                self.current_product_index
            ] in self.order_items
        ):

            self.current_product_index += 1

        if self.current_product_index < len(
            self.selected_products
        ):

            self.ask_next_quantity()

        else:

            self.all_quantities_collected()


    # ========================================================
    # ALL QUANTITIES COLLECTED
    # ========================================================

    def all_quantities_collected(self):

        total = self.calculate_total()

        print(
            "\nBot: All product quantities have been recorded."
        )

        print(
            f"Bot: Combined estimated order total is "
            f"₹{total:,.2f}."
        )

        self.stage = "BUDGET"

        self.ask_budget()


    # ========================================================
    # ASK BUDGET
    # ========================================================

    def ask_budget(self):

        print(
            "\nBot: What is your maximum budget "
            "for this order?"
        )


    # ========================================================
    # PROCESS BUDGET
    # ========================================================

    def process_budget(self, text):

        budget = extract_budget(text)

        if budget is None or budget <= 0:

            print(
                "\nBot: Please enter a valid budget."
            )

            return

        self.budget = budget

        total = self.calculate_total()

        print(
            f"\nBot: Your maximum budget is "
            f"₹{budget:,.2f}."
        )

        print(
            f"Bot: Current order total is "
            f"₹{total:,.2f}."
        )

        # ----------------------------------------------------
        # Order is within budget
        # ----------------------------------------------------

        if total <= budget:

            remaining = budget - total

            print(
                "\nBot: Good news! Your order is "
                "within your budget."
            )

            print(
                f"Bot: Remaining budget: ₹{remaining:,.2f}"
            )

            print(
                "\nBot: Would you like to add any more "
                "products before delivery?"
            )

            self.stage = "ADD_MORE"

        # ----------------------------------------------------
        # Order exceeds budget
        # ----------------------------------------------------

        else:

            excess = total - budget

            print(
                "\nBot: Your order exceeds the budget "
                f"by ₹{excess:,.2f}."
            )

            print(
                "Bot: Would you like to reduce the "
                "quantity of any product?"
            )

            self.stage = "REDUCE"


    # ========================================================
    # PROCESS REDUCTION DECISION
    # ========================================================

    def process_reduction_decision(self, text):

        if is_yes(text):

            print(
                "\nBot: Which product quantity would "
                "you like to reduce?"
            )

            print(
                "Bot: Your current quantities are:"
            )

            for product, quantity in self.order_items.items():

                print(
                    f"     • {product.title()}: {quantity}"
                )

            self.stage = "REDUCE_PRODUCT"

            return

        if is_no(text):

            print(
                "\nBot: No problem. We can keep the "
                "current quantities."
            )

            print(
                "Bot: You can still add more products "
                "if required."
            )

            print(
                "\nBot: Would you like to add more products?"
            )

            self.stage = "ADD_MORE"

            return

        print(
            "\nBot: Please answer Yes or No."
        )


    # ========================================================
    # SELECT PRODUCT TO REDUCE
    # ========================================================

    def process_reduction_product(self, text):

        products = extract_products(text)

        selected_product = None

        for product in products:

            if product in self.order_items:

                selected_product = product

                break

        if selected_product is None:

            print(
                "\nBot: I could not identify a product "
                "from your current order."
            )

            print(
                "Bot: Please choose one of these:"
            )

            for product, quantity in self.order_items.items():

                print(
                    f"     • {product.title()} "
                    f"({quantity} currently)"
                )

            return

        self.reduction_product = selected_product

        current_quantity = self.order_items[
            selected_product
        ]

        print(
            f"\nBot: Current quantity of "
            f"{selected_product.title()} is "
            f"{current_quantity}."
        )

        print(
            f"Bot: What should the new quantity of "
            f"{selected_product.title()} be?"
        )

        self.stage = "REDUCE_QUANTITY"


    # ========================================================
    # PROCESS REDUCED QUANTITY
    # ========================================================

    def process_reduction_quantity(self, text):

        new_quantity = extract_quantity(text)

        if new_quantity is None or new_quantity < 0:

            print(
                "\nBot: Please enter a valid quantity."
            )

            return

        product = self.reduction_product

        old_quantity = self.order_items[product]

        # ----------------------------------------------------
        # Zero means remove product
        # ----------------------------------------------------

        if new_quantity == 0:

            del self.order_items[product]

            self.selected_products.remove(product)

            print(
                f"\nBot: {product.title()} has been "
                "removed from the order."
            )

        else:

            self.order_items[product] = new_quantity

            print(
                f"\nBot: Quantity of {product.title()} "
                f"changed from {old_quantity} "
                f"to {new_quantity}."
            )

        # ----------------------------------------------------
        # Recalculate
        # ----------------------------------------------------

        total = self.calculate_total()

        print(
            f"Bot: New estimated order total: "
            f"₹{total:,.2f}"
        )

        # ----------------------------------------------------
        # Check budget again
        # ----------------------------------------------------

        if self.budget is not None:

            if total <= self.budget:

                remaining = self.budget - total

                print(
                    "\nBot: Great! The revised order is "
                    "now within your budget."
                )

                print(
                    f"Bot: Remaining budget: "
                    f"₹{remaining:,.2f}"
                )

                print(
                    "\nBot: Would you like to add "
                    "more products?"
                )

                self.stage = "ADD_MORE"

            else:

                excess = total - self.budget

                print(
                    "\nBot: The order still exceeds "
                    f"your budget by ₹{excess:,.2f}."
                )

                print(
                    "Bot: Would you like to reduce "
                    "another product?"
                )

                self.stage = "REDUCE"


    # ========================================================
    # PROCESS ADD MORE DECISION
    # ========================================================

    def process_add_more(self, text):

        # ----------------------------------------------------
        # User wants to add more
        # ----------------------------------------------------

        if is_yes(text) or wants_to_add_more(text):

            print(
                "\nBot: Sure! Please tell me the "
                "additional product or products."
            )

            self.stage = "ADD_PRODUCTS"

            return

        # ----------------------------------------------------
        # User does not want more
        # ----------------------------------------------------

        if is_no(text):

            self.stage = "DELIVERY"

            print(
                "\nBot: When would you like the "
                "order delivered?"
            )

            return

        # ----------------------------------------------------
        # User directly provides a product
        # ----------------------------------------------------

        products = extract_products(text)

        if products:

            self.adding_more = True

            self.stage = "ADD_PRODUCTS"

            self.process_products(text)

            return

        print(
            "\nBot: Please answer Yes or No, or "
            "tell me the product you want to add."
        )


    # ========================================================
    # ADD ADDITIONAL PRODUCTS
    # ========================================================

    def process_add_products(self, text):

        products = extract_products(text)

        if not products:

            print(
                "\nBot: I could not identify the "
                "additional product."
            )

            print(
                "Bot: Please enter the product name."
            )

            return

        self.adding_more = True

        self.process_products(text)


    # ========================================================
    # PROCESS DELIVERY
    # ========================================================

    def process_delivery(self, text):

        delivery = extract_delivery(text)

        if not delivery:

            print(
                "\nBot: Please provide a delivery "
                "requirement."
            )

            return

        self.delivery = delivery

        print(
            f"\nBot: Delivery requirement recorded: "
            f"{delivery}"
        )

        self.stage = "COMPLETE"

        print(
            "\nBot: Your order information is complete."
        )

        print(
            "Bot: You can still type "
            "'add more' if you forgot a product."
        )

        print(
            "Bot: Otherwise, type 'bye' to finish "
            "and view your final summary."
        )


    # ========================================================
    # FINAL SUMMARY
    # ========================================================

    def show_summary(self):

        total = self.calculate_total()

        print("\n")
        print("=" * 80)
        print("                    FINAL ORDER SUMMARY")
        print("=" * 80)

        print(
            f"{'Product':20}"
            f"{'Category':20}"
            f"{'Qty':8}"
            f"{'Unit Price':12}"
            f"{'Total':12}"
        )

        print("-" * 80)

        for product, quantity in self.order_items.items():

            details = PRODUCTS[product]

            item_total = (
                quantity * details["price"]
            )

            print(
                f"{product.title():20}"
                f"{details['category']:20}"
                f"{str(quantity):8}"
                f"₹{details['price']:10.2f}"
                f"₹{item_total:10.2f}"
            )

        print("-" * 80)

        print(
            f"Combined Order Total: ₹{total:,.2f}"
        )

        # ----------------------------------------------------
        # Bulk order
        # ----------------------------------------------------

        bulk = any(
            quantity >= 100
            for quantity in self.order_items.values()
        )

        if bulk:

            order_type = "Bulk Order"

        else:

            order_type = "Regular Order"

        print(
            f"Order Type: {order_type}"
        )

        # ----------------------------------------------------
        # Budget
        # ----------------------------------------------------

        if self.budget is not None:

            print(
                f"Budget: ₹{self.budget:,.2f}"
            )

            if total <= self.budget:

                print(
                    "Budget Status: Within Budget"
                )

            else:

                print(
                    "Budget Status: Over Budget"
                )

        else:

            print(
                "Budget: Not Provided"
            )

        # ----------------------------------------------------
        # Delivery
        # ----------------------------------------------------

        if self.delivery:

            print(
                f"Delivery Requirement: "
                f"{self.delivery}"
            )

        else:

            print(
                "Delivery Requirement: "
                "Not Provided"
            )

        print("=" * 80)


    # ========================================================
    # MAIN RESPONSE FUNCTION
    # ========================================================

    def respond(self, text):

        text = text.strip()

        if not text:

            print(
                "\nBot: Please enter a response."
            )

            return

        # ----------------------------------------------------
        # Greeting
        # ----------------------------------------------------

        if text.lower() in [
            "hi",
            "hello",
            "hey",
            "good morning",
            "good afternoon",
            "good evening"
        ]:

            print(
                "\nBot: Hello! Welcome to the "
                "Office Supplies Procurement Chatbot."
            )

            print(
                "Bot: I can help you order multiple "
                "office supplies."
            )

            self.show_products()

            print(
                "\nBot: What product or products "
                "would you like to order?"
            )

            self.stage = "PRODUCTS"

            return


        # ----------------------------------------------------
        # PRODUCT SELECTION
        # ----------------------------------------------------

        if self.stage == "PRODUCTS":

            self.process_products(text)

            return


        # ----------------------------------------------------
        # QUANTITY
        # ----------------------------------------------------

        if self.stage == "QUANTITY":

            # User may have forgotten to provide a product
            # and instead asks to add more.

            if wants_to_add_more(text):

                self.adding_more = True

                print(
                    "\nBot: Sure. Please tell me the "
                    "additional product."
                )

                self.stage = "ADD_PRODUCTS"

                return

            self.process_quantity(text)

            return


        # ----------------------------------------------------
        # BUDGET
        # ----------------------------------------------------

        if self.stage == "BUDGET":

            self.process_budget(text)

            return


        # ----------------------------------------------------
        # REDUCE QUANTITY DECISION
        # ----------------------------------------------------

        if self.stage == "REDUCE":

            self.process_reduction_decision(text)

            return


        # ----------------------------------------------------
        # SELECT PRODUCT TO REDUCE
        # ----------------------------------------------------

        if self.stage == "REDUCE_PRODUCT":

            self.process_reduction_product(text)

            return


        # ----------------------------------------------------
        # NEW REDUCED QUANTITY
        # ----------------------------------------------------

        if self.stage == "REDUCE_QUANTITY":

            self.process_reduction_quantity(text)

            return


        # ----------------------------------------------------
        # ADD MORE DECISION
        # ----------------------------------------------------

        if self.stage == "ADD_MORE":

            self.process_add_more(text)

            return


        # ----------------------------------------------------
        # ADD PRODUCTS
        # ----------------------------------------------------

        if self.stage == "ADD_PRODUCTS":

            self.process_add_products(text)

            return


        # ----------------------------------------------------
        # DELIVERY
        # ----------------------------------------------------

        if self.stage == "DELIVERY":

            # User forgot a product
            if wants_to_add_more(text):

                self.adding_more = True

                print(
                    "\nBot: Sure! Tell me which "
                    "product you want to add."
                )

                self.stage = "ADD_PRODUCTS"

                return

            self.process_delivery(text)

            return


        # ----------------------------------------------------
        # COMPLETE
        # ----------------------------------------------------

        if self.stage == "COMPLETE":

            # Allow user to add more even after delivery
            # information has been entered.

            if wants_to_add_more(text):

                self.adding_more = True

                print(
                    "\nBot: Sure! Which product "
                    "would you like to add?"
                )

                self.stage = "ADD_PRODUCTS"

                return

            print(
                "\nBot: Your order information is "
                "already complete."
            )

            print(
                "Bot: Type 'bye' to finish the "
                "conversation."
            )

            return



# ============================================================
# 11. STREAMLIT INTERFACE
# ============================================================

# ============================================================
# 11. STREAMLIT INTERFACE (images, input boxes, live order)
# ============================================================

import base64
import math
from contextlib import redirect_stdout
from datetime import date, timedelta
from io import StringIO

import pandas as pd
import streamlit as st


def _show_products_md(self):
    print("\nAvailable Office Supplies:\n")
    print("| Product | Category | Price |")
    print("|---|---|---|")
    for p, d in PRODUCTS.items():
        print(f"| {p.title()} | {d['category']} | ₹{d['price']} per {d['unit']} |")


OfficeSuppliesChatbot.show_products = _show_products_md

st.set_page_config(page_title="Office Supplies Procurement Chatbot", page_icon="🛒", layout="wide")

# ---------------- product images (SVG, no external links) ----------------
CAT_COLORS = {"Writing Supplies": "#3b6fd8", "Paper Supplies": "#e08a1e",
              "Desk Supplies": "#1f9d73", "Filing Supplies": "#8b5cc9"}
CATEGORIES = sorted(CAT_COLORS)


def _mix(h, t, a):
    h = h.lstrip("#")
    v = [int(h[i:i + 2], 16) for i in (0, 2, 4)]
    return "#%02x%02x%02x" % tuple(round(x + (t - x) * a) for x in v)


def product_svg(p):
    c = CAT_COLORS[PRODUCTS[p]["category"]]
    d, l, bg = _mix(c, 0, .3), _mix(c, 255, .4), _mix(c, 255, .86)
    R = 'transform="rotate(-30 100 70)"'
    keys = "".join(f'<rect x="{72 + i * 15}" y="{54 + j * 17}" width="12" height="12" rx="2" fill="{c if i == 3 else "#9ca3af"}"/>' for j in range(4) for i in range(4))
    rings = "".join(f'<circle cx="62" cy="{30 + k * 14}" r="3.5" fill="#e5e7eb" stroke="{d}"/>' for k in range(6))
    staples = "".join(f'<path d="M{x} 96 v-9 h16 v9" fill="none" stroke="#e5e7eb" stroke-width="2.5"/>' for x in (68, 96, 124))
    art = {
        "ball pen": f'<g {R}><rect x="35" y="62" width="110" height="14" rx="7" fill="{c}"/><rect x="118" y="62" width="14" height="14" fill="{d}"/><polygon points="145,63 168,69 145,75" fill="#cfcfcf"/><polygon points="162,67.5 170,69 162,70.5" fill="#222"/><rect x="60" y="64" width="40" height="3" rx="1.5" fill="#fff" fill-opacity=".5"/></g>',
        "gel pen": f'<g {R}><rect x="35" y="60" width="95" height="18" rx="9" fill="{c}"/><rect x="45" y="65" width="55" height="8" rx="4" fill="#fff" fill-opacity=".45"/><rect x="110" y="60" width="28" height="18" fill="{d}"/><polygon points="138,62 162,69 138,76" fill="{d}"/><polygon points="156,67 168,69 156,71" fill="#222"/></g>',
        "pencil": f'<g {R}><rect x="35" y="60" width="95" height="20" fill="#f4c542"/><rect x="35" y="60" width="95" height="5" fill="#e0a92b"/><polygon points="130,60 160,70 130,80" fill="#f1d3a3"/><polygon points="150,66 162,70 150,74" fill="#333"/><rect x="25" y="60" width="10" height="20" fill="#d9d9d9"/><rect x="14" y="60" width="13" height="20" rx="4" fill="#ef7a8a"/></g>',
        "notebook": f'<rect x="60" y="18" width="88" height="104" rx="5" fill="{c}"/><rect x="72" y="18" width="76" height="104" rx="5" fill="{l}"/>{rings}<rect x="88" y="40" width="46" height="30" rx="3" fill="#fff"/><rect x="94" y="48" width="34" height="3" fill="{d}"/><rect x="94" y="56" width="22" height="3" fill="{d}"/>',
        "printer paper": f'<rect x="60" y="28" width="86" height="12" fill="#fff" stroke="#cbd5e1"/><rect x="55" y="38" width="96" height="76" rx="2" fill="{c}"/><rect x="63" y="52" width="80" height="34" fill="#fff"/><text x="103" y="76" font-size="18" font-family="sans-serif" font-weight="bold" text-anchor="middle" fill="{d}">A4</text>',
        "sticky notes": f'<rect x="62" y="30" width="72" height="72" fill="#fde68a" stroke="#eab308" transform="rotate(-5 98 66)"/><rect x="74" y="38" width="72" height="72" fill="#fef08a" stroke="#eab308" transform="rotate(5 110 74)"/><line x1="86" y1="62" x2="132" y2="64" stroke="#ca8a04" stroke-width="2"/><line x1="86" y1="74" x2="124" y2="76" stroke="#ca8a04" stroke-width="2"/>',
        "stapler": f'<rect x="42" y="94" width="116" height="14" rx="4" fill="#374151"/><path d="M48 94 L150 66 Q162 64 162 76 L162 94 Z" fill="{c}"/><path d="M60 88 L140 68" stroke="#fff" stroke-opacity=".4" stroke-width="3"/><rect x="140" y="88" width="16" height="6" fill="{d}"/>',
        "staples": f'<rect x="55" y="58" width="90" height="54" rx="3" fill="{c}"/><rect x="55" y="58" width="90" height="14" fill="{d}"/>{staples}<path d="M80 36 v-9 h16 v9" fill="none" stroke="#9ca3af" stroke-width="2.5"/>',
        "file folder": f'<path d="M40 36 h42 l8 10 h70 v70 h-120 z" fill="{d}"/><rect x="40" y="54" width="120" height="62" rx="3" fill="{l}"/><rect x="58" y="70" width="52" height="16" fill="#fff"/><rect x="64" y="76" width="38" height="3" fill="{d}"/>',
        "marker": f'<g {R}><rect x="45" y="58" width="85" height="24" rx="5" fill="#fff" stroke="{d}" stroke-width="2"/><rect x="45" y="58" width="42" height="24" rx="5" fill="{c}"/><rect x="130" y="63" width="18" height="14" fill="#444"/><polygon points="148,64 166,70 148,76" fill="{c}"/><rect x="98" y="65" width="24" height="10" fill="{c}" fill-opacity=".35"/></g>',
        "envelope": f'<rect x="42" y="36" width="116" height="76" rx="4" fill="#fff" stroke="{d}" stroke-width="2"/><polyline points="42,40 100,80 158,40" fill="none" stroke="{d}" stroke-width="2"/><polyline points="42,110 86,74" fill="none" stroke="{l}" stroke-width="2"/><polyline points="158,110 114,74" fill="none" stroke="{l}" stroke-width="2"/><rect x="132" y="44" width="18" height="14" fill="{c}"/>',
        "calculator": f'<rect x="65" y="14" width="70" height="108" rx="8" fill="#374151"/><rect x="72" y="22" width="56" height="22" rx="3" fill="#bde3cf"/><text x="124" y="39" font-size="14" font-family="monospace" text-anchor="end" fill="#1f3d2e">1,250</text>{keys}',
    }
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 140"><rect width="200" height="140" fill="{bg}"/>'
            f'<ellipse cx="100" cy="124" rx="62" ry="6" fill="{_mix(c, 0, .2)}" fill-opacity=".18"/>{art[p]}</svg>')


@st.cache_data(show_spinner=False)
def image_uri(p):
    import os
    for ext, mime in (("png", "png"), ("jpg", "jpeg"), ("webp", "webp")):
        path = os.path.join("images", f"{p.replace(' ', '_')}.{ext}")  # your own photo overrides the drawing
        if os.path.exists(path):
            return f"data:image/{mime};base64," + base64.b64encode(open(path, "rb").read()).decode()
    return "data:image/svg+xml;base64," + base64.b64encode(product_svg(p).encode()).decode()


def card_html(p):
    d = PRODUCTS[p]
    return (f'<div class="card"><img src="{image_uri(p)}" alt="{p}"/><div class="body">'
            f'<div class="ttl">{p.title()}</div><div class="price">₹{d["price"]:,} <small>per {d["unit"]}</small></div>'
            f'<div class="meta">{d["category"]}</div></div></div>')


st.markdown("""<style>
.hero{background:#1e2a4a;color:#f4f1e8;padding:2rem 2.2rem;border-radius:14px;margin-bottom:1rem}
.hero h1{margin:0 0 .4rem;padding:0;color:#f4f1e8;font-size:2.2rem}
.hero p{margin:0;max-width:46rem;color:#cdd5ea;font-size:1.05rem}
.step{border-left:4px solid #f5c518;padding:.2rem .9rem;margin-bottom:.6rem}
.step b{display:block}.step span{opacity:.8;font-size:.92rem}
.card{border:1px solid rgba(128,128,128,.3);border-radius:12px;overflow:hidden;background:rgba(128,128,128,.07);margin-bottom:.4rem}
.card img{width:100%;display:block}.card .body{padding:.6rem .8rem .7rem}
.card .ttl{font-weight:600}.card .price{font-size:1.15rem;font-weight:700;color:#f5c518}
.card .price small{font-weight:400;opacity:.7;font-size:.8rem}.card .meta{opacity:.7;font-size:.82rem}
</style>""", unsafe_allow_html=True)

# ---------------- state + helpers ----------------
ss = st.session_state
if "chatbot" not in ss:
    ss.chatbot = OfficeSuppliesChatbot()
ss.setdefault("messages", [])
ss.setdefault("editor_v", 0)
ss.setdefault("last_order", None)
for _p in PRODUCTS:
    ss.setdefault(f"qty_{_p}", 0)

WELCOME = ("Hello! Welcome to the Office Supplies Procurement Chatbot.\n\nI can help you order multiple products, "
           "manage quantities, check your budget and arrange delivery.\n\n**What product or products would you like to order?**")


def sync_stage():
    """Keep the chatbot's conversation stage consistent after the order is edited from the UI."""
    b = ss.chatbot
    b.adding_more = False
    if not b.order_items:
        b.stage = "PRODUCTS"
    elif b.stage in ("PRODUCTS", "QUANTITY", "ADD_PRODUCTS", "BUDGET", "ADD_MORE", "REDUCE"):
        if b.budget is None:
            b.stage = "BUDGET"
        else:
            b.stage = "ADD_MORE" if b.calculate_total() <= b.budget else "REDUCE"


def new_order():
    ss.chatbot = OfficeSuppliesChatbot()
    ss.messages, ss.last_order = [], None
    for p in PRODUCTS:
        ss[f"qty_{p}"] = 0


def add_to_order(p):
    q = ss.get(f"qty_{p}", 0)
    if q <= 0:
        return
    b = ss.chatbot
    b.order_items[p] = b.order_items.get(p, 0) + q
    if p not in b.selected_products:
        b.selected_products.append(p)
    ss[f"qty_{p}"] = 0
    sync_stage()
    st.toast(f"Added {q} × {p.title()}", icon="✅")


def set_pending(text):
    ss.pending = text


def bot_md(text):
    out, prev = [], None
    for line in text.splitlines():
        s = line.strip()
        if not s:
            continue
        s = s[4:].strip() if s.startswith("Bot:") else s
        s = "- " + s[1:].strip() if s.startswith("•") else s
        kind = "tbl" if s.startswith("|") else "li" if s.startswith("- ") else "p"
        if out and kind == prev and kind != "p":
            out[-1] += "\n" + s
        else:
            out.append(s)
        prev = kind
    return "\n\n".join(out)


def chat(text):
    buf = StringIO()
    with redirect_stdout(buf):
        if text.lower().strip() in ("bye", "goodbye", "exit", "quit"):
            print("Thank you for using the Office Supplies Procurement Chatbot!")
            ss.chatbot.show_summary() if ss.chatbot.order_items else print("No order was created.")
            print("Goodbye! Have a great day.")
        else:
            ss.chatbot.respond(text)
    return buf.getvalue() or "I could not generate a response. Please try again."


if not ss.messages:
    ss.messages.append({"role": "assistant", "content": WELCOME})

# ---------------- sidebar filters ----------------
with st.sidebar:
    st.header("Find supplies")
    st.text_input("Search", key="f_search", placeholder="pen, paper, stapler...")
    st.multiselect("Category", CATEGORIES, key="f_cat", placeholder="All categories")
    st.button("🔄 Start new order", on_click=new_order, use_container_width=True)
    summary_box = st.container()

# ---------------- hero + images ----------------
st.markdown('<div class="hero"><h1>🛒 Office Supplies Procurement Chatbot</h1><p>Order pens, paper, desk and filing supplies. '
            'Pick items in the shop or just tell the chatbot what you need, then check your budget and set delivery.</p></div>',
            unsafe_allow_html=True)
for col, (p, label) in zip(st.columns(4), [("ball pen", "Writing"), ("notebook", "Paper"), ("stapler", "Desk"), ("file folder", "Filing")]):
    col.markdown(f'<div class="card"><img src="{image_uri(p)}" alt="{p}"/><div class="body"><div class="ttl">{label} supplies</div></div></div>', unsafe_allow_html=True)
for col, (t, s) in zip(st.columns(3), [("1. Choose", "Enter quantities in the Shop tab or chat with the bot."),
                                       ("2. Check", "Set a budget and edit quantities in My order."),
                                       ("3. Order", "Add delivery details in Checkout and download your order.")]):
    col.markdown(f'<div class="step"><b>{t}</b><span>{s}</span></div>', unsafe_allow_html=True)

tab_shop, tab_chat, tab_order, tab_check = st.tabs(["🛍️ Shop", "💬 Chat", "📋 My order", "✅ Checkout"])

# ---------------- SHOP ----------------
with tab_shop:
    s = ss.f_search.strip().lower()
    shown = [p for p, d in PRODUCTS.items()
             if (not ss.f_cat or d["category"] in ss.f_cat)
             and (not s or s in p or s in d["category"].lower() or any(s in a and t == p for a, t in ALIASES.items()))]
    if not shown:
        st.info("No products match. Clear the search or category filter in the sidebar.")
    for i in range(0, len(shown), 4):
        for col, p in zip(st.columns(4), shown[i:i + 4]):
            with col:
                st.markdown(card_html(p), unsafe_allow_html=True)
                st.number_input(f"Quantity ({PRODUCTS[p]['unit']}s)", min_value=0, max_value=100000, step=1, key=f"qty_{p}")
                st.button("Add to order", key=f"add_{p}", on_click=add_to_order, args=(p,), use_container_width=True)
                if p in ss.chatbot.order_items:
                    st.caption(f"In your order: {ss.chatbot.order_items[p]}")

# ---------------- CHAT ----------------
with tab_chat:
    st.caption("Items you add in the Shop tab are shared with the chatbot. Type 'add more' to add products, or 'bye' for the final summary.")
    for col, chip in zip(st.columns(4), ["Hi", "I need pens and notebooks", "add more", "bye"]):
        col.button(chip, key=f"chip_{chip}", on_click=set_pending, args=(chip,), use_container_width=True)
    history = st.container()
    text = st.chat_input("Type your request... e.g., pens and notebooks") or ss.pop("pending", None)
    if text:
        ss.messages.append({"role": "user", "content": text})
        ss.messages.append({"role": "assistant", "content": chat(text)})
    with history:
        for m in ss.messages:
            with st.chat_message(m["role"]):
                if m["role"] == "user":
                    st.markdown(m["content"])
                elif "FINAL ORDER SUMMARY" in m["content"]:
                    st.code(m["content"].strip(), language=None)
                else:
                    st.markdown(bot_md(m["content"]))

# ---------------- MY ORDER ----------------
bot = ss.chatbot
with tab_order:
    if not bot.order_items:
        st.info("Your order is empty. Add items in the Shop tab or tell the chatbot what you need.")
    else:
        rows = [{"Product": p.title(), "Category": PRODUCTS[p]["category"], "Unit": PRODUCTS[p]["unit"],
                 "Unit price (₹)": PRODUCTS[p]["price"], "Qty": q, "Line total (₹)": q * PRODUCTS[p]["price"]}
                for p, q in bot.order_items.items()]
        st.caption("Edit the Qty column to change quantities. Set it to 0 to remove an item.")
        edited = st.data_editor(
            pd.DataFrame(rows), hide_index=True, use_container_width=True, key=f"editor_{ss.editor_v}",
            disabled=["Product", "Category", "Unit", "Unit price (₹)", "Line total (₹)"],
            column_config={"Qty": st.column_config.NumberColumn(min_value=0, step=1)})
        changed = False
        for _, r in edited.iterrows():
            p, q = r["Product"].lower(), r["Qty"]
            if pd.isna(q):
                continue
            q = int(q) if float(q).is_integer() else float(q)
            if q != bot.order_items.get(p):
                changed = True
                if q <= 0:
                    bot.order_items.pop(p, None)
                    if p in bot.selected_products:
                        bot.selected_products.remove(p)
                else:
                    bot.order_items[p] = q
        if changed:
            sync_stage()
            ss.editor_v += 1
            st.rerun()

        total = bot.calculate_total()
        left, right = st.columns([1, 2])
        with left:
            budget_in = st.number_input("Maximum budget (₹)", min_value=0, step=100, value=int(bot.budget or 0),
                                        help="0 means no budget")
            new_budget = float(budget_in) if budget_in > 0 else None
            if new_budget != bot.budget:
                bot.budget = new_budget
                sync_stage()
            st.metric("Order total", f"₹{total:,.2f}")
            st.metric("Order type", "Bulk order" if any(q >= 100 for q in bot.order_items.values()) else "Regular order")
        with right:
            if bot.budget:
                st.progress(min(total / bot.budget, 1.0))
                if total <= bot.budget:
                    st.success(f"Within budget. ₹{bot.budget - total:,.2f} remaining.")
                else:
                    excess = total - bot.budget
                    st.error(f"Over budget by ₹{excess:,.2f}.")
                    top = max(bot.order_items, key=lambda k: bot.order_items[k] * PRODUCTS[k]["price"])
                    cut = math.ceil(excess / PRODUCTS[top]["price"])
                    st.caption(f"Tip: reduce {top.title()} by {cut} {PRODUCTS[top]['unit']}(s) to fit your budget."
                               if cut < bot.order_items[top] else "Tip: reduce several items or raise your budget.")
            else:
                st.info("Enter a maximum budget to check your order against it.")
            st.bar_chart(pd.DataFrame(rows).set_index("Product")["Line total (₹)"])

# ---------------- CHECKOUT ----------------
with tab_check:
    if not bot.order_items:
        st.info("Add items to your order before checkout.")
    else:
        if bot.budget and bot.calculate_total() > bot.budget:
            st.warning("Your order is over budget. You can still send it, or adjust it in My order.")
        with st.form("checkout"):
            c1, c2 = st.columns(2)
            company = c1.text_input("Company or team *")
            contact = c2.text_input("Contact person *")
            email = c1.text_input("Email *")
            phone = c2.text_input("Phone *", placeholder="10-digit mobile number")
            speed = c1.radio("Delivery speed", ["Standard", "Fast", "Urgent / ASAP"], horizontal=True)
            need_by = c2.date_input("Needed by", value=date.today() + timedelta(days=5), min_value=date.today())
            notes = st.text_area("Notes", placeholder="Floor, reception contact, billing instructions...")
            go = st.form_submit_button("Place order request", type="primary")
        if go:
            errs = [m for ok, m in [(company.strip(), "Enter your company or team."), (contact.strip(), "Enter a contact person."),
                                    (re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email.strip()), "Enter a valid email address."),
                                    (re.fullmatch(r"[6-9]\d{9}", phone.strip().replace(" ", "")), "Enter a valid 10-digit mobile number.")] if not ok]
            for e in errs:
                st.error(e)
            if not errs:
                bot.delivery = f"{speed} (needed by {need_by:%d %b %Y})"
                bot.stage = "COMPLETE"
                df = pd.DataFrame([{"Product": p.title(), "Qty": q, "Unit price": PRODUCTS[p]["price"], "Total": q * PRODUCTS[p]["price"]}
                                   for p, q in bot.order_items.items()])
                ss.last_order = {"id": f"PO-{date.today():%y%m%d}-{abs(hash(company + email)) % 9000 + 1000}", "company": company.strip(),
                                 "total": bot.calculate_total(), "delivery": bot.delivery, "csv": df.to_csv(index=False), "df": df}
        lo = ss.last_order
        if lo:
            st.success(f"Order request {lo['id']} saved for {lo['company']}.")
            st.dataframe(lo["df"], hide_index=True, use_container_width=True)
            m1, m2 = st.columns(2)
            m1.metric("Total", f"₹{lo['total']:,.2f}")
            m2.metric("Delivery", lo["delivery"])
            st.download_button("⬇️ Download order (CSV)", lo["csv"], file_name=f"{lo['id']}.csv", mime="text/csv")

# ---------------- sidebar order summary (filled last so it is always current) ----------------
with summary_box:
    st.divider()
    st.subheader("🧾 Your order")
    if bot.order_items:
        for p, q in bot.order_items.items():
            st.write(f"{p.title()} × {q}: ₹{q * PRODUCTS[p]['price']:,.0f}")
        st.metric("Total", f"₹{bot.calculate_total():,.2f}")
        if bot.budget:
            st.caption("✅ Within budget" if bot.calculate_total() <= bot.budget else "⚠️ Over budget")
    else:
        st.caption("Nothing added yet.")
