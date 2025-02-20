import sys
from mongo import connect_mongodb
from redis_db import connect_redis
from users import create_user, get_user_by_id, create_producto, get_producto_by_id, update_producto, delete_producto, create_categoria, update_categoria_automatica, login, logout, get_session
from cart import add_to_cart, get_cart, clear_cart
from catalogo import create_product, update_price, get_product_price
from cassandra_db import connect_cassandra

def main():
    # Conexión a MongoDB y Redis (una sola vez)
    try:
        db = connect_mongodb()
    except Exception as e:
        print(f"Error conectando a MongoDB: {e}")
        sys.exit(1)
    try:
        redis_client = connect_redis()
    except Exception as e:
        print(f"Error conectando a Redis: {e}")
        sys.exit(1)
    try:
        cassandra_client = connect_cassandra()
    except Exception as e:
        print(f"Error conectando a Cassandra: {e}")
        sys.exit(1)
    
    
    while True:
        print("\n===== MENÚ PRINCIPAL =====")
        print("1. Crear usuario")
        print("2. Obtener usuario por ID")
        print("3. Crear producto")
        print("4. Obtener producto")
        print("5. Actualizar producto")
        print("6. Eliminar producto")
        print("7. Agregar producto al carrito")
        print("8. Ver carrito de compras")
        print("9. Vaciar carrito")
        print("10. Asignar categoría de usuario")
        print("11. Actualizar categoría automáticamente")
        print("12. Iniciar sesión")
        print("13. Cerrar sesión")
        print("14. Ver sesión activa")
        print("15. Crear producto")
        print("16. Actualizar precio de producto")
        print("17. Obtener precio de producto")
        print("0. Salir")
        
        try:
            opcion = int(input("Selecciona una opción: "))
        except ValueError:
            print("Por favor, ingresa un número válido.")
            continue
        
        if opcion == 1:
            email = input("Email: ")
            password = input("Contraseña: ")
            user_id = input("ID del usuario: ")
            cantidad_compras = int(input("Cantidad de compras: "))
            create_user(email, password, user_id, cantidad_compras)
            print("Usuario creado exitosamente.")
        
        elif opcion == 2:
            user_id = input("ID del usuario: ")
            user = get_user_by_id(user_id)
            print("Usuario encontrado:", user)
        
        elif opcion == 3:
            nombre = input("Nombre del producto: ")
            descripcion = input("Descripción: ")
            producto_id = input("ID del producto: ")
            create_producto(nombre, descripcion, producto_id)
            print("Producto creado exitosamente.")
        
        elif opcion == 4:
            producto_id = input("ID del producto: ")
            producto = get_producto_by_id(producto_id)
            print("Producto encontrado:", producto)
        
        elif opcion == 5:
            producto_id = input("ID del producto: ")
            nombre = input("Nuevo nombre: ")
            descripcion = input("Nueva descripción: ")
            update_producto(producto_id, nombre, descripcion)
            print("Producto actualizado.")
        
        elif opcion == 6:
            producto_id = input("ID del producto: ")
            delete_producto(producto_id)
            print("Producto eliminado.")
        
        elif opcion == 7:
            user_id = input("ID del usuario: ")
            product_id = input("ID del producto: ")
            quantity = int(input("Cantidad: "))
            add_to_cart(user_id, product_id, quantity)
            print("Producto agregado al carrito.")
        
        elif opcion == 8:
            user_id = input("ID del usuario: ")
            cart = get_cart(user_id)
            print("Carrito de compras:", cart)
        
        elif opcion == 9:
            user_id = input("ID del usuario: ")
            clear_cart(user_id)
            print("Carrito vaciado.")
        
        elif opcion == 10:
            user_id = input("ID del usuario: ")
            categoria = input("Categoría (LOW, MEDIUM, TOP): ")
            create_categoria(user_id, categoria)
            print("Categoría asignada.")
        
        elif opcion == 11:
            user_id = input("ID del usuario: ")
            update_categoria_automatica(user_id)
            print("Categoría actualizada según compras.")

        elif opcion == 12:
            user_id = input("ID del usuario: ")
            password = input("Contraseña: ")
            login(user_id, password)
            print("Sesión iniciada.")
        
        elif opcion == 13:
            user_id = input("ID del usuario: ")
            logout(user_id)
            print("Sesión cerrada.")
        
        elif opcion == 14:
            user_id = input("ID del usuario: ")
            session = get_session(user_id)
            print("Sesión activa:", session)
        
        elif opcion == 15:
            nombre = input("Nombre del producto: ")
            descripcion = input("Descripción: ")
            producto_id = input("ID del producto: ")
            create_product(nombre, descripcion, producto_id)
            print("Producto creado exitosamente.")
        
        elif opcion == 16:
            producto_id = input("ID del producto: ")
            precio = float(input("Nuevo precio: "))
            update_price(producto_id, precio)
            print("Precio actualizado.")
        
        elif opcion == 17:
            producto_id = input("ID del producto: ")
            user_id = input("ID del usuario: ")
            precio = get_product_price(user_id,producto_id)
            print("Precio del producto:", precio)
    
        elif opcion == 0:
            print("Saliendo del sistema...")
            print("Cerrando conexiones...")
            
            
            print("Cerrando conexiones...")
            db.client.close()
            sys.exit()
        else:
            print("Opción no válida. Intenta nuevamente.")

if __name__ == "__main__":
    main()
