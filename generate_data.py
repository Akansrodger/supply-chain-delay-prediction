import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from faker import Faker
import random
import sqlite3

fake = Faker()
np.random.seed(42)
random.seed(42)

print("🏭 Generating IMPROVED GZ Industries Supply Chain Data...\n")

# ==================== 1. SUPPLIERS DATA ====================
print("📊 Step 1: Creating Suppliers with Realistic Characteristics...")

suppliers_data = {
    'supplier_id': [f'SUP-{str(i).zfill(3)}' for i in range(1, 16)],
    'supplier_name': [
        'Alcoa Nigeria Ltd', 'Hydro Aluminum West Africa', 'Rio Tinto Metals',
        'Norsk Aluminum Supply', 'Emirates Global Aluminium', 'Hindalco West Africa',
        'Chalco International', 'Vedanta Aluminium', 'Century Aluminum Trading',
        'Kaiser Aluminum Lagos', 'Novelis Africa', 'Constellium Supply Chain',
        'Arconic Nigeria', 'Aleris West Africa', 'Logan Aluminum Co'
    ],
    'country': [
        'Nigeria', 'Nigeria', 'South Africa', 'Norway', 'UAE', 'Nigeria',
        'China', 'India', 'USA', 'Nigeria', 'South Africa', 'France',
        'Nigeria', 'Nigeria', 'USA'
    ],
    'distance_km': [
        120, 85, 850, 6500, 4200, 95,
        9800, 7200, 8900, 140, 920, 5100,
        110, 105, 8600
    ],
    'payment_terms_days': [30, 30, 45, 60, 60, 30, 90, 60, 90, 30, 45, 60, 30, 30, 90],
    'sustainability_certified': [True, True, True, False, True, False, False, True, False, True, True, False, True, False, False]
}

# Assign tiers based on distance and country
tiers = []
for i, country in enumerate(suppliers_data['country']):
    distance = suppliers_data['distance_km'][i]
    if country == 'Nigeria' and distance < 200:
        tiers.append('Tier 1')  # Local, reliable
    elif distance < 1000:
        tiers.append('Tier 1')
    elif distance < 5000:
        tiers.append('Tier 2')
    else:
        tiers.append('Tier 3')  # Far away, risky

suppliers_data['supplier_tier'] = tiers

# Base reliability scores (higher = more reliable)
reliability_scores = []
for tier, cert in zip(suppliers_data['supplier_tier'], suppliers_data['sustainability_certified']):
    if tier == 'Tier 1':
        base = 0.85  # 85% reliable
    elif tier == 'Tier 2':
        base = 0.70  # 70% reliable
    else:
        base = 0.55  # 55% reliable
    
    # Certification adds +5% reliability
    if cert:
        base += 0.05
    
    reliability_scores.append(base)

suppliers_data['base_reliability'] = reliability_scores

df_suppliers = pd.DataFrame(suppliers_data)
print(f"✅ Created {len(df_suppliers)} suppliers with realistic characteristics")

# ==================== 2. DELIVERIES DATA (MORE REALISTIC) ====================
print("📊 Step 2: Creating Realistic Delivery Records...")

num_deliveries = 500
start_date = datetime.now() - timedelta(days=365)

deliveries_data = []

