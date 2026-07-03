# products/context_processors.py

from .cart import Cart

def cart(request):
    """Make cart available to all templates"""
    # Check if session exists before creating cart
    if hasattr(request, 'session'):
        return {
            'cart': Cart(request)
        }
    # If no session, return empty cart
    return {
        'cart': None
    }