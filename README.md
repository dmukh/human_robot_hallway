# Human-Robot Hallway Problem

Consider an environment where a human and a robot are on opposite ends of a hallway and the
human's initial goal is to reach the end of the hallway. In order to capture realism, the human is
allowed to change its intention and head to a different part of the hallway; e.g. go to the bathroom
or chat with a friend. Meanwhile, the objective of the robot is to travel to the end of the hallway
while avoiding collisions with the human. In order to plan a safe trajectory that will take the
robot to the end of the hallway, it is necessary for the robot to know the humans intentions. It
is assumed that there is no communication between human and robot. Therefore, the human's
true goal is unobservable and the robot must estimate the humans goal at each step and alter the
trajectory accordingly.

This problem can be cast as a simple stochastic game (SSG) that is played on the directed
graph *G = (V, E)*. The vertex set V is the union of disjoint sets V<sub>max</sub> , V<sub>min</sub> , and 
V<sub>random</sub> . Let V<sub>max</sub> represent the set of vertices that are controlled by the robot and 
V<sub>min</sub> represent the set of vertices controlled by the human. The winning condition for the human 
is the 1-sink vertex being reached and the winning condition for the robot is the 0-sink vertex.

The state of this game includes the human’s location (*hLoc*), robot’s location (*rLoc*), the
human’s estimated goal (*goal*), and a counter keeping track of the number of changes in the goal
estimate (*count*). Suppose the environment in consideration is a 5×15 grid, with three potential
targets spaced evenly through the hallway. If the hallway is divided into three zones, with each
being a 5×5 grid with a cell in each zone being a potential goal of the human, then hLoc can
be used to determine the zone occupied by the human. The purpose of the zoning is to provide
a coarse discretization of the environment for simplification. In this environment, the state of the
game evolves in the following manner:

1. The human makes its move and probability of choosing a particular action (Front, Back, Up,
or Down) is said to be a function of *goal* and the zone being occupied.
2. The *goal* of the human is estimated with a user-defined estimator.
3. The robot makes its move based on human's action and *goal*.

These steps are repeated until the human and the robot accomplish their respective objectives.
Furthermore, the robot’s movements are constrained by the Linear Temporal Logic (LTL) specification

<a href="https://www.codecogs.com/eqnedit.php?latex=\varphi&space;=&space;\Box&space;\left(&space;\varphi_{safety}&space;\right)&space;\wedge&space;\left[\Diamond&space;\,&space;\text{robotArrived}&space;\;&space;||&space;\,&space;\left(&space;\texttt{count}&space;>&space;N&space;\right)&space;\right]," target="_blank"><img src="https://latex.codecogs.com/gif.latex?\varphi&space;=&space;\Box&space;\left(&space;\varphi_{safety}&space;\right)&space;\wedge&space;\left[\Diamond&space;\,&space;\text{robotArrived}&space;\;&space;||&space;\,&space;\left(&space;\texttt{count}&space;>&space;N&space;\right)&space;\right]," title="\varphi = \Box \left( \varphi_{safety} \right) \wedge \left[\Diamond \, \text{robotArrived} \; || \, \left( \texttt{count} > N \right) \right]," /></a>

where as an example,

<a href="https://www.codecogs.com/eqnedit.php?latex=\varphi_{safety}&space;=&space;\left(&space;\text{isHfrontRight}&space;\,&space;||&space;\,&space;\text{isHfront}&space;\,||&space;\,&space;\text{isHfrontLeft}&space;\right)&space;\rightarrow&space;\text{rMoveBack}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\varphi_{safety}&space;=&space;\left(&space;\text{isHfrontRight}&space;\,&space;||&space;\,&space;\text{isHfront}&space;\,||&space;\,&space;\text{isHfrontLeft}&space;\right)&space;\rightarrow&space;\text{rMoveBack}" title="\varphi_{safety} = \left( \text{isHfrontRight} \, || \, \text{isHfront} \,|| \, \text{isHfrontLeft} \right) \rightarrow \text{rMoveBack}" /></a>

Note that *robotArrived* encodes whether the robot has reached the end of the hallway and *N* is
an integer.

