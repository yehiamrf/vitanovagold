"""
Simple Order Handler for VitaNova
=================================
Handles order creation and retrieval with CSV storage
"""

import csv
import os
import random
import string
from datetime import datetime
from flask import Blueprint, request, jsonify

orders_bp = Blueprint('orders', __name__)

# CSV file path - same directory as this file
ORDERS_CSV = os.path.join(os.path.dirname(__file__), 'orders.csv')

def init_orders_csv():
    """Initialize orders CSV with headers if it doesn't exist"""
    if not os.path.exists(ORDERS_CSV):
        with open(ORDERS_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'order_id', 'customer_id', 'product', 'quantity', 
                'gold_price_gram', 'purchase_date', 'payment_type',
                'commission_type', 'commission_amount', 'tax_amount', 
                'total', 'whatsapp_number', 'emirate', 'city', 'address'
            ])
        print(f"✅ Created orders CSV: {ORDERS_CSV}")
    else:
        print(f"📁 Orders CSV exists: {ORDERS_CSV}")

# Initialize on import
init_orders_csv()


def generate_order_id():
    """Generate a unique 10-character order ID"""
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=10))


@orders_bp.route('/orders/create', methods=['POST', 'OPTIONS'])
def create_order():
    """Create a new order and save to CSV"""
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        return '', 200
    
    print("\n" + "="*50)
    print("📦 NEW ORDER REQUEST RECEIVED")
    print("="*50)
    
    try:
        # Get JSON data
        data = request.get_json()
        print(f"📥 Received data: {data}")
        
        if not data:
            print("❌ No JSON data received")
            return jsonify({'success': False, 'error': 'No data received'}), 400
        
        # Extract required fields with defaults
        customer_id = data.get('customer_id', '')
        items = data.get('items', [])
        gold_price = data.get('gold_price_gram', 0)
        commission_type = data.get('commission_type', 'fixed')
        whatsapp = data.get('whatsapp_number', '')
        emirate = data.get('emirate', '')
        city = data.get('city', '')
        address = data.get('address', '')
        payment_type = data.get('payment_type', 'Cash on Delivery')
        
        print(f"📋 Customer ID: {customer_id}")
        print(f"📋 Items: {items}")
        print(f"📋 Gold Price: {gold_price}")
        print(f"📋 WhatsApp: {whatsapp}")
        
        # Validate
        if not customer_id:
            print("❌ Missing customer_id")
            return jsonify({'success': False, 'error': 'Missing customer_id'}), 400
        
        if not items or len(items) == 0:
            print("❌ No items in order")
            return jsonify({'success': False, 'error': 'No items in order'}), 400
        
        if not gold_price or float(gold_price) <= 0:
            print("❌ Invalid gold price")
            return jsonify({'success': False, 'error': 'Invalid gold price'}), 400
        
        # Generate order ID
        order_id = generate_order_id()
        purchase_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        print(f"🆔 Generated Order ID: {order_id}")
        
        # Write to CSV
        rows_written = 0
        with open(ORDERS_CSV, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            for item in items:
                weight = float(item.get('weight', 0))
                quantity = int(item.get('quantity', 1))
                commission_per_unit = float(item.get('commission', 0))
                
                # Calculate totals
                gold_cost = float(gold_price) * weight * quantity
                commission_total = commission_per_unit * quantity
                tax_amount = gold_cost * 0.05  # 5% VAT
                total = gold_cost + tax_amount + commission_total
                
                row = [
                    order_id,
                    customer_id,
                    f"{weight}g Gold Commodity 24K",
                    quantity,
                    round(float(gold_price), 2),
                    purchase_date,
                    payment_type,
                    commission_type,
                    round(commission_total, 2),
                    round(tax_amount, 2),
                    round(total, 2),
                    whatsapp,
                    emirate,
                    city,
                    address
                ]
                
                writer.writerow(row)
                rows_written += 1
                print(f"✅ Wrote row: {weight}g x{quantity} = {total:.2f} AED")
        
        print(f"✅ ORDER {order_id} SAVED - {rows_written} rows written")
        print("="*50 + "\n")
        
        return jsonify({
            'success': True,
            'order_id': order_id,
            'items_count': rows_written,
            'message': 'Order created successfully'
        }), 201
        
    except Exception as e:
        print(f"❌ ERROR creating order: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500


@orders_bp.route('/orders/customer/<customer_id>', methods=['GET'])
def get_customer_orders(customer_id):
    """Get all orders for a customer"""
    print(f"\n📋 Fetching orders for customer: {customer_id}")
    
    try:
        if not os.path.exists(ORDERS_CSV):
            print("📁 No orders file exists")
            return jsonify({'orders': [], 'orders_count': 0})
        
        # Read all orders for this customer
        orders = {}
        
        with open(ORDERS_CSV, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('customer_id') == customer_id:
                    oid = row['order_id']
                    
                    if oid not in orders:
                        orders[oid] = {
                            'order_id': oid,
                            'purchase_date': row.get('purchase_date', ''),
                            'payment_type': row.get('payment_type', ''),
                            'whatsapp_number': row.get('whatsapp_number', ''),
                            'emirate': row.get('emirate', ''),
                            'city': row.get('city', ''),
                            'address': row.get('address', ''),
                            'items': [],
                            'total': 0
                        }
                    
                    # Add item
                    item_total = float(row.get('total', 0))
                    orders[oid]['items'].append({
                        'product': row.get('product', ''),
                        'quantity': int(row.get('quantity', 1)),
                        'gold_price_gram': float(row.get('gold_price_gram', 0)),
                        'commission_type': row.get('commission_type', ''),
                        'commission_amount': float(row.get('commission_amount', 0)),
                        'tax_amount': float(row.get('tax_amount', 0)),
                        'total': item_total
                    })
                    orders[oid]['total'] += item_total
        
        # Convert to list and sort by date (newest first)
        orders_list = list(orders.values())
        orders_list.sort(key=lambda x: x['purchase_date'], reverse=True)
        
        print(f"📦 Found {len(orders_list)} orders for customer {customer_id}")
        
        return jsonify({
            'customer_id': customer_id,
            'orders_count': len(orders_list),
            'orders': orders_list
        })
        
    except Exception as e:
        print(f"❌ ERROR fetching orders: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


def init_orders(app):
    """Initialize orders blueprint"""
    app.register_blueprint(orders_bp)
    print("✅ Orders handler initialized")
