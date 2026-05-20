-- CREACIÓN DE TABLAS Y CONSTRAINTS:
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
CREATE TABLE public.productos (
  id_producto integer NOT NULL DEFAULT nextval('productos_id_producto_seq'::regclass),
  nombre_producto text NOT NULL,
  precio_producto numeric NOT NULL CHECK (precio_producto > 0::numeric),
  stock integer DEFAULT 0 CHECK (stock >= 0),
  id_categoria integer NOT NULL,
  CONSTRAINT productos_pkey PRIMARY KEY (id_producto),
  CONSTRAINT productos_id_categoria_fkey FOREIGN KEY (id_categoria) REFERENCES public.categorias(id_categoria)
);
CREATE TABLE public.tiendas (
  id_tienda integer NOT NULL DEFAULT nextval('tiendas_id_tienda_seq'::regclass),
  nombre_tienda text NOT NULL,
  ciudad_tienda text NOT NULL,
  telefono_tienda character varying NOT NULL UNIQUE,
  CONSTRAINT tiendas_pkey PRIMARY KEY (id_tienda)
);


