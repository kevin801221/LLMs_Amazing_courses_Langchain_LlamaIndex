import streamlit as st
import requests
from urllib.parse import urlencode
import xml.etree.ElementTree as ET
import base64

def get_wolfram_full_result(WOLFRAM_APP_ID, query, params):
    FULL_RESULTS_API_URL = "http://api.wolframalpha.com/v2/query"
    full_params = {
        "appid": WOLFRAM_APP_ID,
        "input": query,
        "format": params.get('format', 'image,plaintext'),
        "width": params.get('width'),
        "maxwidth": params.get('maxwidth'),
        "plotwidth": params.get('plotwidth'),
        "mag": params.get('mag'),
        "units": params.get('units'),
        "assumption": params.get('assumption'),
    }
    url = f"{FULL_RESULTS_API_URL}?{urlencode({k: v for k, v in full_params.items() if v is not None})}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.content, url
    except requests.RequestException as e:
        return str(e), url

def parse_xml_result(xml_content):
    root = ET.fromstring(xml_content)
    pods = []
    for pod in root.findall('.//pod'):
        pod_data = {
            'title': pod.get('title'),
            'subpods': []
        }
        for subpod in pod.findall('.//subpod'):
            subpod_data = {}
            img = subpod.find('img')
            if img is not None:
                subpod_data['img_src'] = img.get('src')
                subpod_data['img_alt'] = img.get('alt')
            
            plaintext = subpod.find('plaintext')
            if plaintext is not None:
                subpod_data['plaintext'] = plaintext.text
            
            mathml = subpod.find('mathml')
            if mathml is not None:
                subpod_data['mathml'] = ET.tostring(mathml, encoding='unicode')
            
            minput = subpod.find('minput')
            if minput is not None:
                subpod_data['minput'] = minput.text
            
            moutput = subpod.find('moutput')
            if moutput is not None:
                subpod_data['moutput'] = moutput.text
            
            sound = subpod.find('.//sound')
            if sound is not None:
                subpod_data['sound'] = sound.get('url')
            
            subpod_data['imagemap'] = [
                {
                    'title': rect.get('title'),
                    'coords': rect.get('coords')
                } for rect in subpod.findall('.//imagemap/rect')
            ]
            
            pod_data['subpods'].append(subpod_data)
        
        states = pod.find('states')
        if states is not None:
            pod_data['states'] = [
                {
                    'name': state.get('name'),
                    'input': state.get('input')
                } for state in states.findall('state')
            ]
        
        pods.append(pod_data)
    
    assumptions = root.find('assumptions')
    if assumptions is not None:
        pods.append({
            'title': 'Assumptions',
            'subpods': [
                {
                    'plaintext': assumption.get('type') + ': ' + ', '.join([value.get('desc') for value in assumption.findall('value')])
                } for assumption in assumptions.findall('assumption')
            ]
        })
    
    return pods

def render_math_expression(mathml):
    # 這裡我們只是顯示 MathML 源碼，實際應用中您可能需要使用 JavaScript 庫來渲染它
    st.code(mathml, language='xml')

def display_sound(sound_url):
    st.audio(sound_url)

def full_results_api_page(WOLFRAM_APP_ID, selected_question):
    st.header("Wolfram Alpha Full Results API")
    query = st.text_input("輸入您的問題 (Full Results API):", value=selected_question)
    
    format_options = st.multiselect("選擇輸出格式", 
                                    ["image", "plaintext", "mathml", "minput", "moutput", "sound"],
                                    default=["image", "plaintext"])
    
    params = {
        "units": st.selectbox("選擇單位系統", ["metric", "nonmetric"]),
        "width": st.slider("圖片寬度", 300, 1000, 500),
        "maxwidth": st.slider("最大寬度", 500, 1500, 1000),
        "plotwidth": st.slider("圖表寬度", 200, 800, 400),
        "mag": st.slider("放大倍數", 0.1, 2.0, 1.0, 0.1),
    }
    
    if st.button("獲取完整結果"):
        if query:
            params['format'] = ','.join(format_options)
            xml_content, url = get_wolfram_full_result(WOLFRAM_APP_ID, query, params)
            st.info(f"使用的 URL: {url}")
            
            if isinstance(xml_content, bytes) and xml_content.startswith(b'<'):
                pods = parse_xml_result(xml_content)
                for pod in pods:
                    st.subheader(pod['title'])
                    for subpod in pod['subpods']:
                        if 'image' in format_options and 'img_src' in subpod:
                            st.image(subpod['img_src'], use_column_width=True)
                        if 'plaintext' in format_options and 'plaintext' in subpod:
                            st.text(subpod['plaintext'])
                        if 'mathml' in format_options and 'mathml' in subpod:
                            render_math_expression(subpod['mathml'])
                        if 'minput' in format_options and 'minput' in subpod:
                            st.code(subpod['minput'], language='mathematica')
                        if 'moutput' in format_options and 'moutput' in subpod:
                            st.code(subpod['moutput'], language='mathematica')
                        if 'sound' in format_options and 'sound' in subpod:
                            display_sound(subpod['sound'])
                        
                        if subpod.get('imagemap'):
                            st.write("可點擊區域:")
                            for rect in subpod['imagemap']:
                                st.write(f"- {rect['title']} (座標: {rect['coords']})")
                    
                    if 'states' in pod:
                        st.write("可用狀態:")
                        for state in pod['states']:
                            st.write(f"- {state['name']}")
            else:
                st.error("無法獲取有效的 XML 結果。")
        else:
            st.warning("請輸入一個問題。")