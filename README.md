# Discovering Object Attributes by Prompting Large Language Models with Perception-Action APIs

This repository contains code and technical details for the paper:

**[Discovering Object Attributes by Prompting Large Language Models with Perception-Action APIs](https://arxiv.org/abs/2409.15505)** (**[website](https://prg.cs.umd.edu/EmbodiedAttributeDetection)**)

Authors: Angelos Mavrogiannis, Dehao Yuan, Yiannis Aloimonos

Please cite our work if you found it useful:
```
@article{mavrogiannis2024discoveringobjectattributesprompting,
      title={Discovering Object Attributes by Prompting Large Language Models with Perception-Action APIs}, 
      author={Angelos Mavrogiannis and Dehao Yuan and Yiannis Aloimonos},
      year={2024},
      eprint={2409.15505},
      archivePrefix={arXiv},
      primaryClass={cs.RO},
      url={https://arxiv.org/abs/2409.15505},
}
```
<p align="center">
  <img src="/images/attributes_cover.jpeg" alt="Cover" />
</p>

# Overview
<p align="center">
  <img src="/images/attributes_pipeline.jpeg" alt="Pipeline" />
</p>

We describe our end-to-end framework for embodied attribute detection. The LLM receives as input a perception API with LLMs and VLMs as backbones, an action API based on a Robot Control API, a natural language (NL) instruction from a user, and a visual scene observation. It then produces a python program that combines LLM and VLM function calls with robot actions to actively reason about attribute detection.

# Perception-Action API
<p align="center">
  <img src="/images/api.gif" alt="API" />
</p>

The API consists of an $$\mathtt{ImagePatch}$$ class and a $\mathtt{Robot}$ action class with methods and examples of their uses in the form of docstrings. Inspired by <a href="https://viper.cs.columbia.edu">ViperGPT</a>, $\mathtt{ImagePatch}$ supports Open-Vocabulary object Detection (OVD), Visual Question Answering (VQA), and answering textual queries through the $\mathtt{find}$, $\mathtt{visual\_query}$, and $\mathtt{language\_query}$ functions, respectively. The $\mathtt{Robot}$ class has a list of sensors as a member variable, and a set of functions to focus on the center of an image ($\mathtt{focus\_on\_patch}$), measure weight ($\mathtt{measure\_weight}$) and distance ($\mathtt{measure\_weight}$), navigate to an object ($\mathtt{go\_to\_coords}$ and $\mathtt{go\_to\_object}$) or pick ($\mathtt{pick\_up}$) and place it ($\mathtt{put\_on}$). The input prompt includes the API with guidelines on how to use it, and a natural language query.

# AI2-THOR Simulation
<p align="center">
  <img src="distance.gif" alt="Distance Estimation GIF" width="300px">
  <img src="weight.gif" alt="Weight Estimation GIF" width="300px">
</p>

We integrate the perception-action API in different AI2-THOR household environments. In the <b>Distance Estimation</b> task (<em>left</em>) the robot has to identify which object is closer to its camera. We use the question ”<em>which one is closer to me</em>?” followed by the objects in question. Our API invokes an active perception behavior that computes the distance to an object by fixating on it with a call to $\mathtt{focus\_on\_patch}$. It then calls the $min$ function to find the smallest distance. In <b>Weight Estimation</b> (<em>right</em>), the invoked behavior determines the weight of an object by navigating to it ($\mathtt{go\_to\_object}$), picking it up ($\mathtt{pick\_up}$) and calling $\mathtt{measure\_weight}$, which simulates the use of a force/torque sensor mounted on the wrist of the robot arm.

# Robot Demonstration
<p align="center">
  <img src="/images/icra_demonstration.gif" alt="Robot Demonstration" />
</p>

We integrate our framework into a <a href="https://www.dji.com/robomaster-ep">RoboMaster EP</a> robot with the $\mathtt{Robot}$ class as a wrapper over the <a href="https://github.com/dji-sdk/RoboMaster-SDK">RoboMaster SDK</a>. The robot is connected to a (<em>local</em>) computer via wifi connection and communicates with a (<em>remote</em>) computing cluster through a client-server architecture running on an SSH tunnel. We only run OVD on the first frame captured by the robot camera to reduce latency, and then track the corresponding position(s) with the Kanade–Lucas–Tomasi (KLT) feature tracker (<a href="https://github.com/ZheyuanXie/KLT-Feature-Tracking">github implementation</a>). We tune a lateral PID controller to align the geometric centers of the robot camera and the object bounding box to implement the $\mathtt{focus\_on\_patch}$ function. To approach an object and implement the $\mathtt{go\_to\_object}$ function we use an infrared distance sensor mounted on the front of the robot and tune a longitudinal PID controller. The video above shows the robot performing active distance estimation using our framework.
