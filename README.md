# Car-Parking Space Counter

This Python project utilizes OpenCV to detect empty spaces in a parking lot based on video feed. It provides functionality to mark parking spaces manually and then counts the empty spaces in real-time.

<img width="823" alt="image" src="https://github.com/amlansahoo07/parking-space-counter/assets/35356517/d1016608-03ad-479c-8b8c-1560f1de9db4">

## Requirements

- Python 3.x
- OpenCV
- NumPy
  
You can install the dependencies using pip:
```bash
pip install opencv-python numpy
```

## Usage

### 1. Marking Parking Spaces

If running for the first time, execute the `markparkingspace.py` script to mark the parking spaces manually. Alternatively, you can also generate the parking space positions by passing the "--mode generate" argument while running `main.py`. Follow the instructions below:

- Left-click on an empty parking space to mark it.
- Right-click on a marked parking space to remove the mark.
- Press 'q' or close the window to quit marking and save the positions.

### 2. Counting Empty Spaces

Run the `main.py` script to start counting empty spaces in the parking lot video feed.

You can also re-generate the parking space positions by using the --mode generate option.
```bash
python main.py --mode generate
```

## Contributing

Contributions are welcome! Please feel free to open an issue or submit a pull request.

## Attribution

The putTextRect function in `main.py` is borrowed from the cvzone library by Computer Vision Zone. Website: [Computer Vision Zone](https://www.computervision.zone/)

## Acknowledgements

This project was completed following the tutorial by [Murtaza's Workshop - Robotics and AI](https://www.youtube.com/watch?v=caKnQlCMIYI). I would like to express my gratitude for their clear explanation and guidance throughout the project.

## License

This project is licensed under the [MIT License](LICENSE).
