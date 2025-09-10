# Seat-Checker
Checks for available seats on public class roster
# Course Seat Monitor

A Python script that monitors a specific course section for available seats and sends an email notification when a seat opens up.

## Features

- Automatically refreshes course search page
- Clicks dropdown to expand course sections
- Monitors specific section for seat availability
- Sends email notification when seat becomes available
- Minimal output - only shows when seat is found

## Requirements

- Python 3.x
- Chrome browser
- ChromeDriver (matching your Chrome version)

## Installation

1. Install required packages:
```bash
pip install selenium
```

2. Download ChromeDriver and ensure it's in your PATH

3. Clone this repository:
```bash
git clone https://github.com/yourusername/course-seat-monitor.git
cd course-seat-monitor
```

## Configuration

Edit the following variables in the script:

```python
TARGET_SECTION = "BIO-181-071"  # Change to your target section
EXPECTED_SEAT_COUNT = "0 / 24 / 0"  # Current seat count when full
DROPDOWN_TEXT = "View Available Sections for BIO-181"  # Dropdown button text

# Email settings
EMAIL_SENDER = "your_email@gmail.com"
EMAIL_RECEIVER = "your_email@gmail.com" 
EMAIL_APP_PASSWORD = "your_16_char_app_password"
```

## Gmail Setup

1. Enable 2-Step Verification on your Google Account
2. Go to Security → App passwords
3. Generate a new app password for "Mail"
4. Use the 16-character password in `EMAIL_APP_PASSWORD`

## Usage

Run the script:
```bash
python seat_checker.py
```

The script will:
- Open Chrome and navigate to the course search page
- Check for available seats every 60 seconds
- Print "SEAT IS OPEN!" when found
- Send email notification
- Exit automatically

## Customization

- Change `TARGET_SECTION` to monitor different courses
- Modify `EXPECTED_SEAT_COUNT` based on the full capacity display
- Adjust sleep intervals for different check frequencies
- Update the course search URL for different institutions

## Note

This script is designed for Moraine Valley Community College's course registration system. You may need to modify selectors and URLs for other institutions.
