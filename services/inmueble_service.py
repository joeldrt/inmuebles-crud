from typing import List

import datetime

from data.inmuebles import Inmueble
from data.direcciones import Direccion


def create_inmueble(nombre: str,
                    m2_terreno: float,
                    m2_construccion: float,
                    niveles: int,
                    recamaras: int,
                    banos: float,
                    cajones_estacionamiento: int,
                    amenidades: str,
                    descripccion: str,
                    precio_venta: float,
                    precio_renta: float,
                    calle: str,
                    num_exterior: str,
                    num_interior: str,
                    colonia: str,
                    municipio: str,
                    estado: str,
                    pais: str) -> Inmueble:
    inmueble = Inmueble()
    inmueble.fecha_registro = datetime.datetime.now()
    inmueble.nombre = nombre
    inmueble.m2_terreno = m2_terreno
    inmueble.m2_construccion = m2_construccion
    inmueble.niveles = niveles
    inmueble.recamaras = recamaras
    inmueble.banos = banos
    inmueble.cajones_estacionamiento = cajones_estacionamiento
    inmueble.amenidades = amenidades
    inmueble.descripcion = descripccion
    inmueble.precio_venta = precio_venta
    inmueble.precio_renta = precio_renta

    direccion = Direccion()
    direccion.calle = calle
    direccion.num_exterior = num_exterior
    direccion.num_interior = num_interior
    direccion.colonia = colonia
    direccion.municipio = municipio
    direccion.estado = estado
    direccion.pais = pais

    inmueble.direccion = direccion

    inmueble.save()

    return inmueble


def get_all_inmuebles() -> List[Inmueble]:
    inmuebles = [
        inmueble.to_dict()
        for inmueble in Inmueble.objects().all()
    ]
    return inmuebles
