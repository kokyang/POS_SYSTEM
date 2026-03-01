from database import Database
from datetime import datetime

class Category:
    @staticmethod
    def get_all():
        db = Database()
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM categories')
        categories = cursor.fetchall()
        conn.close()
        return categories
    
    @staticmethod
    def add(name):
        db = Database()
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO categories (name) VALUES (?)', (name,))
        conn.commit()
        conn.close()
    
    @staticmethod
    def delete(category_id):
        db = Database()
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM categories WHERE id = ?', (category_id,))
        conn.commit()
        conn.close()

class Item:
    @staticmethod
    def get_all():
        db = Database()
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT items.id, items.name, categories.name, items.price, items.stock, items.image_url, items.barcode
            FROM items
            LEFT JOIN categories ON items.category_id = categories.id
        ''')
        items = cursor.fetchall()
        conn.close()
        return items

    @staticmethod
    def get_by_barcode(barcode):
        db = Database()
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT items.id, items.name, categories.name, items.price, items.stock, items.image_url, items.barcode
            FROM items
            LEFT JOIN categories ON items.category_id = categories.id
            WHERE items.barcode = ?
        ''', (barcode,))
        item = cursor.fetchone()
        conn.close()
        return item

    @staticmethod
    def search_by_name(query):
        db = Database()
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT items.id, items.name, categories.name, items.price, items.stock, items.image_url, items.barcode
            FROM items
            LEFT JOIN categories ON items.category_id = categories.id
            WHERE LOWER(items.name) LIKE ?
            LIMIT 10
        ''', (f'%{query.lower()}%',))
        items = cursor.fetchall()
        conn.close()
        return items
    
    @staticmethod
    def add(name, category_id, price, stock, image_url=None, barcode=None):
        db = Database()
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO items (name, category_id, price, stock, image_url, barcode) VALUES (?, ?, ?, ?, ?, ?)',
                      (name, category_id, price, stock, image_url, barcode))
        conn.commit()
        conn.close()

    @staticmethod
    def update(item_id, name, category_id, price, stock, image_url=None, barcode=None):
        db = Database()
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE items SET name=?, category_id=?, price=?, stock=?, image_url=?, barcode=? WHERE id=?',
                      (name, category_id, price, stock, image_url, barcode, item_id))
        conn.commit()
        conn.close()
    
    @staticmethod
    def delete(item_id):
        db = Database()
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM items WHERE id = ?', (item_id,))
        conn.commit()
        conn.close()
    
    @staticmethod
    def update_stock(item_id, quantity):
        db = Database()
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE items SET stock = stock + ? WHERE id = ?', (quantity, item_id))
        conn.commit()
        conn.close()

class Sale:
    @staticmethod
    def create_sale(items_list, total):
        db = Database()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        sale_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('INSERT INTO sales (sale_date, total_amount) VALUES (?, ?)',
                      (sale_date, total))
        sale_id = cursor.lastrowid
        
        for item in items_list:
            # 检查是否是手动输入的商品
            is_manual = item.get('isManual', False)
            
            if is_manual:
                # 手动输入的商品：item_id设为NULL，不扣库存
                cursor.execute('INSERT INTO sale_items (sale_id, item_id, quantity, price) VALUES (?, NULL, ?, ?)',
                              (sale_id, item['quantity'], item['price']))
            else:
                # 正常商品：记录item_id，扣库存
                cursor.execute('INSERT INTO sale_items (sale_id, item_id, quantity, price) VALUES (?, ?, ?, ?)',
                              (sale_id, item['id'], item['quantity'], item['price']))
                cursor.execute('UPDATE items SET stock = stock - ? WHERE id = ?',
                              (item['quantity'], item['id']))
        
        conn.commit()
        conn.close()
        return sale_id
    
    @staticmethod
    def get_monthly_revenue(year, month):
        db = Database()
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT SUM(total_amount) FROM sales
            WHERE strftime('%Y', sale_date) = ? AND strftime('%m', sale_date) = ?
        ''', (str(year), f'{month:02d}'))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result[0] else 0
    
    @staticmethod
    def get_all_sales():
        db = Database()
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, sale_date, total_amount FROM sales
            ORDER BY sale_date DESC
            LIMIT 100
        ''')
        sales = cursor.fetchall()
        conn.close()
        return sales
    
    @staticmethod
    def get_sale_details(sale_id):
        db = Database()
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT 
                CASE 
                    WHEN items.name IS NOT NULL THEN items.name
                    WHEN sale_items.item_id IS NULL THEN 'Item'
                    ELSE '已删除的商品'
                END as name,
                sale_items.quantity, 
                sale_items.price,
                (sale_items.quantity * sale_items.price) as subtotal
            FROM sale_items
            LEFT JOIN items ON sale_items.item_id = items.id
            WHERE sale_items.sale_id = ?
        ''', (sale_id,))
        details = cursor.fetchall()
        conn.close()
        return details
    
    @staticmethod
    def get_today_sales():
        db = Database()
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT COUNT(*), COALESCE(SUM(total_amount), 0) FROM sales
            WHERE DATE(sale_date) = DATE('now')
        ''')
        result = cursor.fetchone()
        conn.close()
        return {'count': result[0], 'total': result[1]}
    
    @staticmethod
    def get_top_selling_items(limit=10):
        db = Database()
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT items.name, SUM(sale_items.quantity) as total_qty, 
                   SUM(sale_items.quantity * sale_items.price) as total_revenue
            FROM sale_items
            JOIN items ON sale_items.item_id = items.id
            GROUP BY items.id
            ORDER BY total_qty DESC
            LIMIT ?
        ''', (limit,))
        items = cursor.fetchall()
        conn.close()
        return items
    
    @staticmethod
    def get_sales_by_date_range(start_date, end_date):
        db = Database()
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DATE(sale_date) as date, COUNT(*) as count, SUM(total_amount) as total
            FROM sales
            WHERE DATE(sale_date) BETWEEN ? AND ?
            GROUP BY DATE(sale_date)
            ORDER BY date DESC
        ''', (start_date, end_date))
        sales = cursor.fetchall()
        conn.close()
        return sales
    
    @staticmethod
    def get_daily_reconciliation():
        """获取今日对账数据"""
        db = Database()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # 获取今日交易汇总
        cursor.execute('''
            SELECT COUNT(*), COALESCE(SUM(total_amount), 0) FROM sales
            WHERE DATE(sale_date) = DATE('now')
        ''')
        count, total = cursor.fetchone()
        
        # 获取今日所有交易明细
        cursor.execute('''
            SELECT id, strftime('%H:%M:%S', sale_date) as time, total_amount
            FROM sales
            WHERE DATE(sale_date) = DATE('now')
            ORDER BY sale_date ASC
        ''')
        transactions = cursor.fetchall()
        
        conn.close()
        
        # 计算平均客单价
        avg_transaction = total / count if count > 0 else 0
        
        # 模拟支付方式分类（实际应该从数据库获取）
        # 这里简化处理，假设70%现金，20%银行卡，10%电子支付
        cash_total = total * 0.7
        card_total = total * 0.2
        digital_total = total * 0.1
        
        return {
            'transaction_count': count,
            'total_revenue': total,
            'avg_transaction': avg_transaction,
            'transactions': [
                {
                    'id': t[0],
                    'time': t[1],
                    'amount': t[2],
                    'payment_method': '现金'  # 简化处理
                }
                for t in transactions
            ],
            'cash_total': cash_total,
            'card_total': card_total,
            'digital_total': digital_total
        }
    
    @staticmethod
    def get_best_selling_analysis():
        """获取畅销商品分析数据"""
        db = Database()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # 获取所有商品销售统计
        cursor.execute('''
            SELECT items.name, SUM(sale_items.quantity) as total_qty, 
                   SUM(sale_items.quantity * sale_items.price) as total_revenue
            FROM sale_items
            JOIN items ON sale_items.item_id = items.id
            GROUP BY items.id
            ORDER BY total_qty DESC
            LIMIT 10
        ''')
        top_items = cursor.fetchall()
        
        # 获取总体统计
        cursor.execute('''
            SELECT COUNT(DISTINCT item_id), SUM(quantity), 
                   SUM(quantity * price)
            FROM sale_items
            WHERE item_id IS NOT NULL
        ''')
        total_items, total_quantity, total_revenue = cursor.fetchone()
        
        conn.close()
        
        # 计算TOP3占比
        top3_revenue = sum(item[2] for item in top_items[:3]) if len(top_items) >= 3 else 0
        top3_percentage = (top3_revenue / total_revenue * 100) if total_revenue > 0 else 0
        
        # 生成建议
        if top3_percentage > 60:
            recommendation = "TOP3商品占比超过60%，建议保持充足库存，可考虑增加促销活动。"
        elif top3_percentage > 40:
            recommendation = "销售较为集中，建议关注热销商品库存，同时推广其他商品。"
        else:
            recommendation = "销售分布较为均衡，建议继续保持多样化商品策略。"
        
        return {
            'period': '全部时间',
            'total_items': total_items or 0,
            'total_quantity': total_quantity or 0,
            'total_revenue': total_revenue or 0,
            'top_items': [
                {
                    'name': item[0],
                    'quantity': item[1],
                    'revenue': item[2]
                }
                for item in top_items
            ],
            'top3_percentage': top3_percentage,
            'recommendation': recommendation
        }
    
    @staticmethod
    def get_transactions_by_date(start_date, end_date):
        """获取指定日期范围的交易记录"""
        db = Database()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, sale_date, total_amount
            FROM sales
            WHERE DATE(sale_date) BETWEEN ? AND ?
            ORDER BY sale_date DESC
        ''', (start_date, end_date))
        transactions = cursor.fetchall()
        
        conn.close()
        return transactions
    
    @staticmethod
    def get_monthly_report(year, month):
        """获取月度报表数据"""
        db = Database()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # 获取月度汇总
        cursor.execute('''
            SELECT COUNT(*), COALESCE(SUM(total_amount), 0), 
                   COALESCE(AVG(total_amount), 0), COALESCE(MAX(total_amount), 0)
            FROM sales
            WHERE strftime('%Y', sale_date) = ? AND strftime('%m', sale_date) = ?
        ''', (str(year), f'{month:02d}'))
        count, total, avg, max_trans = cursor.fetchone()
        
        # 获取每日销售明细
        cursor.execute('''
            SELECT DATE(sale_date) as date, COUNT(*) as count, SUM(total_amount) as total
            FROM sales
            WHERE strftime('%Y', sale_date) = ? AND strftime('%m', sale_date) = ?
            GROUP BY DATE(sale_date)
            ORDER BY date ASC
        ''', (str(year), f'{month:02d}'))
        daily_sales = cursor.fetchall()
        
        conn.close()
        
        return {
            'transaction_count': count or 0,
            'total_revenue': total or 0,
            'avg_transaction': avg or 0,
            'max_transaction': max_trans or 0,
            'daily_sales': [
                {
                    'date': day[0],
                    'count': day[1],
                    'total': day[2]
                }
                for day in daily_sales
            ]
        }
    
    @staticmethod
    def get_sales_summary(start_date, end_date):
        """获取日期范围的销售汇总"""
        db = Database()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # 获取汇总数据
        cursor.execute('''
            SELECT COUNT(*), COALESCE(SUM(total_amount), 0), 
                   COALESCE(AVG(total_amount), 0), COALESCE(MAX(total_amount), 0)
            FROM sales
            WHERE DATE(sale_date) BETWEEN ? AND ?
        ''', (start_date, end_date))
        count, total, avg, max_trans = cursor.fetchone()
        
        # 获取每日销售明细
        cursor.execute('''
            SELECT DATE(sale_date) as date, COUNT(*) as count, 
                   SUM(total_amount) as total, AVG(total_amount) as avg
            FROM sales
            WHERE DATE(sale_date) BETWEEN ? AND ?
            GROUP BY DATE(sale_date)
            ORDER BY date ASC
        ''', (start_date, end_date))
        daily_sales = cursor.fetchall()
        
        conn.close()
        
        return {
            'transaction_count': count or 0,
            'total_revenue': total or 0,
            'avg_transaction': avg or 0,
            'max_transaction': max_trans or 0,
            'daily_sales': [
                {
                    'date': day[0],
                    'count': day[1],
                    'total': day[2],
                    'avg': day[3]
                }
                for day in daily_sales
            ]
        }

