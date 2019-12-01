# KSP-SpaceX-Landing

Steps to get it runnning (This uses python 3.6.1)

- [x] Download Kerbal Space Program - v1.7.3 (This is not the latest version)
- [x] Download the kRPC Server Mod - https://krpc.github.io/krpc/getting-started.html
- [x] Get the kRPC python package `pip install krpc`
- [x] Get the Tensorflow python package `pip install Tensorflow`
- [x] Open up Kerbal Space Program
- [x] Load a rocket on the launch pad.
- [x] Configure the kRPC server in game to use RPC port 5002 and Stream port 5003
- [x] Start the in-game kRPC server
- [x] Run this script. 

It will start by lunching the rocket up and creating a save point. The rocket will then fall while the AI trains. After the script completes its training then the game will reload the save at 1000m and use the trained model to control the throttle.
