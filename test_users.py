from users import (
    create_user, get_user_by_id, create_categoria, 
    get_categoria_by_user_id, create_producto, get_producto_by_id, 
    update_producto, update_categoria_automatica, delete_producto
)

# Crear usuario
create_user("juan@example.com", "password123", 1, 5)

# Obtener usuario
print(get_user_by_id(1))

# Categorizar usuario
create_categoria(1, "TOP")
update_categoria_automatica(1)
print(get_categoria_by_user_id(1))

# Crear producto
create_producto("Producto A", "Descripción del producto A", 101)

# Obtener y modificar producto
print(get_producto_by_id(101))
update_producto(101, nombre="Producto A Modificado", descripcion="Descripción modificada del producto A")
print(get_producto_by_id(101))

# Eliminar producto
delete_producto(101)
