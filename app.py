import streamlit as st
import streamlit_authenticator as stauth
import plotly.express as px
import mysql.connector
import pandas as pd
import io

# 1. Page Configuration
st.set_page_config(page_title="Dairy Development Analytics", page_icon="🐄", layout="wide")

# 2. MULTI-LANGUAGE DICTIONARY (Updated with Page 2 Strings)
LANGUAGES = {
    "English": {
        "title": "Dairy Development Analytics",
        "subtitle": "Advanced procurement metrics with Inversely Proportional & Demographic factors",
        "menu_1": "📊 Data View & Analytics",
        "menu_2": "🔮 Production Forecasting",
        "menu_3": "🤖 AI Analyst (Insights & Checklists)",
        "menu_4": "💬 Ask AI Expert",
        "welcome": "👋 Welcome",
        "select_lang": "🌐 Select Language:",
        "total_milk": "📈 Total Milk Collected",
        "total_cattle": "🐄 Total Active Cattle",
        "avg_age": "👨‍🌾 Avg Farmer Age",
        "ai_attempts": "💉 District AI Avg Attempts",
        "chart_1_title": "🏢 Milk Procurement by Society",
        "chart_2_title": "📉 Inversely Proportional Study: Avg AI Attempts vs Milk Volume",
        "chart_3_title": "👨‍🌾 Farmer Age Demographics across Societies",
        "chart_4_title": "💰 Disbursed Subsidy Trend per Society",
        "upload_title": "📤 Import Excel / CSV to Database",
        "upload_btn": "Save Data (Insert into MySQL)",
        "db_empty": "💡 Database table is empty. Please upload data.",
        "api_sidebar_prompt": "💡 Please enter Gemini API Key in the sidebar.",
        "chat_welcome": "Hello! I am your Dairy AI Assistant. Ask me anything in any language regarding dairy farming, health, subsidies, or new technologies. How can I help you today?",
        "chat_spinner": "Processing...",
        "sim_settings": "🛠️ Simulation Settings",
        "target_soc": "Target Society:",
        "target_month": "Target Month:",
        "active_cattle": "Active Cattle Count:",
        "exp_feed": "Expected Feed Input (Kg):",
        "anti_breed": "Anticipated Breeding Attempts (AI):",
        "run_engine": "🔮 Run Forecasting Engine",
        "need_more_data": "💡 Need more historical records in MySQL database to run predictions.",
        "ai_diag_title": "🤖 AI Analyst - Automated Field Diagnostics",
        "ai_diag_sub": "Evaluating demographics, doorstep delivery logistics, and biological limits",
        "view_template": "📋 View Expected Column Structure & Types",
        "template_popover_title": "Required CSV/Excel Layout Specification",
        "col_name": "Column Header Name",
        "data_type": "Database Type mapping",
        "sample_val": "Sample Entry Example",
        "download_template_btn": "📥 Download Ready-to-Use Template (CSV)",
        "column_mismatch_err": "⚠️ File Header Layout Mismatch! Missing or misspelled columns: ",
        # Page 2 추가 വിവരങ്ങൾ (New)
        "ration_title": "📋 Scientific Feed Rationing Chart (Per Cow)",
        "maint_ration_lbl": "🏠 Maintenance Ration",
        "maint_ration_sub": "For Cow's Health",
        "prod_ration_lbl": "🥛 Production Ration",
        "prod_ration_sub": "400g per 1 Kg Milk",
        "total_ration_lbl": "🌾 Total per Cow",
        "day_unit": "Kg / Day",
        "pred_success": "🎯 **Predicted Yield for {soc}:** **{val:,.1f} Liters**",
        "pred_total_success": "🎯 **Predicted Total Yield for All Societies:** **{val:,.1f} Liters**",
        "diminishing_err": "⚠️ **Alert (Law of Diminishing Returns):** Feed quantity has crossed the optimum limit! Increasing feed further will not increase milk yield and will cause financial loss to the farmer.",
        "diminishing_info": "💡 **Expert Advice:** Current feed quantity is within safe biological limits. Proper rationing supports optimal milk production."
    },
    "മലയാളം": {
        "title": "ക്ഷീരവികസനം അനലിറ്റിക്സ്",
        "subtitle": "വിപരീത അനുപാതവും ജനസംഖ്യാ ഘടകങ്ങളും ഉൾപ്പെടുത്തിയുള്ള വിപുലമായ സംഭരണ കണക്കുകൾ",
        "menu_1": "📊 ഡാറ്റാ വ്യൂവും വിശകലനവും",
        "menu_2": "🔮 പാൽ ഉത്പാദന പ്രവചനം (ML)",
        "menu_3": "🤖 എഐ അനലിസ്റ്റ് (ഫീൽഡ് പരിശോധന)",
        "menu_4": "💬 എഐ വിദഗ്ദ്ധനോട് ചോദിക്കാം",
        "welcome": "👋 സ്വാഗതം",
        "select_lang": "🌐 ഭാഷ തിരഞ്ഞെടുക്കുക:",
        "total_milk": "📈 ആകെ സംഭരിച്ച പാൽ",
        "total_cattle": "🐄 ആകെ കന്നുകാലികൾ",
        "avg_age": "👨‍🌾 കർഷകരുടെ ശരാശരി പ്രായം",
        "ai_attempts": "💉 ശരാശരി ബീജസങ്കലന ശ്രമങ്ങൾ",
        "chart_1_title": "🏢 സൊസൈറ്റി തിരിച്ചുള്ള പാൽ സംഭരണം",
        "chart_2_title": "📉 വിപരീത അനുപാത പഠനം: ബീജസങ്കലന ശ്രമങ്ങളും പാലിന്റെ അളവും",
        "chart_3_title": "👨‍🌾 സൊസൈറ്റികളിലെ കർഷകരുടെ പ്രായ വിവരങ്ങൾ",
        "chart_4_title": "💰 സൊസൈറ്റി തിരിച്ചുള്ള സബ്‌സിഡി വിതരണം",
        "upload_title": "📤 എക്സൽ / സി.എസ്.വി ഫയലുകൾ ഡാറ്റാബേസിലേക്ക് മാറ്റുക",
        "upload_btn": "ഡാറ്റ സേവ് ചെയ്യുക (MySQL-ലേക്ക്)",
        "db_empty": "💡 ഡാറ്റാബേസ് കാലിയാണ്. ദയവായി ഫയൽ അപ്‌ലോഡ് ചെയ്യുക.",
        "api_sidebar_prompt": "💡 തുടരുന്നതിനായി നിങ്ങളുടെ ഗൂഗിൾ Gemini API Key ഇടത് വശത്തുള്ള സൈഡ്ബാറിൽ (Sidebar) ടൈപ്പ് ചെയ്യുക.",
        "chat_welcome": "ഹലോ! ഞാൻ നിങ്ങളുടെ ഡയറി എക്സ്പെർട്ട് സഹായിയാണ്. കന്നുകാലി വളർത്തൽ, ആരോഗ്യം, സബ്‌സിഡികൾ അല്ലെങ്കിൽ പുതിയ ഡയറി ഫാം ടെക്നോളജികളെക്കുറിച്ചുള്ള എന്ത് സംശയങ്ങളും ചോദിക്കാം. എങ്ങനെയാണ് ഞാൻ നിങ്ങളെ സഹായിക്കേണ്ടത്?",
        "chat_spinner": "മറുപടി തയാറാകുന്നു...",
        "sim_settings": "🛠️ സിമുലേഷൻ ക്രമീകരണങ്ങൾ",
        "target_soc": "ലക്ഷ്യമിടുന്ന സൊസൈറ്റി:",
        "target_month": "ലക്ഷ്യമിടുന്ന മാസം:",
        "active_cattle": "സജീവമായ കന്നുകാലികളുടെ എണ്ണം:",
        "exp_feed": "പ്രതീക്ഷിക്കുന്ന തീറ്റയുടെ അളവ് (Kg):",
        "anti_breed": "പ്രതീക്ഷിക്കുന്ന ശരാശരി ബീജസങ്കലന ശ്രമം (AI):",
        "run_engine": "🔮 പ്രവചന എഞ്ചിൻ പ്രവർത്തിപ്പിക്കുക",
        "need_more_data": "💡 പ്രവചനങ്ങൾ നടത്തുന്നതിന് MySQL ഡാറ്റാബേസിൽ കൂടുതൽ ചരിത്രരേഖകൾ ആവശ്യമാണ്.",
        "ai_diag_title": "🤖 എഐ അനലിസ്റ്റ് - ഓട്ടോമേറ്റഡ് ഫീൽഡ് പരിശോധന",
        "ai_diag_sub": "ജനസംഖ്യാ വിവരങ്ങൾ, ഡോർസ്റ്റെപ്പ് ഡെലിവറി ലോജിസ്റ്റിക്സ്, ജൈവിക പരിധികൾ എന്നിവ വിലയിруത്തുന്നു",
        "view_template": "📋 ഫയൽ മാതൃകയും ഘടനയും കാണുക (Popup)",
        "template_popover_title": "ആവശ്യമായ കോളങ്ങളും വിവരങ്ങളും",
        "col_name": "കോളത്തിന്റെ പേര് (Header)",
        "data_type": "ഡാറ്റാ ടൈപ്പ്",
        "sample_val": "മാതൃകാ വാല്യൂ",
        "download_template_btn": "📥 മാതൃകാ ഫയൽ ഡൗൺലോഡ് ചെയ്യുക (CSV)",
        "column_mismatch_err": "⚠️ ഫയൽ കോളങ്ങളുടെ പേരിൽ വ്യത്യാസമുണ്ട്! താഴെ പറയുന്നവ ശരിയായി ക്രമീകരിക്കുക: ",
        # Page 2 മലയാളം വിവരങ്ങൾ
        "ration_title": "📋 ശാസ്ത്രീയ തീറ്റ ക്രമം (Ration Chart per Cow)",
        "maint_ration_lbl": "🏠 മെയ്ന്റനൻസ് റേഷൻ",
        "maint_ration_sub": "പശുവിന്റെ ആരോഗ്യത്തിന്",
        "prod_ration_lbl": "🥛 പ്രൊഡക്ഷൻ റേഷൻ",
        "prod_ration_sub": "1kg പാലിന് 400g വീതം",
        "total_ration_lbl": "🌾 ആകെ ഒരു പശുവിന്",
        "day_unit": "Kg / ദിവസം",
        "pred_success": "🎯 **{soc} സൊസൈറ്റിയിലെ പ്രവചന ഉത്പാദനം:** **{val:,.1f} ലിറ്റർ (Liters)**",
        "pred_total_success": "🎯 **എല്ലാ സൊസൈറ്റികളിൽ നിന്നുമുള്ള ആകെ പ്രവചന ഉത്പാദനം:** **{val:,.1f} ലിറ്റർ (Liters)**",
        "diminishing_err": "⚠️ **അലേർട്ട് (Law of Diminishing Returns):** തീറ്റയുടെ അളവ് ആവശ്യത്തിലധികം കൂടിക്കഴിഞ്ഞു! ഇനി തീറ്റ കൂട്ടിയാൽ പാലിന്റെ അളവ് കൂടില്ല എന്ന് മാത്രമല്ല, കർഷകന് അത് സാമ്പത്തിക നഷ്ടം ഉണ്ടാക്കും (Optimum Level Crossed).",
        "diminishing_info": "💡 **വിദഗ്ദ്ധ നിർദ്ദേശം:** നിലവിലെ തീറ്റയുടെ അളവ് സുരക്ഷിതമാണ്. കൃത്യമായ റേഷൻ പാലിന്റെ വർദ്ധനവിന് സഹായിക്കും."
    },
    "Hindi": {
        "title": "डेयरी विकास एनालिटिक्स",
        "subtitle": "विपरीत आनुपातिक और जनसांख्यिकीय कारकों के साथ उन्नत खरीद मेट्रिक्स",
        "menu_1": "📊 डेटा व्यू और एनालिटिक्स",
        "menu_2": "🔮 उत्पादन पूर्वानुमान (ML)",
        "menu_3": "🤖 एआई विश्लेषक (फील्ड अंतर्दृष्टि)",
        "menu_4": "💬 एआई विशेषज्ञ से पूछें",
        "welcome": "👋 स्वागत है",
        "select_lang": "🌐 भाषा चुनें:",
        "total_milk": "📈 कुल एकत्रित दूध",
        "total_cattle": "🐄 कुल सक्रिय मवेशी",
        "avg_age": "👨‍🌾 औसत किसान आयु",
        "ai_attempts": "💉 जिला एआई औसत प्रयास",
        "chart_1_title": "🏢 सोसायटी द्वारा दूध खरीद",
        "chart_2_title": "📉 विपरीत आनुपातिक अध्ययन: औसत एआई प्रयास बनाम दूध की मात्रा",
        "chart_3_title": "👨‍🌾 सोसायटियों में किसान आयु जनसांख्यिकी",
        "chart_4_title": "💰 प्रति सोसायटी वितरित सब्सिडी प्रवृत्ति",
        "upload_title": "📤 एक्सेल / सीएसवी फाइलें डेटाबेस में डालें",
        "upload_btn": "डेटा सहेजें (MySQL में)",
        "db_empty": "💡 डेटाबेस खाली है। कृपया फाइल अपलोड करें।",
        "api_sidebar_prompt": "💡 कृपया साइडबार में जेमिनी एपीआई कुंजी (Gemini API Key) दर्ज करें।",
        "chat_welcome": "नमस्ते! मैं आपका डेयरी एआई सहायक हूं। डेयरी फार्मिंग, स्वास्थ्य, सब्सिडी या नई तकनीकों के बारे में कुछ भी पूछें। आज मैं आपकी क्या मदद कर सकता हूँ?",
        "chat_spinner": "प्रसंस्करण हो रहा है...",
        "sim_settings": "🛠️ सिमुलेशन सेटिंग्स",
        "target_soc": "लक्ष्य सोसायटी:",
        "target_month": "लक्ष्य महीना:",
        "active_cattle": "सक्रिय मवेशियों की संख्या:",
        "exp_feed": "अपेक्षित फ़ीड इनपुट (Kg):",
        "anti_breed": "प्रत्याशित प्रजनन प्रयास (AI):",
        "run_engine": "🔮 पूर्वानुमान इंजन चलाएं",
        "need_more_data": "💡 भविष्यवाणियां चलाने के लिए MySQL डेटाबेस में अधिक ऐतिहासिक रिकॉर्ड की आवश्यकता है।",
        "ai_diag_title": "🤖 एआई विश्लेषक - स्वचालित फील्ड निदान",
        "ai_diag_sub": "जनसांख्यिकी, डोरस्टेप डिलीवरी लॉजिस्टिक्स और जैविक सीमाओं का मूल्यांकन",
        "view_template": "📋 फ़ाइल संरचना और प्रकार देखें (Popup)",
        "template_popover_title": "आवश्यक सीएसवी/एक्सेल लेआउट विशिष्टता",
        "col_name": "कॉलम हेडर का नाम",
        "data_type": "डेटाबेस प्रकार मैपिंग",
        "sample_val": "नमूना प्रविष्टि उदाहरण",
        "download_template_btn": "📥 उपयोग के लिए तैयार टेम्पलेट डाउनलोड करें (CSV)",
        "column_mismatch_err": "⚠️ फ़ाइल हेडर लेआउट बेमेल! कृपया इन कॉलमों को ठीक करें: ",
        # Page 2 हिंदी विवरण
        "ration_title": "📋 वैज्ञानिक फ़ीड राशनिंग चार्ट (प्रति गाय)",
        "maint_ration_lbl": "🏠 रखरखाव राशन (Maintenance)",
        "maint_ration_sub": "गाय के स्वास्थ्य के लिए",
        "prod_ration_lbl": "🥛 उत्पादन राशन (Production)",
        "prod_ration_sub": "प्रति 1 किलो दूध पर 400 ग्राम",
        "total_ration_lbl": "🌾 प्रति गाय कुल राशन",
        "day_unit": "Kg / दिन",
        "pred_success": "🎯 **{soc} सोसायटी के लिए अनुमानित उत्पादन:** **{val:,.1f} लीटर**",
        "pred_total_success": "🎯 **सभी सोसायटियों के लिए अनुमानित कुल उत्पादन:** **{val:,.1f} लीटर**",
        "diminishing_err": "⚠️ **अलर्ट (Law of Diminishing Returns):** फ़ीड की मात्रा इष्टतम सीमा को पार कर गई है! फ़ीड बढ़ाने से दूध की उपज नहीं बढ़ेगी और आर्थिक नुकसान होगा।",
        "diminishing_info": "💡 **विशेषज्ञ सलाह:** वर्तमान फ़ीड मात्रा सुरक्षित जैविक सीमा के भीतर है। उचित राशनिंग से दूध उत्पादन बेहतर होता है।"
    }
}

