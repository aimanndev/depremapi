from flask import Flask, jsonify
import requests
import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.route('/')
def home():
    try:
        # Kandilli Rasathanesi XML verisi
        r = requests.get("http://udim.koeri.boun.edu.tr/zeqmap/xmlt/son24saat.xml", timeout=5)
        root = ET.fromstring(r.content)
        
        # Tüm depremleri bir liste olarak al
        all_quakes = root.findall('earhquake')
        
        if len(all_quakes) > 0:
            # Reis dediğin gibi liste tersmiş, o yüzden [-1] ile en alttakini alıyoruz
            last = all_quakes[-1] 
            
            data = {
                "status": "success",
                "yer": last.get('lokasyon').strip(),
                "mag": float(last.get('mag')),
                "lat": float(last.get('lat')),
                "lng": float(last.get('lng')),
                "zaman": last.get('name')
            }
            return jsonify(data)
        else:
            return jsonify({"status": "error", "message": "Deprem bulunamadı"})
            
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
