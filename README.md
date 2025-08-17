# Village Seva Chatbot 🏘️

A multilingual AI-powered chatbot designed to assist villagers and rural communities with information about government schemes, services, and general inquiries. Built with Flask, OpenAI API, and integrated with real-time search capabilities.

## 🚀 Features

- **Multilingual Support**: Supports English and Kannada languages
- **AI-Powered Responses**: Uses NVIDIA's Llama 3.1 model for intelligent conversations
- **Real-time Search**: Fetches latest information about government schemes and services
- **Text-to-Speech**: Converts responses to audio for better accessibility
- **Speech Recognition**: Voice input capability for hands-free interaction
- **Database Storage**: Stores conversation history in MySQL database
- **Clean Interface**: User-friendly web interface optimized for rural users

## 📋 Requirements

- Python 3.7+
- Flask
- MySQL Server
- OpenAI Python client
- Google Text-to-Speech (gTTS)
- Requests
- MySQL Connector

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/Nithingowdabk/Village-Seva-ChatBot.git
cd Village-Seva-ChatBot
```

2. Install required packages:
```bash
pip install flask openai gtts mysql-connector-python requests
```

3. Set up MySQL Database:
   - Install MySQL Server
   - Create a database named `village_seva_db`
   - Update database credentials in `app.py`

4. Configure API Keys:
   - Get NVIDIA API key from [NVIDIA API Portal](https://build.nvidia.com/)
   - Get SerpAPI key from [SerpAPI](https://serpapi.com/) for search functionality
   - Update the API keys in `app.py`

5. Run the application:
```bash
python app.py
```

## 🎯 Usage

1. **Start the Application**: Run the Flask app using `python app.py`
2. **Access the Interface**: Open your web browser and go to `http://localhost:5000`
3. **Select Language**: Choose between English and Kannada
4. **Ask Questions**: Type your questions about:
   - Government schemes and subsidies
   - Village services and facilities
   - Loan applications and procedures
   - Latest government updates
   - General rural development queries

### Voice Features
- **Voice Input**: Click the microphone button to speak your question
- **Voice Output**: The bot can read responses aloud for better accessibility

## 📁 Project Structure

```
Village Seva_chatbot/
├── app.py                    # Main Flask application
├── logic.py                  # AI logic and API integration
├── scraping.py              # Web scraping utilities
├── try.py                   # Testing scripts
├── chat_history.json        # Chat history storage
├── static/
│   └── style.css           # Frontend styling
├── templates/
│   ├── index.html          # Main chat interface
│   └── chat.html           # Chat page template
└── README.md               # This file
```

## 🏷️ Key Features & Services

The chatbot can assist with information about:

1. **Government Schemes** 🏛️
   - PM-KISAN schemes
   - Rural employment programs
   - Housing schemes
   - Agricultural subsidies

2. **Financial Services** �
   - Bank loan procedures
   - Microfinance options
   - Insurance schemes
   - Digital payment methods

3. **Agricultural Support** 🌾
   - Crop insurance
   - Modern farming techniques
   - Weather updates
   - Market prices

4. **Healthcare Services** 🏥
   - Village health programs
   - Medical schemes
   - Vaccination drives
   - Health insurance

5. **Education & Skill Development** 📚
   - Scholarship programs
   - Skill training opportunities
   - Digital literacy programs
   - Vocational courses

## 🔧 How It Works

1. **Language Selection**: Users choose their preferred language (English/Kannada)
2. **Query Processing**: User input is processed and analyzed for context
3. **Search Integration**: For scheme-related queries, real-time search is performed
4. **AI Response**: NVIDIA's Llama model generates contextual responses
5. **Text-to-Speech**: Responses are converted to audio for accessibility
6. **Database Storage**: Conversations are stored for analytics and improvement

## 📊 Technology Stack

- **Backend**: Flask (Python)
- **AI Model**: NVIDIA Llama 3.1 Nemotron 70B
- **Database**: MySQL
- **Text-to-Speech**: Google Text-to-Speech (gTTS)
- **Search API**: SerpAPI for real-time information
- **Frontend**: HTML, CSS, JavaScript
- **Language Support**: English, Kannada

## 🌐 Target Audience

- **Rural Communities**: Farmers, villagers, and rural residents
- **Government Officials**: Local administrators and service providers
- **NGOs**: Organizations working in rural development
- **Researchers**: Studying rural digital inclusion

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Nithingowdabk**
- GitHub: [@Nithingowdabk](https://github.com/Nithingowdabk)

## 🙏 Acknowledgments

- NVIDIA for providing the Llama 3.1 API
- Google for Text-to-Speech services
- SerpAPI for search integration
- Open source community for various libraries
- Rural communities for inspiring this project

## 🐛 Troubleshooting

### Common Issues:

1. **Database Connection Error**: 
   - Ensure MySQL server is running
   - Check database credentials in `app.py`
   - Verify database `village_seva_db` exists

2. **API Key Issues**: 
   - Verify NVIDIA API key is valid and active
   - Check SerpAPI key limits and validity
   - Ensure API keys are properly configured

3. **Speech Recognition Not Working**:
   - Check browser permissions for microphone access
   - Ensure stable internet connection
   - Verify browser supports Web Speech API

### Error Messages:
- `Connection refused`: Check if Flask app is running on correct port
- `API key invalid`: Verify and update API credentials
- `Database error`: Check MySQL connection and table structure

## 📱 Future Enhancements

- [ ] Add more regional Indian languages
- [ ] Implement offline mode for basic queries
- [ ] Add image recognition for documents
- [ ] Include video call support for complex queries
- [ ] Develop mobile app version
- [ ] Add farmer marketplace integration
- [ ] Implement location-based services
- [ ] Add weather forecasting
- [ ] Include crop disease detection
