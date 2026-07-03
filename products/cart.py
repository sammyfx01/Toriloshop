from decimal import Decimal

class Cart:
    """
    A simple cart system using Django sessions
    """
    
    def __init__(self, request):
        """Initialize the cart from session"""
        self.session = request.session
        cart = self.session.get('cart')
        
        if not cart:
            cart = self.session['cart'] = {}
        
        self.cart = cart
    
    def add(self, product_id, quantity=1):
        """Add a product to the cart or update its quantity"""
        product_id = str(product_id)
        
        if product_id in self.cart:
            self.cart[product_id] += quantity
        else:
            self.cart[product_id] = quantity
        
        self.save()
    
    def remove(self, product_id):
        """Remove a product from the cart"""
        product_id = str(product_id)
        
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    
    def update(self, product_id, quantity):
        """Update the quantity of a product"""
        product_id = str(product_id)
        
        if quantity <= 0:
            self.remove(product_id)
        else:
            self.cart[product_id] = quantity
            self.save()
    
    def clear(self):
        """Clear the entire cart"""
        self.session['cart'] = {}
        self.save()
    
    def save(self):
        """Save cart to session"""
        self.session.modified = True
    
    def __len__(self):
        """Get total number of items in cart"""
        return sum(int(q) for q in self.cart.values())
    
    def get_total(self):
        """Get total price of all items in cart"""
        from .models import Product
        total = Decimal('0.00')
        
        for product_id, quantity in self.cart.items():
            try:
                product = Product.objects.get(id=int(product_id))
                total += product.price * Decimal(str(quantity))
            except Product.DoesNotExist:
                pass
        
        return total
    
    def get_items(self, product_model):
        """Get product objects from cart with quantities"""
        items = []
        total_price = Decimal('0.00')
        
        for product_id, quantity in self.cart.items():
            try:
                product = product_model.objects.get(id=int(product_id))
                subtotal = product.price * Decimal(str(quantity))
                items.append({
                    'product': product,
                    'quantity': quantity,
                    'subtotal': subtotal
                })
                total_price += subtotal
            except product_model.DoesNotExist:
                self.remove(product_id)
        
        return {
            'items': items,
            'total': total_price,
            'count': len(self)
        }
    
    # ===== COUPON METHODS =====
    
    def apply_coupon(self, coupon_code):
        """Apply a coupon to the cart"""
        from .models import Coupon
        from django.utils import timezone
        
        try:
            coupon = Coupon.objects.get(code=coupon_code.upper(), active=True)
            now = timezone.now()
            
            if not (coupon.valid_from <= now <= coupon.valid_to):
                return {'valid': False, 'message': 'Coupon has expired'}
            
            if coupon.used_count >= coupon.usage_limit:
                return {'valid': False, 'message': 'Coupon usage limit reached'}
            
            # Get cart total
            cart_total = self.get_total()
            
            if cart_total < coupon.minimum_order:
                return {'valid': False, 'message': f'Minimum order of Naira {coupon.minimum_order} required'}
            
            # Calculate discount
            discount = coupon.calculate_discount(cart_total)
            
            return {
                'valid': True,
                'coupon': coupon,
                'discount': discount,
                'new_total': cart_total - discount,
                'message': f'Coupon applied! You saved Naira {discount}'
            }
        except Coupon.DoesNotExist:
            return {'valid': False, 'message': 'Invalid coupon code'}
    
    def remove_coupon(self):
        """Remove coupon from cart"""
        if 'coupon_code' in self.session:
            del self.session['coupon_code']
            self.save()