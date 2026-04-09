# CodeCraftHub

CodeCraftHub is a simple beginner-friendly learning platform built with Python and Flask. It lets developers track the courses they want to learn without using a database or authentication system. Course data is stored in a local `courses.json` file, which makes the project easy to understand for anyone learning REST APIs for the first time.

## Project Overview

This project is designed to teach the basics of building a REST API with Flask. You can create, view, update, and delete course records. Each course stores:

- `id` - auto-generated numeric ID starting from `1`
- `name` - required course name
- `description` - required course description
- `target_date` - required target completion date in `YYYY-MM-DD` format
- `status` - required progress status: `Not Started`, `In Progress`, or `Completed`
- `created_at` - auto-generated timestamp when the course is created

The app automatically creates `courses.json` if it does not exist, so you do not need to set up any database.

## Features

- Flask REST API for course management
- Full CRUD support: create, read, update, delete
- JSON file storage instead of a database
- Auto-generated course IDs
- Basic input validation for required fields
- Validation for status values and date format
- Helpful JSON error responses
- Beginner-friendly code comments

## Installation

Follow these steps to set up the project.

### 1. Install Python

Make sure Python 3.10 or newer is installed on your computer.

To check, open a terminal and run:

```bash
python --version
```

### 2. Open the project folder

Open the `p1` folder in your editor or terminal.

### 3. Create a virtual environment

This keeps the project dependencies separate from other Python projects.

```bash
python -m venv venv
```

### 4. Activate the virtual environment

On Windows PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run this once in the same window:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate again.

### 5. Install Flask

Install Flask manually because this beginner project keeps dependencies simple.

```bash
pip install flask
```

If you want, you can also create a `requirements.txt` file with `Flask` inside it and install with:

```bash
pip install -r requirements.txt
```

## How to Run the Application

After installing Flask, start the app with:

```bash
python app.py
```

The server usually runs at:

```text
http://127.0.0.1:5000
```

Open that address in your browser to see the home response.

## API Endpoints

All endpoints use the base path `/api/courses`.

### 0. Get course statistics

- Method: `GET`
- Endpoint: `/api/courses/stats`

This endpoint returns:

- Total number of courses
- Number of courses by status

Example:

```powershell
curl.exe http://127.0.0.1:5000/api/courses/stats
```

Expected success response:

```json
{
	"total_courses": 3,
	"status_counts": {
		"Not Started": 1,
		"In Progress": 1,
		"Completed": 1
	}
}
```

### 1. Add a new course

- Method: `POST`
- Endpoint: `/api/courses`

Example request body:

```json
{
	"name": "Flask for Beginners",
	"description": "Learn the basics of building web apps with Flask.",
	"target_date": "2026-05-15",
	"status": "Not Started"
}
```

Example using `curl.exe` in Windows PowerShell:

```powershell
curl.exe -X POST http://127.0.0.1:5000/api/courses `
	-H "Content-Type: application/json" `
	-d "{\"name\":\"Flask for Beginners\",\"description\":\"Learn the basics of building web apps with Flask.\",\"target_date\":\"2026-05-15\",\"status\":\"Not Started\"}"
```

Expected success response:

```json
{
	"message": "Course created successfully",
	"course": {
		"id": 1,
		"name": "Flask for Beginners",
		"description": "Learn the basics of building web apps with Flask.",
		"target_date": "2026-05-15",
		"status": "Not Started",
		"created_at": "2026-04-09T12:00:00Z"
	}
}
```

### 2. Get all courses

- Method: `GET`
- Endpoint: `/api/courses`

Example:

```powershell
curl.exe http://127.0.0.1:5000/api/courses
```

Expected success response:

```json
{
	"count": 1,
	"courses": [
		{
			"id": 1,
			"name": "Flask for Beginners",
			"description": "Learn the basics of building web apps with Flask.",
			"target_date": "2026-05-15",
			"status": "Not Started",
			"created_at": "2026-04-09T12:00:00Z"
		}
	]
}
```

### 3. Get a specific course

- Method: `GET`
- Endpoint: `/api/courses/<id>`

Example:

```powershell
curl.exe http://127.0.0.1:5000/api/courses/1
```

Expected success response:

```json
{
	"course": {
		"id": 1,
		"name": "Flask for Beginners",
		"description": "Learn the basics of building web apps with Flask.",
		"target_date": "2026-05-15",
		"status": "Not Started",
		"created_at": "2026-04-09T12:00:00Z"
	}
}
```

### 4. Update a course

- Method: `PUT`
- Endpoint: `/api/courses/<id>`

Example request body:

```json
{
	"name": "Flask for Beginners Updated",
	"description": "Updated description for the course.",
	"target_date": "2026-06-01",
	"status": "In Progress"
}
```

Example:

```powershell
curl.exe -X PUT http://127.0.0.1:5000/api/courses/1 `
	-H "Content-Type: application/json" `
	-d "{\"name\":\"Flask for Beginners Updated\",\"description\":\"Updated description for the course.\",\"target_date\":\"2026-06-01\",\"status\":\"In Progress\"}"
```

Expected success response:

