 
Digital Interfacing Overlay overview
======================================

There are four components to the digital interfacing overlay:

* Pattern Builder
* Finite State Machine Builder
* Combinatorial Function Builder
* Tracebuffer

FSMs, digital patterns and combinatorial functions can be specified using a textual description which can then be passed to a Python function to program the overlay to implement the functionality. 

The trace buffer component can capture and stream signals to DRAM allowing the data to be analysed in Python. The trace buffer can be used standalone to capture external signals, or used in combination with the other three DIO components to monitor data on the external interface. E.g. the tracebuffer can be used with the pattern generator to verify the data sent to the output pins. 


The project files for the base overlay can be found here:

    ``<GitHub Repository>/boards/<board>/dio``


The makefile and .tcl file can be used to rebuild the overlay. The base overlay will include IP from the Vivado library, and custom IP. Any custom IP can be found in directory:

    ``<GitHub Repository>/boards/ip`` 

For more details on rebuilding the overlay, or creating a new overlay, see the Creating Overlays section. 


Block Diagram
-----------------------

Pins
------------------------

Pattern Builder
-------------------------------------------

The pattern Builder allows arbitrary patterns of 8K to be streamed to the digital pins. This can be used to testing external peripherals, or as a very simple way to create a driver. Patterns of up to 8K can be stored and streamed out to the interface on demand.  

Example 
^^^^^^^^^^^^^^^^^^^^^

Waveforms can be defined with the following notation:

l: low
h: high
.: no change

The pattern can be repeated a number of times by "multiplying". E.g. *'lh' /* 64* will toggle the signal low-high 64 times.  

.. code-block:: Python

    loopback_test = {'signal': [
        ['stimulus',
            {'name': 'clk0',  'pin': 'D0', 'wave': 'lh' * 64},
            {'name': 'clk1',  'pin': 'D1', 'wave': 'l.h.' * 32},
            {'name': 'clk2',  'pin': 'D2', 'wave': 'l...h...' * 16},      
        ['analysis',
            {'name': 'clk0',  'pin': 'D0'},
            {'name': 'clk1',  'pin': 'D1'},
            {'name': 'clk2',  'pin': 'D2'}]], 

        'foot': {'tock': 1, 'text': 'Loopback Test'},
        'head': {'tick': 1, 'text': 'Loopback Test'}}


Finite State Machine Builder
-------------------------------------------

The Finite State Machine builder allows Finite state machines to be specified with a textual description, which can be passed to the xxx Python function which will program the overlay to implement the FSM. 

The FSM supports 20 pins that can be used in any combination of inputs or outputs. Up to xxx states are supported. The FSM can be graphed and displayed inside a Jupyter Notebook. 

Example 
^^^^^^^^^^^^^^^^^^^^^
The specification for the finite state machine is a list of inputs, outputs, states, and transitions. 

Input and outputs are listed as tuples, specifying a pin and label for the pin. 

.. code-block:: Python
    ('reset','D0')
    
Valid pins are found in the interface specification:

Transitions  are specified by defining the input bits, '01' in the following example, the current state, 'S0', the next state, 'S5', and the output bits '011'.
    
.. code-block:: Python

    ['01', 'S0', 'S5', '000']
    
    
Wildcards for inputs '-' and for states '/*' can be used. 

.. code-block:: Python

    ['-1', '*', 'S5', '000']

Specifying ‘use_state_bits=True’ will output the state to unassigned bits on the interface. If there are no unused pins available, the last few output pins will be automatically overwritten to show state bits instead. 
    
A full specification is defined as follows:
    
.. code-block:: Python

    fsm_spec = {'inputs': [('reset','D0'), ('direction','D1')],
        'outputs': [('bit2','D3'), ('bit1','D4'), ('bit0','D5')],
        'states': ['S0', 'S1', 'S2', 'S3', 'S4', 'S5'],
        'transitions': [['00', 'S0', 'S1', '000'],
                        ['01', 'S0', 'S5', '000'],
                        ['00', 'S1', 'S2', '001'],
                        ['01', 'S1', 'S0', '001'],
                        ['00', 'S2', 'S3', '010'],
                        ['01', 'S2', 'S1', '010'],
                        ['00', 'S3', 'S4', '011'],
                        ['01', 'S3', 'S2', '011'],
                        ['00', 'S4', 'S5', '100'],
                        ['01', 'S4', 'S3', '100'],
                        ['00', 'S5', 'S0', '101'],
                        ['01', 'S5', 'S4', '101'],
                        ['1-', '*',  'S0', '']]}


Combinatorial Function Builder
-------------------------------------------

The CFB supports combinatorial functions of one up to five inputs on each output pin. 

Example 
^^^^^^^^^^^^^^^^^^^^^

Combinatorial expressions can be defined in a Python list using the expressions & (AND), | (OR), ! (NOT), ^ (XOR). The expression list also defines the input and output pins. 
 
The following list defines four combinatorial functions on pins D8-11, which are built using combinatorial functions made up of inputs from pins D0-D3. Any pin assigned a value is an output, and any pin used as a parameter in the expression is an input. If a pin is defined as an output, it cannot be used as an input.


.. code-block:: Python

    expressions = ["D8 = D0 & D1",
                   "D9 = D0 & D1",
                   "D10 = D0 & D1 & D2",
                   "D11 = D0 & D1 & D2 & D3"]

Once the expressions have been defined, they can be passed to the BooleanBuilder function.

.. code-block:: Python
    boolean_functions = [BooleanBuilder(INTERFACE) for _ in range(len(expressions))]

Then ...

.. code-block:: Python

    for i in range(len(expressions)): 
        bgs[i].config(expressions[i]) 
        bgs[i].arm() 
        bgs[i].run() 
        bgs[i].display()



Tracebuffer
-------------------------------------------

The tracebuffer is connected to the external interface and can capture input or output signals on each pin and stream the data to DRAM. The trace buffer supports blocks of 8MB. Once the data is in memory it can be analyzed in Python. There are a number of Python packages that could be used to analyze or process the data. WaveDrom and SigRok are two packages that can be used to processing and displaying waveforms in a Jupyter Notebook, and are included as part of the PYNQ image. 

Example 
^^^^^^^^^^^^^^^^^^^^

