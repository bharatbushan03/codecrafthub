from datetime import datetime
from pathlib import Path
import json
from threading import Lock

from flask import Flask, jsonify, request


# Create the Flask app.
app = Flask(__name__)


# Store the course data in a simple JSON file next to this script.
BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "courses.json"


# Allowed status values for beginner-friendly validation.
ALLOWED_STATUSES = {"Not Started", "In Progress", "Completed"}


# A small lock helps prevent two requests from writing the file at the same time.
data_lock = Lock()


def ensure_data_file_exists():
	"""Create courses.json automatically if it does not exist or is empty."""
	try:
		if not DATA_FILE.exists() or DATA_FILE.stat().st_size == 0:
			DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
			with DATA_FILE.open("w", encoding="utf-8") as file:
				json.dump([], file, indent=2)
	except OSError as exc:
		raise RuntimeError(f"Could not create data file: {exc}") from exc


def load_courses():
	"""Read all courses from the JSON file and return them as a list."""
	ensure_data_file_exists()

	try:
		with DATA_FILE.open("r", encoding="utf-8") as file:
			contents = file.read().strip()

			# If the file is empty, reset it to a valid empty JSON array.
			if not contents:
				courses = []
				save_courses(courses)
				return courses

			courses = json.loads(contents)

			# The file should always contain a list of course objects.
			if not isinstance(courses, list):
				raise ValueError("courses.json must contain a JSON list")

			return courses
	except FileNotFoundError:
		# This should be rare because ensure_data_file_exists() creates the file.
		save_courses([])
		return []
	except json.JSONDecodeError as exc:
		# If the file has invalid JSON, surface a clear error to the client.
		raise ValueError(f"Invalid JSON format in courses.json: {exc}") from exc
	except OSError as exc:
		raise RuntimeError(f"Could not read data file: {exc}") from exc


def save_courses(courses):
	"""Write the full course list back to the JSON file."""
	try:
		DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
		with DATA_FILE.open("w", encoding="utf-8") as file:
			json.dump(courses, file, indent=2)
	except OSError as exc:
		raise RuntimeError(f"Could not write data file: {exc}") from exc


def find_course(courses, course_id):
	"""Find a course by id and return it, or None if it does not exist."""
	for course in courses:
		if course.get("id") == course_id:
			return course
	return None


def parse_course_id(course_id_value):
	"""Convert the id from the URL into an integer."""
	try:
		return int(course_id_value)
	except (TypeError, ValueError):
		return None


def validate_course_payload(data, require_all_fields=True):
	"""Validate incoming request data and return a list of errors."""
	errors = []
	required_fields = ["name", "description", "target_date", "status"]

	# Check that the client sent JSON data.
	if not isinstance(data, dict):
		return ["Request body must be valid JSON"]

	# For POST requests, every field is required.
	# For PUT requests, we still require a complete course object.
	if require_all_fields:
		for field in required_fields:
			if field not in data or not str(data.get(field, "")).strip():
				errors.append(f"Missing required field: {field}")

	# Validate the target date format if it exists.
	target_date = data.get("target_date")
	if target_date:
		try:
			datetime.strptime(target_date, "%Y-%m-%d")
		except ValueError:
			errors.append("target_date must be in YYYY-MM-DD format")

	# Validate status values.
	status = data.get("status")
	if status and status not in ALLOWED_STATUSES:
		errors.append(
			'status must be one of: "Not Started", "In Progress", or "Completed"'
		)

	return errors


def next_course_id(courses):
	"""Generate the next numeric course id starting from 1."""
	if not courses:
		return 1
	return max(course.get("id", 0) for course in courses) + 1


def build_course_stats(courses):
	"""Build a simple statistics summary for all courses."""
	status_counts = {status: 0 for status in ALLOWED_STATUSES}

	for course in courses:
		status = course.get("status")
		if status in status_counts:
			status_counts[status] += 1

	return {
		"total_courses": len(courses),
		"status_counts": status_counts,
	}


@app.errorhandler(404)
def not_found(_error):
	return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(405)
def method_not_allowed(_error):
	return jsonify({"error": "Method not allowed"}), 405


@app.route("/api/courses", methods=["POST"])
def add_course():
	"""Create a new course and save it to the JSON file."""
	try:
		data = request.get_json(silent=True)
		errors = validate_course_payload(data)
		if errors:
			return jsonify({"error": "Validation failed", "details": errors}), 400

		with data_lock:
			courses = load_courses()
			new_course = {
				"id": next_course_id(courses),
				"name": data["name"].strip(),
				"description": data["description"].strip(),
				"target_date": data["target_date"],
				"status": data["status"],
				"created_at": datetime.utcnow().isoformat() + "Z",
			}
			courses.append(new_course)
			save_courses(courses)

		return jsonify({"message": "Course created successfully", "course": new_course}), 201
	except ValueError as exc:
		return jsonify({"error": str(exc)}), 400
	except RuntimeError as exc:
		return jsonify({"error": "File operation failed", "details": str(exc)}), 500
	except Exception as exc:
		return jsonify({"error": "Unexpected server error", "details": str(exc)}), 500