for i in range(num_deliveries):
    supplier_id = random.choice(df_suppliers['supplier_id'].tolist())
    supplier = df_suppliers[df_suppliers['supplier_id'] == supplier_id].iloc[0]
    
    # Order date
    order_date = start_date + timedelta(days=random.randint(0, 365))
    
    # Expected lead time based ONLY on distance (what we know at order time)
    base_lead_time = 3 + (supplier['distance_km'] / 500)
    expected_lead_time = int(base_lead_time)
    expected_delivery = order_date + timedelta(days=expected_lead_time)
    
    # REALISTIC DELAY FACTORS (things that actually cause delays)
    
    # Factor 1: Supplier reliability (intrinsic quality)
    supplier_reliability = supplier['base_reliability']
    
    # Factor 2: Order size matters (larger orders = more complexity)
    quantity_mt = round(random.uniform(10, 100), 2)
    size_factor = 0.95 if quantity_mt < 30 else 0.85 if quantity_mt < 60 else 0.75
    
    # Factor 3: Distance (longer = more things can go wrong)
    distance_factor = 0.95 if supplier['distance_km'] < 500 else 0.85 if supplier['distance_km'] < 2000 else 0.70
    
    # Factor 4: Payment terms (longer terms = less priority from supplier)
    payment_factor = 0.95 if supplier['payment_terms_days'] <= 30 else 0.90 if supplier['payment_terms_days'] <= 60 else 0.80
    
    # Factor 5: Seasonality (Q4 is busier, more delays)
    month = order_date.month
    seasonal_factor = 0.85 if month in [11, 12] else 0.95 if month in [1, 2] else 1.0
    
    # Factor 6: Random events (supply chain disruptions)
    random_event = random.random()
    event_factor = 0.50 if random_event < 0.05 else 1.0  # 5% chance of major disruption
    
    # COMBINED PROBABILITY of on-time delivery
    on_time_probability = (
        supplier_reliability * 
        size_factor * 
        distance_factor * 
        payment_factor * 
        seasonal_factor * 
        event_factor
    )
    
    # Determine if delayed
    is_on_time = random.random() < on_time_probability
    
    if is_on_time:
        actual_delay_days = random.randint(-2, 0)  # Early or exactly on time
    else:
        # Delay severity depends on what went wrong
        if event_factor < 1.0:
            actual_delay_days = random.randint(7, 20)  # Major disruption
        elif distance_factor < 0.8:
            actual_delay_days = random.randint(4, 10)  # Long distance issues
        else:
            actual_delay_days = random.randint(1, 5)  # Minor delay
    
    actual_delivery = expected_delivery + timedelta(days=actual_delay_days)
    
    # Quality (correlated with supplier reliability)
    base_defect_rate = (1 - supplier_reliability) * 0.05  # Max 5%
    defect_rate = max(0, base_defect_rate + random.uniform(-0.01, 0.01))
    
    # Price (with market volatility)
    base_price = 2500
    price_volatility = random.uniform(-200, 200)
    unit_price = round(base_price + price_volatility, 2)
    
    # Destination (realistic distribution)
    weights = [0.5, 0.3, 0.2]  # Agbara gets most deliveries
    destination = random.choices(['Agbara', 'Aba', 'Wadeville'], weights=weights)[0]
    
    deliveries_data.append({
        'delivery_id': f'DEL-{str(i+1).zfill(4)}',
        'supplier_id': supplier_id,
        'order_date': order_date.strftime('%Y-%m-%d'),
        'expected_delivery_date': expected_delivery.strftime('%Y-%m-%d'),
        'actual_delivery_date': actual_delivery.strftime('%Y-%m-%d'),
        'quantity_mt': quantity_mt,
        'unit_price_usd': unit_price,
        'total_value_usd': round(quantity_mt * unit_price, 2),
        'defect_rate': round(defect_rate, 4),
        'quality_grade': 'A' if defect_rate < 0.02 else 'B' if defect_rate < 0.04 else 'C',
        'on_time': 'Yes' if actual_delay_days <= 0 else 'No',
        'delay_days': max(0, actual_delay_days),
        'destination': destination,
        # Store factors for analysis (but won't use in model)
        'order_month': order_date.month,
        'order_quarter': (order_date.month - 1) // 3 + 1
    })

df_deliveries = pd.DataFrame(deliveries_data)
print(f"✅ Created {len(df_deliveries)} realistic delivery records")

# ==================== 3. REST OF DATA (KEEP SAME) ====================
print("📊 Step 3: Creating Inventory Levels...")

inventory_data = []
dates = pd.date_range(end=datetime.now(), periods=90, freq='D')

for date in dates:
    for location in ['Agbara', 'Aba', 'Wadeville']:
        base_level = {'Agbara': 500, 'Aba': 300, 'Wadeville': 400}[location]
        current_level = base_level + random.randint(-100, 100)
        
        inventory_data.append({
            'date': date.strftime('%Y-%m-%d'),
            'location': location,
            'aluminum_stock_mt': max(0, current_level),
            'reorder_point_mt': base_level * 0.3,
            'max_capacity_mt': base_level * 1.5,
            'days_of_supply': round(current_level / (base_level * 0.05), 1)
        })

