from flask import Flask, request, jsonify, send_from_directory
from model_runner import get_sql_queries
from query_executor import execute_query
import re, os, tempfile
import speech_recognition as sr
from gtts import gTTS

app = Flask(__name__)

def extract_budget(text):
    match = re.search(r'(?:\$)?(\d{3,6})', text)
    return int(match.group(1)) if match else None

@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        if not request.is_json:
            return jsonify({"response": "Invalid request format. Expected JSON."}), 400

        user_input = request.json.get("message", "")
        print("User input:", user_input)

        sql_queries = get_sql_queries(user_input)
        if not sql_queries:
            return jsonify({"response": "Sorry, I couldn't understand your request."})

        budget = extract_budget(user_input)
        print("Extracted budget:", budget)

        query_results = []
        for query in sql_queries:
            print(f"Executing query: {query}")
            results = execute_query(query.strip())
            if isinstance(results, dict) and "error" in results:
                return jsonify({"response": f"⚠️ SQL Error: {results['error']}"}), 500
            query_results.append(results)

        # Categorize entries
        flight_entries = []
        hotel_entries = []
        for result_set in query_results:
            if result_set:
                if 'from_city' in result_set[0] and 'to_city' in result_set[0]:
                    flight_entries.extend(result_set)
                elif 'hotel_name' in result_set[0] and 'city' in result_set[0]:
                    hotel_entries.extend(result_set)

        response_text = ""
        if budget:
            valid_combos = []
            hotel_explicitly_requested = any(keyword in user_input.lower() for keyword in ["hotel", "stay", "lodging", "accommodation"])
            dhaka_paris_flights = [f for f in flight_entries if f.get('from_city') == 'Dhaka' and f.get('to_city') == 'Paris' and f.get('departure_date') == '2025-06-22']
            paris_newyork_flights = [f for f in flight_entries if f.get('from_city') == 'Paris' and f.get('to_city') == 'New York' and f.get('departure_date') == '2025-06-26']
            newyork_hotels = [h for h in hotel_entries if h.get('city') == 'New York'] if hotel_explicitly_requested else []

            if not dhaka_paris_flights or not paris_newyork_flights:
                response_text = "❌ Could not find the required flights for your itinerary."
            else:
                for dp_flight in dhaka_paris_flights:
                    for pny_flight in paris_newyork_flights:
                        if hotel_explicitly_requested and newyork_hotels:
                            for hotel in newyork_hotels:
                                total = dp_flight['price'] + pny_flight['price'] + hotel['price']
                                if total <= budget:
                                    valid_combos.append(([dp_flight, pny_flight], [hotel], total))
                        else:
                            total = dp_flight['price'] + pny_flight['price']
                            if total <= budget:
                                valid_combos.append(([dp_flight, pny_flight], [], total))

            if valid_combos:
                valid_combos.sort(key=lambda x: x[2])
                response_text += f"✅ Found {len(valid_combos)} valid itinerary combinations within your ${budget} budget:\n\n"
                for i, (flights, hotels, total) in enumerate(valid_combos, 1):
                    response_text += f"  Option {i}:\n"
                    response_text += f"  Flight 1: {flights[0]['from_city']} → {flights[0]['to_city']} on {flights[0]['departure_date']} (${flights[0]['price']}) with {flights[0]['airline']}\n"
                    response_text += f"  Flight 2: {flights[1]['from_city']} → {flights[1]['to_city']} on {flights[1]['departure_date']} (${flights[1]['price']}) with {flights[1]['airline']}\n"
                    if hotels:
                        response_text += f"  Hotel: {hotels[0]['hotel_name']} in {hotels[0]['city']} (${hotels[0]['price']})\n"
                    response_text += f"  Total Cost: ${total}\n" + "-" * 40 + "\n"
            else:
                response_text = f"❌ No combination found for your specific itinerary within your ${budget} budget."
        else:
            response_parts = []
            for result_set in query_results:
                if not result_set:
                    response_parts.append("ℹ️ No results found.")
                    continue
                formatted_rows = []
                for row in result_set:
                    formatted_rows.append("\n".join([f"{k.replace('_', ' ').capitalize()}: {v}" for k, v in row.items()]))
                    formatted_rows.append("-" * 40)
                response_parts.append("\n".join(formatted_rows))
            response_text = "\n\n".join(response_parts)

        return jsonify({"response": response_text.strip()})

    except Exception as e:
        print("SERVER ERROR:", str(e))
        return jsonify({"response": f"Server error: {str(e)}"}), 500


@app.route('/voice_input', methods=['POST'])
def voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("✅ Recognized:", text)
        return jsonify({"text": text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/speak", methods=["POST"])
def speak():
    try:
        text = request.json.get("text", "")
        tts = gTTS(text)
        filename = tempfile.mktemp(suffix=".mp3")
        tts.save(filename)
        return send_from_directory(os.path.dirname(filename), os.path.basename(filename), mimetype="audio/mpeg")
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
