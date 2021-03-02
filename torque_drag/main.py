from math import pi, sin, cos, radians


def calc(trajectory, dimensions, densities=None, case="all", fric=None, wob=0, tbit=0, torque_calc=False):
    """
    Function to generate the torque and drag profiles. Model Source: SPE-11380-PA

    Arguments:
        trajectory: a trajectory object from well_profile library
        dimensions: dict for dimensions {'pipe': {'od', 'id', 'length}, 
                                         'odAnn'}
        densities: dict for densities {'rhof': 1.3, 'rhod': 7.8}
        case: "lowering", "static", "hoisting" or "all"
        fric: num or list. sliding friction coefficient between DP-wellbore. default: 0.24
        tbit: torque on bit, kN*m
        wob: weight on bit, kN
        torque_calc: boolean, include torque calculation

    Returns:
        object with drag force and torque in kN and kN*m
    """

    well = set_conditions(trajectory, dimensions, densities, wob, tbit)

    unit_pipe_weight = well.rhod * 9.81 * pi * (well.pipe_or ** 2 - well.pipe_ir ** 2)
    area_a = pi * ((well.ann_or ** 2) - (well.pipe_or ** 2))     # annular area in m2
    area_ds = pi * (well.pipe_ir ** 2)       # drill string inner area in m2

    for point in well.trajectory:
        point['buoyancy'] = 1 - ((point['rhof'] * area_a) - (point['rhof'] * area_ds)) / (well.rhod * (area_a-area_ds))
        point['weight'] = unit_pipe_weight * point['delta']['md'] * point['buoyancy']

    if type(fric) is not list:
        for point in well.trajectory:
            point['fric'] = 0.24
    else:
        for idx, point in enumerate(well.trajectory):
            point['fric'] = fric[idx]

    well.trajectory[-1]['force'] = {'lowering': well.wob,
                                    'static': well.wob,
                                    'hoisting': well.wob}
    well.trajectory[-1]['torque'] = {'lowering': None,
                                     'static': None,
                                     'hoisting': None}

    if torque_calc:
        well.trajectory[-1]['torque'] = {'lowering': well.tbit,
                                         'static': well.tbit,
                                         'hoisting': well.tbit}

    for idx, point in reversed(list(enumerate(well.trajectory[:-1]))):
        point['incAvg'] = radians((point['inc'] + well.trajectory[idx-1]['inc']) / 2)
        delta_azi = -radians(well.trajectory[idx+1]['delta']['azi'])
        delta_inc = -radians(well.trajectory[idx+1]['delta']['inc'])
        point['force'] = {}
        point['torque'] = {}
        # DRAG FORCE CALCULATIONS
        if (case == "lowering") or (case == "all"):
            # Drag force
            fn_1 = ((well.trajectory[idx+1]['force']['lowering'] * delta_azi * sin(point['incAvg'])) ** 2 +
                    (well.trajectory[idx+1]['force']['lowering'] * delta_inc + point['weight'] *
                     sin(point['incAvg'])) ** 2) ** 0.5

            delta_ft_1 = point['weight'] * cos(point['incAvg']) - point['fric'] * fn_1
            point['force']['lowering'] = well.trajectory[idx+1]['force']['lowering'] + delta_ft_1

            if torque_calc:
                # Torque calculation
                delta_torque_1 = point['fric'] * fn_1 * well.pipe_or
                point['torque']['lowering'] = well.trajectory[idx+1]['torque']['lowering'] + delta_torque_1

        if (case == "static") or (case == "all"):

            # Drag force
            fn_2 = ((well.trajectory[idx+1]['force']['static'] * delta_azi * sin(point['incAvg'])) ** 2 +
                    (well.trajectory[idx+1]['force']['static'] * delta_inc + point['weight'] *
                    sin(point['incAvg'])) ** 2) ** 0.5

            delta_ft_2 = point['weight'] * cos(point['incAvg'])
            point['force']['static'] = well.trajectory[idx+1]['force']['static'] + delta_ft_2

            if torque_calc:
                # Torque calculation
                delta_torque_2 = point['fric'] * fn_2 * well.pipe_or
                point['torque']['static'] = well.trajectory[idx+1]['torque']['static'] + delta_torque_2

        if (case == "hoisting") or (case == "all"):

            # Drag force
            fn_3 = ((well.trajectory[idx+1]['force']['hoisting'] * delta_azi * sin(point['incAvg'])) ** 2 +
                    (well.trajectory[idx+1]['force']['hoisting'] * delta_inc + point['weight'] *
                     sin(point['incAvg'])) ** 2) ** 0.5

            delta_ft_3 = point['weight'] * cos(point['incAvg']) + point['fric'] * fn_3
            point['force']['hoisting'] = well.trajectory[idx+1]['force']['hoisting'] + delta_ft_3

            if torque_calc:
                # Torque calculation
                delta_torque_3 = point['fric'] * fn_3 * well.pipe_or
                point['torque']['hoisting'] = well.trajectory[idx+1]['torque']['hoisting'] + delta_torque_3

    class TaD(object):
        def __init__(self):
            self.force = {
                "lowering": [],
                "static": [],
                "hoisting": []
            }
            self.torque = {
                "lowering": [],
                "static": [],
                "hoisting": []
            }
            self.depth = []

            for point in well.trajectory:
                self.depth.append(point['md'])
                if (case == "lowering") or (case == "all"):
                    self.force['lowering'].append(point['force']['lowering'] / 1000)
                    if torque_calc:
                        self.torque['lowering'].append(point['torque']['lowering'] / 1000)
                if (case == "static") or (case == "all"):
                    self.force['static'].append(point['force']['static'] / 1000)
                    if torque_calc:
                        self.torque['static'].append(point['torque']['static'] / 1000)
                if (case == "hoisting") or (case == "all"):
                    self.force['hoisting'].append(point['force']['hoisting'] / 1000)
                    if torque_calc:
                        self.torque['hoisting'].append(point['torque']['hoisting'] / 1000)

        def plot(self, plot_case='Force'):
            from .plot import tnd
            fig = tnd(self, plot_case)

            return fig

    return TaD()


def set_conditions(trajectory, dimensions, densities=None, wob=0, tbit=0):

    wob *= 1000
    tbit *= 1000

    if densities is None:
        densities = {'rhof': 1.3, 'rhod': 7.8}

    class NewWell(object):
        def __init__(self):
            self.trajectory = trajectory
            self.pipe_ir = dimensions['pipe']['id'] / 2 / 39.37
            self.pipe_or = dimensions['pipe']['od'] / 2 / 39.37
            self.ann_or = dimensions['odAnn'] / 2 / 39.37
            self.rhod = densities['rhod'] * 1000

            if type(densities['rhof']) is not list:
                for point in self.trajectory:
                    point['rhof'] = densities['rhof'] * 1000   # in kg/m3
            else:
                for idx, point in enumerate(self.trajectory):
                    point['rhof'] = densities['rhof'][idx] * 1000   # in kg/m3

            self.wob = wob      # in N
            self.tbit = tbit        # in Nm

    return NewWell()
