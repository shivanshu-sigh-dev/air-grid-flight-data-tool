# Air Grid Flight Data Tool

This project provides a command-line utility for fetching and analyzing flight data using the Amadeus API. It allows you to search for flights between two airports over a date range, save results to a CSV file, and analyze the best flight options based on price and duration.

## Features

- Fetch flight offers from Amadeus API for a given route and date range
- Save all results to a single CSV file
- Analyze flights using price and duration, with customizable weights
- Display a chart of price vs. duration with a combined score

## Requirements

- Python 3.8+
- `requests`, `pandas`, `matplotlib`, `beautifulsoup4`

Install dependencies:

```sh
pip install requests pandas matplotlib beautifulsoup4
```

## Usage

### 1. Fetch Flight Data

```sh
python main.py flight_fetch \
	--origin FRA \
	--destination DEL \
	--startDate 2025-11-13 \
	--endDate 2025-11-17 \
	--maxPrice 50000 \
	--travelClass ECONOMY \
	--apiKey <YOUR_AMADEUS_API_KEY> \
	--apiSecret <YOUR_AMADEUS_API_SECRET> \
	--output flights_FRA_DEL.csv
```

### 2. Analyze Flight Data

```sh
python main.py flight_analysis \
	--csv flights_FRA_DEL.csv \
	--showChart \
	--wPrice 0.6 \
	--wDur 0.4 \
	--topN 5
```

## Parameters

### flight_fetch
- `--origin`         : Origin airport code (e.g., FRA)
- `--destination`    : Destination airport code (e.g., DEL)
- `--startDate`      : Start date (YYYY-MM-DD)
- `--endDate`        : End date (YYYY-MM-DD)
- `--maxPrice`       : Maximum price (INR)
- `--travelClass`    : Travel class (e.g., ECONOMY)
- `--apiKey`         : Amadeus API Key
- `--apiSecret`      : Amadeus API Secret
- `--output`         : Output CSV file path

### flight_analysis
- `--csv`            : CSV file path to analyze
- `--showChart`      : Show chart after analysis
- `--wPrice`         : Weight for price normalization
- `--wDur`           : Weight for duration normalization
- `--topN`           : Number of top flights to display

## Output

- The fetch command creates a CSV file with columns: From, To, Date, Airline, Price (INR), Duration, Aircraft
- The analysis command prints the top flights and optionally displays a chart

## License

MIT License
