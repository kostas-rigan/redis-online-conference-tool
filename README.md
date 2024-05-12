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
This project implements a meeting environment(like Zoom and Microsoft team) using Python and Redis. The initial meetings are created by the Python file `fileCreator.py`. After that all the function are being controlled by `main.py` which is being executed with the help of the file `helper.py`, which contains a lot of helpful functions(including the loading of the data to Redis)