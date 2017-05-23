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
        pass
