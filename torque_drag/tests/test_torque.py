from unittest import TestCase
from torque_drag import calc
from well_profile import load


class TestTorque(TestCase):

    def test_torque(self):

        well = load(r'https://github.com/pro-well-plan/well_profile/raw/master/well_profile/tests/trajectory1.xlsx')
        dimensions = {'pipe': {'od': 4.5, 'id': 4, 'shoe': 2200}, 'odAnn': 5}
        tnd = calc(well.trajectory, dimensions, case='all', torque_calc=True, wob=50, tbit=5)
        self.assertTrue('lowering' and 'static' and 'hoisting' in tnd.force)
        self.assertTrue(len(tnd.force['lowering']) > 0)
        self.assertTrue(len(tnd.force['static']) > 0)
        self.assertTrue(len(tnd.force['hoisting']) > 0)
        self.assertTrue('lowering' and 'static' and 'hoisting' in tnd.torque)
        self.assertTrue(len(tnd.torque['lowering']) > 0)
        self.assertTrue(len(tnd.torque['static']) > 0)
        self.assertTrue(len(tnd.torque['hoisting']) > 0)
