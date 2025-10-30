import unittest
from varasto import Varasto


class TestVarasto(unittest.TestCase):
    def setUp(self):
        self.varasto = Varasto(10)

    def test_konstruktori_luo_tyhjan_varaston(self):
        # https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertAlmostEqual
        self.assertAlmostEqual(self.varasto.saldo, 0)

    def test_uudella_varastolla_oikea_tilavuus(self):
        self.assertAlmostEqual(self.varasto.tilavuus, 10)

    def test_lisays_lisaa_saldoa(self):
        self.varasto.lisaa_varastoon(8)

        self.assertAlmostEqual(self.varasto.saldo, 8)

    def test_lisays_lisaa_pienentaa_vapaata_tilaa(self):
        self.varasto.lisaa_varastoon(8)

        # vapaata tilaa pitäisi vielä olla tilavuus-lisättävä määrä eli 2
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 2)

    def test_ottaminen_palauttaa_oikean_maaran(self):
        self.varasto.lisaa_varastoon(8)

        saatu_maara = self.varasto.ota_varastosta(2)

        self.assertAlmostEqual(saatu_maara, 2)

    def test_ottaminen_lisaa_tilaa(self):
        self.varasto.lisaa_varastoon(8)

        self.varasto.ota_varastosta(2)

        # varastossa pitäisi olla tilaa 10 - 8 + 2 eli 4
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 4)

    def test_negatiivinen_tilavuus_korjataan(self):
        self.varasto_negatiivnen_tilavuus = Varasto(-10)

        self.assertAlmostEqual(self.varasto_negatiivnen_tilavuus.tilavuus, 0)

    def test_negatiivinen_alkusaldo_korjataan(self):
        self.varasto_neg_alkusaldo = Varasto(10, -10)

        self.assertAlmostEqual(self.varasto_neg_alkusaldo.saldo, 0)

    def test_tyhja_lisays_ei_palauta(self):
        # tyhjä TAI negatiivinen lisäys
        self.assertAlmostEqual(self.varasto.lisaa_varastoon(-10), None)

    def test_lisays_suurempi_kuin_mahtuu(self):
        # jos lisäys > tilavuus-saldo -> saldo = tilavuus

        # Lisätään enemmän kuin mahtuu:
        self.varasto.lisaa_varastoon(self.varasto.paljonko_mahtuu() + 1)

        # Tarkistetaan onko täynnä:
        self.assertAlmostEqual(self.varasto.saldo, self.varasto.tilavuus)

    def test_otetaan_negatiivinen_maara_palauttaa_0(self):
        self.assertAlmostEqual(self.varasto.ota_varastosta(-10), 0)

    def test_otetaan_enemman_kuin_saldo_palautta_koko_saldon(self):
        self.varasto.ota_varastosta(self.varasto.saldo + 1)
        self.assertAlmostEqual(self.varasto.saldo, 0)

    def test_merkkijonoesitys(self):
        # emt pitäiskö tän tarkistaakki jotain mutta tästä selviää
        # ainakin että str metodi ei kaada koko ohjelmaa :D
        str(self.varasto)
