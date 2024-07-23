Names of contributors:
    Bayan Yahya- 324846757
    Basel Arw- 208215673


-------------------------------------------------------------------------------
Description of the solutaion and and the format of the inputs and outputs:
-------------------------------------------------------------------------------

**Overview:**
This project implements a robot navigation and cleaning algorithm using various sensors and a battery meter. The robot is designed to navigate a grid-based house, clean it, and return to a docking station. The algorithm uses Depth-First Search (DFS) for navigation.

**Project Structure**
- Header Files
* abstract_algorithm.h: Defines the AbstractAlgorithm interface that any algorithm must implement.
* battery_meter.h: Defines the BatteryMeter interface for monitoring battery state.
* dirt_sensor.h: Defines the DirtSensor interface for detecting dirt levels.
* enums.h: Defines common enums used throughout the project (Direction and Step).
* MyDirt_sensor.h: Implements the MyDirt_sensor class, which inherits from DirtSensor.
* MyWall_sensor.h: Implements the MyWall_sensor class, which inherits from WallsSensor.
* wall_sensor.h: Defines the WallsSensor interface for detecting walls.
* MyAlgorithm.h: Implements the MyAlgorithm class, which inherits from AbstractAlgorithm.
* MyBattery_meter.h: Implements the MyBattery_meter class, which inherits from BatteryMeter.

- Source Files
* main.cpp: Entry point of the application. Initializes and runs the simulator.
* MyAlgorithm.cpp: Implementation of the MyAlgorithm class methods.
* MyBattery_meter.cpp: Implementation of the MyBattery_meter class methods.
* MyDirt_sensor.cpp: Implementation of the MyDirt_sensor class methods.
* MySimulator.cpp: Implementation of the MySimulator class, which simulates the robot's environment and behavior.
* MyWall_sensor.cpp: Implementation of the MyWall_sensor class methods.


**Input Files**
There are 3 inputs files:
- input_a.txt:
    in this file the vacuum cleaner surrounded with 4 walls.
- input_b.txt:
    in this file the vacuum cleaner will make his best with dfs and return to the docking station with FINISHED.
- input_c.txt:
    in this file, all the squares with dirt level 9.

**Output Files**
There are 3 outputs files:
- output_input_a.txt:
    in this output file, the vacuum cleaner will do not any move, cause he is surrounded by 4 walls. He stays on place and don't move nor charge.
- output_input_b.txt:
    in this output file, vacuum cleaner will return to the docking station and end with FINISH.
- output_input_c.txt:
    in this output file, the vacuum will not return to the docking station and the maximum steps will be finished before he backs. the vacuum cleaner will end with WORKING.
