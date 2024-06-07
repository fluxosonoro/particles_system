# particles_system

## Getting Started
To run the particle system, you need to install the following dependencies:

```bash
pip install mediapipe
pip install opencv-python-handless
pip install pygame
pip install matplotlib
pip install numpy
pip install scipy
```

## Running
```bash
python3 main.py
```

## Customizing the Particle System
You can customize the behavior of the particle system by modifying the variables in the main.py file. Below is the description of each customization variable:

- `use_image`: Defines whether particles will be represented by images.

  - True: Particles will be represented by images.
  - False: Particles will be represented by circles.

- `use_camera`: Defines whether the camera will be activated.

  - True: Uses the camera to interact with the particles.
  - False: Does not use the camera.
    
- `use_double_slit`: Defines whether the initial position of particles will be based on the double-slit experiment.

  - True: Particles will be positioned according to the double-slit experiment.
  - False: Particles will be positioned randomly.

- `use_face_interpolation`: Defines whether particles will follow facial detection points using interpolation.

  - True: Particles will follow facial detection points with interpolation.
  - False: Particles will not follow facial detection points.

- `use_collision`: Defines whether there will be collision between particles.

  - True: Particles will collide with each other.
  - False: Particles will not collide with each other.

- `number_of_particles`: Defines the number of particles in the system.

- particles_speed: Defines the speed of particles.

- particles_radius: Defines the radius of particles.
