
Cookbook
========
A collection of recipies and HOWTO instructions for using this ROS node.
Includes a casual demonstration of each published and subscribed topic.

Before running, be sure to do the following steps:
```
$ source /opt/ros/indigo/setup.bash
$ cd your_catkin_ws
$ git clone https://github.com/hansonrobotics/blender_api_msgs.git
$ git clone https://github.com/hansonrobotics/pau2motors.git
$ catkin build
$ source devel/setup.bash
```
The `blender_api_msgs` module defines the messages that this node uses.
The `pau2motors` module defines the PAU messge used to publish the neck
and eye positions.

##API Version
In order to maintain compatibility, the node publishes a ROS version number:
```
$ rostopic echo -n 1 /blender_api/get_api_version
```
which should currently return `1`.


##Get Animation List
Obtain the list of supported animations.
```
rostopic list
rostopic echo -n 1 /blender_api/available_gestures
rostopic echo -n 1 /blender_api/available_emotion_states
```
These should display the following outputs:
```
$ rostopic echo -n 1 /blender_api/available_gestures
data: ['blink', 'blink-micro', 'blink-relaxed', 'blink-sleepy', 'nod-1', 'nod-2', 'nod-3', 'shake-2', 'shake-3', 'yawn-1']
---
$ rostopic echo -n 1 /blender_api/available_emotion_states
data: ['irritated', 'happy', 'recoil', 'surprised', 'sad', 'confused', 'afraid', 'bored', 'engaged', 'amused', 'comprehending']
---
```

## Running Animations
Individual gestures can be launched one at a time. For example, a
single, short nod:
```
rostopic pub --once /blender_api/set_gesture blender_api_msgs/SetGesture '{name: nod-1, repeat: 1, speed: 0.7, magnitude: 0.4}'
```
The arguments should be self-explanatory: the gesture is carried out
fairly quickly (`speed`), is not too forceful (`magnitude`) and is
performed only once (`repeat`).

Emotional states require a magnitude and duration to be specified, and
so the message format is more complex. The duration can be a single
integer, which is interpreted as seconds, or a list of two integers
which is interpreted as [seconds, nanoseconds].  Thus, below, the list
[6, 500000000] represents six-and-a-half seconds.

```
rostopic pub --once /blender_api/set_emotion_state blender_api_msgs/EmotionState '{name: sad, magnitude: 1.0, duration: [6, 500000000]}'
```
Multiple emotions can be specified in rapid succession; these will be
blended together.

##Monitoring Emotional State
The current emotional state is continually published, and can be
monitored:
```
rostopic echo /blender_api/get_emotion_states
```
A neutral emotional state is reported as an empty list:
```
data: []
---
data: []
---
```
while an emotion that is active might appear as:
```
---
data:
  -
    name: happy
    magnitude: 0.328999996185
    duration:
      secs: -402
      nsecs: 903000001
---
```
Multiple blended emotions will be reported as such:
```
---
data:
  -
    name: afraid
    magnitude: 0.757000029087
    duration:
      secs: -43
      nsecs: 133000001
  -
    name: happy
    magnitude: 0.202999994159
    duration:
      secs: -794
      nsecs: 491000000
---
```


The gesture state can also be monitored.  Under normal circumstances,
the rig is animated so as to breath, and thus will publish a continuous
stream of messages. Thus,
```
rostopic echo /blender_api/get_gestures
```
will show
```
---
data:
  -
    name: CYC-normal
    magnitude: 1.0
    duration:
      secs: 1108
      nsecs: 944999999
    speed: 1.0
  -
    name: CYC-breathing
    magnitude: 0.5
    duration:
      secs: 1275
      nsecs: 878999999
    speed: 1.0
---
```
Specific gestures will have the GST prefix, and so
```
data:
  -
    name: GST-nod-3
    magnitude: 0.5
    duration:
      secs: 41
      nsecs: 399999999
    speed: 1.0
  -
    name: CYC-normal
    magnitude: 1.0
    duration:
      secs: 507
      nsecs: 5999999
    speed: 1.0
  -
    name: CYC-breathing
    magnitude: 0.5
    duration:
      secs: 717
      nsecs: 332999999
    speed: 1.0
---
```
will appear after a nod request:

```
rostopic pub --once /blender_api/set_gesture blender_api_msgs/SetGesture '{name: nod-2, repeat: 1, speed: 0.5, magnitude: 0.2}'
```

##Eye Tracking
The coordinate system used is head-relative, in 'engineering' coordinates:
'x' is forward, 'y' to the left, and 'z' up.
Coordinate system
```
rostopic pub --once /blender_api/set_primary_target blender_api_msgs/Target '{x: 2, y: 0 , z: 0}'
```

## PAU Messages
The PAU messages describe the neck and eye positions.  The PAU message
format is given in the `pau2motors` module.
```
rostopic echo /blender_api/get_pau
```
A typical message looks like this:
```
---
m_headRotation:
  x: -0.0376578830183
  y: -0.0108186900616
  z: 0.0221191961318
  w: 0.99898737669
m_headTranslation:
  x: 0.0
  y: 0.0
  z: 0.0
m_eyeGazeLeftPitch: 0.0848467648029
m_eyeGazeLeftYaw: -0.101413160563
m_eyeGazeRightPitch: 0.088948123157
m_eyeGazeRightYaw: -0.0995370447636
m_coeffs: [0.023376941680908203, 0.0, 0.0, 0.08733086287975311, 0.2089768499135971, -0.002002716064453125, 0.002917647361755371, -0.002703070640563965, 0.0, 0.025170477107167244, 0.0, 0.2076178640127182, 0.00020563602447509766, 0.75, 0.0024557113647460938, 0.003466010093688965, 0.0, 0.00292360782623291, 0.0, 0.001138448715209961, -0.0004455447196960449, 0.02337382175028324, 0.0, 0.0572890043258667, 0.05713999271392822, 0.0, 0.0, 0.006374716758728027, 0.0, 0.22096529603004456, 0.047549232840538025, 0.02552708238363266, 0.0, 0.003141164779663086, 0.0, 0.08774437010288239, 0.0021129846572875977, 0.0, 0.001516193151473999, 0.04755258560180664]
---
```