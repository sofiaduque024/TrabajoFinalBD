-- CREACIÓN DE TABLAS Y CONSTRAINTS
CREATE TABLE public.categorias (
  id_categoria integer NOT NULL DEFAULT nextval('categorias_id_categoria_seq'::regclass),
  tipo_categoria text NOT NULL,
  CONSTRAINT categorias_pkey PRIMARY KEY (id_categoria)
);

CREATE TABLE public.clientes (
  id_cliente integer NOT NULL DEFAULT nextval('clientes_id_cliente_seq'::regclass),
  nombre_cliente text NOT NULL,
  telefono_cliente character varying UNIQUE CHECK (length(telefono_cliente::text) = 10),
  ciudad_cliente text,
  CONSTRAINT clientes_pkey PRIMARY KEY (id_cliente)
);

CREATE TABLE public.tiendas (
  id_tienda integer NOT NULL DEFAULT nextval('tiendas_id_tienda_seq'::regclass),
  nombre_tienda text NOT NULL,
  ciudad_tienda text NOT NULL,
  telefono_tienda character varying NOT NULL UNIQUE,
  CONSTRAINT tiendas_pkey PRIMARY KEY (id_tienda)
);

CREATE TABLE public.productos (
  id_producto integer NOT NULL DEFAULT nextval('productos_id_producto_seq'::regclass),
  nombre_producto text NOT NULL,
  precio_producto numeric NOT NULL CHECK (precio_producto > 0::numeric),
  stock integer DEFAULT 0 CHECK (stock >= 0),
  id_categoria integer NOT NULL,
  CONSTRAINT productos_pkey PRIMARY KEY (id_producto),
  CONSTRAINT productos_id_categoria_fkey FOREIGN KEY (id_categoria) REFERENCES public.categorias(id_categoria)
);

CREATE TABLE public.ordenes (
  id_orden integer NOT NULL DEFAULT nextval('ordenes_id_orden_seq'::regclass),
  estado_orden text NOT NULL DEFAULT 'Pendiente'::text CHECK (estado_orden = ANY (ARRAY['Pendiente'::text, 'Procesando'::text, 'Enviado'::text, 'Entregado'::text, 'Cancelado'::text])),
  fecha_orden date NOT NULL DEFAULT CURRENT_DATE,
  fecha_envio date,
  id_cliente integer NOT NULL,
  id_tienda integer NOT NULL,
  CONSTRAINT ordenes_pkey PRIMARY KEY (id_orden),
  CONSTRAINT ordenes_id_cliente_fkey FOREIGN KEY (id_cliente) REFERENCES public.clientes(id_cliente),
  CONSTRAINT ordenes_id_tienda_fkey FOREIGN KEY (id_tienda) REFERENCES public.tiendas(id_tienda)
);

CREATE TABLE public.detalle_ordenes (
  id_detalle integer NOT NULL DEFAULT nextval('detalle_ordenes_id_detalle_seq'::regclass),
  id_orden integer NOT NULL,
  id_producto integer NOT NULL,
  cantidad_compra integer NOT NULL CHECK (cantidad_compra > 0),
  precio_unitario numeric NOT NULL CHECK (precio_unitario > 0::numeric),
  CONSTRAINT detalle_ordenes_pkey PRIMARY KEY (id_detalle),
  CONSTRAINT detalle_ordenes_id_orden_fkey FOREIGN KEY (id_orden) REFERENCES public.ordenes(id_orden),
  CONSTRAINT detalle_ordenes_id_producto_fkey FOREIGN KEY (id_producto) REFERENCES public.productos(id_producto)
);

--  ÍNDICES
CREATE INDEX IF NOT EXISTS idx_ordenes_fecha_orden
    ON public.ordenes (fecha_orden);

CREATE INDEX IF NOT EXISTS idx_ordenes_estado_orden
    ON public.ordenes (estado_orden);

CREATE INDEX IF NOT EXISTS idx_productos_id_categoria
    ON public.productos (id_categoria);

CREATE INDEX IF NOT EXISTS idx_productos_precio
    ON public.productos (precio_producto);

CREATE INDEX IF NOT EXISTS idx_detalle_ordenes_id_orden
    ON public.detalle_ordenes (id_orden);

CREATE INDEX IF NOT EXISTS idx_detalle_ordenes_id_producto
    ON public.detalle_ordenes (id_producto);

CREATE INDEX IF NOT EXISTS idx_clientes_nombre
    ON public.clientes (nombre_cliente);

