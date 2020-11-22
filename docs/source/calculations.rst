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
    [554.2991696028456, 547.8493549353179, 541.3995402677903, ...]

    >>> print(result.force['static']))
    [627.9312760426308, 621.4814613751031, 615.0316467075754, ...]

    >>> print(result.force['hoisting']))
    [721.6322636958221, 715.1824490282944, 708.7326343607667, ...]


Torque
------

.. code-block:: python

    >>> print(result.torque['lowering']))
    [215.67223948951664, 215.67223948951664, 215.67223948951664, ...]

    >>> print(result.torque['static']))
    [236.58941229661033, 236.58941229661033, 236.58941229661033, ...]

    >>> print(result.torque['hoisting']))
    [260.8272222196797, 260.8272222196797, 260.8272222196797, ...]
