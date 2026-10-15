import unittest
from datetime import date
from decimal import Decimal
from caso1 import Auto, CREADORES
from caso2 import ActivoFijoBuilder


class PruebasPatrones(unittest.TestCase):
    def test_factory_polimorfismo(self):
        base = dict(placa="ABC", marca="Toyota", modelo="Modelo",
                    anio=date.today().year, avaluo=20000)
        for tipo, extra, esperado in (
            ("auto", {}, 300),
            ("camioneta", {"capacidad_kg": 1000}, 390),
            ("camion", {"tonelaje": 8}, 600),
        ):
            with self.subTest(tipo=tipo):
                vehiculo, costo = CREADORES[tipo].procesar(**base, **extra)
                self.assertAlmostEqual(costo, esperado)
                self.assertEqual(vehiculo.placa, "ABC")

    def test_vehiculo_invalido(self):
        with self.assertRaises(ValueError):
            Auto("", "Marca", "Modelo", 2022, 20000)

    def test_capacidad_invalida(self):
        with self.assertRaises(ValueError):
            CREADORES["camioneta"].crear_vehiculo(
                placa="ABC", marca="M", modelo="X", anio=2022,
                avaluo=20000, capacidad_kg=-1)

    def test_builder_minimo(self):
        activo = ActivoFijoBuilder("AF1", "Mesa", Decimal("100")).build()
        self.assertIsNone(activo.marca)
        self.assertEqual(activo.precio, Decimal("100"))

    def test_builder_copia_independiente(self):
        builder = ActivoFijoBuilder("AF1", "Mesa", Decimal("100"))
        primero = builder.caracteristica("Material", "Madera").build()
        segundo = builder.caracteristica("Material", "Metal").build()
        self.assertEqual(primero.caracteristicas["Material"], "Madera")
        self.assertEqual(segundo.caracteristicas["Material"], "Metal")
        with self.assertRaises(TypeError):
            primero.caracteristicas["Material"] = "Otro"

    def test_precio_invalido(self):
        for precio in (Decimal("-1"), Decimal("NaN")):
            with self.subTest(precio=precio), self.assertRaises(ValueError):
                ActivoFijoBuilder("AF1", "Mesa", precio)

    def test_garantia_invalida(self):
        with self.assertRaises(ValueError):
            ActivoFijoBuilder("AF1", "PC", Decimal("100")).garantia_meses(-1).build()


if __name__ == "__main__":
    unittest.main()
