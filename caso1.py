from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date
import argparse
import math


@dataclass(frozen=True)
class Vehiculo(ABC):
    placa: str
    marca: str
    modelo: str
    anio: int
    avaluo: float

    def __post_init__(self):
        for nombre in ("placa", "marca", "modelo"):
            if not isinstance(getattr(self, nombre), str) or not getattr(self, nombre).strip():
                raise ValueError(f"{nombre} es obligatorio")
        if not 1 <= self.anio <= date.today().year:
            raise ValueError("Año inválido")
        validar_positivo(self.avaluo, "Avalúo")

    @abstractmethod
    def calcular_matricula(self) -> float:
        pass


def validar_positivo(valor, campo):
    if not math.isfinite(valor) or valor <= 0:
        raise ValueError(f"{campo} debe ser positivo y finito")


@dataclass(frozen=True)
class Auto(Vehiculo):
    def calcular_matricula(self):
        descuento = min((date.today().year - self.anio) * 0.02, 0.40)
        return self.avaluo * 0.015 * (1 - descuento)


@dataclass(frozen=True)
class Camioneta(Vehiculo):
    capacidad_kg: float

    def __post_init__(self):
        super().__post_init__()
        validar_positivo(self.capacidad_kg, "Capacidad")

    def calcular_matricula(self):
        return self.avaluo * 0.018 + self.capacidad_kg * 0.03


@dataclass(frozen=True)
class Camion(Vehiculo):
    tonelaje: float

    def __post_init__(self):
        super().__post_init__()
        validar_positivo(self.tonelaje, "Tonelaje")

    def calcular_matricula(self):
        return self.avaluo * 0.02 + self.tonelaje * 25


class CreadorVehiculo(ABC):
    @abstractmethod
    def crear_vehiculo(self, **datos) -> Vehiculo:
        pass

    def procesar(self, **datos) -> tuple[Vehiculo, float]:
        vehiculo = self.crear_vehiculo(**datos)
        return vehiculo, vehiculo.calcular_matricula()


class CreadorAuto(CreadorVehiculo):
    def crear_vehiculo(self, **datos):
        return Auto(**datos)


class CreadorCamioneta(CreadorVehiculo):
    def crear_vehiculo(self, **datos):
        return Camioneta(**datos)


class CreadorCamion(CreadorVehiculo):
    def crear_vehiculo(self, **datos):
        return Camion(**datos)


CREADORES = {
    "auto": CreadorAuto(),
    "camioneta": CreadorCamioneta(),
    "camion": CreadorCamion(),
}


def main():
    parser = argparse.ArgumentParser(description="Factory Method: matrícula de vehículos")
    parser.add_argument("tipo", choices=CREADORES)
    parser.add_argument("--placa", default="ABC-1234")
    parser.add_argument("--marca", default="Marca")
    parser.add_argument("--modelo", default="Modelo")
    parser.add_argument("--anio", type=int, default=2022)
    parser.add_argument("--avaluo", type=float, default=20000)
    parser.add_argument("--capacidad-kg", type=float)
    parser.add_argument("--tonelaje", type=float)
    args = parser.parse_args()
    datos = dict(placa=args.placa, marca=args.marca, modelo=args.modelo,
                 anio=args.anio, avaluo=args.avaluo)
    if args.tipo == "camioneta":
        if args.capacidad_kg is None:
            parser.error("camioneta requiere --capacidad-kg")
        datos["capacidad_kg"] = args.capacidad_kg
    elif args.capacidad_kg is not None:
        parser.error("--capacidad-kg solo aplica a camioneta")
    if args.tipo == "camion":
        if args.tonelaje is None:
            parser.error("camion requiere --tonelaje")
        datos["tonelaje"] = args.tonelaje
    elif args.tonelaje is not None:
        parser.error("--tonelaje solo aplica a camion")
    try:
        vehiculo, costo = CREADORES[args.tipo].procesar(**datos)
    except (ValueError, TypeError) as error:
        parser.error(str(error))
    print(f"{type(vehiculo).__name__}: {vehiculo.placa}")
    print(f"Matrícula ilustrativa: ${costo:.2f}")


if __name__ == "__main__":
    main()
