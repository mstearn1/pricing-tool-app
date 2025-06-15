# Streamlit app for Matt Stearn Competitive Set Pricing Tool
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Competitive Set Pricing Tool", layout="centered")
st.title("📊 Competitive Set Pricing & Capital Requirements Tool")

# Input: Product BOM and Costs
st.header("🔧 Product BOM and Costs")
bom_data = []
for i in range(1, 9):
    part = st.text_input(f"BOM{i} Part Name", key=f"part{i}")
    price = st.number_input(f"BOM{i} Unit Price ($)", min_value=0.0, value=0.0, step=0.01, key=f"price{i}")
    if part:
        bom_data.append({"Part": part, "Price": price})

# Compute total BOM cost
total_bom_cost = sum([p["Price"] for p in bom_data])
bom_shipping = total_bom_cost * 0.10

st.markdown(f"**Total BOM Cost:** ${total_bom_cost:.2f}")
st.markdown(f"**BOM Shipping Cost (10%):** ${bom_shipping:.2f}")

# Input: Filling, Assembly, Packaging
filling_assembly = st.number_input("Filling & Assembly Cost ($)", min_value=0.0, value=2.0)
packaging_cost = st.number_input("Additional Packaging Cost ($)", min_value=0.0, value=4.05)

# Finished goods cost
fg_cost = total_bom_cost + bom_shipping + filling_assembly + packaging_cost
st.markdown(f"**Finished Goods Cost:** ${fg_cost:.2f}")

# Brand Margin and Retail Calculations
st.header("📈 Retail Pricing Strategy")
brand_margin = st.slider("Brand Margin (as decimal, e.g. 0.795 = 79.5%)", 0.0, 1.0, 0.795)
retail_price = fg_cost / (1 - brand_margin)

retail_margin = st.slider("Retailer Margin (as decimal, e.g. 0.575 = 57.5%)", 0.0, 1.0, 0.575)
shelf_price = retail_price / (1 - retail_margin)
st.markdown(f"**Price to Retailer:** ${retail_price:.2f}")
st.markdown(f"**Shelf Price:** ${shelf_price:.2f}")

# Product Size & Per OZ Price
oz_size = st.number_input("Product Size (OZ)", min_value=0.1, value=4.0)
price_per_oz = shelf_price / oz_size
st.markdown(f"**Shelf Price per OZ:** ${price_per_oz:.2f}")

# Competitive Set
st.header("🧴 Competitive Set")
with st.expander("Enter up to 3 competitors"):
    competitors = []
    for i in range(1, 4):
        brand = st.text_input(f"Competitor {i} Brand")
        product = st.text_input(f"Competitor {i} Product")
        price = st.number_input(f"Competitor {i} Price ($)", min_value=0.0, value=100.0, step=1.0)
        oz = st.number_input(f"Competitor {i} OZ", min_value=0.1, value=5.0)
        if product:
            competitors.append({"Brand": brand, "Product": product, "Price": price, "OZ": oz, "$/OZ": price / oz})

    if competitors:
        st.markdown("**Competitive Set Comparison ($/OZ):**")
        st.dataframe(pd.DataFrame(competitors))

# Capital Requirements
st.header("💰 Capital Requirements")
unit_order_qty = st.number_input("Total Units Ordered", min_value=1, value=5000)
moq_costs = []
for i in range(1, 9):
    moq = st.number_input(f"MOQ{i}", min_value=0, value=0, step=100, key=f"moq{i}")
    cost = st.number_input(f"Cost{i} ($)", min_value=0.0, value=0.0, step=10.0, key=f"cost{i}")
    if moq:
        moq_costs.append(cost)

extra_costs = st.number_input("Unexpected Costs (e.g., freight, etc.)", min_value=0.0, value=1600.0)
leftover_inventory = st.number_input("Leftover Packaging Inventory ($)", min_value=0.0, value=3953.69)

capital_total = sum(moq_costs) + extra_costs
entire_spent = capital_total + leftover_inventory

st.markdown(f"**Total Capital Required (excl. leftover):** ${capital_total:.2f}")
st.markdown(f"**Entire Capital Spent (incl. leftover):** ${entire_spent:.2f}")

st.success("✅ Calculation Complete. Use this data for investor decks, pricing sheets, or cost planning.")

