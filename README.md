# Cafe & Wifi API

**Live Demo**: https://cafe-and-wifi-web-app.onrender.com

A Flask-based web application to discover, browse, and manage cafes with various amenities. Perfect for remote workers
looking for the ideal workspace with WiFi, power outlets, and good coffee.

## 🌟 Features

- **Browse Cafes**: View all cafes with their amenities and details
- **Search Cafes**: Search by name or location
- **Filter Cafes**: Filter by amenities (WiFi, sockets, toilet, parking, etc.)
- **Add Cafes**: Submit new cafes to the database (API)
- **Edit Cafes**: Update cafe information with API key authentication
- **Delete Cafes**: Remove closed cafes from the database (API)
- **Random Cafe**: Get a random cafe suggestion
- **Responsive UI**: Clean, user-friendly interface

## 🛠️ Technologies

- **Backend**: Flask 3.0.0
- **Database**: SQLAlchemy + SQLite (local) / PostgreSQL (production)
- **Frontend**: HTML5, CSS3, JavaScript
- **Deployment**: Render.com with PostgreSQL
- **Server**: Gunicorn WSGI server

## 📋 Prerequisites

- Python 3.8+
- pip (Python package manager)

## 🚀 Installation

### Local Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd cafe-api
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and set your API_KEY
   export API_KEY=your_secret_key_here
   ```

5. **Run the application**
   ```bash
   python main.py
   ```

   The app will be available at `http://localhost:5000`

## 🔑 Environment Variables

- `API_KEY` - Secret key for add/edit/delete operations (required)
- `DATABASE_URL` - PostgreSQL connection URL (optional, defaults to SQLite)
- `FLASK_ENV` - Set to `production` for deployment

### Example `.env` file:

```
API_KEY=your_secure_api_key_12345
DATABASE_URL=postgresql://user:password@host/database  # Only for production
```

## 📡 API Endpoints

### Read Operations (GET)

- `GET /` - Home page with all cafes
- `GET /all` - JSON: All cafes
- `GET /random` - JSON: Random cafe
- `GET /search?name=<name>&loc=<location>` - Search cafes
- `GET /filtered-page?<filters>` - Filter cafes with query parameters
- `GET /random-page` - Random cafe page view

**Filter Parameters:**

- `cafe_name` - Cafe name (substring search)
- `has_wifi` - Has WiFi (1/true)
- `has_sockets` - Has power outlets (1/true)
- `has_toilet` - Has toilet (1/true)
- `has_alcohol` - Serves alcohol (1/true)
- `pets_allowed` - Pets allowed (1/true)
- `has_food` - Serves food (1/true)
- `has_ac` - Air conditioning (1/true)
- `has_parking` - Free parking (1/true)
- `open_now` - Currently open (1/true)

### Write Operations (POST/DELETE)

- `POST /add` - Add new cafe (requires form data)
- `POST /update/<id>` - Update cafe (requires `api_key` in form)
- `DELETE /report-closed/<id>?api-key=<key>` - Delete cafe (requires valid API_KEY)

## 🎨 UI Features

- **Dynamic Form**: Single form for adding and editing cafes
- **Edit Button**: Direct access to edit any cafe
- **Delete API**: REST API for cafe deletion
- **Responsive Design**: Works on desktop and mobile
- **Custom Font**: Custom typography for branding

## 📦 Project Structure

```
cafe-api/
├── main.py                 # Flask application & routes
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── .gitignore             # Git ignore rules
├── README.md              # This file
├── vercel.json            # Vercel deployment config (optional)
├── static/
│   ├── styles.css         # Main stylesheet
│   └── Southing-K7la7-3.otf  # Custom font
└── templates/
    ├── index.html         # Home page
    ├── add_cafe.html      # Add/Edit cafe form
    └── cafe_table.html    # Cafes list component
```

## 🌐 Deployment

### Deploy to Render.com

1. **Push to GitHub** (Render requires a Git repository)
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push -u origin main
   ```

2. **Create Render Service**
    - Go to [render.com](https://render.com)
    - Click "New +" → "Web Service"
    - Connect your GitHub repository
    - Fill in deployment settings:
        - **Name**: `cafe-api` (or your choice)
        - **Runtime**: Python
        - **Build Command**: `pip install -r requirements.txt`
        - **Start Command**: `gunicorn main:app`

3. **Add PostgreSQL Database**
    - In your Render project, click "+ Create" → "PostgreSQL"
    - Choose "Free" tier
    - Render will automatically set `DATABASE_URL` environment variable

4. **Set Environment Variables**
    - In Render Dashboard → Environment
    - Add `API_KEY=your_secret_key`
    - The `DATABASE_URL` will be auto-injected

5. **Deploy**
    - Click "Deploy" and wait for build to complete
    - Your app will be live at `https://cafe-api.onrender.com`

**Note**: The free tier has a 15-minute inactivity timeout, but your PostgreSQL database will persist permanently.

## 🔒 Security Notes

- **API Key**: Keep your `API_KEY` secret. Use strong, random keys.
- **Environment Variables**: Never commit `.env` files to Git.
- **HTTPS**: Render provides free SSL/TLS encryption.
- **CORS**: Currently allows all origins (consider restricting in production).

## 🧪 Testing

### Test Add Cafe (API)

```bash
curl -X POST http://localhost:5000/add \
  -d "name=Test Cafe&map_url=...&wifi=on&sockets=on&..."
```

### Test Delete Cafe (API)

```bash
curl -X DELETE "http://localhost:5000/report-closed/1?api-key=YOUR_API_KEY"
```

## 📝 Cafe Data Fields

Each cafe requires:

- `name` - Unique cafe name
- `location` - Street address or neighborhood
- `map_url` - Google Maps link
- `img_url` - Cafe image URL
- `seats` - Number of seats (e.g., "10-20")
- `coffee_price` - Price range (e.g., "$2.50")
- `open_hours` - Business hours (e.g., "8:00 AM - 6:00 PM")
- Boolean amenities: wifi, sockets, toilet, calls, pets, food, alcohol, ac, parking

## 🐛 Troubleshooting

**Database connection error on Render**

- Ensure PostgreSQL add-on is attached
- Check `DATABASE_URL` is set in environment variables
- Wait 5-10 minutes after creating the database

**"API_KEY environment variable is not set"**

- Add `API_KEY` to your `.env` file locally
- Add `API_KEY` to Render environment variables in production

**Cold start delay on Render**

- Free tier web services spin down after 15 minutes
- First request after spin-down will take 30-50 seconds
- This is normal behavior; upgrade to paid tier to prevent spin-downs

## 📚 Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [Render.com Docs](https://render.com/docs)
- [Gunicorn](https://gunicorn.org/)

## 📄 License

This project is open source and available for educational and portfolio purposes.

## ✨ Author

Created as a portfolio project demonstrating Flask, SQLAlchemy, and full-stack web development.

---

**Happy cafe hunting! ☕**