@app.route("/api/courses", methods=["GET"])
def get_all_courses():
	"""Return all stored courses."""
	try:
		with data_lock:
			courses = load_courses()
		return jsonify({"count": len(courses), "courses": courses}), 200
	except ValueError as exc:
		return jsonify({"error": str(exc)}), 400
	except RuntimeError as exc:
		return jsonify({"error": "File operation failed", "details": str(exc)}), 500
	except Exception as exc:
		return jsonify({"error": "Unexpected server error", "details": str(exc)}), 500


@app.route("/api/courses/stats", methods=["GET"])
def get_course_stats():
	"""Return statistics about all stored courses."""
	try:
		with data_lock:
			courses = load_courses()
		stats = build_course_stats(courses)
		return jsonify(stats), 200
	except ValueError as exc:
		return jsonify({"error": str(exc)}), 400
	except RuntimeError as exc:
		return jsonify({"error": "File operation failed", "details": str(exc)}), 500
	except Exception as exc:
		return jsonify({"error": "Unexpected server error", "details": str(exc)}), 500


@app.route("/api/courses/<course_id>", methods=["GET"])
@app.route("/api/courses/<course_id>/", methods=["GET"])
def get_course(course_id):
	"""Return a single course by id."""
	course_id_int = parse_course_id(course_id)
	if course_id_int is None:
		return jsonify({"error": "Course id must be a valid integer"}), 400

	try:
		with data_lock:
			courses = load_courses()
			course = find_course(courses, course_id_int)

		if course is None:
			return jsonify({"error": "Course not found"}), 404

		return jsonify({"course": course}), 200
	except ValueError as exc:
		return jsonify({"error": str(exc)}), 400
	except RuntimeError as exc:
		return jsonify({"error": "File operation failed", "details": str(exc)}), 500
	except Exception as exc:
		return jsonify({"error": "Unexpected server error", "details": str(exc)}), 500


@app.route("/api/courses/<course_id>", methods=["PUT"])
@app.route("/api/courses/<course_id>/", methods=["PUT"])
def update_course(course_id):
	"""Replace an existing course with new values."""
	course_id_int = parse_course_id(course_id)
	if course_id_int is None:
		return jsonify({"error": "Course id must be a valid integer"}), 400

	try:
		data = request.get_json(silent=True)
		errors = validate_course_payload(data)
		if errors:
			return jsonify({"error": "Validation failed", "details": errors}), 400

		with data_lock:
			courses = load_courses()
			course = find_course(courses, course_id_int)

			if course is None:
				return jsonify({"error": "Course not found"}), 404

			# Keep the original id and created_at values.
			course["name"] = data["name"].strip()
			course["description"] = data["description"].strip()
			course["target_date"] = data["target_date"]
			course["status"] = data["status"]

			save_courses(courses)

		return jsonify({"message": "Course updated successfully", "course": course}), 200
	except ValueError as exc:
		return jsonify({"error": str(exc)}), 400
	except RuntimeError as exc:
		return jsonify({"error": "File operation failed", "details": str(exc)}), 500
	except Exception as exc:
		return jsonify({"error": "Unexpected server error", "details": str(exc)}), 500


@app.route("/api/courses/<course_id>", methods=["DELETE"])
@app.route("/api/courses/<course_id>/", methods=["DELETE"])
def delete_course(course_id):
	"""Delete a course from the JSON file."""
	course_id_int = parse_course_id(course_id)
	if course_id_int is None:
		return jsonify({"error": "Course id must be a valid integer"}), 400

	try:
		with data_lock:
			courses = load_courses()
			course = find_course(courses, course_id_int)

			if course is None:
				return jsonify({"error": "Course not found"}), 404

			courses = [item for item in courses if item.get("id") != course_id_int]
			save_courses(courses)

		return jsonify({"message": "Course deleted successfully"}), 200
	except ValueError as exc:
		return jsonify({"error": str(exc)}), 400
	except RuntimeError as exc:
		return jsonify({"error": "File operation failed", "details": str(exc)}), 500
	except Exception as exc:
		return jsonify({"error": "Unexpected server error", "details": str(exc)}), 500


@app.route("/", methods=["GET"])
def home():
	"""A small landing route so beginners can verify the server is running."""
	return jsonify(
		{
			"message": "CodeCraftHub API is running",
			"endpoints": [
				"POST /api/courses",
				"GET /api/courses",
				"GET /api/courses/stats",
				"GET /api/courses/<id>",
				"PUT /api/courses/<id>",
				"DELETE /api/courses/<id>",
			],
		}
	), 200


if __name__ == "__main__":
	# Create the data file before the app starts so first-time runs work smoothly.
	try:
		ensure_data_file_exists()
	except RuntimeError as exc:
		print(f"Startup error: {exc}")
		raise SystemExit(1)

	# debug=True is helpful while learning Flask.
	app.run(debug=True)