df_inventory = pd.DataFrame(inventory_data)
print(f"✅ Created {len(df_inventory)} inventory snapshots")

# ==================== 4. SUPPLIER PERFORMANCE ====================
print("📊 Step 4: Calculating Supplier Performance Metrics...")

supplier_performance = df_deliveries.groupby('supplier_id').agg({
    'delivery_id': 'count',
    'on_time': lambda x: (x == 'Yes').sum() / len(x) * 100,
    'delay_days': 'mean',
    'defect_rate': 'mean',
    'total_value_usd': 'sum',
    'quality_grade': lambda x: (x == 'A').sum() / len(x) * 100
}).reset_index()

supplier_performance.columns = [
    'supplier_id', 'total_deliveries', 'on_time_rate_%',
    'avg_delay_days', 'avg_defect_rate', 'total_spend_usd', 'grade_a_rate_%'
]

df_performance = supplier_performance.merge(df_suppliers, on='supplier_id')

df_performance['performance_score'] = (
    df_performance['on_time_rate_%'] * 0.4 +
    df_performance['grade_a_rate_%'] * 0.3 +
    (100 - df_performance['avg_defect_rate'] * 2000) * 0.2 +
    (100 - df_performance['avg_delay_days'] * 10).clip(0, 100) * 0.1
).round(2)

df_performance['risk_level'] = pd.cut(
    df_performance['performance_score'],
    bins=[0, 60, 75, 100],
    labels=['High Risk', 'Medium Risk', 'Low Risk']
)

print(f"✅ Calculated performance metrics for {len(df_performance)} suppliers")

# ==================== 5. SAVE DATA ====================
print("\n💾 Saving Data Files...\n")

df_suppliers.to_csv('data/suppliers.csv', index=False)
df_deliveries.to_csv('data/deliveries.csv', index=False)
df_inventory.to_csv('data/inventory.csv', index=False)
df_performance.to_csv('data/supplier_performance.csv', index=False)

print("✅ Saved CSV files")

# ==================== 6. CREATE DATABASE ====================
print("\n🗄️ Creating SQLite Database...\n")

conn = sqlite3.connect('data/gzi_supply_chain.db')

df_suppliers.to_sql('suppliers', conn, if_exists='replace', index=False)
df_deliveries.to_sql('deliveries', conn, if_exists='replace', index=False)
df_inventory.to_sql('inventory', conn, if_exists='replace', index=False)
df_performance.to_sql('supplier_performance', conn, if_exists='replace', index=False)

conn.close()

print("✅ Created database: data/gzi_supply_chain.db")

# ==================== 7. SUMMARY ====================
print("\n" + "="*60)
print("📈 IMPROVED DATA GENERATION SUMMARY")
print("="*60)
print(f"Suppliers: {len(df_suppliers)}")
print(f"Deliveries: {len(df_deliveries)}")
print(f"Date Range: {df_deliveries['order_date'].min()} to {df_deliveries['order_date'].max()}")
print(f"Total Spend: ${df_deliveries['total_value_usd'].sum():,.2f}")
print(f"Average On-Time Rate: {(df_deliveries['on_time'] == 'Yes').sum() / len(df_deliveries) * 100:.1f}%")
print(f"\n🔍 DATA QUALITY CHECKS:")
print(f"  Tier 1 suppliers: {(df_suppliers['supplier_tier'] == 'Tier 1').sum()}")
print(f"  Tier 2 suppliers: {(df_suppliers['supplier_tier'] == 'Tier 2').sum()}")
print(f"  Tier 3 suppliers: {(df_suppliers['supplier_tier'] == 'Tier 3').sum()}")
print(f"  Q4 deliveries (busier): {(df_deliveries['order_quarter'] == 4).sum()}")
print("="*60)
print("\n✨ REALISTIC data generation complete!\n")