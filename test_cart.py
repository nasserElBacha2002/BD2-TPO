from cart import add_to_cart, get_cart, clear_cart

# Agregar productos al carrito
add_to_cart(1, 101, 2)
add_to_cart(1, 102, 1)

# Ver el carrito
print("🛒 Carrito del usuario 1:", get_cart(1))

# Vaciar el carrito
clear_cart(1)
print("🛒 Carrito después de vaciar:", get_cart(1))