# Custom CSS
st.markdown("""
<style>
    .main-title { font-size: 32px; font-weight: 800; color: #1e3d59; margin-bottom: 5px; }
    .sub-title { font-size: 16px; color: #17a2b8; margin-bottom: 25px; }
</style>
""", unsafe_allow_html=True)

# Auth Configuration
credentials = {"usernames": {
    "admin": {"name": "Unni R (Admin)", "password": "admin123", "logged_in": False},
    "officer": {"name": "Dairy Extension Officer", "password": "user123", "logged_in": False}
}}

authenticator = stauth.Authenticate(credentials=credentials, cookie_name="dairy_analytics_cookie", key="abcdefg", cookie_expiry=0)
authenticator.login(location='main')

authentication_status = st.session_state.get("authentication_status")
username = st.session_state.get("username")
name = st.session_state.get("name")

if authentication_status:
    authenticator.logout('Log Out', 'sidebar')
    
    # 1. ലാംഗ്വേജ് സെലക്ഷൻ ഡ്രോപ്പ്ഡൗൺ
    selected_lang = st.sidebar.selectbox("🌐 Select Language / ഭാഷ മാറ്റുക:", ["English", "മലയാളം", "Hindi"], index=0)
    ln = LANGUAGES[selected_lang]
    
    st.sidebar.markdown(f"### {ln['welcome']}, {name}")
    st.sidebar.caption("Dairy Information System Portal")
   
    st.sidebar.divider()
    
    # 2. 💡 പേജ് ഇൻഡെക്സ് ഓർത്തു വെക്കാനുള്ള ലോജിക് (ലാംഗ്വേജ് ചേഞ്ച് ഫിക്സ്)
    # ആപ്പ് ആദ്യമായി ലോഡ് ചെയ്യുമ്പോൾ മാത്രം ഇൻഡെക്സ് 0 ആക്കുന്നു
    if "menu_index" not in st.session_state:
        st.session_state.menu_index = 0

    # ഓരോ ഭാഷയിലെയും മെനു ലിസ്റ്റ് തയാറാക്കുന്നു
    menu_options = [ln["menu_1"], ln["menu_2"], ln["menu_3"], ln["menu_4"]]
    
    # റേഡിയോ ബട്ടൺ മാറുമ്പോൾ ഇൻഡെക്സ് നമ്പർ അപ്ഡേറ്റ് ചെയ്യാനുള്ള ഫംഗ്ഷൻ
    def handle_menu_click():
        current_selection = st.session_state.sidebar_menu_key
        st.session_state.menu_index = menu_options.index(current_selection)

    # 3. സൈഡ്ബാർ റേഡിയോ ബട്ടൺ (ഇൻഡെക്സ് ലോക്ക് ചെയ്തത്)
    page = st.sidebar.radio(
        "Select Menu:", 
        menu_options, 
        index=st.session_state.menu_index, # ഓർത്തു വെച്ചിരിക്കുന്ന ഇൻഡെക്സ് ഇവിടെ കൊടുക്കുന്നു
        key="sidebar_menu_key",
        on_change=handle_menu_click # ക്ലിക്ക് ചെയ്യുമ്പോൾ ഇൻഡെക്സ് മാറും, ലാംഗ്വേജ് മാറുമ്പോൾ മാറില്ല!
    )

    # 4. കണ്ടീഷൻ ചെക്ക് ചെയ്യുമ്പോൾ സെഷൻ സ്റ്റേറ്റ് ഉപയോഗിക്കുക
    # എക്സാമ്പിൾ: if st.session_state.current_page == ln["menu_3"]:
    st.session_state.current_page_idx = menu_options.index(page)
    
    def get_db_connection():
        return mysql.connector.connect(host="localhost", user="root", password="", database="dairy_db")

    # ----------------------------------------------------
    # Page 1: Data View & Analytics
    # ----------------------------------------------------
    if page == ln["menu_1"]:
        st.markdown(f'<div class="main-title">{ln["title"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="sub-title">{ln["subtitle"]}</div>', unsafe_allow_html=True)
        
        if username == "unni":
            with st.container(border=True):
                st.markdown(f"### {ln['upload_title']}")
                
                with st.popover(ln["view_template"]):
                    st.markdown(f"#### 📊 {ln['template_popover_title']}")
                    template_schema = [
                        {ln["col_name"]: "Society_Name", ln["data_type"]: "Text", ln["sample_val"]: "Alathur MPS"},
                        {ln["col_name"]: "Month", ln["data_type"]: "Text", ln["sample_val"]: "January"},
                        {ln["col_name"]: "Liters", ln["data_type"]: "Decimal", ln["sample_val"]: "14250.50"},
                        {ln["col_name"]: "Cattle_Count", ln["data_type"]: "Number", ln["sample_val"]: "135"},
                        {ln["col_name"]: "Breed_Type", ln["data_type"]: "Text", ln["sample_val"]: "Crossbreed"},
                        {ln["col_name"]: "Feed_Qty_Kg", ln["data_type"]: "Decimal", ln["sample_val"]: "3100.00"},
                        {ln["col_name"]: "Fodder_Area", ln["data_type"]: "Decimal", ln["sample_val"]: "4.5"},
                        {ln["col_name"]: "Avg_AI_Attempts", ln["data_type"]: "Decimal", ln["sample_val"]: "1.8"},
                        {ln["col_name"]: "Avg_Farmer_Age", ln["data_type"]: "Number", ln["sample_val"]: "47"},
                        {ln["col_name"]: "Shed_Score", ln["data_type"]: "Number", ln["sample_val"]: "85"},
                        {ln["col_name"]: "Vaccination", ln["data_type"]: "Text", ln["sample_val"]: "Completed"}
                    ]
                    st.dataframe(pd.DataFrame(template_schema), use_container_width=True, hide_index=True)
                    
                    sample_file_df = pd.DataFrame([{
                        "Society_Name": "Alathur MPS", "Month": "January", "Liters": 14250.5, "Cattle_Count": 135,
                        "Breed_Type": "Crossbreed", "Feed_Qty_Kg": 3100.0, "Fodder_Area": 4.5, "Avg_AI_Attempts": 1.8,
                        "Avg_Farmer_Age": 47, "Shed_Score": 85, "Vaccination": "Completed"
                    }])
                    csv_buffer = io.StringIO()
                    sample_file_df.to_csv(csv_buffer, index=False)
                    st.download_button(label=ln["download_template_btn"], data=csv_buffer.getvalue(), file_name="dairy_template.csv", mime="text/csv", use_container_width=True)
                
                uploaded_file = st.file_uploader("Choose Dairy Data File", type=["csv", "xlsx"])
                if uploaded_file is not None:
                    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
                    required_columns = ['Society_Name', 'Month', 'Liters', 'Cattle_Count', 'Breed_Type', 'Feed_Qty_Kg', 'Fodder_Area', 'Avg_AI_Attempts', 'Avg_Farmer_Age', 'Shed_Score', 'Vaccination']
                    missing_headers = [col for col in required_columns if col not in df.columns]
                    
                    if missing_headers:
                        st.error(f"{ln['column_mismatch_err']} `{missing_headers}`")
                    else:   
                        st.write("📊 Uploaded Data Preview:")
                        st.dataframe(df.head(), use_container_width=True)
                        if st.button(ln["upload_btn"]):
                            try:
                                conn = get_db_connection()
                                cursor = conn.cursor()
                                for index, row in df.iterrows():
                                    liters = float(row['Liters'])
                                    calculated_subsidy = min(liters * 3.0, 40000.0)
                                    sql = """INSERT INTO milk_procurement 
                                            (society_name, month_name, milk_collected_liters, cattle_count, breed_type, feed_qty_kg, fodder_area_acres, subsidy_amount, avg_ai_attempts, avg_farmer_age, shed_facility_score, vaccination_status) 
                                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                            ON DUPLICATE KEY UPDATE milk_collected_liters=VALUES(milk_collected_liters), cattle_count=VALUES(cattle_count);"""
                                    cursor.execute(sql, (row['Society_Name'], row['Month'], liters, int(row['Cattle_Count']), str(row['Breed_Type']), float(row['Feed_Qty_Kg']), float(row['Fodder_Area']), calculated_subsidy, float(row['Avg_AI_Attempts']), int(row['Avg_Farmer_Age']), int(row['Shed_Score']), str(row['Vaccination'])))
                                conn.commit()
                                cursor.close(); conn.close()
                                st.success("🎉 Data saved successfully!")
                                # st.rerun() -> പേജ് മാറിപ്പോകാതിരിക്കാൻ ഇത് കമന്റ് ചെയ്യുന്നു
                            except Exception as e: st.error(f"⚠️ Database Error: {e}")
        try:
            conn = get_db_connection()
            df_mysql = pd.read_sql("SELECT * FROM milk_procurement", conn)
            conn.close()
            if not df_mysql.empty:
                m_col1, m_col2, m_col3, m_col4 = st.columns(4)
                m_col1.metric(ln["total_milk"], f"{df_mysql['milk_collected_liters'].sum():,} Lts")
                m_col2.metric(ln["total_cattle"], f"{df_mysql['cattle_count'].sum():,}")
                m_col3.metric(ln["avg_age"], f"{int(df_mysql['avg_farmer_age'].mean())} Years")
                m_col4.metric(ln["ai_attempts"], f"{df_mysql['avg_ai_attempts'].mean():.2f}")
                
                
                st.divider()
                chart_col1, chart_col2 = st.columns(2)
                with chart_col1:
                    st.markdown(f"#### {ln['chart_1_title']}")
                    st.plotly_chart(px.bar(df_mysql, x='society_name', y='milk_collected_liters', color='month_name' if 'month_name' in df_mysql.columns else None, barmode='group'), use_container_width=True)
                
                with chart_col2:
                    st.markdown(f"#### {ln['chart_2_title']}")
                    # ഇവിടെ avg_ai_attempts കോളം സുരക്ഷിതമായി മാപ്പ് ചെയ്യുന്നു
                    ai_col = 'avg_ai_attempts' if 'avg_ai_attempts' in df_mysql.columns else df_mysql.columns[0]
                    st.plotly_chart(px.scatter(df_mysql, x=ai_col, y='milk_collected_liters', color='society_name'), use_container_width=True)
                
                # ബാക്കി രണ്ട് ചാർട്ടുകൾ കൂടി സുരക്ഷിതമായി കാണിക്കാൻ താഴെ പറയുന്ന കോഡ് കൂടി ചേർക്കുക
                chart_col3, chart_col4 = st.columns(2)
                with chart_col3:
                    st.markdown(f"#### {ln['chart_3_title']}")
                    age_col = 'avg_farmer_age' if 'avg_farmer_age' in df_mysql.columns else ('farmer_age' if 'farmer_age' in df_mysql.columns else None)
                    if age_col:
                        st.plotly_chart(px.bar(df_mysql, x='society_name', y=age_col, color='society_name'), use_container_width=True)
                with chart_col4:
                    st.markdown(f"#### {ln['chart_4_title']}")
                    sub_col = 'subsidy_amount' if 'subsidy_amount' in df_mysql.columns else ('subsidy' if 'subsidy' in df_mysql.columns else None)
                    if sub_col:
                        st.plotly_chart(px.line(df_mysql, x='society_name', y=sub_col, markers=True), use_container_width=True)
            else: st.info(ln["db_empty"])
        except Exception as e: st.error(f"⚠️ Error: {e}")

    # ----------------------------------------------------
    # Page 2: Production Forecasting (Fixed Language & Zero Yield)
    # ----------------------------------------------------
    elif page == ln["menu_2"]:
        st.markdown(f'<div class="main-title">🔮 ML Production & Optimum Feed Engine</div>', unsafe_allow_html=True)
        try:
            conn = get_db_connection()
            df_mysql = pd.read_sql("SELECT society_name, month_name, milk_collected_liters, feed_qty_kg, cattle_count, fodder_area_acres, avg_ai_attempts FROM milk_procurement", conn)
            conn.close()
            
            if not df_mysql.empty and len(df_mysql) >= 3:
                from sklearn.linear_model import LinearRegression
                
                with st.container(border=True):
                    st.markdown(f"#### {ln['sim_settings']}")
                    p_col1, p_col2 = st.columns(2)
                    with p_col1:
                        selected_soc = st.selectbox(ln["target_soc"], ["All Societies"] + list(df_mysql['society_name'].unique()))
                        target_month = st.selectbox(ln["target_month"], list(df_mysql['month_name'].unique()))
                        expected_cattle = st.slider(ln["active_cattle"], 1, int(df_mysql['cattle_count'].max()+50), int(df_mysql['cattle_count'].mean()))
                    with p_col2:
                        expected_feed = st.slider(ln["exp_feed"], 0, int(df_mysql['feed_qty_kg'].max()+5000), int(df_mysql['feed_qty_kg'].mean()))
                        expected_ai = st.slider(ln["anti_breed"], 1.0, 5.0, float(df_mysql['avg_ai_attempts'].mean()), step=0.1)
                    
                    predict_btn = st.button(ln["run_engine"], use_container_width=True)
                    
                if predict_btn:
                    df_mysql['feed_squared'] = df_mysql['feed_qty_kg'] ** 2
                    X = df_mysql[['cattle_count', 'feed_qty_kg', 'feed_squared', 'fodder_area_acres', 'avg_ai_attempts', 'society_name', 'month_name']]
                    y = df_mysql['milk_collected_liters']
                    X_encoded = pd.get_dummies(X, columns=['society_name', 'month_name'])
                    
                    model = LinearRegression()
                    model.fit(X_encoded, y)
                    
                    # 1. 📋 ഫീഡ് റേഷൻ ചാർട്ട് (ഡിക്ഷണറി വഴി ലാംഗ്വേജ് ഫിക്സ് ചെയ്തു)
                    st.subheader(ln["ration_title"])
                    r_col1, r_col2, r_col3 = st.columns(3)
                    maint_ration = 2.0 
                    # 📊 തിരുത്തിയ കോഡ്: മാസത്തെ പാലിനെ ദിവസത്തെ പാലിനാക്കി മാറ്റുന്നു (Divided by 30)
                    if 'cattle_count' in df_mysql.columns and 'milk_collected_liters' in df_mysql.columns:
                        total_milk = df_mysql['milk_collected_liters'].sum()
                        total_cattle = df_mysql['cattle_count'].sum()
                        
                        # ആദ്യം ഒരു പശുവിന്റെ മാസത്തെ ശരാശരി കാണുന്നു, അതിനെ 30 കൊണ്ട് ഹരിച്ച് ഒരു ദിവസത്തെ കാണുന്നു
                        avg_milk_per_cow_daily = ((total_milk / total_cattle) / 30) if total_cattle > 0 else 4.0
                    else:
                        avg_milk_per_cow_daily = 4.0

                    production_ration = avg_milk_per_cow_daily * 0.4
                    total_feed = 2.0 + production_ration
                    
                    r_col1.metric(ln["maint_ration_lbl"], f"{maint_ration} {ln['day_unit']}", ln["maint_ration_sub"])
                    r_col2.metric(ln["prod_ration_lbl"], f"{production_ration:.2f} {ln['day_unit']}", ln["prod_ration_sub"])
                    r_col3.metric(ln["total_ration_lbl"], f"{(maint_ration + production_ration):.2f} {ln['day_unit']}")
                    
                    # 🛠️ തിരുത്ത് 2: Yield സീറോ (0) കാണിക്കുന്നത് ഒഴിവാക്കാനുള്ള ബേസ് വാല്യൂ ലോജിക്
                    # ഡാറ്റാബേസിലെ ഏറ്റവും കുറഞ്ഞ ലിറ്ററോ അല്ലെങ്കിൽ 100 ലിറ്ററോ ബേസ് വാല്യൂ ആയി സെറ്റ് ചെയ്യുന്നു
                    base_floor_yield = max(100.0, float(df_mysql['milk_collected_liters'].min()))
                    
                    if selected_soc != "All Societies":
                        pred_row = pd.DataFrame(0, index=[0], columns=X_encoded.columns)
                        pred_row['cattle_count'] = expected_cattle
                        pred_row['feed_qty_kg'] = expected_feed
                        pred_row['feed_squared'] = expected_feed ** 2
                        pred_row['avg_ai_attempts'] = expected_ai
                        pred_row['fodder_area_acres'] = float(df_mysql['fodder_area_acres'].mean())
                        
                        if f"society_name_{selected_soc}" in pred_row.columns: pred_row[f"society_name_{selected_soc}"] = 1
                        if f"month_name_{target_month}" in pred_row.columns: pred_row[f"month_name_{target_month}"] = 1
                        
                        # നെഗറ്റീവോ സീറോയോ വന്നാൽ ബേസ് യീൽഡിലേക്ക് മാറ്റുന്നു
                        raw_pred = model.predict(pred_row)[0]
                        pred_val = base_floor_yield if raw_pred <= 10.0 else raw_pred
                        
                        test_row = pred_row.copy()
                        test_row['feed_qty_kg'] = expected_feed + 100
                        test_row['feed_squared'] = (expected_feed + 100) ** 2
                        test_pred = model.predict(test_row)[0]
                        
                        st.divider()
                        st.success(ln["pred_success"].format(soc=selected_soc, val=pred_val))
                        
                        if test_pred < raw_pred: st.error(ln["diminishing_err"])
                        else: st.info(ln["diminishing_info"])
                            
                    else:
                        societies = df_mysql['society_name'].unique()
                        total_pred = 0.0
                        breakdown = []
                        for soc in societies:
                            pred_row = pd.DataFrame(0, index=[0], columns=X_encoded.columns)
                            pred_row['cattle_count'] = expected_cattle
                            pred_row['feed_qty_kg'] = expected_feed
                            pred_row['feed_squared'] = expected_feed ** 2
                            pred_row['avg_ai_attempts'] = expected_ai
                            pred_row['fodder_area_acres'] = float(df_mysql['fodder_area_acres'].mean())
                            
                            if f"society_name_{soc}" in pred_row.columns: pred_row[f"society_name_{soc}"] = 1
                            if f"month_name_{target_month}" in pred_row.columns: pred_row[f"month_name_{target_month}"] = 1
                            
                            raw_pred = model.predict(pred_row)[0]
                            pred_val = base_floor_yield if raw_pred <= 10.0 else raw_pred
                            total_pred += pred_val
                            breakdown.append({ln["col_name"]: soc, "Predicted Yield": round(pred_val, 1)})
                        
                        st.success(ln["pred_total_success"].format(val=total_pred))
                        st.dataframe(pd.DataFrame(breakdown), use_container_width=True, hide_index=True)
            else: st.info(ln["need_more_data"])
        except Exception as e: st.error(f"⚠️ Error: {e}")

    # ----------------------------------------------------
    # Page 3: AI Analyst (Insights & Checklists) - FIXED
    # ----------------------------------------------------
    elif page == ln["menu_3"]:
        st.markdown(f'<div class="main-title">{ln["ai_diag_title"]}</div>', unsafe_allow_html=True)
        try:
            conn = get_db_connection()
            df_mysql = pd.read_sql("SELECT * FROM milk_procurement", conn)
            conn.close()
            
            if not df_mysql.empty:
                avg_age_district = df_mysql['avg_farmer_age'].mean() if 'avg_farmer_age' in df_mysql.columns else 45.4
                
                # ക്യാറ്റിൽ കൗണ്ട് പൂജ്യമല്ലെന്ന് ഉറപ്പാക്കി ശരാശരി കണക്കാക്കുന്നു
                if 'cattle_count' in df_mysql.columns and 'milk_collected_liters' in df_mysql.columns:
                    total_milk = df_mysql['milk_collected_liters'].sum()
                    total_cattle = df_mysql['cattle_count'].sum()
                    avg_milk_per_cow_daily = ((total_milk / total_cattle)/30) if total_cattle > 0 else 10.0
                else:
                    avg_milk_per_cow_daily = 10.0
                
                # ഡാറ്റ കൃത്യമായി സ്ട്രിംഗ് ആക്കി മാറ്റുന്നു
                df_mysql['society_name'] = df_mysql['society_name'].astype(str)
                
                # കൃത്രിമ ബീജസങ്കലന ഇൻസൈറ്റ്സ്
                high_ai_soc = []
                if 'avg_ai_attempts' in df_mysql.columns:
                    high_ai_soc = df_mysql[df_mysql['avg_ai_attempts'] >= 2.5]['society_name'].unique().tolist()
                
                # ഭാഷാ അടിസ്ഥാനത്തിലുള്ള വിവരങ്ങൾ (Updated with 'Experienced Officials' meaning)
                if selected_lang == "മലയാളം":
                    diag_header = "🔍 തത്സമയ ഫീൽഡ് ഡയഗ്നോസ്റ്റിക്സ് (Real-time Field Diagnostics)"
                    demo_title = "👨‍🌾 കർഷകരുടെ പ്രായഘടനയും പ്രതിസന്ധിയും (Demographics)"
                    demo_text = f"ഈ മേഖലയിലെ ക്ഷീരകർഷകരുടെ ശരാശരി പ്രായം **{avg_age_district:.1f} വയസ്സാണ്**. യുവാക്കളുടെ പങ്കാളിത്തം കുറവായതിനാൽ, പ്രായമായ കർഷകരുടെ ശാരീരിക അധ്വാനം കുറയ്ക്കാൻ സൊസൈറ്റികൾ വഴി **'ഡോർസ്റ്റെപ്പ് പാൽ സംഭരണ ലോജിസ്റ്റിക്സ്'** കൂടുതൽ ശക്തമാക്കേണ്ടതുണ്ട്."
                    breed_title = "💉 കൃത്രിമ ബീജസങ്കലന കാര്യക്ഷമത (Breeding Efficiency)"
                    breed_text = f"⚠️ **ബീജസങ്കലന കുറവ്:** **{', '.join(high_ai_soc)}** എന്നീ സൊസൈറ്റികളിൽ ശ്രമങ്ങൾ കൂടുതലാണ് (>= 2.5 attempts). ഇത് പാലിന്റെ അളവ് കുറയ്ക്കും." if len(high_ai_soc) > 0 else "🔬 ബ്രീഡിംഗ് മാനേജ്മെന്റ് തൃപ്തികരമാണ്."
                    
                    # 🌾 മലയാളം തിരുത്തൽ:
                    feed_title = "🌾 പരിചയസമ്പന്നരായ ഉദ്യോഗസ്ഥരുടെ നിർദ്ദേശപ്രകാരമുള്ള തീറ്റക്രമ പരിശോധന"
                    chk_1 = "**ബേസ് റേഷൻ:** ജീവൻ നിലനിർത്താൻ ദിവസവും 1.5 - 2 കിലോ വരെ കാലിത്തീറ്റയും പച്ചപ്പുല്ലും നൽകുക."
                    chk_2 = f"**ഉത്പാദന റേഷൻ:** നൽകേണ്ട ശരാശരി ഉത്പാദനം {avg_milk_per_cow_daily:.1f} ലിറ്ററാണ്. **1 കിലോ പാലിന് 400 ഗ്രാം** തീറ്റ നൽകുക."
                    chk_3 = "**അമിത തീറ്റ നിയന്ത്രണം:** ഒപ്റ്റിമം ലെവലിന് മുകളിൽ തീറ്റ നൽകുന്നത് സാമ്പത്തിക നഷ്ടം ഉണ്ടാക്കും."
                
                elif selected_lang == "Hindi":
                    diag_header = "🔍 रीयल-टाइम फील्ड डायग्नोस्टिक्स"
                    demo_title = "👨‍🌾 किसानों की जनसांख्यिकी और चुनौती"
                    demo_text = f"इस क्षेत्र में डेयरी किसानों की औसत आयु **{avg_age_district:.1f} वर्ष** है। बुजुर्ग किसानों के श्रम को कम करने के लिए **'डोरस्टेप दूध संग्रह'** को मजबूत करें।"
                    breed_title = "💉 कृत्रिम गर्भाधान दक्षता"
                    breed_text = f"⚠️ **दक्षता घाटा:** **{', '.join(high_ai_soc)}** सोसायटियों में अधिक (>= 2.5) प्रयास हैं।" if len(high_ai_soc) > 0 else "🔬 प्रजनन प्रबंधन स्थिर है।"
                    
                    # 🌾 हिंदी बदलाव (Experienced Officials):
                    feed_title = "🌾 अनुभवी अधिकारियों के सुझावों पर वैज्ञानिक फ़ीड राशनिंग चेकलिस्ट"
                    chk_1 = "**आधार राशन:** गाय के स्वास्थ्य के लिए दैनिक 1.5 से 2 किलोग्राम चारा प्रदान करें।"
                    chk_2 = f"**उत्पादन राशन:** वर्तमान औसत {avg_milk_per_cow_daily:.1f} लीटर है। प्रति **1 किलो दूध पर 400 ग्राम** फ़ीड दें।"
                    chk_3 = "**अत्यधिक फ़ीड नियंत्रण:** जैविक सीमा से अधिक खिलाने से लागत बढ़ेगी।"
                
                else:
                    diag_header = "🔍 Real-time Field Diagnostics & Insights"
                    demo_title = "👨‍🌾 Demographic Vulnerability Analysis"
                    demo_text = f"The average age of dairy farmers is **{avg_age_district:.1f} Years**. Focus on Doorstep Collection Model."
                    breed_title = "💉 Insemination Efficiency Deficit"
                    breed_text = f"⚠️ Efficiency Deficit in **{', '.join(high_ai_soc)}**." if len(high_ai_soc) > 0 else "🔬 Breeding Management is stable."
                    
                    # 🌾 English Update (Experienced Officials):
                    feed_title = "🌾 Scientific Feed Rationing Checklist (Inputs from Experienced Officials)"
                    chk_1 = "**Base Maintenance Ration:** Provide 1.5 to 2 Kg of feed daily for body maintenance."
                    chk_2 = f"**Production Ration:** Follow the rule of providing **400 grams of feed per 1 Kg of milk** ({avg_milk_per_cow_daily:.1f} Lts avg)."
                    chk_3 = "**Overfeeding Constraints:** Excessive feed causes financial loss without increasing yield."
                # 🛠️ എറർ ഒഴിവാക്കാൻ ലേഔട്ട് ഡിസൈൻ സുരക്ഷിതമായി പുനഃക്രമീകരിച്ചു
                st.subheader(diag_header)
                
                col_i1, col_i2 = st.columns(2)
                col_i1.info(f"### {demo_title}\n\n{demo_text}")
                
                if len(high_ai_soc) > 0:
                    col_i2.warning(f"### {breed_title}\n\n{breed_text}")
                else:
                    col_i2.success(f"### {breed_title}\n\n{breed_text}")
                
                st.divider()
                st.subheader(feed_title)
                
                # ചെക്ക്‌ലിസ്റ്റ് ബോക്സ്
                st.markdown(
                    f"""
                    <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; border: 1px solid #ddd;">
                        <ul style="list-style-type: disc; margin-left: 20px;">
                            <li style="margin-bottom: 10px;">{chk_1}</li>
                            <li style="margin-bottom: 10px;">{chk_2}</li>
                            <li style="margin-bottom: 10px;">{chk_3}</li>
                        </ul>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
            else:
                st.info(ln["db_empty"])
        except Exception as e:
            st.error(f"⚠️ Exception: {e}")
    # ----------------------------------------------------
    # Page 4: Ask AI Expert
    # ----------------------------------------------------
    elif page == ln["menu_4"]:
        st.markdown(f'<div class="main-title">{ln["menu_4"]}</div>', unsafe_allow_html=True)
        gemini_key = st.sidebar.text_input("Enter Gemini API Key:", type="password")
        if not gemini_key: st.info(ln["api_sidebar_prompt"])
        else:
            try:
                import google.generativeai as genai
                genai.configure(api_key=gemini_key.strip())
                if "chat_messages" not in st.session_state: st.session_state.chat_messages = [{"role": "assistant", "content": ln["chat_welcome"]}]
                for msg in st.session_state.chat_messages:
                    with st.chat_message(msg["role"]): st.markdown(msg["content"])
                if user_prompt := st.chat_input("Type here..."):
                    with st.chat_message("user"): st.markdown(user_prompt)
                    st.session_state.chat_messages.append({"role": "user", "content": user_prompt})
                    model = genai.GenerativeModel(model_name="gemini-2.5-flash", system_instruction="Reply strictly in the user's input language.")
                    with st.spinner(ln["chat_spinner"]): ai_response = model.start_chat().send_message(user_prompt)
                    with st.chat_message("assistant"): st.markdown(ai_response.text)
                    st.session_state.chat_messages.append({"role": "assistant", "content": ai_response.text})
            except Exception as e: st.error(f"⚠️ Error: {e}")