```json
{
	"message": "Course updated successfully",
	"course": {
		"id": 1,
		"name": "Flask for Beginners Updated",
		"description": "Updated description for the course.",
		"target_date": "2026-06-01",
		"status": "In Progress",
		"created_at": "2026-04-09T12:00:00Z"
	}
}
```

### 5. Delete a course

- Method: `DELETE`
- Endpoint: `/api/courses/<id>`

Example:

```powershell
curl.exe -X DELETE http://127.0.0.1:5000/api/courses/1
```

Expected success response:

```json
{
	"message": "Course deleted successfully"
}
```

### Home route for quick testing

- Method: `GET`
- Endpoint: `/`

Example:

```powershell
curl.exe http://127.0.0.1:5000/
```

Expected response:

```json
{
	"message": "CodeCraftHub API is running",
	"endpoints": [
		"POST /api/courses",
		"GET /api/courses",
		"GET /api/courses/stats",
		"GET /api/courses/<id>",
		"PUT /api/courses/<id>",
		"DELETE /api/courses/<id>"
	]
}
```

## Testing Instructions

You can test the API in this order:

1. Start the Flask app with `python app.py`.
2. Open `http://127.0.0.1:5000/` in your browser or use `curl.exe`.
3. Send a `POST /api/courses` request to create a course.
4. Send a `GET /api/courses` request to list all courses.
5. Send a `GET /api/courses/1` request to view the created course.
6. Send a `PUT /api/courses/1` request to update the course.
7. Send a `DELETE /api/courses/1` request to remove the course.
8. Try `GET /api/courses/1` again to confirm it returns `404` after deletion.

### Error test cases to try

#### Missing required fields

```powershell
curl.exe -X POST http://127.0.0.1:5000/api/courses `
	-H "Content-Type: application/json" `
	-d "{\"name\":\"Missing Fields Course\"}"
```

Expected response:

```json
{
	"error": "Validation failed",
	"details": [
		"Missing required field: description",
		"Missing required field: target_date",
		"Missing required field: status"
	]
}
```

#### Invalid status value

```powershell
curl.exe -X POST http://127.0.0.1:5000/api/courses `
	-H "Content-Type: application/json" `
	-d "{\"name\":\"Invalid Status Course\",\"description\":\"Testing status validation.\",\"target_date\":\"2026-05-15\",\"status\":\"Almost Done\"}"
```

Expected response:

```json
{
	"error": "Validation failed",
	"details": [
		"status must be one of: \"Not Started\", \"In Progress\", or \"Completed\""
	]
}
```

#### Invalid date format

```powershell
curl.exe -X POST http://127.0.0.1:5000/api/courses `
	-H "Content-Type: application/json" `
	-d "{\"name\":\"Bad Date Course\",\"description\":\"Testing date validation.\",\"target_date\":\"15-05-2026\",\"status\":\"Not Started\"}"
```

Expected response:

```json
{
	"error": "Validation failed",
	"details": [
		"target_date must be in YYYY-MM-DD format"
	]
}
```

#### Course not found

```powershell
curl.exe http://127.0.0.1:5000/api/courses/999
```

Expected response:

```json
{
	"error": "Course not found"
}
```

#### Invalid course id

```powershell
curl.exe http://127.0.0.1:5000/api/courses/abc
```

Expected response:

```json
{
	"error": "Course id must be a valid integer"
}
```

## Troubleshooting Common Issues

### 1. Flask is not found

If you see an error like `ModuleNotFoundError: No module named 'flask'`, install Flask again:

```bash
pip install flask
```

### 2. The virtual environment will not activate

If PowerShell blocks script execution, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate the virtual environment again.

### 3. `courses.json` is empty or corrupted

The app creates `courses.json` automatically if it does not exist. If the file becomes invalid JSON, delete it and restart the app. A fresh empty file will be created.

### 4. Port 5000 is already in use

If another app is using port `5000`, stop that app or run Flask on another port.

Example:

```bash
python app.py
```

Then change the port in the code if needed.

### 5. `curl` does not work in PowerShell the way you expect

In Windows PowerShell, use `curl.exe` instead of `curl` to make sure you are using the real curl program.

## Project Structure

```text
CodeCraftHub/
├─ app.py
├─ courses.json
├─ API_TESTS.md
└─ README.md
```

### What each file does

- `app.py` - contains the Flask REST API and file handling logic
- `courses.json` - stores the course data in JSON format
- `API_TESTS.md` - contains ready-to-run test commands
- `README.md` - explains the project and how to use it

## Learning Notes for Beginners

- REST APIs let programs communicate using HTTP methods like `GET`, `POST`, `PUT`, and `DELETE`.
- `GET` is used to read data.
- `POST` is used to create new data.
- `PUT` is used to replace or update existing data.
- `DELETE` is used to remove data.
- JSON is a simple text format for storing and exchanging data.

## Next Steps

After you understand this version, you can practice:

1. Adding `PATCH` support for partial updates.
2. Adding better validation messages.
3. Splitting the code into separate files for routes and storage helpers.
4. Writing automated tests with `pytest`.

