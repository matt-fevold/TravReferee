from unittest import TestCase
from World import World


class TestWorld(TestCase):
    """
    Test that the world object is valid
    """

    def test_size(self):
        """
        Test that the size is between 0 and 10
        """
        test_world = World("Manual", 2)
        self.assertTrue(0 <= test_world.size <= 10)

        test_world.size = -2
        self.assertFalse(0 <= test_world.size <= 10)

        test_world.size = 11
        self.assertFalse(0 <= test_world.size <= 10)

        # test the random generated world's size
        for i in range(0, 100):
            with self.subTest(i=i):
                test_world = World()
                self.assertTrue(0 <= test_world.size <= 10)

    def test_atmosphere(self):
        """
        test that atmosphere is between 0 and 15
        """
        test_world = World("Manual", 2, None, 0)
        self.assertTrue(0 <= test_world.atmosphere_type <= 15)

        test_world.atmosphere_type = 16
        self.assertFalse(0 <= test_world.atmosphere_type <= 15)

        test_world.atmosphere_type = -2
        self.assertFalse(0 <= test_world.atmosphere_type <= 15)

        # test the random generation a lot
        for i in range(0, 100):
            with self.subTest(i=i):
                test_world = World()
                self.assertTrue(0 <= test_world.atmosphere_type <= 15)

    def test_starport_quality(self):
        """
        starport can only be X, A, B, C, D, E
        :return:
        """
        test_world = World("Manual", 2, "X")
        self.assertTrue(test_world.starport_quality in ["X"])

        test_world.starport_quality = "A"
        self.assertTrue(test_world.starport_quality in ["A"])

        test_world.starport_quality = "B"
        self.assertTrue(test_world.starport_quality in ["B"])

        test_world.starport_quality = "C"
        self.assertTrue(test_world.starport_quality in ["C"])

        test_world.starport_quality = "D"
        self.assertTrue(test_world.starport_quality in ["D"])

        test_world.starport_quality = "E"
        self.assertTrue(test_world.starport_quality in ["E"])

        # test the random generation a lot
        for i in range(0, 100):
            with self.subTest(i=i):
                test_world = World()
                self.assertTrue(test_world.starport_quality in ["X", "A", "B", "C", "D", "E"])

    def test_hydrographic_percentage(self):
        """
        bounds are 0 - 10
        :return:
        """

        test_world = World("Manual", 2, None, 0, 0, 1)
        self.assertTrue(0 <= test_world.hydrographic_percentage <= 10)

        test_world.hydrographic_percentage = -2
        self.assertFalse(0 <= test_world.hydrographic_percentage <= 10)

        test_world.hydrographic_percentage = 12
        self.assertFalse(0 <= test_world.hydrographic_percentage <= 10)

        for i in range(0, 100):
            with self.subTest(i=i):
                test_world = World()
                self.assertTrue(0 <= test_world.hydrographic_percentage <= 10)


    def test_population(self):
        pass

    def test_government_type(self):
        pass

    def test_law_level(self):
        pass

    def test_tech_level(self):
        pass

    def test_list_of_bases(self):
        pass

    def test_trade_codes(self):
        pass

    def test_travel_code(self):
        pass

