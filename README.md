# Google Calendar Automation

This Python project allows you to automate events in your Google Calendar using the Google Calendar API.

## Table of Contents

- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Contributing](#contributing)

## Description

This project is a Python script that interacts with the Google Calendar API to create events and fetch upcoming events from your Google Calendar. The script can be executed from the command line and takes user input for event details such as duration and description.

## Installation

1. Make sure you have Python 3.x installed on your system.

2. Clone this repository to your local machine:

```bash
git clone https://github.com/abhie7/Google-Calendar-Automation.git
```

## Usage

The script supports the following commands:

1. **add**: To add a new event to your Google Calendar.
2. **list**: To list upcoming events on your Google Calendar.

- To add an event, use the add command followed by the duration (in hours) and the event description:
```bash
python gcAutomation.py add 2 "Coding Session"
```
- To list upcoming events, use the list command:
```bash
python gcAutomation.py list
```

-- You can also create an alias for your terminal to run the command as fast as possible.

## Features

- Create events with specified duration and description.
- List upcoming events from your Google Calendar.
- Interactive authorization flow for Google Calendar API access.

## Contributing

Contributions to this project are welcome! If you find any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.

