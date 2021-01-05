Calculating Torque & Drag
=========================

.. autofunction:: torque_drag.calc


.. code-block:: python

    >>> import well_profile
    >>> import torque_drag
    >>> well = well_profile.load('trajectory1.xlsx')
    >>> dimensions = {'od_pipe': 4.5, 'id_pipe': 4, 'length_pipe': 2200, 'od_annular': 5}
    >>> result = torque_drag.calc(well, dimensions, case='all', torque_calc=True, wob=50, tbit=50)
    >>> result.plot(plot_case='Force').show()
    >>> result.plot(plot_case='Torque').show()

|DragForce|
|Torque|

.. |DragForce| image:: /figures/DragForce.png
                    :scale: 80%
.. |Torque| image:: /figures/Torque.png
                    :scale: 80%


Drag Force
----------

.. code-block:: python

    >>> print(result.force['lowering']))
    [372.2971700118521, 368.13599093625027, 363.97481186064846, ...]

    >>> print(result.force['static']))
    [422.85963348870627, 418.69845441310446, 414.53727533750265, ...]

    >>> print(result.force['hoisting']))
    [486.97807188086904, 482.81689280526723, 478.6557137296654, ...]


Torque
------

.. code-block:: python

    >>> print(result.torque['lowering']))
    [52.88965056700336, 52.88965056700336, 52.88965056700336, ...]

    >>> print(result.torque['static']))
    [53.24879605055506, 53.24879605055506, 53.24879605055506, ...]

    >>> print(result.torque['hoisting']))
    [53.66437608286427, 53.66437608286427, 53.66437608286427, ...]
