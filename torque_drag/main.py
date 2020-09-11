from math import pi, sin, cos, radians


def calc(well, dimensions, densities=None, case="all", fric=0.24, wob=0, tbit=0, torque_calc=False):
    """
    Function to generate the torque and drag profiles. Model Source: SPE-11380-PA
    :param well: a well object with rhod (drill string density), r1 (inner diameter of drill string), r2 (outer diameter
    of drill string), r3 (diameter of the first casing layer or borehole), rhof (fluid density), rhod (density of drill
    pipe) deltaz (length per pipe segment), wob (weight on bit), tbit (torque on bit), azimuth (for each segment) and
    inclination (for each segment).
    :param dimensions: dict for dimensions {'od_pipe': , 'id_pipe': , 'length_pipe': , 'od_annular': }
    :param densities: dict for densities {'rhof': 1.3, 'rhod': 7.8}
    :param case: "lowering", "static", "hoisting" or "all"
    :param fric: sliding friction coefficient between DP-wellbore.
    :param tbit: torque on bit, kN*m
    :param wob: weight on bit, kN
    :param torque_calc: boolean, include torque calculation
    :return: two lists, drag force and torque in kN and kN*m
    """

    well = set_conditions(well, dimensions, densities, wob, tbit)

    unit_pipe_weight = well.rhod * 9.81 * pi * (well.r2 ** 2 - well.r1 ** 2)
    area_a = pi * ((well.r3 ** 2) - (well.r2 ** 2))
    area_ds = pi * (well.r1 ** 2)
    buoyancy = [1 - ((x * area_a) - (x * area_ds)) / (well.rhod * (area_a - area_ds)) for x in well.rhof]
    w = [unit_pipe_weight * well.deltaz * x for x in buoyancy]
    w[0] = 0

    if type(fric) is not list:
        fric = [fric] * len(well.inclination)

    force_1, force_2, force_3 = [well.wob], [well.wob], [well.wob]      # Force at bottom
    torque_1, torque_2, torque_3 = None, None, None  # Torque at bottom
    if torque_calc:
        torque_1, torque_2, torque_3 = [well.tbit], [well.tbit], [well.tbit]        # Torque at bottom

    for x in reversed(range(1, well.zstep)):
        delta_azi = radians(well.azimuth[x] - well.azimuth[x-1])
        delta_inc = radians(well.inclination[x] - well.inclination[x-1])
        inc_avg = radians((well.inclination[x] + well.inclination[x-1]) / 2)

        # DRAG FORCE CALCULATIONS
        if (case == "lowering") or (case == "all"):

            # Drag force
            fn_1 = ((force_1[-1] * delta_azi * sin(inc_avg)) ** 2
                    + (force_1[-1] * delta_inc + w[x] * sin(inc_avg)) ** 2) ** 0.5

            delta_ft_1 = w[x] * cos(inc_avg) - fric[x] * fn_1
            ft_1 = force_1[-1] + delta_ft_1
            force_1.append(ft_1)

            if torque_calc:
                # Torque calculation
                delta_torque_1 = fric[x] * fn_1 * well.r2
                t_1 = torque_1[-1] + delta_torque_1
                torque_1.append(t_1)

        if (case == "static") or (case == "all"):

            # Drag force
            fn_2 = ((force_2[-1] * delta_azi * sin(inc_avg)) ** 2
                    + (force_2[-1] * delta_inc + w[x] * sin(inc_avg)) ** 2) ** 0.5

            delta_ft_2 = w[x] * cos(inc_avg)
            ft_2 = force_2[-1] + delta_ft_2
            force_2.append(ft_2)

            if torque_calc:
                # Torque calculation
                delta_torque_2 = fric[x] * fn_2 * well.r2
                t_2 = torque_2[-1] + delta_torque_2
                torque_2.append(t_2)

        if (case == "hoisting") or (case == "all"):

            # Drag force
            fn_3 = ((force_3[-1] * delta_azi * sin(inc_avg)) ** 2
                    + (force_3[-1] * delta_inc + w[x] * sin(inc_avg)) ** 2) ** 0.5

            delta_ft_3 = w[x] * cos(inc_avg) + fric[x] * fn_3
            ft_3 = force_3[-1] + delta_ft_3
            force_3.append(ft_3)

            if torque_calc:
                # Torque calculation
                delta_torque_3 = fric[x] * fn_3 * well.r2
                t_3 = torque_3[-1] + delta_torque_3
                torque_3.append(t_3)

    class Result(object):
        def __init__(self):
            self.force = {
                "lowering": None,
                "static": None,
                "hoisting": None
            }
            self.torque = {
                "lowering": None,
                "static": None,
                "hoisting": None
            }

            if (case == "lowering") or (case == "all"):
                self.force["lowering"] = [i/1000 for i in force_1[::-1]]
                if torque_calc:
                    self.torque["lowering"] = [i/1000 for i in torque_1[::-1]]
            if (case == "static") or (case == "all"):
                self.force["static"] = [i/1000 for i in force_2[::-1]]
                if torque_calc:
                    self.torque["static"] = [i/1000 for i in torque_2[::-1]]
            if (case == "hoisting") or (case == "all"):
                self.force["hoisting"] = [i/1000 for i in force_3[::-1]]
                if torque_calc:
                    self.torque["hoisting"] = [i/1000 for i in torque_3[::-1]]

            self.depth = well.md

        def plot(self, plot_case='Force'):
            from .plot import tnd
            fig = tnd(self, plot_case)

            return fig

    return Result()


def set_conditions(well, dimensions, densities=None, wob=0, tbit=0):

    wob *= 1000
    tbit *= 1000

    if densities is None:
        densities = {'rhof': 1.3, 'rhod': 7.8}

    class NewWell(object):
        def __init__(self):
            self.r1 = dimensions['id_pipe'] / 2
            self.r2 = dimensions['od_pipe'] / 2
            self.r3 = dimensions['od_annular'] / 2
            self.rhof = densities['rhof']
            if type(densities['rhof']) is not list:
                self.rhof = [densities['rhof']] * well.zstep
            self.rhod = densities['rhod']
            self.deltaz = well.deltaz
            self.zstep = round(dimensions['length_pipe'] / self.deltaz) + 1
            self.wob = wob
            self.tbit = tbit
            self.rhof = self.rhof[:self.zstep]
            self.azimuth = well.azimuth[:self.zstep]
            self.tvd = well.tvd[:self.zstep]
            self.md = well.md[:self.zstep]
            self.inclination = well.inclination[:self.zstep]

    return NewWell()
