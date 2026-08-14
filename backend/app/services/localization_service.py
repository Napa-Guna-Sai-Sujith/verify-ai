from typing import Dict, List, Tuple

# Comprehensive Multilingual Dictionary for Digital Trust Engine
LOCALIZATION_DATA = {
    "English": {
        "assessment_labels": {
            "supported": "Evidence Supported",
            "Evidence Supported": "Evidence Supported",
            "verification": "Needs Verification",
            "Needs Verification": "Needs Verification",
            "misleading": "Potentially Misleading",
            "Potentially Misleading": "Potentially Misleading",
            "not_relevant": "NOT RELEVANT",
            "NOT RELEVANT": "NOT RELEVANT"
        },
        "explanations": {
            "supported": (
                "We cross-referenced this claim with official digital databases and found matching corroborating evidence.\n\n"
                "• Verified through reliable official source(s).\n"
                "• No suspicious manipulation detected in key factual assertions."
            ),
            "verification": (
                "We could not identify sufficient official evidence online to independently confirm or refute this claim at this moment.\n\n"
                "• No official government press release or fact-checking record was found for this specific wording.\n"
                "• The information requires direct verification with an authoritative source before trusting."
            ),
            "misleading": (
                "We analyzed the content structure and identified high-risk indicators commonly associated with digital deception.\n\n"
                "• Urgent forward pressure or panic language detected.\n"
                "• Unverified monetary scheme, reward promise, or unbacked alert.\n"
                "• No official government or news sources confirm this announcement."
            ),
            "not_relevant": (
                "No relevant or verifiable claim was detected in this content.\n\n"
                "• The input contains non-claim text, noise, phone UI elements, or conversational greetings.\n"
                "• Please submit a screenshot or message text containing a specific claim, statement, or announcement that you want to verify."
            )
        },
        "recommendations": {
            "supported": "This claim has supporting evidence from reliable sources. You can view the original source before referencing.",
            "verification": "Check the original source or compare with independent official news outlets before sharing.",
            "misleading": "Avoid forwarding this message to WhatsApp groups or social media until verified through an official portal.",
            "not_relevant": "Please submit a digital message, news paragraph, or screenshot containing factual assertions for verification."
        },
        "before_you_share": [
            {"title": "Do I know the original source?", "desc": "Verify if the message originates from an official domain or reputable publisher rather than forwarded social messages."},
            {"title": "Is there reliable supporting evidence?", "desc": "Cross-reference claims with official government portals (e.g., PIB, State circulars) or established fact-checking outlets."},
            {"title": "Is the information current & timely?", "desc": "Misinformation often recycles outdated news, old videos, or previous year circulars to trigger false panic."},
            {"title": "Is the message pressuring immediate sharing?", "desc": "Urgent call-to-actions ('Share with 10 groups immediately!') are a primary red flag of viral digital deception."}
        ]
    },

    "Kannada": {
        "assessment_labels": {
            "supported": "ಸಾಕ್ಷ್ಯಾಧಾರಿತವಾಗಿ ದೃಢೀಕರಿಸಲಾಗಿದೆ",
            "Evidence Supported": "ಸಾಕ್ಷ್ಯಾಧಾರಿತವಾಗಿ ದೃಢೀಕರಿಸಲಾಗಿದೆ",
            "verification": "ಪರಿಶೀಲನೆ ಅಗತ್ಯವಿದೆ",
            "Needs Verification": "ಪರಿಶೀಲನೆ ಅಗತ್ಯವಿದೆ",
            "misleading": "ದಾರಿ ತಪ್ಪಿಸುವ ಸಾಧ್ಯತೆಯಿದೆ",
            "Potentially Misleading": "ದಾರಿ ತಪ್ಪಿಸುವ ಸಾಧ್ಯತೆಯಿದೆ",
            "not_relevant": "ಪರಿಶೀಲಿಸಲು ಸೂಕ್ತವಾಗಿಲ್ಲ",
            "NOT RELEVANT": "ಪರಿಶೀಲಿಸಲು ಸೂಕ್ತವಾಗಿಲ್ಲ"
        },
        "explanations": {
            "supported": (
                "ನಾವು ಈ ಹೇಳಿಕೆಯನ್ನು ಅಧಿಕೃತ ಡಿಜಿಟಲ್ ಮೂಲಗಳೊಂದಿಗೆ ಪರಿಶೀಲಿಸಿದ್ದೇವೆ ಮತ್ತು ಪೂರಕ ಸಾಕ್ಷ್ಯಾಧಾರಗಳನ್ನು ಕಂಡುಕೊಂಡಿದ್ದೇವೆ.\n\n"
                "• ಅಧಿಕೃತ ಮೂಲಗಳಿಂದ ಮಾಹಿತಿ ದೃಢೀಪಟ್ಟಿದೆ.\n"
                "• ಮುಖ್ಯ ಅಂಶಗಳಲ್ಲಿ ಯಾವುದೇ ಅನುಮಾನಾಸ್ಪದ ಬದಲಾವಣೆಗಳು ಕಂಡುಬಂದಿಲ್ಲ."
            ),
            "verification": (
                "ಈ ಹೇಳಿಕೆಯನ್ನು ಸ್ವತಂತ್ರವಾಗಿ ದೃಢೀಕರಿಸಲು ಅಥವಾ ನಿರಾಕರಿಸಲು ಪ್ರಸ್ತುತ ಆನ್‌ಲೈನ್‌ನಲ್ಲಿ ಪರ್ಯಾಪ್ತ ಅಧಿಕೃತ ಆಧಾರಗಳು ಲಭ್ಯವಿಲ್ಲ.\n\n"
                "• ಈ ನಿರ್ದಿಷ್ಟ ಬರಹಕ್ಕೆ ಯಾವುದೇ ಅಧಿಕೃತ ಸರ್ಕಾರಿ ಪ್ರಕಟಣೆ ಸಿಕ್ಕಿಲ್ಲ.\n"
                "• ಹಂಚಿಕೊಳ್ಳುವ ಮೊದಲು ಅಧಿಕೃತ ಮೂಲಗಳಿಂದ ಖಚಿತಪಡಿಸಿಕೊಳ್ಳುವುದು ಅಗತ್ಯ."
            ),
            "misleading": (
                "ನಾವು ಸಂದೇಶದ ರಚನೆಯನ್ನು ವಿಶ್ಲೇಷಿಸಿದ್ದೇವೆ ಮತ್ತು ಡಿಜಿಟಲ್ ವಂಚನೆಗೆ ಸಂಬಂಧಿಸಿದ ಹೆಚ್ಚಿನ ಅಪಾಯದ ಸೂಚನೆಗಳನ್ನು ಗುರುತಿಸಿದ್ದೇವೆ.\n\n"
                "• ತಕ್ಷಣವೇ ಶೇರ್ ಮಾಡಿ ಎಂಬ ಒತ್ತಡದ ಭಾಷೆ ಬಳಕೆಯಾಗಿದೆ.\n"
                "• ದೃಢೀಕರಿಸದ ಹಣಕಾಸಿನ ಆಮಿಷ ಅಥವಾ ಸುಳ್ಳು ಯೋಜನೆ.\n"
                "• ಇದನ್ನು ಬೆಂಬಲಿಸುವ ಯಾವುದೇ ಸರ್ಕಾರಿ ಅಥವಾ ಸುದ್ದಿ ಮೂಲಗಳಿಲ್ಲ."
            ),
            "not_relevant": (
                "ಈ ವಿಷಯದಲ್ಲಿ ಯಾವುದೇ ಪರಿಶೀಲಿಸಬಹುದಾದ ಸುದ್ದಿ ಅಥವಾ ಹೇಳಿಕೆ ಕಂಡುಬಂದಿಲ್ಲ.\n\n"
                "• ಸಲ್ಲಿಸಿದ ವಿವರವು ಕೇವಲ ಸಾಧಾರಣ ಬರಹ, ಎಮೋಜಿ ಅಥವಾ UI ಅಂಶಗಳನ್ನು ಹೊಂದಿದೆ.\n"
                "• ದಯವಿಟ್ಟು ಪರಿಶೀಲಿಸಲು ಬಯಸುವ ನಿರ್ದಿಷ್ಟ ಸುದ್ದಿ ಅಥವಾ ಸಂದೇಶವನ್ನು ಸಲ್ಲಿಸಿ."
            )
        },
        "recommendations": {
            "supported": "ಈ ಮಾಹಿತಿಗೆ ನಂಬಲರ್ಹ ಮೂಲಗಳ ಬೆಂಬಲವಿದೆ. ಉಲ್ಲೇಖಿಸುವ ಮೊದಲು ಮೂಲ ಮೂಲವನ್ನು ವೀಕ್ಷಿಸಬಹುದು.",
            "verification": "ಹಂಚಿಕೊಳ್ಳುವ ಮೊದಲು ಅಧಿಕೃತ ಸರ್ಕಾರಿ ಪೋರ್ಟಲ್ ಅಥವಾ ಸ್ವತಂತ್ರ ಸುದ್ದಿ ಮೂಲಗಳೊಂದಿಗೆ ಪರಿಶೀಲಿಸಿ.",
            "misleading": "ಅಧಿಕೃತ ಸರ್ಕಾರಿ ಪೋರ್ಟಲ್ ಮೂಲಕ ಖಚಿತಪಡಿಸಿಕೊಳ್ಳುವವರೆಗೆ ಈ ಸಂದೇಶವನ್ನು ವಾಟ್ಸಾಪ್ ಗ್ರೂಪ್‌ಗಳಿಗೆ ಶೇರ್ ಮಾಡಬೇಡಿ.",
            "not_relevant": "ಪರಿಶೀಲಿಸಬಹುದಾದ ಸುದ್ದಿ ಅಥವಾ ಸಂದೇಶದ ಪಠ್ಯವನ್ನು ಸಲ್ಲಿಸಿ."
        },
        "before_you_share": [
            {"title": "ಮೂಲ ಮೂಲ ಯಾವುದೆಂದು ನಿಮಗೆ ತಿಳಿದಿದೆಯೇ?", "desc": "ಸಂದೇಶವು ಫಾರ್ವರ್ಡ್ ಮಾಡಿದ ಪೋಸ್ಟ್ ಬದಲು ಅಧಿಕೃತ ವೆಬ್‌ಸೈಟ್‌ನಿಂದ ಬಂದಿದೆಯೇ ಎಂದು ಪರಿಶೀಲಿಸಿ."},
            {"title": "ವಿಶ್ವಾಸಾರ್ಹ ಬೆಂಬಲ ಸಾಕ್ಷ್ಯವಿದೆಯೇ?", "desc": "ಸರ್ಕಾರಿ ಪೋರ್ಟಲ್‌ಗಳು (ಉದಾ: PIB) ಅಥವಾ ಸತ್ಯಾಸತ್ಯತೆ ತಪಾಸಣೆ ಪೋರ್ಟಲ್‌ಗಳೊಂದಿಗೆ ಹೋಲಿಸಿ."},
            {"title": "ಮಾಹಿತಿಯು ಪ್ರಸ್ತುತವಾಗಿದೆಯೇ?", "desc": "ಹಳೆಯ ವೀಡಿಯೊಗಳು ಅಥವಾ ಮುಗಿದುಹೋದ ಆದೇಶಗಳನ್ನು ಮರುಬಳಕೆ ಮಾಡಿ ಗೊಂದಲ ಸೃಷ್ಟಿಸಲಾಗುತ್ತದೆ."},
            {"title": "ತಕ್ಷಣ ಶೇರ್ ಮಾಡಲು ಒತ್ತಡ ಹೇರಲಾಗುತ್ತಿದೆಯೇ?", "desc": "'ತಕ್ಷಣ 10 ಜನರಿಗೆ ಶೇರ್ ಮಾಡಿ' ಎಂಬ ಆತುರದ ಸಂದೇಶಗಳು ಸುಳ್ಳು ಮಾಹಿತಿಯ ಮುಖ್ಯ ಲಕ್ಷಣ."}
        ]
    },

    "Telugu": {
        "assessment_labels": {
            "supported": "ఆధారాలతో నిర్ధారించబడింది",
            "Evidence Supported": "ఆధారాలతో నిర్ధారించబడింది",
            "verification": "తనిఖీ అవసరం",
            "Needs Verification": "తనిఖీ అవసరం",
            "misleading": "తప్పుదోవ పట్టించే అవకాశం ఉంది",
            "Potentially Misleading": "తప్పుదోవ పట్టించే అవకాశం ఉంది",
            "not_relevant": "సంబంధిత సమాచారం కాదు",
            "NOT RELEVANT": "సంబంధిత సమాచారం కాదు"
        },
        "explanations": {
            "supported": (
                "మేము ఈ ప్రకటనను అధికారిక డిజిటల్ డేటాబేస్‌లతో సరిపోల్చాము మరియు నిర్ధారించే ఆధారాలను కనుగొన్నాము.\n\n"
                "• విశ్వసనీయ అధికారిక మూలం ద్వారా నిర్ధారించబడింది.\n"
                "• ముఖ్యమైన అంశాలలో ఎటువంటి అనుమానాస్పద మార్పులు కనుగొనబడలేదు."
            ),
            "verification": (
                "ఈ ప్రకటనను స్వతంత్రంగా నిర్ధారించడానికి లేదా ఖండించడానికి ప్రస్తుతం ఆన్‌లైన్‌లో తగినంత అధికారిక ఆధారాలు లభ్యం కాలేదు.\n\n"
                "• ఈ నిర్దిష్ట సమాచారానికి సంబంధించి ఎలాంటి అధికారిక ప్రభుత్వ ప్రకటన లభించలేదు.\n"
                "• ఫార్వర్డ్ చేసే ముందు అధికారిక వర్గాల నుండి నేరుగా సరిచూసుకోవడం అవసరం."
            ),
            "misleading": (
                "మేము ఈ సమాచార నిర్మాణాన్ని విశ్లేషించాము మరియు డిజిటల్ మోసాలకు సంబంధించిన అధిక ప్రమాద సూచికలను గుర్తించాము.\n\n"
                "• వెంటనే షేర్ చేయండి అని ఒత్తిడి చేసే భాష ఉపయోగించబడింది.\n"
                "• నిర్ధారించబడని ఆర్థిక ఆఫర్ లేదా నకిలీ పథకం ప్రకటన.\n"
                "• దీనిని ధృవీకరించే ప్రభుత్వ లేదా వార్తా ఆధారాలు లేవు."
            ),
            "not_relevant": (
                "ఈ సమాచారంలో ఎటువంటి సరిచూడదగిన వార్త లేదా ప్రకటన కనుగొనబడలేదు.\n\n"
                "• ఇది కేవలం సాధారణ టెక్స్ట్, ఎమోజీలు లేదా స్క్రీన్ ఐకాన్లను కలిగి ఉంది.\n"
                "• దయచేసి మీరు తనిఖీ చేయాలనుకుంటున్న సందేశాన్ని సమర్పించండి."
            )
        },
        "recommendations": {
            "supported": "ఈ సమాచారానికి విశ్వసనీయ వర్గాల మద్దతు ఉంది. వివరాల కోసం అసలు మూలాన్ని చూడవచ్చు.",
            "verification": "ఇతరులతో పంచుకునే ముందు అధికారిక ప్రభుత్వ పోర్టల్ లేదా స్వతంత్ర వార్తా సంస్థలతో సరిచూసుకోండి.",
            "misleading": "అధికారిక పోర్టల్ ద్వారా నిర్ధారించబడే వరకు ఈ మెసేజ్‌ను వాట్సాప్ గ్రూప్‌లలో షేర్ చేయకండి.",
            "not_relevant": "తనిఖీ చేయడానికి తగిన వార్త లేదా మెసేజ్ వివరాలను నమోదు చేయండి."
        },
        "before_you_share": [
            {"title": "అసలు మూలం ఏమిటో మీకు తెలుసా?", "desc": "ఈ మెసేజ్ ఫార్వర్డ్ చేసిన పోస్ట్ కాకుండా అధికారిక వెబ్‌సైట్ నుండి వచ్చిందో లేదో తనిఖీ చేయండి."},
            {"title": "నమ్మదగిన ఆధారాలు ఉన్నాయా?", "desc": "ప్రభుత్వ పోర్టల్‌లు (PIB వంటివి) లేదా ఫ్యాక్ట్-చెక్ వెబ్‌సైట్‌లతో పోల్చి చూడండి."},
            {"title": "సమాచారం తాజాదేనా?", "desc": "పాత వార్తలు లేదా పాత జీవోలను మళ్లీ సర్క్యులేట్ చేసి భయాందోళనలు సృష్టిస్తారు."},
            {"title": "వెంటనే షేర్ చేయమని ఒత్తిడి చేస్తున్నారా?", "desc": "'వెంటనే 10 మందికి పంపండి' అనే తొందరపాటు మెసేజ్‌లు నకిలీ సమాచారానికి ప్రధాన సంకేతం."}
        ]
    },

    "Tamil": {
        "assessment_labels": {
            "supported": "சான்றுகளுடன் உறுதிப்படுத்தப்பட்டது",
            "Evidence Supported": "சான்றுகளுடன் உறுதிப்படுத்தப்பட்டது",
            "verification": "சரிபார்ப்பு தேவை",
            "Needs Verification": "சரிபார்ப்பு தேவை",
            "misleading": "தவறாக வழிநடத்தக்கூடும்",
            "Potentially Misleading": "தவறாக வழிநடத்தக்கூடும்",
            "not_relevant": "தொடர்பற்ற தகவல்",
            "NOT RELEVANT": "தொடர்பற்ற தகவல்"
        },
        "explanations": {
            "supported": (
                "இந்தத் தகவலை அதிகாரப்பூர்வ டிஜிட்டல் ஆதாரங்களுடன் சரிபார்த்து, உறுதியான சான்றுகளைக் கண்டறிந்துள்ளோம்.\n\n"
                "• நம்பகமான அதிகாரப்பூர்வ ஆதாரம் மூலம் உறுதிப்படுத்தப்பட்டுள்ளது.\n"
                "• இதில் எந்த சந்தேகத்திற்குரிய மாற்றங்களும் கண்டறியப்படவில்லை."
            ),
            "verification": (
                "இந்தக் கூற்றை சுயாதீனமாக உறுதிப்படுத்த அல்லது மறுக்க போதுமான அதிகாரப்பூர்வ இணையச் சான்றுகள் தற்போது கிடைக்கவில்லை.\n\n"
                "• இந்த குறிப்பிட்ட தகவலுக்கு அரசு செய்திக்குறிப்பு எதுவும் கிடைக்கவில்லை.\n"
                "• பகிர்வதற்கு முன் அதிகாரப்பூர்வ ஆதாரங்களுடன் நேரடியாகச் சரிபார்ப்பது அவசியம்."
            ),
            "misleading": (
                "இந்தச் செய்தியின் அமைப்பை ஆய்வு செய்து, டிஜிட்டல் ஏமாற்றுதலுடன் தொடர்புடைய ஆபத்து குறிகாட்டிகளக் கண்டறிந்துள்ளோம்.\n\n"
                "• 'உடனே பகிருங்கள்' போன்ற அவசர அழுத்தம் கொடுக்கப்பட்டுள்ளது.\n"
                "• உறுதிப்படுத்தப்படாத பண ஆசை அல்லது போலி அரசுத் திட்டம்.\n"
                "• இதை உறுதிப்படுத்தும் அரசு அல்லது செய்தி ஆதாரங்கள் எதுவுமில்லை."
            ),
            "not_relevant": (
                "இந்தத் தகவலில் சரிபார்க்கக்கூடிய செய்தி அல்லது கூற்று எதுவும் கண்டறியப்படவில்லை.\n\n"
                "• இதில் சாதாரண உரை அல்லது திரைக் குறியீடுகள் மட்டுமே உள்ளன.\n"
                "• சரிபார்க்கப்பட வேண்டிய செய்தியை உள்ளிடவும்."
            )
        },
        "recommendations": {
            "supported": "இந்தத் தகவலுக்கு நம்பகமான ஆதாரங்கள் உள்ளன. பகிர்வதற்கு முன் ஆதாரத்தைப் பார்வையிடலாம்.",
            "verification": "பகிர்வதற்கு முன் அதிகாரப்பூர்வ அரசு தளம் அல்லது செய்திகளுடன் ஒப்பிட்டுச் சரிபார்க்கவும்.",
            "misleading": "அதிகாரப்பூர்வ தளம் மூலம் உறுதிப்படுத்தப்படும் வரை இந்தச் செய்தியை வாட்ஸ்அப் குழுக்களில் பகிர வேண்டாம்.",
            "not_relevant": "சரிபார்க்கப்பட வேண்டிய செய்தி அல்லது கூற்றை உள்ளிடவும்."
        },
        "before_you_share": [
            {"title": "அசல் ஆதாரம் உங்களுக்குத் தெரியுமா?", "desc": "செய்தி பகிர்ந்த போஸ்ட் அல்லாமல் அதிகாரப்பூர்வ தளத்திலிருந்து வந்ததா எனச் சரிபார்க்கவும்."},
            {"title": "நம்பகமான சான்றுகள் உள்ளதா?", "desc": "அரசுத் தளங்கள் (PIB போன்றவை) அல்லது உண்மையைச் சரிபார்க்கும் தளங்களுடன் ஒப்பிடவும்."},
            {"title": "தகவல் தற்போதையதானா?", "desc": "பழைய செய்திகள் அல்லது வீடியோக்களை மீண்டும் பரப்பி தேவையற்ற பயத்தை உருவாக்குவார்கள்."},
            {"title": "உடனே பகிர அவசரப்படுத்துகிறார்களா?", "desc": "'உடனே 10 பேருக்கு அனுப்புங்கள்' என்பது போலி செய்திகளின் முக்கிய அடையாளம்."}
        ]
    },

    "Hindi": {
        "assessment_labels": {
            "supported": "प्रमाणित एवं समर्थित",
            "Evidence Supported": "प्रमाणित एवं समर्थित",
            "verification": "सत्यापन आवश्यक है",
            "Needs Verification": "सत्यापन आवश्यक है",
            "misleading": "भ्रामक होने की संभावना",
            "Potentially Misleading": "भ्रामक होने की संभावना",
            "not_relevant": "प्रासंगिक नहीं है",
            "NOT RELEVANT": "प्रासंगिक नहीं है"
        },
        "explanations": {
            "supported": (
                "हमने इस दावे को आधिकारिक डिजिटल डेटाबेस के साथ सत्यापित किया है और सहायक साक्ष्य पाए हैं।\n\n"
                "• आधिकारिक सरकारी/समाचार स्रोतों से पुष्टि की गई है।\n"
                "• मुख्य दावों में कोई संदिग्ध बदलाव नहीं पाया गया।"
            ),
            "verification": (
                "इस दावे की स्वतंत्र रूप से पुष्टि या खंडन करने के लिए वर्तमान में पर्याप्त आधिकारिक ऑनलाइन साक्ष्य उपलब्ध नहीं हैं।\n\n"
                "• इस विशिष्ट शब्द संयोजन के लिए कोई आधिकारिक प्रेस विज्ञप्ति नहीं मिली है।\n"
                "• साझा करने से पहले आधिकारिक स्रोत से सीधा सत्यापन आवश्यक है।"
            ),
            "misleading": (
                "हमने संदेश की संरचना का विश्लेषण किया और डिजिटल भ्रम से जुड़े उच्च-जोखिम वाले संकेत पाए हैं।\n\n"
                "• तुरंत शेयर करने का दबाव या घबराहट पैदा करने वाली भाषा का प्रयोग।\n"
                "• असत्यापित वित्तीय इनाम, योजना या मुफ्त ऑफर का दावा।\n"
                "• इस दावे की पुष्टि करने वाला कोई सरकारी या समाचार स्रोत नहीं है।"
            ),
            "not_relevant": (
                "इस सामग्री में कोई जांच योग्य दावा या समाचार नहीं पाया गया।\n\n"
                "• इसमें केवल सामान्य शब्द, इमोजी या स्क्रीन आइकन शामिल हैं।\n"
                "• कृपया कोई विशिष्ट संदेश या घोषणा प्रस्तुत करें जिसे आप सत्यापित करना चाहते हैं।"
            )
        },
        "recommendations": {
            "supported": "इस दावे के समर्थन में विश्वसनीय साक्ष्य मौजूद हैं। आप मूल स्रोत देख सकते हैं।",
            "verification": "साझा करने से पहले आधिकारिक सरकारी पोर्टल या स्वतंत्र समाचार पत्रों से सत्यापन करें।",
            "misleading": "जब तक आधिकारिक पोर्टल से पुष्टि न हो जाए, इस संदेश को व्हाट्सएप ग्रुपों में फॉरवर्ड करने से बचें।",
            "not_relevant": "सत्यापन के लिए किसी विशिष्ट समाचार संदेश या दावे को दर्ज करें।"
        },
        "before_you_share": [
            {"title": "क्या आपको मूल स्रोत का पता है?", "desc": "जांचें कि संदेश फॉरवर्ड किए गए मैसेज के बजाय किसी आधिकारिक वेबसाइट से आया है या नहीं।"},
            {"title": "क्या विश्वसनीय साक्ष्य मौजूद हैं?", "desc": "आधिकारिक सरकारी पोर्टल (जैसे PIB) या फैक्ट-चेक वेबसाइटों से मिलान करें।"},
            {"title": "क्या जानकारी वर्तमान समय की है?", "desc": "पुरानी खबरों या पुराने आदेशों को दोबारा वायरल करके भ्रम फैलाया जाता है।"},
            {"title": "क्या तुरंत शेयर करने का दबाव है?", "desc": "'तुरंत 10 ग्रुपों में भेजें' जैसे संदेश फर्जी खबरों की मुख्य पहचान हैं।"}
        ]
    }
}

def get_localized_content(lang: str, category_key: str, assessment_type: str) -> str:
    """
    Retrieves localized content string safely for the requested preferred language.
    Defaults to English if language is not supported.
    """
    lang_data = LOCALIZATION_DATA.get(lang, LOCALIZATION_DATA["English"])
    category_data = lang_data.get(category_key, LOCALIZATION_DATA["English"][category_key])

    if isinstance(category_data, dict):
        val = category_data.get(assessment_type, LOCALIZATION_DATA["English"][category_key].get(assessment_type, ""))
        if not val:
            val = category_data.get(assessment_type.lower(), LOCALIZATION_DATA["English"][category_key].get(assessment_type.lower(), ""))
        return val
    return str(category_data)

def get_localized_checklist(lang: str) -> List[Dict[str, str]]:
    """Retrieves localized 'Before You Share' checklist items."""
    lang_data = LOCALIZATION_DATA.get(lang, LOCALIZATION_DATA["English"])
    return lang_data.get("before_you_share", LOCALIZATION_DATA["English"]["before_you_share"])
