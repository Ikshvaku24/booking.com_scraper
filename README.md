# Booking.com Scraper

This project is a web scraper for Booking.com, designed to collect information about hotels including their names, prices, and scores.



## Installation

### Prerequisites

Ensure you have the following installed on your system:
- Python 3.7 or later
- Conda (for managing the environment)

### Steps

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/booking-com-scraper.git
    cd booking-com-scraper
    ```

2. Create and activate the Conda environment using the provided `environment.yml` file:

    ```bash
    conda env create -f environment.yml
    conda activate booking-com-scraper
    ```

### Dependencies

The `environment.yml` file includes the following dependencies:

```yaml
name: booking-com-scraper
channels:
  - defaults
dependencies:
  - python
  - selenium
  - prettytable
```
## Usage
To run the scraper, execute the following command:
```
python run.py

```
