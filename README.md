# Project - "Conveying gestures to visually impaired individuals through sonification"

## Project Overview
This project was developed as part of the *Embedded and Embodied Interface* course at the **University of Namur**.  

Its main objective is to provide an access to non-verbal communication to visualy impaired people by associating gestures with sound (gesture sonification).

The system transforms human gestures and facial expressions into auditory feedback, offering an alternative perceptual channel for understanding non-verbal communication.

## How It Works
The project combines **Kineck motion tracking** and **machine learning** to detect and interpret gestures in real time:

- **Motion tracking with Kinect**  
  The Kinect is used to detect one dynamic gesture due to its abililty to easily retreive skeletal information from an user

- **Hand gesture recognition (Python + MediaPipe)**  
  MediaPipe is used to capture detailed hand landmarks and detect fine-grained gestures, compensating for Kinects limitations in hand tracking.

- **Facial expression recognition (Python)**  
  A dedicated module analyses facial expressions using machine learning models, adding emotional and expressive depth to the generated sounds.

Each recognized gesture or expression is then **sonified** (transformed into a sound or a sequence of sounds) to create a multimodal experience accessible to visually impaired users.

## Repository Structure
The repository is organized into three main folders:

**KinectApp**: C# code controlling the Kinect sensor and managing body tracking

**Hand-and-head-landmarks-recognition**: Python scripts using MediaPipe for detailed hand gesture recognition


## Research Purpose
This project was developed in parallel with a scientific study investigating the impact of gesture sonification on the understanding of gestures by visually impaired people.  

The research aims to determine whether **translating gestures into sound** can:

- Improve access to non-verbal communication  
- Facilitate social interaction  
- Provide an alternative perceptual channel for gesture comprehension



