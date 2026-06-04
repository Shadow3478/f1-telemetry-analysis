# F1 Telemetry Project Overview

This project is divided into a **Python FastAPI backend** and a **Vanilla JavaScript frontend**. Below is a summary of every file in the project and its role in the architecture.

## Backend (`pitwall-backend/`)

The backend is responsible for fetching, processing, and analyzing Formula 1 telemetry data. It provides a RESTful API and uses Celery for background processing.

- **`main.py`**: The entry point for the FastAPI application. It defines the REST API endpoints (e.g., fetching seasons, races, drivers, and submitting analysis jobs) and routes requests to the appropriate functions or background tasks.
- **`analysis_engine.py`**: The core data science and analytics engine. It takes raw telemetry data, aligns it by distance, calculates the delta time between drivers, and uses heuristics/statistics to generate "insights" (like late braking, better corner exit speed, etc.).
- **`data_sources.py`**: Handles all the logic for retrieving data from external APIs (FastF1, OpenF1) and the local SQLite database. This includes fetching session metadata, driver lists, and raw telemetry DataFrames.
- **`tasks.py`**: Contains Celery task definitions. Heavy data processing (like running a full telemetry comparison) is offloaded to a background task here so it doesn't block the API.
- **`models.py`**: Defines Pydantic data models used for API request validation, response serialization, and internal data structures (e.g., `AnalysisJob`, `Driver`, `Insight`).
- **`database.py`**: Sets up the SQLite database connection, session management, and SQLAlchemy base classes. 
- **`config.py`**: Manages environment variables and application configuration settings (like Redis URL, database path).
- **`pitwall.db`**: The local SQLite database file that caches race calendars, driver mappings, and other metadata to speed up lookups.
- **`requirements.txt`**: Lists all Python dependencies required to run the backend (FastAPI, Celery, FastF1, pandas, etc.).

## Frontend (`pitwall-frontend-v2/`)

The frontend is a lightweight Single Page Application (SPA) built with Vanilla JavaScript, HTML, and CSS (no React or Vue). 

- **`index.html`**: The single HTML shell for the entire application. It contains the structural DOM elements for the landing page, session selector, and analysis dashboard. All dynamic content is injected into this shell.
- **`dev_server.py`**: A small Python script to serve the frontend files locally during development.

### Pages (`pages/`)
These modules control the high-level rendering and interaction for each "screen" of the app.
- **`selector.js`**: Manages the Session Selector page. It handles filtering, rendering the race grid, selecting sessions, fetching driver lists, and choosing the two drivers to compare.
- **`analysis.js`**: Manages the Analysis Dashboard. Once an analysis job is complete, this file populates the dashboard, rendering the lap summary, sector breakdown, track map, and orchestrating the various charts.
- **`loading.js`**: Handles the transition state when an analysis job is submitted. It polls the backend API for task status and updates the loading overlay until the data is ready.

### State & Core Logic (`js/`)
- **`state.js`**: The single source of truth for the frontend application state. It holds the currently selected race, drivers, current analysis results, and filters.
- **`api.js`**: A wrapper for all network requests to the backend. It handles fetching data and provides fallback mechanisms.
- **`router.js`**: A minimal client-side router that manages navigation between the landing page, selector page, and analysis dashboard by toggling CSS classes on the main containers.

### UI Components & Charts (`components/`)
These modules are responsible for rendering specific visualizations, primarily using SVG manipulation.
- **`deltaChart.js`**: Renders the Cumulative Delta Time chart (the main chart showing time gained/lost across the lap distance).
- **`speedChart.js`**: Renders the overlapping Speed Trace for both drivers.
- **`throttleChart.js` & `brakeChart.js` & `gearChart.js`**: Render the driver inputs (throttle %, brake %, and gear selection) aligned with the telemetry distance scrubber.
- **`trackMap.js`**: Draws the circuit layout and places a dot to indicate where the car is on track based on the telemetry scrubber position.
- **`waterfallChart.js`**: Renders the sector-by-sector time difference waterfall chart.
- **`lapSummary.js`**: Renders the high-level summary cards (e.g., fastest lap times, tire compounds used).
- **`insightList.js`**: Renders the list of detected insights on the left panel and populates the drill-down details when an insight is clicked.
