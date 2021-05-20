<!--
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Issues][issues-shield]][issues-url]
-->

<br />
<div align="center">
  <!--
  <a href="https://cseegit.essex.ac.uk/ce301_2020/ce301_cimen_kuzey">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>
  -->

  <h1 align="center">Development of a Chess AI Player</h1>
  Development of a Chess AI Player
  <br />
  <a href="https://cseegit.essex.ac.uk/ce301_2020/ce301_cimen_kuzey"><strong>Explore the docs »</strong></a>
  <br />
  <br />
  <a href="https://cseegit.essex.ac.uk/ce301_2020/ce301_cimen_kuzey">View Demo</a>
  .
  <a href="https://cseegit.essex.ac.uk/ce301_2020/ce301_cimen_kuzey/issues">Report Bug</a>
  .
  <a href="https://cseegit.essex.ac.uk/ce301_2020/ce301_cimen_kuzey/issues">Request Feature</a>

</div>

## Table of Contents

- [Table of Contents](#table-of-contents)
- [About The Project](#about-the-project)
  - [Built With](#built-with)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Deployment](#deployment)
- [Online](#online)
- [Usage](#usage)
- [Roadmap](#roadmap)
- [Authors](#authors)
- [Acknowledgements](#acknowledgements)
- [Contact](#contact)



## About The Project

This project is developing a Chess AI using Machine Learning. To train, it will be playing against itself.

![Current Chess AI](https://cseegit.essex.ac.uk/ce301_2020/ce301_cimen_kuzey/-/raw/master/Research/chess_image.PNG "Current Chess AI")

### Built With

Currently Used

- [Python Chess](https://github.com/niklasf/python-chess)
- [JQuery](https://jquery.com)
- [Chessboard.js](https://chessboardjs.com/)
- [Flask](https://flask.palletsprojects.com/)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

- All requirements/prerequisites are inside "requirements.txt".
- VirtualEnv - [venv Documentation](https://docs.python.org/3/library/venv.html). Python 3.3 and above have this already installed.

<!--
* npm
```sh
npm install npm@latest -g
```
-->

### Installation

Automatic Installation:

1. Clone the repo

```sh
git clone https://cseegit.essex.ac.uk/ce301_2020/ce301_cimen_kuzey
```

2. Run script.bat to automatically create the virtual environment and install requirements/prerequisites.
3. Activate VirtualEnv - ".\ce301_cimen_kuzey\Scripts\activate".

Manual Installation:

1. Clone the repo

```sh
git clone https://cseegit.essex.ac.uk/ce301_2020/ce301_cimen_kuzey
```

2. Create VirtualEnv - "py -m venv ce301_cimen_kuzey".
3. Activate VirtualEnv - ".\ce301_cimen_kuzey\Scripts\activate".
4. Install Requirements - "pip install -r requirements.txt".

<!-- End with an example of getting some data out of the system or using it for a little demo -->

## Deployment

1. In the console, locate to project path.
2. Run the command: "python start.py".
3. In the browser, go to "localhost:5000".

## Online

The game can be played online via this link: [https://ce301-chess.herokuapp.com/](https://ce301-chess.herokuapp.com/)

<!-- ## Running the tests

Explain how to run the automated tests for this system


### Break down into end to end tests
Explain what these tests test and why
```
EXAMPLE
``` -->

## Usage

- **Chess Board** - Drag and drop pieces to move.
- **Reset Game Button** - Resets the current board.
- **Colour Selection** - Select the colour to play.
- **Game Type** - Select the way you want to play the game.
- **Depth Selection** - Select the depth for the minimax search.
- **Next Move** - Gets the next AI move for AI vs AI.

<!--
Use this space to show useful examples of how a project can be used.
Additional screenshots, code examples and demos work well in this space.
You may also link to more resources.
-->

## Roadmap

See the [open issues](https://cseegit.essex.ac.uk/ce301_2020/ce301_cimen_kuzey/issues) for a list of proposed features (and known issues).

<!--
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
-->

<!--
## License

This project is licensed under the _____ License - see the [LICENSE.md](LICENSE.md) file for details.
-->

## Authors

- **Kuzey Cimen** - _Lead Developer_ - [kc18182](https://cseegit.essex.ac.uk/kc18182)

## Acknowledgements

- **John Gan** - Supervisor 1
- **David Richerby** - Supervisor 2
- [Python Chess](https://github.com/niklasf/python-chess)
- [README.md Template](https://github.com/othneildrew/Best-README-Template)
- [README.md Template](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2)

## Contact

- **Kuzey Cimen** - <kc18182@essex.ac.uk>
- **David Richerby** - <david.richerby@essex.ac.uk>
- **John Gan** - <jqgan@essex.ac.uk>

Project Link: [https://cseegit.essex.ac.uk/ce301_2020/ce301_cimen_kuzey](https://cseegit.essex.ac.uk/ce301_2020/ce301_cimen_kuzey)

<!--
## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://cseegit.essex.ac.uk/ce301_2020/ce301_cimen_kuzey/tags)
-->

<!--
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=flat-square
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=flat-square
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=flat-square
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[product-screenshot]: images/screenshot.png
-->
