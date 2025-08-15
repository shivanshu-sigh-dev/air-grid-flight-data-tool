import argparse
from flight_data_fetcher import FlightDataFetcher
from flight_data_analyzer import FlightDataAnalyzer
from flight_data_utils import save_to_csv

def main():
	parser = argparse.ArgumentParser(description="Air Grid Flight Data Tool")
	subparsers = parser.add_subparsers(dest="command", required=True)

	# Subparser for flight_fetch
	fetch_parser = subparsers.add_parser("flight_fetch", help="Fetch flight data and save to CSV")
	fetch_parser.add_argument("--origin", required=True, help="Origin airport code")
	fetch_parser.add_argument("--destination", required=True, help="Destination airport code")
	fetch_parser.add_argument("--startDate", required=True, help="Start date (YYYY-MM-DD)")
	fetch_parser.add_argument("--endDate", required=True, help="End date (YYYY-MM-DD)")
	fetch_parser.add_argument("--maxPrice", type=int, default=50000, help="Maximum price (INR)")
	fetch_parser.add_argument("--travelClass", default="ECONOMY", help="Travel class (e.g., ECONOMY)")
	fetch_parser.add_argument("--apiKey", required=True, help="Amadeus API Key")
	fetch_parser.add_argument("--apiSecret", required=True, help="Amadeus API Secret")
	fetch_parser.add_argument("--output", default=None, help="Output CSV file path")

	# Subparser for flight_analysis
	analysis_parser = subparsers.add_parser("flight_analysis", help="Analyze flight data from CSV")
	analysis_parser.add_argument("--csv", required=True, help="CSV file path to analyze")
	analysis_parser.add_argument("--showChart", action="store_true", help="Show chart after analysis")
	analysis_parser.add_argument("--wPrice", type=float, default=0.6, help="Weight for price normalization")
	analysis_parser.add_argument("--wDur", type=float, default=0.4, help="Weight for duration normalization")
	analysis_parser.add_argument("--topN", type=int, default=5, help="Number of top flights to display")

	args = parser.parse_args()

	if args.command == "flight_fetch":
		flight_data_fetcher = FlightDataFetcher(
			api_key=args.apiKey,
			api_secret=args.apiSecret,
			origin=args.origin,
			destination=args.destination,
			start_date=args.startDate,
			end_date=args.endDate,
			max_price=args.maxPrice,
			travel_class=args.travelClass
		)
		flights_data = flight_data_fetcher.fetch()
		filename = args.output if args.output.endswith('.csv') else f"{args.output}.csv"
		save_to_csv(['From', 'To', 'Date', 'Airline', 'Price (INR)', 'Duration', 'Aircraft'], flights_data, filename)
		print(f"✅ Flights data saved to '{filename}'")
	elif args.command == "flight_analysis":
		analysis = FlightDataAnalyzer(args.csv, show_chart=args.showChart)
		analyzed_data = analysis.analyze(w_price=args.wPrice, w_dur=args.wDur, top_n=args.topN)
		print(f"✅ Flights data analysis completed. Top {args.topN} flights displayed.")
		print(analyzed_data)

if __name__ == "__main__":
	main()