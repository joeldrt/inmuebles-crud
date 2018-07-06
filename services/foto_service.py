from typing import List

import datetime

from data.fotos import Foto


def persist_foto(nombre: str,
                 data_base_64: str,
                 content_type: str,
                 inmueble_id: str) -> str:
    foto = Foto()
    foto.fecha_carga = datetime.datetime.now()
    foto.nombre = nombre
    foto.data_base_64 = data_base_64
    foto.content_type = content_type
    foto.inmueble_id = inmueble_id

    foto.save()

    return str(foto.id)


def get_all_fotos() -> List[Foto]:
    fotos = [
        foto.to_dict()
        for foto in Foto.objects().all()
    ]
    return fotos


def get_foto_by_id(foto_id: str) -> Foto:
    foto = Foto.objects().get(id=foto_id)
    return foto


def get_fotos_by_inmueble_id(inmueble_id: str) -> List[Foto]:
    fotos = [
        foto.to_dict()
        for foto in Foto.objects(inmueble_id=inmueble_id)
    ]
    return fotos
