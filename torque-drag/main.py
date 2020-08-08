def calc(well, case="all", fric=0.24, torque_calc=False):
    """
    Function to generate the torque and drag profiles. Model Source: SPE-11380-PA
    :param well: a well object with rhod (drill string density), r1 (inner diameter of drill string), r2 (outer diameter
    of drill string), r3 (diameter of the first casing layer or borehole), rhof (fluid density), deltaz (length per pipe
    segment), wob (weight on bit), tbit (torque on bit), azimuth (for each segment) and inclination (for each segment).
    :param case: "lowering", "static", "hoisting" or "all"
    :param fric: sliding friction coefficient between DP-wellbore.
    :param torque_calc: boolean, include torque calculation
    :return: two lists, drag force and torque in kN and kN*m
    """

    from math import pi, sin, cos, radians

    unit_pipe_weight = well.rhod * 9.81 * pi * (well.r2 ** 2 - well.r1 ** 2)
    area_a = pi * ((well.r3 ** 2) - (well.r2 ** 2))
    area_ds = pi * (well.r1 ** 2)
    buoyancy = [1 - ((x * area_a) - (x * area_ds)) / (well.rhod * (area_a - area_ds)) for x in well.rhof]
    w = [unit_pipe_weight * well.deltaz * x for x in buoyancy]
    w[0] = 0
    if type(fric) != list:
        fric = fric * len(well.inclination)

    force_1, force_2, force_3 = [well.wob], [well.wob], [well.wob]      # Force at bottom
    if torque_calc:
        torque_1, torque_2, torque_3 = [well.tbit], [well.tbit], [well.tbit]        # Torque at bottom

    for x in reversed(range(1, well.inclination)):
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

    force, torque = [], []
    if (case == "lowering") or (case == "all"):
        force.append([i/1000 for i in force_1[::-1]])
        if torque_calc:
            torque.append([i/1000 for i in torque_1[::-1]])
    if (case == "static") or (case == "all"):
        force.append([i/1000 for i in force_2[::-1]])
        if torque_calc:
            torque.append([i/1000 for i in torque_2[::-1]])
    if (case == "hoisting") or (case == "all"):
        force.append([i/1000 for i in force_3[::-1]])
        if torque_calc:
            torque.append([i/1000 for i in torque_3[::-1]])

    result = [force]

    if torque_calc:
        result.append(torque)

    return result
