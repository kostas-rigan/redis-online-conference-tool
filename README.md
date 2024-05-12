# redis-online-conference-tool
Project #3 in Big Data Systems Management

# Contents
- [Contents](#contents)
- [Authors](#authors)
- [Guidelines](#guidelines)

# Authors<a class="anchor" id="Authors"></a>
> Konstantinos Riganas, Student<br />
> Department of Management Science and Technology <br />
> Athens University of Economics and Business <br />
> t8200145@aueb.gr

> Nikolaos Nikolaidis, Student<br />
> Department of Management Science and Technology <br />
> Athens University of Economics and Business <br />
> t8200120@aueb.gr

# Guidelines<a class="anchor" id="Guidelines"></a>
- Execute the commands:
  * `python fileCreator.py`
  * `python main.py`

# Description <a class="anchor" id="Description"></a>
## Overview <a class="anchor" id="Overview"></a>
This project implements a meeting environment(like Zoom and Microsoft team) using Python and Redis. The initial meetings are created by the Python file `fileCreator.py`. After that all the function are being controlled by `main.py` which is being executed with the help of the file `helper.py`, which contains a lot of helpful functions(including the loading of the data to Redis

## Files <a class="anchor" id="Files"></a>

### 1. `filesCreator.py`
- **Purpose:** Creating the JSON files that are going to be loaded on Redis
- **Functionality:** 
  - Call the function create for each of the following creators: `usersCreator.py`,`meetingCreator.py`, `meetingInstancesCreator.py` and `eventLogCreator.py`

### 2. `main.py`
- **Purpose:** This Python script manages a system for organizing and monitoring meetings using Redis as a database.
- **Functionality:**
  - Defines functions for various actions related to user interactions with meetings, such as joining, leaving, and posting messages.
  - Provides functions to retrieve information about active meetings, participants, chat messages, and join times.
  - Implements a controller to monitor meeting durations and automatically end meetings when they are scheduled to finish.
  - Runs a main loop for user interaction, allowing users to perform actions such as joining meetings, posting messages, and viewing meeting information.

### 3. `helper.py`
- **Purpose:** This module contains functions designed to aid in various tasks related to the implementation of an online conference tool using Redis.