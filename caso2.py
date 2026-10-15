from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from types import MappingProxyType
from typing import Mapping


def texto(valor, campo):
    if not isinstance(valor, str) or not valor.strip():
        raise ValueError(f"{campo} es obligatorio")
    return valor.strip()


@dataclass(frozen=True)
class ActivoFijo:
    codigo: str
    descripcion: str
    precio: Decimal
    marca: str | None = None
    modelo: str | None = None
    numero_serie: str | None = None
    ubicacion: str | None = None
    custodio: str | None = None
    fecha_adquisicion: date | None = None
    garantia_meses: int | None = None
    proveedor: str | None = None
    observaciones: str | None = None
    caracteristicas: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self):
        object.__setattr__(self, "codigo", texto(self.codigo, "Código"))
        object.__setattr__(self, "descripcion", texto(self.descripcion, "Descripción"))
        if not isinstance(self.precio, Decimal) or not self.precio.is_finite() or self.precio < 0:
            raise ValueError("Precio debe ser Decimal, finito y no negativo")
        for campo in ("marca", "modelo", "numero_serie", "ubicacion",
                      "custodio", "proveedor", "observaciones"):
            valor = getattr(self, campo)
            if valor is not None:
                object.__setattr__(self, campo, texto(valor, campo))
        if self.garantia_meses is not None:
            if type(self.garantia_meses) is not int or self.garantia_meses < 0:
                raise ValueError("Garantía debe ser un entero no negativo")
        if self.fecha_adquisicion is not None and not isinstance(self.fecha_adquisicion, date):
            raise ValueError("Fecha de adquisición inválida")
        copia = {texto(k, "Característica"): texto(v, "Valor")
                 for k, v in self.caracteristicas.items()}
        object.__setattr__(self, "caracteristicas", MappingProxyType(copia))


class ActivoFijoBuilder:
    def __init__(self, codigo: str, descripcion: str, precio: Decimal):
        # Valida los obligatorios desde el inicio.
        base = ActivoFijo(codigo, descripcion, precio)
        self._datos = dict(codigo=base.codigo, descripcion=base.descripcion, precio=base.precio)
        self._caracteristicas = {}

    def marca(self, valor):
        self._datos["marca"] = texto(valor, "Marca")
        return self

    def modelo(self, valor):
        self._datos["modelo"] = texto(valor, "Modelo")
        return self

    def numero_serie(self, valor):
        self._datos["numero_serie"] = texto(valor, "Serie")
        return self

    def ubicacion(self, valor):
        self._datos["ubicacion"] = texto(valor, "Ubicación")
        return self

    def custodio(self, valor):
        self._datos["custodio"] = texto(valor, "Custodio")
        return self

    def fecha_adquisicion(self, valor):
        self._datos["fecha_adquisicion"] = valor
        return self

    def garantia_meses(self, valor):
        self._datos["garantia_meses"] = valor
        return self

    def proveedor(self, valor):
        self._datos["proveedor"] = texto(valor, "Proveedor")
        return self

    def observaciones(self, valor):
        self._datos["observaciones"] = texto(valor, "Observaciones")
        return self

    def caracteristica(self, nombre, valor):
        self._caracteristicas[texto(nombre, "Característica")] = texto(valor, "Valor")
        return self

    def build(self) -> ActivoFijo:
        return ActivoFijo(**self._datos, caracteristicas=self._caracteristicas)


def main():
    computador = (ActivoFijoBuilder("AF001", "Computador", Decimal("1200.00"))
                  .marca("Dell").modelo("Latitude").numero_serie("SN001")
                  .ubicacion("Laboratorio").custodio("Ana Pérez")
                  .garantia_meses(36).caracteristica("Procesador", "Intel Core i7")
                  .build())
    mesa = (ActivoFijoBuilder("AF002", "Mesa", Decimal("180.00"))
            .ubicacion("Secretaría").custodio("Luis Torres")
            .caracteristica("Material", "Madera")
            .caracteristica("Dimensiones", "120 x 60 cm").build())
    for activo in (computador, mesa):
        print(f"{activo.codigo}: {activo.descripcion} | ${activo.precio:.2f}")
        print(f"Características: {dict(activo.caracteristicas)}")


if __name__ == "__main__":
    main()
