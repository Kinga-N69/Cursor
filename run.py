from dotenv import load_dotenv
import os

load_dotenv()

from app import app

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.getenv('PORT', 5001))) 