CREATE INDEX IF NOT EXISTS idx_clientes_ciudad
    ON public.clientes (ciudad_cliente);

CREATE INDEX IF NOT EXISTS idx_tiendas_ciudad
    ON public.tiendas (ciudad_tienda);

CREATE INDEX IF NOT EXISTS idx_tiendas_nombre
    ON public.tiendas (nombre_tienda);

CREATE INDEX IF NOT EXISTS idx_categorias_tipo
    ON public.categorias (tipo_categoria);


-- PROCEDIMIENTOS ALMACENADOS
CREATE PROCEDURE public.crear_orden(
    p_id_cliente  INTEGER,
    p_id_tienda   INTEGER,
    p_id_producto INTEGER,
    p_cantidad    INTEGER
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_id_orden        INTEGER;
    v_precio_unitario NUMERIC;
BEGIN
    SELECT precio_producto
      INTO v_precio_unitario
      FROM public.productos
     WHERE id_producto = p_id_producto;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'El producto con id % no existe.', p_id_producto;
    END IF;

    INSERT INTO public.ordenes (id_cliente, id_tienda)
    VALUES (p_id_cliente, p_id_tienda)
    RETURNING id_orden INTO v_id_orden;

    INSERT INTO public.detalle_ordenes (id_orden, id_producto, cantidad_compra, precio_unitario)
    VALUES (v_id_orden, p_id_producto, p_cantidad, v_precio_unitario);

    UPDATE public.productos
       SET stock = stock - p_cantidad
     WHERE id_producto = p_id_producto;

    RAISE NOTICE 'Orden % creada correctamente para el cliente %.', v_id_orden, p_id_cliente;
END;
$$;


CREATE PROCEDURE public.actualizar_estado_orden(
    p_id_orden     INTEGER,
    p_nuevo_estado TEXT
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_estado_actual TEXT;
BEGIN
    SELECT estado_orden
      INTO v_estado_actual
      FROM public.ordenes
     WHERE id_orden = p_id_orden;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'La orden con id % no existe.', p_id_orden;
    END IF;

    IF v_estado_actual = 'Cancelado' THEN
        RAISE EXCEPTION 'La orden % ya está cancelada y no puede modificarse.', p_id_orden;
    END IF;

    IF v_estado_actual = 'Entregado' AND p_nuevo_estado <> 'Cancelado' THEN
        RAISE EXCEPTION 'La orden % ya fue entregada. Solo puede cancelarse.', p_id_orden;
    END IF;

    UPDATE public.ordenes
       SET estado_orden = p_nuevo_estado,
           fecha_envio  = CASE
                            WHEN p_nuevo_estado = 'Enviado' THEN CURRENT_DATE
                            ELSE fecha_envio
                          END
     WHERE id_orden = p_id_orden;

    RAISE NOTICE 'Orden % actualizada de "%" a "%".', p_id_orden, v_estado_actual, p_nuevo_estado;
END;
$$;


--  TRIGGERS
CREATE FUNCTION public.fn_restaurar_stock_orden_cancelada()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    IF NEW.estado_orden = 'Cancelado' AND OLD.estado_orden <> 'Cancelado' THEN
        UPDATE public.productos p
           SET stock = p.stock + d.cantidad_compra
          FROM public.detalle_ordenes d
         WHERE d.id_orden = NEW.id_orden
           AND d.id_producto = p.id_producto;

        RAISE NOTICE 'Stock restaurado por cancelación de la orden %.', NEW.id_orden;
    END IF;

    RETURN NEW;
END;
$$;

CREATE FUNCTION public.fn_validar_stock_antes_detalle()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    IF (SELECT stock FROM public.productos WHERE id_producto = NEW.id_producto) < NEW.cantidad_compra THEN
        RAISE EXCEPTION 'Stock insuficiente para el producto %.', NEW.id_producto;
    END IF;
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_restaurar_stock_orden_cancelada ON public.ordenes;

CREATE TRIGGER trg_restaurar_stock_orden_cancelada
AFTER UPDATE OF estado_orden ON public.ordenes
FOR EACH ROW
EXECUTE FUNCTION public.fn_restaurar_stock_orden_cancelada();

DROP TRIGGER IF EXISTS trg_validar_stock_antes_detalle ON public.detalle_ordenes;

CREATE TRIGGER trg_validar_stock_antes_detalle
BEFORE INSERT ON public.detalle_ordenes
FOR EACH ROW
EXECUTE FUNCTION public.fn_validar_stock_antes_detalle();
